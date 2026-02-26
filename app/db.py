# SQLite for this project because it's easy to run and easy to reproduce
# DATABASE_URL can be overridden via env for tests or future deployments

import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite needs check_same_thread=False because FastAPI may use threads
# For non-SQLite databases this option isn't needed
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    echo=False, # keep SQL logs off by default (can turn on when debugging)
    connect_args=connect_args,
)


def init_db() -> None:
    # Create tables if they don't exist yet
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    # One DB session per request
    # FastAPI handles closing the generator dependency automatically
    with Session(engine) as session:
        yield session