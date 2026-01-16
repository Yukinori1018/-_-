from __future__ import annotations

import argparse
from pathlib import Path

from youtube_analysis.analyzer import analyze
from youtube_analysis.config import YouTubeConfig
from youtube_analysis.reporting import write_report
from youtube_analysis.sample_data import SAMPLE_CHANNEL, SAMPLE_COMMENTS, SAMPLE_VIDEO


def run_sample(output_dir: Path) -> None:
    analysis = analyze(SAMPLE_CHANNEL, SAMPLE_VIDEO, SAMPLE_COMMENTS)
    report_path, metrics_path = write_report(
        output_dir, SAMPLE_CHANNEL, SAMPLE_VIDEO, analysis, SAMPLE_COMMENTS
    )
    print(f"Sample report written to {report_path}")
    print(f"Sample metrics written to {metrics_path}")


def run_api(channel_id: str, video_id: str, output_dir: Path) -> None:
    config = YouTubeConfig.from_env()
    if not config.api_key:
        raise RuntimeError("YOUTUBE_API_KEY is not set")

    from youtube_analysis.youtube_client import YouTubeClient

    client = YouTubeClient(api_key=config.api_key)
    channel = client.get_channel(channel_id)
    video = client.get_video(video_id)
    comments = client.get_comments(video_id)
    analysis = analyze(channel, video, comments)
    report_path, metrics_path = write_report(output_dir, channel, video, analysis, comments)
    print(f"Report written to {report_path}")
    print(f"Metrics written to {metrics_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="YouTube analysis agent MVP")
    parser.add_argument("--channel-id", help="Target channel ID")
    parser.add_argument("--video-id", help="Target video ID")
    parser.add_argument("--sample", action="store_true", help="Run with sample data")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for report output (default: output)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    output_dir = Path(args.output_dir)

    if args.sample:
        run_sample(output_dir)
        return

    if not args.channel_id or not args.video_id:
        parser.error("--channel-id and --video-id are required unless --sample is used")

    run_api(args.channel_id, args.video_id, output_dir)


if __name__ == "__main__":
    main()
