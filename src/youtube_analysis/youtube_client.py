from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


@dataclass
class YouTubeClient:
    api_key: str

    def _service(self):
        return build("youtube", "v3", developerKey=self.api_key)

    def get_channel(self, channel_id: str) -> dict[str, Any]:
        try:
            response = (
                self._service()
                .channels()
                .list(part="snippet,statistics", id=channel_id)
                .execute()
            )
        except HttpError as exc:
            raise RuntimeError(f"YouTube API error: {exc}") from exc

        items = response.get("items", [])
        if not items:
            raise ValueError("Channel not found")

        item = items[0]
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        return {
            "id": item.get("id"),
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "subscriberCount": int(stats.get("subscriberCount", 0)),
            "videoCount": int(stats.get("videoCount", 0)),
            "viewCount": int(stats.get("viewCount", 0)),
        }

    def get_video(self, video_id: str) -> dict[str, Any]:
        try:
            response = (
                self._service()
                .videos()
                .list(part="snippet,statistics", id=video_id)
                .execute()
            )
        except HttpError as exc:
            raise RuntimeError(f"YouTube API error: {exc}") from exc

        items = response.get("items", [])
        if not items:
            raise ValueError("Video not found")

        item = items[0]
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        return {
            "id": item.get("id"),
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "publishedAt": snippet.get("publishedAt"),
            "tags": snippet.get("tags", []),
            "viewCount": int(stats.get("viewCount", 0)),
            "likeCount": int(stats.get("likeCount", 0)),
            "commentCount": int(stats.get("commentCount", 0)),
        }

    def get_comments(self, video_id: str, max_results: int = 50) -> list[dict[str, str]]:
        try:
            response = (
                self._service()
                .commentThreads()
                .list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(max_results, 100),
                    textFormat="plainText",
                )
                .execute()
            )
        except HttpError as exc:
            if "disabled" in str(exc):
                return []
            raise RuntimeError(f"YouTube API error: {exc}") from exc

        comments: list[dict[str, str]] = []
        for item in response.get("items", []):
            snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
            comments.append(
                {
                    "author": snippet.get("authorDisplayName", ""),
                    "text": snippet.get("textDisplay", ""),
                }
            )
        return comments
