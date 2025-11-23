"""
Unit tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_login_success(client: TestClient):
    """Test successful login."""
    response = client.post(
        "/api/auth/login",
        data={"username": "user", "password": "user123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        data={"username": "user", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_get_current_user(client: TestClient, auth_headers):
    """Test getting current user info."""
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert data["username"] == "user"


def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without token."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401

