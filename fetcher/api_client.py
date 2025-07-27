"""API client for forum interactions."""

import httpx
from typing import List, Dict, Any, Optional
from .config import Config


class ForumAPIClient:
    """Client for interacting with the forum API."""

    def __init__(self, config: Config):
        self.config = config
        self.client = httpx.Client(
            base_url=config.api_base_url,
            timeout=30.0,
            headers=config.headers,
            event_hooks={'request': [self._auth_interceptor]}
        )
        self._access_token: Optional[str] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def _auth_interceptor(self, request: httpx.Request):
        """Interceptor that ensures Authorization header is present on every request."""
        # Skip auth check for the auth endpoint itself
        if request.url.path.endswith('/auth'):
            return
        # Check if Authorization header is missing
        if not self._access_token:
            self._access_token = self._post_auth()

        request.headers["Authorization"] = f"Bearer {self._access_token}"

    def _post_auth(self):
        """Post authentication to get access token."""
        payload = {
            "data": {"key": self.config.api_key, "secret": self.config.api_secret}
        }
        response = self.client.post("/auth", json=payload)

        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("data").get("token")

        if not access_token:
            raise ValueError("Authentication failed: No token received")

        return access_token

    def get_links(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch links from the /links endpoint."""
        params = {}
        if limit:
            params["limit"] = limit

        response = self.client.get("/links", params=params)
        response.raise_for_status()
        return response.json()['data']

    def get_comments(self, link_id: str) -> List[Dict[str, Any]]:
        """Fetch comments for a specific link."""
        response = self.client.get(f"/links/{link_id}/comments")
        response.raise_for_status()
        return response.json()['data']

    def close(self):
        """Close the HTTP client."""
        self.client.close()
