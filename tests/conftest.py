# Shared pytest fixtures used across multiple test files
# Using a separate SQLite DB for tests so real application data is not affected

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.main import app
from app.db import get_session

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})


def override_get_session():
    with Session(engine) as session:
        yield session


@pytest.fixture()
def client():
    SQLModel.metadata.create_all(engine)

    app.dependency_overrides[get_session] = override_get_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
# Create tables one per test run (simple and predictable)
# dependency_overrides lets me plug the test session into the app cleanly