"""
Pytest configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.auth_service import USERS_DB, get_password_hash
import os
from pymongo import MongoClient

# Set test environment variables
os.environ["MONGODB_HOST"] = os.getenv("MONGODB_HOST", "localhost")
os.environ["MONGODB_PORT"] = os.getenv("MONGODB_PORT", "27017")
os.environ["MONGO_USER"] = os.getenv("MONGO_USER", "aacuser")
os.environ["MONGO_PASS"] = os.getenv("MONGO_PASS", "SECRET")
os.environ["AAC_DATABASE"] = os.getenv("AAC_DATABASE", "aac_test")
os.environ["SECRET_KEY"] = os.getenv("SECRET_KEY", "test-secret-key")


@pytest.fixture(scope="function")
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def mongo_available():
    """
    Return True if MongoDB is reachable with test settings.

    Many environments (e.g., CI) may not have MongoDB running. Tests that
    require live DB behavior should skip when MongoDB is unavailable.
    """
    host = os.environ.get("MONGODB_HOST", "localhost")
    port = os.environ.get("MONGODB_PORT", "27017")
    user = os.environ.get("MONGO_USER", "")
    password = os.environ.get("MONGO_PASS", "")

    connection_string = f"mongodb://{user}:{password}@{host}:{port}" if user else f"mongodb://{host}:{port}"

    client = None
    try:
        # Use a short timeout so tests don't hang when Mongo isn't running.
        client = MongoClient(connection_string, serverSelectionTimeoutMS=500)
        client.admin.command("ping")
        return True
    except Exception:
        return False
    finally:
        try:
            if client is not None:
                client.close()
        except Exception:
            pass


@pytest.fixture(scope="function")
def auth_headers(client):
    """Get authentication headers for test user."""
    response = client.post(
        "/api/auth/login",
        data={"username": "user", "password": "user123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_headers(client):
    """Get authentication headers for admin user."""
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

