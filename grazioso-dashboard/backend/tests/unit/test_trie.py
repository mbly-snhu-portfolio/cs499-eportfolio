"""
Unit tests for Trie data structure.
"""
import pytest
from app.utils.trie import Trie, TrieNode


class TestTrieNode:
    """Tests for TrieNode class."""
    
    def test_trie_node_initialization(self):
        """Test TrieNode initialization."""
        node = TrieNode()
        assert node.children == {}
        assert node.is_end_of_word is False
        assert node.count == 0


class TestTrie:
    """Tests for Trie class."""
    
    def test_trie_initialization(self):
        """Test Trie initialization."""
        trie = Trie()
        assert trie.root is not None
        assert trie.size == 0
    
    def test_insert_single_word(self):
        """Test inserting a single word."""
        trie = Trie()
        trie.insert("test")
        assert trie.size == 1
        assert trie.search("test") is True
    
    def test_insert_multiple_words(self):
        """Test inserting multiple words."""
        trie = Trie()
        words = ["test", "testing", "tested", "tester"]
        for word in words:
            trie.insert(word)
        assert trie.size == 4
        assert all(trie.search(word) for word in words)
    
    def test_search_nonexistent_word(self):
        """Test searching for a word that doesn't exist."""
        trie = Trie()
        trie.insert("test")
        assert trie.search("nonexistent") is False
        assert trie.search("tes") is False  # Prefix but not complete word
    
    def test_case_insensitive(self):
        """Test case-insensitive insertion and search."""
        trie = Trie()
        trie.insert("Test")
        assert trie.search("test") is True
        assert trie.search("TEST") is True
        assert trie.search("TeSt") is True
    
    def test_search_prefix(self):
        """Test prefix search functionality."""
        trie = Trie()
        words = ["test", "testing", "tested", "tester", "temp", "temporary"]
        trie.build_from_list(words)
        
        results = trie.search_prefix("test")
        assert len(results) > 0
        assert "test" in results
        assert "testing" in results
        assert "tested" in results
        assert "tester" in results
        assert "temp" not in results
    
    def test_search_prefix_limit(self):
        """Test prefix search with limit."""
        trie = Trie()
        words = [f"test{i}" for i in range(20)]
        trie.build_from_list(words)
        
        results = trie.search_prefix("test", limit=5)
        assert len(results) <= 5
    
    def test_search_prefix_empty(self):
        """Test prefix search with no matches."""
        trie = Trie()
        trie.insert("test")
        results = trie.search_prefix("xyz")
        assert results == []
    
    def test_build_from_list(self):
        """Test building Trie from a list."""
        trie = Trie()
        words = ["apple", "app", "application", "apply"]
        trie.build_from_list(words)
        assert trie.size == 4
        assert all(trie.search(word) for word in words)
    
    def test_duplicate_insertion(self):
        """Test inserting the same word multiple times."""
        trie = Trie()
        trie.insert("test")
        trie.insert("test")
        trie.insert("test")
        assert trie.size == 1  # Size should remain 1
        assert trie.search("test") is True
    
    def test_frequency_counting(self):
        """Test frequency counting for ranking."""
        trie = Trie()
        trie.insert("test")
        trie.insert("test")
        trie.insert("testing")
        
        # Check that count is incremented
        node = trie.root
        for char in "test":
            node = node.children[char]
        assert node.count == 2
    
    def test_clear(self):
        """Test clearing the Trie."""
        trie = Trie()
        trie.insert("test")
        trie.insert("testing")
        assert trie.size == 2
        
        trie.clear()
        assert trie.size == 0
        assert trie.search("test") is False
    
    def test_empty_string(self):
        """Test handling of empty strings."""
        trie = Trie()
        trie.insert("")
        assert trie.size == 0  # Empty strings should not be inserted
        
        trie.insert("test")
        results = trie.search_prefix("")
        assert len(results) > 0  # Empty prefix should return all words
    
    def test_whitespace_handling(self):
        """Test handling of whitespace in words."""
        trie = Trie()
        trie.insert("  test  ")
        assert trie.search("test") is True
        assert trie.search("  test  ") is True

