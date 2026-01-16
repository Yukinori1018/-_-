from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable


@dataclass
class AnalysisResult:
    title_length: int
    tag_count: int
    engagement_rate: float
    view_subscriber_ratio: float
    avg_views_per_video: float
    click_through_rate: float | None
    top_comment_terms: list[tuple[str, int]]


def _tokenize(text: str) -> list[str]:
    normalized = "".join(char if char.isalnum() else " " for char in text)
    tokens = [token for token in normalized.split() if len(token) > 1]
    return tokens


def _top_terms(texts: Iterable[str], top_n: int = 5) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    for text in texts:
        counter.update(_tokenize(text.lower()))
    return counter.most_common(top_n)


def analyze(channel: dict, video: dict, comments: list[dict[str, str]]) -> AnalysisResult:
    title_length = len(video.get("title", ""))
    tags = video.get("tags", [])
    tag_count = len(tags)

    view_count = max(video.get("viewCount", 0), 1)
    like_count = video.get("likeCount", 0)
    comment_count = video.get("commentCount", 0)
    subscriber_count = max(channel.get("subscriberCount", 0), 1)

    engagement_rate = (like_count + comment_count) / view_count
    view_subscriber_ratio = view_count / subscriber_count
    video_count = max(channel.get("videoCount", 0), 1)
    avg_views_per_video = channel.get("viewCount", 0) / video_count
    click_through_rate = video.get("clickThroughRate")

    top_comment_terms = _top_terms([c.get("text", "") for c in comments])

    return AnalysisResult(
        title_length=title_length,
        tag_count=tag_count,
        engagement_rate=engagement_rate,
        view_subscriber_ratio=view_subscriber_ratio,
        avg_views_per_video=avg_views_per_video,
        click_through_rate=click_through_rate,
        top_comment_terms=top_comment_terms,
    )
