import os

import pytest

# Must be set before the app is imported so the engine points at a throwaway SQLite file.
os.environ["DATABASE_URL"] = "sqlite:///./test_tasks.db"

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client


def pytest_sessionfinish(session, exitstatus):  # noqa: ARG001
    engine.dispose()
    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")
