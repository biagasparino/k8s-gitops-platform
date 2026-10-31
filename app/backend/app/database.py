"""Database engine configuration.

Inside Kubernetes the connection is assembled from discrete variables so that the
non-sensitive parts (host, port, name) can live in a ConfigMap and the sensitive
parts (user, password) in a Secret. A full DATABASE_URL still wins if provided.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


def build_database_url() -> URL:
    explicit = os.getenv("DATABASE_URL")
    if explicit:
        return make_url(explicit)

    host = os.getenv("DB_HOST")
    if host:
        return URL.create(
            "postgresql+psycopg2",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=host,
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "tasks"),
        )

    return make_url("sqlite:///./local.db")


_url = build_database_url()
_connect_args = {"check_same_thread": False} if _url.get_backend_name() == "sqlite" else {}

engine = create_engine(_url, pool_pre_ping=True, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
