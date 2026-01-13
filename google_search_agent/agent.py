"""Google Search Agent implementation using google-search-api.py."""

import os
from pathlib import Path
import importlib.util
from typing import List, Any, Optional


def _load_google_search_api():
    """Load google-search-api.py module"""
    current_dir = Path(__file__).parent
    google_search_api_path = current_dir / "google-search-api.py"
    
    if not google_search_api_path.exists():
        raise FileNotFoundError(f"google-search-api.py not found at {google_search_api_path}")
    
    spec = importlib.util.spec_from_file_location(
        "google_search_api",
        google_search_api_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load the module
_google_search_api_module = _load_google_search_api()
google_search_api = _google_search_api_module.google_search


def search(query: str, num: int = 10, start: int = 0) -> List[Any]:
    """
    Perform a Google Custom Search using google-search-api.py.
    
    Args:
        query: The search query string.
        num: Number of search results to return (1-10, default: 10).
        start: Pagination start index (default: 0).
    
    Returns:
        List of dictionaries containing search results with:
        - title: Title of the result
        - link: URL of the result
        - snippet: Brief description of the result
        - rank: Rank of the result (1-based)
    """
    return google_search_api(query=query, num=num, start=start)


# Re-export for convenience
__all__ = ['google_search_api', 'search']
