from __future__ import annotations

from typing import Any

import requests


class HNClient:
    """Generic HTTP client for HackerNews API."""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self._session = requests.Session()

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> HNClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def get(self, path: str) -> requests.Response:
        """Make a GET request to the API."""
        url = f"{self.BASE_URL}{path}"
        return self._session.get(url, timeout=self.timeout)
