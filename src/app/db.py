import os
from contextlib import asynccontextmanager
from typing import Generator, AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

DEFAULT_DB_URL = "sqlite:///./movies.db"

def get_database_url() -> str:
    # Examples:
    #  - sqlite:///./movies.db
    #  - postgresql+psycopg://USER:PASSWORD@HOST:5432/DB
    return os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# SQLAlchemy 2.0 engine
def create_db_engine() -> Engine:
    url = get_database_url()
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    return create_engine(url, echo=False, connect_args=connect_args, future=True)

engine = create_db_engine()
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

# For FastAPI lifespan (startup/shutdown)
@asynccontextmanager
async def lifespan(app):
    # Auto create tables (simple for this project)
    from .models import SQLModel  # noqa: F401 (ensures models are imported)
    SQLModel.metadata.create_all(engine)
    yield