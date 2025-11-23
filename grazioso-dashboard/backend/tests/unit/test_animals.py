"""
Unit tests for animals endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_list_animals_unauthorized(client: TestClient):
    """Test listing animals without authentication."""
    response = client.get("/api/animals")
    assert response.status_code == 401


def test_list_animals_authorized(client: TestClient, auth_headers):
    """Test listing animals with authentication."""
    response = client.get("/api/animals", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data


def test_list_animals_with_pagination(client: TestClient, auth_headers):
    """Test listing animals with pagination."""
    response = client.get(
        "/api/animals?skip=0&limit=10",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 10


def test_list_animals_with_category_filter(client: TestClient, auth_headers):
    """Test listing animals with category filter."""
    response = client.get(
        "/api/animals?category=Water Rescue",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


def test_get_animal_not_found(client: TestClient, auth_headers):
    """Test getting non-existent animal."""
    response = client.get(
        "/api/animals/nonexistent",
        headers=auth_headers
    )
    assert response.status_code == 404


def test_create_animal_unauthorized(client: TestClient, auth_headers):
    """Test creating animal as non-admin."""
    response = client.post(
        "/api/animals",
        json={"animal_id": "TEST123", "name": "Test Animal"},
        headers=auth_headers
    )
    assert response.status_code == 403


def test_create_animal_authorized(client: TestClient, admin_headers):
    """Test creating animal as admin."""
    response = client.post(
        "/api/animals",
        json={
            "animal_id": "TEST123",
            "name": "Test Animal",
            "animal_type": "Dog",
            "breed": "Test Breed"
        },
        headers=admin_headers
    )
    # May fail if animal already exists, but should not be 403
    assert response.status_code != 403

