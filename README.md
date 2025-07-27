# Fetcher

A modular Python application that fetches links and comments from a forum API based on OpenAPI specification.

## Features

- Configurable API connection using environment variables
- Fetches last N links from `/links` endpoint
- Retrieves comments/conversations for each link
- Displays formatted output with link details and comments
- Modular structure with separate services and models

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

Run the application:
```bash
fetcher
```

Or run directly:
```bash
python -m fetcher.main
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
```

## Output Format

For each link, the application displays:
- Link ID
- Creation timestamp
- Content
- Associated comments with author and timestamp

## Dependencies

- `httpx` - HTTP client for API requests
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation and parsing