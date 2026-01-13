"""
APIs Provided:
1. google_search: Search using Google Custom Search API with a query string.
"""

import logging
import os
from typing import Dict, Optional, Any, List
from pathlib import Path
import uuid

### New MCP
from mcp.server.fastmcp import FastMCP

## Configuration
LOG_ENABLE = False

AGENT_ID = "derek/google_deep_research_agent"
AGENT_NAME = "Google Deep Research Agent"

ROOT_DIR = Path(__file__).parent

# Initialize Google Search API (using google-search-api.py)
print(f"Initializing Google Search API (using google-search-api.py)...")
logging.info(f"Initializing Google Search API (using google-search-api.py)")

from dotenv import load_dotenv
load_dotenv()
CX = "b148d4aa1418c4059"
API_KEY = os.environ.get("GOOGLE_SEARCH_ACCESS_KEY")

# Import google-search-api.py (filename has hyphen, need to use importlib)
try:
    import importlib.util
    google_search_api_path = ROOT_DIR / "google_search_agent" / "google-search-api.py"
    if google_search_api_path.exists():
        spec = importlib.util.spec_from_file_location(
            "google_search_api",
            google_search_api_path
        )
        google_search_api_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(google_search_api_module)
        google_search_api = google_search_api_module.google_search
        API_KEY = API_KEY
        CX = CX
        print(f"✅ Using google-search-api.py")
        print(f"   API Key: {API_KEY[:10]}...")
        print(f"   Search Engine ID: {CX[:10]}...")
        print("--- Google Search API Initialized Successfully ---")
    else:
        print(f"❌ google-search-api.py not found at {google_search_api_path}")
        google_search_api = None
except Exception as e:
    print(f"❌ Failed to import google-search-api.py: {e}")
    import traceback
    traceback.print_exc()
    google_search_api = None

# Create an MCP server
mcp = FastMCP(AGENT_NAME, json_response=True)

@mcp.tool()
def google_search(
    query: str,
    num: int = 10,
    full_response: bool = False,
) -> Dict:
    """
    Search the web using Google Custom Search API. Returns search results with titles, links, and snippets.
    Optionally returns the full API response with all metadata.

    Args:
        query: REQUIRED. The search query string. This can be any search term or question you want to search for.
        num: Optional. Number of search results to return (1-10). Defaults to 10.
        full_response: Optional. If True, returns the complete API response with all metadata. Defaults to False.

    Returns:
        A dictionary containing:
        - 'results': List of search results, each with 'title', 'link', and 'snippet'
        - 'total_results': Total number of results found (approximate)
        - 'query': The original search query
        - 'message': Status message
        - 'response': (only if full_response=True) The complete API response with all metadata
    """
    results = []
    total_results = 0
    response: Dict[str, Any] = {}
    message = "Success"

    if not query or not query.strip():
        error_response = {
            "results": [],
            "total_results": 0,
            "query": query,
            "message": "Error: Query cannot be empty.",
        }
        if full_response:
            error_response["response"] = {}
        return error_response

    if num < 1 or num > 10:
        error_response = {
            "results": [],
            "total_results": 0,
            "query": query,
            "message": "Error: num must be between 1 and 10.",
        }
        if full_response:
            error_response["response"] = {}
        return error_response

    if google_search_api is None:
        error_response = {
            "results": [],
            "total_results": 0,
            "query": query,
            "message": "Error: Google Search API not initialized. Please check google-search-api.py file.",
        }
        if full_response:
            error_response["response"] = {}
        return error_response

    try:
        # Use google-search-api.py directly
        simple_results = google_search_api(query=query, num=num, start=0)
        
        # Convert to expected format (remove rank field, keep title, link, snippet)
        for item in simple_results:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            })
        
        # Get total_results by making a direct API call (google-search-api.py doesn't return it)
        # We'll make a minimal call just to get the totalResults from searchInformation
        if full_response or len(results) > 0:
            try:
                import requests
                # Get API_KEY and CX from the loaded module
                api_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}&num=1"
                api_response = requests.get(api_url, timeout=10)
                api_response.raise_for_status()
                api_data = api_response.json()
                total_results = int(api_data.get("searchInformation", {}).get("totalResults", 0))
                
                if full_response:
                    # Return the full API response
                    response = api_data
                else:
                    response = {}
            except Exception as e:
                # Fallback: use approximate value
                total_results = len(results)
                response = {}
        else:
            total_results = 0
            response = {}
        
        message = f"Successfully retrieved {len(results)} search results for query: {query[:50]}..."
            
    except Exception as e:
        print(f"Failed to search with Google: {e}")
        message = f"Failed to search: {str(e)}"
        results = []
        total_results = 0
        response = {}

    return_dict = {
        "results": results,
        "total_results": total_results,
        "query": query,
        "message": message,
    }
    
    if full_response:
        return_dict["response"] = response
    
    return return_dict


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Hello, I am Agent A2Z Google Search Agent, who can help you search the web using Google Custom Search API. You can ask me to search for anything like 'latest news about AI', 'Python tutorial', 'best restaurants in New York', etc. I can search the internet and provide you with relevant search results including titles, links, and snippets.",
        "formal": "I am the A2Z Google Search Agent, a web search assistant powered by Google Custom Search API. I can help you find information and search for any topic on the web.",
        "casual": "Hey! I'm the Google Search Agent. Ask me to search for anything and I'll find it for you!",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    # STARTUP: Initialize Google Search Agent
    print("--- APPLICATION STARTUP ---")
    # Agent is already initialized at module level
    # If needed, we can add async initialization here

    async with mcp.session_manager.run():
        yield

    # SHUTDOWN: Cleanup
    print("--- APPLICATION SHUTDOWN ---")
    # google-search-api.py doesn't require explicit cleanup


async def get_mcp_root_id_handler(request):
    """
    This function handles the GET request to the root of the MCP application (i.e., /mcp).
    """
    unique_id = AGENT_ID
    return JSONResponse({"id": AGENT_ID})


# --- Starlette Route Function (for the main / route) ---
async def starlette_root_id_endpoint(request):
    """
    Starlette endpoint to serve the root path of the main application: http://<server>:7005/
    """
    unique_id = str(uuid.uuid4())[:8]
    return JSONResponse({"app_root_id": unique_id})


## Route: single endpoint, Mount: /xxx all the subsequent urls
mcp_app = mcp.streamable_http_app()
mcp_app.routes.insert(
    0, Route("/mcp", get_mcp_root_id_handler, methods=["GET"])
)

## GET /mcp : 1. Mount("/", app=mcp_app) -> 2. mcp_app.Route, e.g. http://0.0.0.0:7005/
## POST /mcp : 1. Mount("/", app=mcp_app) -> 3. mcp_app /json_rpc handler

# Mount using Host-based routing
app = Starlette(
    routes=[
        Mount("/", app=mcp_app),
    ],
    lifespan=lifespan,
)

# Define the argument parser
def parse_args():
    """Parses command line arguments for the server port."""
    import argparse

    parser = argparse.ArgumentParser(description="Run the A2Z Google Search Agent MCP Server.")
    parser.add_argument(
        "--port",
        type=int,
        default=7005,  # Set a default port (different from perplexity agent's 7004)
        help="The port number on which to run the server (e.g., 7005).",
    )
    return parser.parse_args()


# Run with streamable HTTP transport
if __name__ == "__main__":
    """
    """

    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7005)
    args = parser.parse_args()

    print(f"Starting MCP server on port {args.port}")
    os.environ["MCP_SERVER_URL"] = f"http://0.0.0.0:{args.port}/mcp"
    mcp.run("streamable-http")


