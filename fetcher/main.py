"""Main application entry point."""

import sys

from .config import Config
from .services import FileService, ForumService


def main():
    config = Config()

    # Validate configuration
    if not config.validate():
        print("Error: Missing required configuration. Please check your .env file.")
        print("Required: API_BASE_URL, API_KEY, API_SECRET")
        sys.exit(1)

    print(f"Fetching up to {config.max_records} links from {config.api_base_url}...")

    try:
        # Initialize service and fetch data
        forum_service = ForumService(config)
        file_service = FileService()

        # records = forum_service.fetch_articles_with_comments(config.max_records)
        # file_service.save_records_to_file(records, 'articles')

        records = forum_service.fetch_entries_with_comments(config.max_records)
        file_service.save_records_to_file(records, 'microblog')

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
