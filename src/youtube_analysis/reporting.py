from __future__ import annotations

from pathlib import Path
import csv

from youtube_analysis.analyzer import AnalysisResult


def write_report(
    output_dir: Path,
    channel: dict,
    video: dict,
    analysis: AnalysisResult,
    comments: list[dict[str, str]],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "report.md"
    metrics_path = output_dir / "metrics.csv"

    if analysis.click_through_rate is None:
        ctr_line = "- CTR (提供値または推定): N/A"
    else:
        ctr_line = f"- CTR (提供値または推定): {analysis.click_through_rate:.2%}"

    report_lines = [
        "# YouTube 競合分析レポート (MVP)",
        "",
        "## チャンネル概要",
        f"- チャンネル名: {channel.get('title')}",
        f"- 登録者数: {channel.get('subscriberCount')}",
        f"- 総再生数: {channel.get('viewCount')}",
        f"- 平均視聴回数 (総再生/動画数): {analysis.avg_views_per_video:.0f}",
        "",
        "## 動画概要",
        f"- タイトル: {video.get('title')}",
        f"- 公開日: {video.get('publishedAt')}",
        f"- 視聴回数: {video.get('viewCount')}",
        f"- いいね数: {video.get('likeCount')}",
        f"- コメント数: {video.get('commentCount')}",
        ctr_line,
        "",
        "## インサイト",
        f"- タイトル文字数: {analysis.title_length}",
        f"- タグ数: {analysis.tag_count}",
        f"- エンゲージ率 (いいね+コメント / 再生数): {analysis.engagement_rate:.2%}",
        f"- 視聴数 / 登録者数: {analysis.view_subscriber_ratio:.2f}",
        f"- 平均視聴回数 (チャンネル全体): {analysis.avg_views_per_video:.0f}",
        "",
        "### コメント頻出語",
    ]

    if analysis.top_comment_terms:
        report_lines.extend(
            [f"- {term}: {count}" for term, count in analysis.top_comment_terms]
        )
    else:
        report_lines.append("- コメントが取得できませんでした")

    report_lines.append("")
    report_lines.append("## コメントサンプル")
    for comment in comments[:5]:
        report_lines.append(f"- {comment.get('text')}")

    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    metrics_rows = [
        {
            "metric": "title_length",
            "value": analysis.title_length,
        },
        {
            "metric": "tag_count",
            "value": analysis.tag_count,
        },
        {
            "metric": "engagement_rate",
            "value": analysis.engagement_rate,
        },
        {
            "metric": "view_subscriber_ratio",
            "value": analysis.view_subscriber_ratio,
        },
        {
            "metric": "avg_views_per_video",
            "value": analysis.avg_views_per_video,
        },
        {
            "metric": "click_through_rate",
            "value": analysis.click_through_rate,
        },
    ]
    with metrics_path.open("w", encoding="utf-8", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(metrics_rows)

    return report_path, metrics_path
