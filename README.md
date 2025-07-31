# Deep Query

A modular Python application combining forum data fetching with intelligent semantic search and classification capabilities.

## Overview

Deep Query consists of two main packages:
- **Fetcher**: Handles API communication and data retrieval from forum endpoints
- **Cognition**: Provides semantic search and content classification functionality

## Features

### 📡 Fetcher Package
- OpenAPI-compliant forum API integration
- Fetches **articles/links** and **microblog entries** with their comments
- Configurable connection management via environment variables
- Structured data models with Pydantic validation (Record, RecordType)
- Retry mechanism with exponential backoff
- JSON output formatting and file persistence
- Unified data structure for both content types

### 🧠 Cognition Package  
- **Semantic search** across fetched articles, microblog entries, and comments
- **Content classification** to categorize forum posts by topic/sentiment
- **Cross-content analysis** - find similar articles and microblog discussions
- **Comment thread analysis** - extract insights from conversation patterns
- Extensible ML pipeline architecture ready for NLP models

## Installation

1. Install dependencies:
```bash
pip install -e .
```

2. Copy the environment template:
```bash
cp .env .env
```

3. Configure your API credentials in `.env`:
```
API_BASE_URL=https://your-forum-api.com
API_KEY=your_api_key
API_SECRET=your_api_secret
MAX_LINKS=10
```

## Usage

### Fetcher
Run the data fetcher:
```bash
fetcher
```

Or run directly:
```bash
python -m fetcher.main
```

### Cognition
The cognition package provides programmatic APIs for semantic analysis:
```python
from cognition import search, classifier
# Implementation coming soon
```

## Project Structure

```
fetcher/
├── __init__.py          # Package initialization
├── main.py              # Application entry point
├── config.py            # Configuration management
├── models.py            # Data models (Link, Comment)
├── api_client.py        # HTTP API client
├── services.py          # Business logic
└── formatter.py         # Output formatting

cognition/
├── __init__.py          # Package initialization
├── search.py            # Semantic search functionality
├── classifier.py        # Classification functionality
└── models.py            # Data models for ML operations
```

## Data Flow

1. **Fetcher** retrieves diverse forum content:
   - Articles/links with metadata and discussions
   - Microblog entries with comment threads
   - Unified Record format for both content types
2. **Cognition** performs intelligent analysis:
   - Semantic similarity matching across all content
   - Topic classification of articles vs microblog posts
   - Comment sentiment and thread pattern analysis
3. Results persisted to JSON files in `tmp/` directory for further processing

## Output Format

### Fetcher Output
For each record (article or microblog entry):
- Record ID and type (`article/link` or `entry/microblog`)  
- Creation timestamp
- Title and description content
- Source URL
- Full comment threads with discussion context

### Cognition Output  
- **Search results**: Ranked content by semantic relevance across articles + microblogs
- **Classifications**: Topic categories, content types, sentiment analysis
- **Recommendations**: Similar articles, related microblog discussions
- **Insights**: Comment thread patterns, cross-content relationships

## Dependencies

### Core Dependencies
- `httpx` - Async HTTP client for API requests
- `python-dotenv` - Environment variable management  
- `pydantic` - Data validation and parsing
- `requests` - HTTP library for API communication

### Development Dependencies
- `pytest` - Testing framework
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `ruff` - Fast Python linter