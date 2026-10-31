import asyncio
import logging
import os
import socket
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("tasks-api")


async def _wait_for_database(attempts: int = 20, delay: float = 2.0) -> None:
    """Retry the first connection: in Kubernetes the API and the database start together."""
    for attempt in range(1, attempts + 1):
        try:
            await asyncio.to_thread(Base.metadata.create_all, bind=engine)
            logger.info("database schema ready")
            return
        except Exception as exc:  # noqa: BLE001 - we only log and retry
            logger.warning("database not ready (attempt %s/%s): %s", attempt, attempts, exc)
            await asyncio.sleep(delay)
    raise RuntimeError("database never became available")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await _wait_for_database()
    yield


app = FastAPI(title="Tasks API", version=os.getenv("APP_VERSION", "dev"), lifespan=lifespan)


# --------------------------------------------------------------------------- health
@app.get("/health/live", tags=["health"])
def liveness():
    """Liveness probe: the process is up. Deliberately does NOT touch the database,
    so a database outage never causes Kubernetes to restart healthy API pods."""
    return {"status": "alive"}


@app.get("/health/ready", tags=["health"])
def readiness(response: Response, db: Session = Depends(get_db)):
    """Readiness probe: the pod can serve traffic only if the database answers."""
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        logger.error("readiness check failed: %s", exc)
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not-ready"}
    return {"status": "ready"}


@app.get("/api/info", tags=["meta"])
def info():
    """Shows which pod answered — handy to watch load balancing across replicas."""
    return {"pod": socket.gethostname(), "version": os.getenv("APP_VERSION", "dev")}


# ---------------------------------------------------------------------------- tasks
@app.get("/api/tasks", response_model=list[schemas.TaskOut], tags=["tasks"])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(models.Task).order_by(models.Task.id.desc()).limit(100)).all()


@app.post("/api/tasks", response_model=schemas.TaskOut, status_code=201, tags=["tasks"])
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(title=payload.title.strip())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.patch("/api/tasks/{task_id}", response_model=schemas.TaskOut, tags=["tasks"])
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = payload.done
    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=204, tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return Response(status_code=204)
