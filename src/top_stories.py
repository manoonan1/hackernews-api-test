from __future__ import annotations

from src.client import HNClient


class TopStoriesAPI:

    def __init__(self, client: HNClient) -> None:
        self.client = client

    def get_top_stories_response(self):
        """Fetch top stories response (for status code checks)."""
        return self.client.get("/topstories.json")

    def get_top_stories(self) -> list[int]:
        """Get list of top story IDs."""
        return self.get_top_stories_response().json()

    def find_first_top_story(self) -> dict:
        """Find the first item that is a story (not a job)."""
        for story_id in self.get_top_stories():
            item = self.client.get(f"/item/{story_id}.json").json()
            if item.get("type") == "story":
                return item
        raise ValueError("No stories found in top stories")

    def find_first_top_story_with_comments(self) -> dict:
        """Find the first story that has comments."""
        for story_id in self.get_top_stories():
            item = self.client.get(f"/item/{story_id}.json").json()
            if item.get("type") == "story" and item.get("kids"):
                return item
        raise ValueError("No stories with comments found in top stories")
