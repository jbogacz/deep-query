"""Service layer for forum operations."""

import json
import os
from datetime import datetime
from typing import List

from .api_client import ForumAPIClient
from .config import Config
from .models import Record, RecordType


class ForumService:
    """Service for fetching and processing forum data."""

    def __init__(self, config: Config):
        self.config = config

    def fetch_articles_with_comments(
        self, max_links: int | None = None
    ) -> List[Record]:
        """Fetch articles and their associated comments."""
        max_links = max_links or self.config.max_records
        records = []

        with ForumAPIClient(self.config) as client:
            links = client.get_links(limit=max_links)

            for link in links:
                record = Record(
                    id=str(link["id"]),
                    title=link["title"],
                    description=link["description"],
                    source=f"https://wykop.pl/link/{link['id']}",
                    type=RecordType.ARTICLE,
                )

                # Fetch comments if available
                if link.get("comments", {}).get("count", 0) > 0:
                    comments = client.get_comments(link["id"])
                    record.set_comments(
                        [c.get("content", "") for c in comments if c.get("content", "")]
                    )

                records.append(record)

        print(f"Fetched {len(records)} articles.")
        return records


class FileService:
    """Service for file operations."""

    @staticmethod
    def save_records_to_file(records: List[Record], output_directory: str = "tmp"):
        # Create tmp directory if it doesn't exist
        tmp_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            output_directory,
        )
        os.makedirs(tmp_dir, exist_ok=True)

        # Save records as JSON with timestamp filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_records.json"
        output_directory = os.path.join(tmp_dir, filename)

        # Convert Record objects to dictionaries for JSON serialization
        records_data = [record.model_dump() for record in records]

        # Write records to file
        with open(output_directory, "w", encoding="utf-8") as f:
            json.dump(records_data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(records)} records to {output_directory}")
