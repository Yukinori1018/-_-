from dataclasses import dataclass
import os


@dataclass
class YouTubeConfig:
    api_key: str | None = None

    @classmethod
    def from_env(cls) -> "YouTubeConfig":
        return cls(api_key=os.getenv("YOUTUBE_API_KEY"))
