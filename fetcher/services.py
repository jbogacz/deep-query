"""Service layer for forum operations."""

from typing import List

from .api_client import ForumAPIClient
from .config import Config
from .models import Record


class ForumService:
    """Service for fetching and processing forum data."""

    def __init__(self, config: Config):
        self.config = config

    def fetch_links_with_comments(self, max_links: int | None = None) -> List[Record]:
        """Fetch links and their associated comments."""
        max_links = max_links or self.config.max_links
        records = []

        with ForumAPIClient(self.config) as client:
            links = client.get_links(limit=max_links)

            for link in links:
                record = Record(
                    id=str(link['id']),
                    title=link['title'],
                    description=link['description'],
                )

                # Fetch comments if available
                if link.get('comments', {}).get('count', 0) > 0:
                    comments = client.get_comments(link['id'])
                    record.set_comments([c.get('content', '') for c in comments if c.get('content', '')])

                records.append(record)

        return records
