"""API client for forum interactions."""

from typing import Any, Dict, List, Optional

import httpx

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

    def _get_list(self, endpoint: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Generic method to fetch a list of items from the API."""
        if limit <= 50:
            # Single page request
            params = {}
            if limit:
                params["limit"] = limit

            response = self.client.get("endpoint", params=params)
            response.raise_for_status()
            return response.json()['data']

        # Multi-page request for limit > 50
        all = []
        page = 1
        per_page = 50
        remaining = limit

        while remaining > 0:
            current_limit = min(per_page, remaining)
            params = {
                "limit": current_limit,
                "page": page
            }

            response = self.client.get("/links", params=params)
            response.raise_for_status()
            page_data = response.json()['data']

            if not page_data:  # No more data available
                break

            all.extend(page_data)
            remaining -= len(page_data)
            page += 1

            # If we got fewer items than requested, we've reached the end
            if len(page_data) < current_limit:
                break

        return all

    def get_links(self, limit: int = 25) -> List[Dict[str, Any]]:
        """Fetch links from the /links endpoint with paging support."""
        return self._get_list("/links", limit)

    def get_comments(self, link_id: str) -> List[Dict[str, Any]]:
        """Fetch comments for a specific link."""
        response = self.client.get(f"/links/{link_id}/comments")
        response.raise_for_status()
        return response.json()['data']

    def close(self):
        """Close the HTTP client."""
        self.client.close()
