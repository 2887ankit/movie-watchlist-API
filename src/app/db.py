# src/app/db.py
import os
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

DEFAULT_DB_URL = "sqlite:///./movies.db"

def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DB_URL)

def create_db_engine():
    url = get_database_url()
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, echo=False, connect_args=connect_args, future=True)

engine = create_db_engine()
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

def get_session():
    with SessionLocal() as session:
        yield session

@asynccontextmanager
async def lifespan(app):
    # Import models so their tables are registered on SQLModel.metadata
    from . import models  # noqa: F401 (import side-effect registers Movie table)
    SQLModel.metadata.create_all(engine)
    yield
