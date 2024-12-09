import pytest
from fastapi.testclient import TestClient
from app.main import app
from pymongo import MongoClient


@pytest.fixture(scope="session")
def test_client():
    """Fixture for creating a FastAPI test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Fixture for connecting to a test MongoDB instance."""
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["test_db"]

    # Ensure the database is clean before running the test
    db.stocks.delete_many({})

    yield db  # Provide the test database instance to the test

    # Clean up after the test
    db.stocks.delete_many({})
    client.drop_database("test_db")