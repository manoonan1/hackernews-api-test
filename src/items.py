from __future__ import annotations

from typing import Any

from src.client import HNClient


class ItemsAPI:

    def __init__(self, client: HNClient) -> None:
        self.client = client

    def get_item_response(self, item_id: int):
        """Fetch item response (for status code checks)."""
        return self.client.get(f"/item/{item_id}.json")

    def get_item(self, item_id: int) -> dict[str, Any]:
        """Fetch item as dict."""
        return self.get_item_response(item_id).json()

    def get_first_comment(self, story: dict) -> dict[str, Any]:
        """Get the first comment of a story."""
        if not story.get("kids"):
            raise ValueError("Story has no comments")
        return self.get_item(story["kids"][0])
