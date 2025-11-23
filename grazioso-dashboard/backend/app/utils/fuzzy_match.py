"""
Fuzzy string matching using Levenshtein distance algorithm.
"""
from typing import List, Tuple
from Levenshtein import distance as levenshtein_distance


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity score between two strings using Levenshtein distance.
    
    Similarity is calculated as: 1 - (distance / max_length)
    Returns a value between 0.0 (completely different) and 1.0 (identical).
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    if not str1 and not str2:
        return 1.0
    if not str1 or not str2:
        return 0.0
    
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 1.0
    
    dist = levenshtein_distance(str1, str2)
    similarity = 1.0 - (dist / max_len)
    return max(0.0, similarity)


def find_best_matches(
    query: str,
    candidates: List[str],
    threshold: float = 0.6,
    max_results: int = 10
) -> List[Tuple[str, float]]:
    """
    Find best matching strings from a list of candidates.
    
    Args:
        query: Query string to match against
        candidates: List of candidate strings
        threshold: Minimum similarity threshold (0.0 to 1.0)
        max_results: Maximum number of results to return
        
    Returns:
        List of (candidate, similarity_score) tuples, sorted by similarity (descending)
    """
    if not query or not candidates:
        return []
    
    results: List[Tuple[str, float]] = []
    
    for candidate in candidates:
        similarity = calculate_similarity(query, candidate)
        if similarity >= threshold:
            results.append((candidate, similarity))
    
    # Sort by similarity (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:max_results]


def fuzzy_search(
    query: str,
    text_list: List[str],
    threshold: float = 0.6,
    max_results: int = 10
) -> List[str]:
    """
    Perform fuzzy search and return matching strings.
    
    Args:
        query: Query string
        text_list: List of strings to search
        threshold: Minimum similarity threshold
        max_results: Maximum number of results
        
    Returns:
        List of matching strings, sorted by similarity
    """
    matches = find_best_matches(query, text_list, threshold, max_results)
    return [text for text, _ in matches]

