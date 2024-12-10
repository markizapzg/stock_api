import pytest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="function")
def test_client():
    """Provide a test client for the FastAPI app."""
    client = TestClient(app)
    yield client

@pytest.fixture(scope="function")
def test_db():
    """Set up a test MongoDB instance."""
    client = MongoClient("mongodb://mongo:27017/")
    db = client["test_db"]

    # Ensure the database is clean before starting
    db.stocks.delete_many({})

    yield db

    # Clean up after the test
    client.drop_database("test_db")
