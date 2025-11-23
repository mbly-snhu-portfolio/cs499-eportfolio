"""
Unit tests for fuzzy string matching.
"""
import pytest
from app.utils.fuzzy_match import (
    calculate_similarity,
    find_best_matches,
    fuzzy_search
)


class TestCalculateSimilarity:
    """Tests for similarity calculation."""
    
    def test_identical_strings(self):
        """Test similarity of identical strings."""
        assert calculate_similarity("test", "test") == 1.0
    
    def test_completely_different_strings(self):
        """Test similarity of completely different strings."""
        similarity = calculate_similarity("abc", "xyz")
        assert 0.0 <= similarity < 1.0
    
    def test_similar_strings(self):
        """Test similarity of similar strings."""
        similarity = calculate_similarity("test", "tast")
        assert similarity > 0.5
    
    def test_case_insensitive(self):
        """Test that similarity is case-insensitive."""
        assert calculate_similarity("Test", "test") == 1.0
        assert calculate_similarity("TEST", "test") == 1.0
    
    def test_empty_strings(self):
        """Test handling of empty strings."""
        assert calculate_similarity("", "") == 1.0
        assert calculate_similarity("test", "") == 0.0
        assert calculate_similarity("", "test") == 0.0
    
    def test_whitespace_handling(self):
        """Test handling of whitespace."""
        similarity = calculate_similarity("  test  ", "test")
        assert similarity > 0.8  # Should be very similar after stripping


class TestFindBestMatches:
    """Tests for finding best matches."""
    
    def test_exact_match(self):
        """Test finding exact matches."""
        candidates = ["apple", "banana", "cherry"]
        matches = find_best_matches("apple", candidates, threshold=0.9)
        assert len(matches) > 0
        assert matches[0][0] == "apple"
        assert matches[0][1] == 1.0
    
    def test_fuzzy_match(self):
        """Test finding fuzzy matches."""
        candidates = ["apple", "apples", "application", "banana"]
        matches = find_best_matches("appl", candidates, threshold=0.6)
        assert len(matches) > 0
        assert "apple" in [m[0] for m in matches]
    
    def test_threshold_filtering(self):
        """Test that threshold filters results correctly."""
        candidates = ["apple", "banana", "cherry"]
        matches_high = find_best_matches("apple", candidates, threshold=0.9)
        matches_low = find_best_matches("apple", candidates, threshold=0.1)
        assert len(matches_low) >= len(matches_high)
    
    def test_max_results_limit(self):
        """Test that max_results limits the number of results."""
        candidates = [f"test{i}" for i in range(20)]
        matches = find_best_matches("test", candidates, max_results=5)
        assert len(matches) <= 5
    
    def test_sorting_by_similarity(self):
        """Test that results are sorted by similarity."""
        candidates = ["testing", "test", "tester"]
        matches = find_best_matches("test", candidates, threshold=0.5)
        assert len(matches) > 0
        # Results should be sorted by similarity (descending)
        similarities = [m[1] for m in matches]
        assert similarities == sorted(similarities, reverse=True)
    
    def test_no_matches(self):
        """Test when no matches are found."""
        candidates = ["apple", "banana", "cherry"]
        matches = find_best_matches("xyz", candidates, threshold=0.9)
        assert matches == []
    
    def test_empty_candidates(self):
        """Test with empty candidate list."""
        matches = find_best_matches("test", [], threshold=0.5)
        assert matches == []


class TestFuzzySearch:
    """Tests for fuzzy search function."""
    
    def test_basic_fuzzy_search(self):
        """Test basic fuzzy search functionality."""
        text_list = ["apple", "apples", "application", "banana"]
        results = fuzzy_search("appl", text_list, threshold=0.6)
        assert len(results) > 0
        assert "apple" in results
    
    def test_returns_strings_only(self):
        """Test that fuzzy_search returns only strings, not tuples."""
        text_list = ["test", "testing", "tested"]
        results = fuzzy_search("test", text_list, threshold=0.5)
        assert all(isinstance(r, str) for r in results)
        assert all(r in text_list for r in results)
    
    def test_threshold_filtering(self):
        """Test threshold filtering in fuzzy_search."""
        text_list = ["apple", "banana", "cherry"]
        results_high = fuzzy_search("apple", text_list, threshold=0.9)
        results_low = fuzzy_search("apple", text_list, threshold=0.1)
        assert len(results_low) >= len(results_high)
    
    def test_max_results(self):
        """Test max_results parameter."""
        text_list = [f"test{i}" for i in range(20)]
        results = fuzzy_search("test", text_list, threshold=0.5, max_results=5)
        assert len(results) <= 5

