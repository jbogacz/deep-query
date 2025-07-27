"""Main application entry point."""

import json
import os
import sys
from datetime import datetime

from .config import Config
from .services import ForumService


def main():
    """Main application function."""
    # Load configuration
    config = Config()

    # Validate configuration
    if not config.validate():
        print("Error: Missing required configuration. Please check your .env file.")
        print("Required: API_BASE_URL, API_KEY, API_SECRET")
        sys.exit(1)

    print(f"Fetching up to {config.max_links} links from {config.api_base_url}...")

    try:
        # Initialize service and fetch data
        service = ForumService(config)
        links = service.fetch_links_with_comments(config.max_links)
        print(f"Fetched {len(links)} links with comments.")

        # Create tmp directory if it doesn't exist
        tmp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)

        # Save links as JSON with timestamp filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_links.json"
        filepath = os.path.join(tmp_dir, filename)

        # Convert Record objects to dictionaries for JSON serialization
        links_data = [link.model_dump() for link in links]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(links_data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(links)} links to {filepath}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
