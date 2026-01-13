# Google Search API Based Deep Research Agent

[GitHub](https://github.com/aiagenta2z/ai-agent-marketplace) | [Agent MCP Deployment](https://deepnlp.org/doc/agent_mcp_deployment) | [AI Agent Marketplace](https://deepnlp.org/store/ai-agent) | [OneKey MCP Router](https://deepnlp.org/doc/onekey_mcp_router)

A Google Search Deep Research Agent to conduct multi turns search calling Google Custome Search API and conduct deep research to answer your question.

[Agent Live URL](https://derekzz.aiagenta2z.com/google-deep-research-agent/mcp) on aiagenta2z.com deployed.


## Features

- **Google Search**: Search the web using Google Custom Search API directly
- **Simplified Results**: Get simplified search results with titles, links, snippets, and rank


## Prerequisites

1. **Google API Key**: You need a Google API key with Custom Search API enabled
   - Get it from [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the "Custom Search API" for your project

2. **Google Custom Search Engine ID**: You need to create a Custom Search Engine
   - Create one at [Google Custom Search](https://programmablesearchengine.google.com/)
   - Get your Search Engine ID (cx parameter)


## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export GOOGLE_SEARCH_ACCESS_KEY="your-api-key-here"
export GOOGLE_SEARCH_ENGINE_ID="your-search-engine-id-here"
```

Or create a `.env` file:
```
GOOGLE_SEARCH_ACCESS_KEY=your-api-key-here
```

## Usage

### Start the MCP Server

**Option 1: Using the startup script (recommended)**
```bash
./run_mcp_server.sh [PORT]
```

Default port is 7005. You can specify a different port:
```bash
./run_mcp_server.sh 7006
```

**Option 2: Using uvicorn (production)**
```bash
uvicorn server:app --host 0.0.0.0 --port 7005
```

**Option 3: Direct Python execution (development)**
```bash
python3 server.py --port 7005
```

### API Endpoints

The server exposes MCP endpoints at:
- `http://0.0.0.0:7005/mcp` (or your specified port)

### Available Tools

1. **google_search**: Search with simplified or full results
   - Parameters:
     - `query` (required): Search query string
     - `num` (optional): Number of results (1-10, default: 10)
     - `full_response` (optional): If True, returns complete API response (default: False)
   - Returns: Dictionary with results, total_results, query, message, and optionally full response

### Test the MCP Server

You can test the MCP server using curl or the test script:

```bash
# Test MCP endpoint
curl http://127.0.0.1:7005/mcp
```

## Project Structure

```
google_search_agent/
├── google_search_agent/
│   ├── __init__.py
│   ├── agent.py              # GoogleSearchAgent implementation
│   └── google-search-api.py  # Original Google Search API implementation
├── server.py                  # MCP server implementation
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project configuration
├── run_mcp_server.sh          # Startup script
└── README.md                  # This file
```

### Production Mode
```bash
uvicorn server:app --host 0.0.0.0 --port 7005
```
- Better performance
- Supports hot reload (`--reload`)
- Supports multiple workers (`--workers N`)
- Recommended for production
