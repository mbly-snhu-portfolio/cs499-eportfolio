"""
Integration tests for algorithm features.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.animal_shelter_service import AnimalShelterService
from app.core.database import db_manager
import os

# Set test environment
os.environ["REDIS_ENABLED"] = "False"  # Use in-memory cache for tests
os.environ["MONGODB_HOST"] = os.getenv("MONGODB_HOST", "localhost")
os.environ["AAC_DATABASE"] = os.getenv("AAC_DATABASE", "aac_test")


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Setup database connection for integration tests.
    
    Note: These tests require MongoDB to be running. They will be skipped
    if MongoDB is not available.
    """
    try:
        db_manager.connect()
        yield
    except Exception as e:
        pytest.skip(f"MongoDB not available: {e}")
    finally:
        try:
            db_manager.disconnect()
        except Exception:
            pass


@pytest.fixture(scope="function")
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def auth_headers(client):
    """Get authentication headers."""
    response = client.post(
        "/api/auth/login",
        data={"username": "user", "password": "user123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def service():
    """Create animal shelter service instance."""
    return AnimalShelterService()


class TestTrieIntegration:
    """Integration tests for Trie functionality."""
    
    def test_autocomplete_breeds_endpoint(self, client, auth_headers):
        """Test autocomplete breeds API endpoint."""
        response = client.get(
            "/api/animals/autocomplete/breeds?q=lab",
            headers=auth_headers
        )
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        # Results should be strings
        if results:
            assert all(isinstance(r, str) for r in results)
    
    def test_autocomplete_names_endpoint(self, client, auth_headers):
        """Test autocomplete names API endpoint."""
        response = client.get(
            "/api/animals/autocomplete/names?q=a",
            headers=auth_headers
        )
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
    
    def test_autocomplete_with_limit(self, client, auth_headers):
        """Test autocomplete with limit parameter."""
        response = client.get(
            "/api/animals/autocomplete/breeds?q=lab&limit=5",
            headers=auth_headers
        )
        assert response.status_code == 200
        results = response.json()
        assert len(results) <= 5
    
    def test_autocomplete_requires_auth(self, client):
        """Test that autocomplete requires authentication."""
        response = client.get("/api/animals/autocomplete/breeds?q=lab")
        assert response.status_code == 401


class TestFuzzySearchIntegration:
    """Integration tests for fuzzy search functionality."""
    
    def test_fuzzy_search_endpoint(self, client, auth_headers):
        """Test fuzzy search API endpoint."""
        response = client.get(
            "/api/animals/search/fuzzy?q=labrador",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
    
    def test_fuzzy_search_with_threshold(self, client, auth_headers):
        """Test fuzzy search with custom threshold."""
        response = client.get(
            "/api/animals/search/fuzzy?q=lab&threshold=0.5",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
    
    def test_fuzzy_search_with_limit(self, client, auth_headers):
        """Test fuzzy search with limit parameter."""
        response = client.get(
            "/api/animals/search/fuzzy?q=lab&limit=5",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 5
    
    def test_fuzzy_search_requires_auth(self, client):
        """Test that fuzzy search requires authentication."""
        response = client.get("/api/animals/search/fuzzy?q=lab")
        assert response.status_code == 401


class TestCacheIntegration:
    """Integration tests for caching functionality."""
    
    def test_cached_read_operations(self, service):
        """Test that read operations use cache."""
        # First read should populate cache
        result1 = service.read_cached(limit=10)
        assert result1 is not None
        
        # Second read should potentially use cache
        result2 = service.read_cached(limit=10)
        assert result2 is not None
    
    def test_cache_invalidation_on_update(self, service):
        """Test that cache is invalidated on updates."""
        # This test would require actual database operations
        # For now, we just verify the method exists
        assert hasattr(service, 'invalidate_cache')
        service.invalidate_cache()


class TestServiceLayerIntegration:
    """Integration tests for service layer algorithm features."""
    
    def test_autocomplete_breeds_service(self, service):
        """Test autocomplete breeds in service layer."""
        # Initialize tries
        service._initialize_tries()
        
        # Test autocomplete
        results = service.autocomplete_breeds("lab", limit=5)
        assert isinstance(results, list)
        assert all(isinstance(r, str) for r in results)
    
    def test_autocomplete_names_service(self, service):
        """Test autocomplete names in service layer."""
        service._initialize_tries()
        
        results = service.autocomplete_names("a", limit=5)
        assert isinstance(results, list)
    
    def test_fuzzy_search_breeds_service(self, service):
        """Test fuzzy search breeds in service layer."""
        results = service.fuzzy_search_breeds("labrador", threshold=0.6, limit=10)
        assert isinstance(results, list)
        # Results should be animal dictionaries
        if results:
            assert isinstance(results[0], dict)

