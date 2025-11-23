"""
Integration tests for animals endpoints with database.
"""
import pytest
from fastapi.testclient import TestClient
from app.core.database import db_manager


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Setup test database."""
    try:
        db_manager.connect()
        yield
    finally:
        if db_manager.client:
            # Clean up test data
            test_db = db_manager.client[db_manager.database.name]
            test_db.animals.delete_many({"animal_id": {"$regex": "^TEST"}})
        db_manager.disconnect()


def test_create_and_read_animal(client: TestClient, admin_headers):
    """Test creating and reading an animal."""
    # Create animal
    create_response = client.post(
        "/api/animals",
        json={
            "animal_id": "TEST001",
            "name": "Integration Test Animal",
            "animal_type": "Dog",
            "breed": "Test Breed"
        },
        headers=admin_headers
    )
    
    if create_response.status_code == 201:
        created = create_response.json()
        animal_id = created.get("id") or created.get("_id")
        
        # Read animal
        read_response = client.get(
            f"/api/animals/{animal_id}",
            headers=admin_headers
        )
        assert read_response.status_code == 200
        data = read_response.json()
        assert data["name"] == "Integration Test Animal"


def test_update_animal(client: TestClient, admin_headers):
    """Test updating an animal."""
    # First create an animal
    create_response = client.post(
        "/api/animals",
        json={
            "animal_id": "TEST002",
            "name": "Original Name",
            "animal_type": "Dog"
        },
        headers=admin_headers
    )
    
    if create_response.status_code == 201:
        created = create_response.json()
        animal_id = created.get("id") or created.get("_id")
        
        # Update animal
        update_response = client.put(
            f"/api/animals/{animal_id}",
            json={"name": "Updated Name"},
            headers=admin_headers
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["name"] == "Updated Name"


def test_delete_animal(client: TestClient, admin_headers):
    """Test deleting an animal."""
    # First create an animal
    create_response = client.post(
        "/api/animals",
        json={
            "animal_id": "TEST003",
            "name": "To Be Deleted",
            "animal_type": "Dog"
        },
        headers=admin_headers
    )
    
    if create_response.status_code == 201:
        created = create_response.json()
        animal_id = created.get("id") or created.get("_id")
        
        # Delete animal
        delete_response = client.delete(
            f"/api/animals/{animal_id}",
            headers=admin_headers
        )
        assert delete_response.status_code == 204
        
        # Verify deletion
        read_response = client.get(
            f"/api/animals/{animal_id}",
            headers=admin_headers
        )
        assert read_response.status_code == 404

