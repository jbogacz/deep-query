"""Configuration module for environment variables and settings."""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables."""

    def __init__(self):
        self.api_base_url: str = os.getenv("API_BASE_URL", "")
        self.api_key: str = os.getenv("API_KEY", "")
        self.api_secret: str = os.getenv("API_SECRET", "")
        self.max_records: int = int(os.getenv("MAX_RECORDS", "10"))
        self._access_token: Optional[str] = None

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        required_fields = [self.api_base_url, self.api_key, self.api_secret]
        return all(field for field in required_fields)

    def set_access_token(self, token: str) -> None:
        """Set the access token for API requests."""
        self._access_token = token

    def get_access_token(self) -> Optional[str]:
        """Get the current access token."""
        return self._access_token

    def has_valid_token(self) -> bool:
        """Check if we have a valid access token."""
        return self._access_token is not None

    @property
    def headers(self) -> dict:
        """Get HTTP headers for API requests."""
        if self._access_token:
            return {
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json",
            }
        else:
            return {"Content-Type": "application/json"}
