"""
Trie data structure for efficient prefix search and autocomplete.
"""
from typing import Dict, List, Optional


class TrieNode:
    """Node in the Trie data structure."""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.count: int = 0  # Track frequency for ranking


class Trie:
    """
    Trie (prefix tree) data structure for efficient autocomplete search.
    
    Time Complexity:
    - Insert: O(m) where m is the length of the word
    - Search: O(m) where m is the length of the word
    - Prefix Search: O(m + k) where m is prefix length, k is number of results
    
    Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of words,
    M is average word length
    """
    
    def __init__(self):
        """Initialize an empty Trie."""
        self.root = TrieNode()
        self.size = 0
    
    def insert(self, word: str) -> None:
        """
        Insert a word into the Trie.
        
        Args:
            word: Word to insert (case-insensitive)
        """
        if not word:
            return
        
        word = word.lower().strip()
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_of_word:
            self.size += 1
        node.is_end_of_word = True
        node.count += 1
    
    def search(self, word: str) -> bool:
        """
        Check if a word exists in the Trie.
        
        Args:
            word: Word to search for (case-insensitive)
            
        Returns:
            True if word exists, False otherwise
        """
        if not word:
            return False
        
        word = word.lower().strip()
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_of_word
    
    def _collect_words(self, node: TrieNode, prefix: str, results: List[tuple], limit: int) -> None:
        """
        Recursively collect words from a node.
        
        Args:
            node: Current Trie node
            prefix: Current prefix string
            results: List to store (word, count) tuples
            limit: Maximum number of results to collect
        """
        if len(results) >= limit:
            return
        
        if node.is_end_of_word:
            results.append((prefix, node.count))
        
        # Sort children for consistent ordering
        for char in sorted(node.children.keys()):
            if len(results) >= limit:
                break
            self._collect_words(node.children[char], prefix + char, results, limit)
    
    def search_prefix(self, prefix: str, limit: int = 10) -> List[str]:
        """
        Search for all words with the given prefix.
        
        Args:
            prefix: Prefix to search for (case-insensitive). Empty string returns all words.
            limit: Maximum number of results to return
            
        Returns:
            List of words matching the prefix, sorted by frequency (descending)
        """
        prefix = prefix.lower().strip() if prefix else ""
        node = self.root
        
        # If prefix is empty, start from root (return all words)
        if prefix:
            # Navigate to prefix node
            for char in prefix:
                if char not in node.children:
                    return []
                node = node.children[char]
        
        # Collect all words with this prefix (or all words if prefix is empty)
        results: List[tuple] = []
        self._collect_words(node, prefix, results, limit)
        
        # Sort by frequency (descending) and return words only
        results.sort(key=lambda x: x[1], reverse=True)
        return [word for word, _ in results]
    
    def build_from_list(self, words: List[str]) -> None:
        """
        Build Trie from a list of words.
        
        Args:
            words: List of words to insert
        """
        for word in words:
            self.insert(word)
    
    def clear(self) -> None:
        """Clear all words from the Trie."""
        self.root = TrieNode()
        self.size = 0

