# YouTube 自動分析エージェント (MVP)

## 目的
競合チャンネルや動画を調査・分析し、勝てる要因を仮説化するための土台を構築します。Phase 1〜2の最小実装として、**1チャンネル / 1動画の分析**を行うCLIを用意しました。

## 透明性: これから行うロジック
1. **YouTube Data API からチャンネル/動画/コメントを取得**
2. **タイトル・タグ・統計値・コメント頻出語を抽出**
3. **簡易インサイト (例: CTR、平均視聴回数、エンゲージ率、タイトル長)** を計算
4. **Markdown/CSVレポートに出力**

## 使い方

### 1) APIキーを使う場合
```bash
export YOUTUBE_API_KEY="YOUR_API_KEY"
python -m youtube_analysis.cli --channel-id "UC_x5XG1OV2P6uZZ5FSM9Ttw" --video-id "dQw4w9WgXcQ"
```

### 2) サンプルデータで動作確認
```bash
python -m youtube_analysis.cli --sample
```

## 出力
- `output/report.md`
- `output/metrics.csv`

## 解析対象 (初期設定)
- ジャンル: 日本称賛、日本観光
- データソース: YouTube API
- 優先指標: CTR、チャンネル登録者数、平均視聴回数
- 出力形式: CSV、レポート

## 次のステップ
- 複数キーワード・競合リストのループ処理
- 追加指標 (CTR/維持率が得られる場合は外部推定)
- サムネイルの視覚分析 (画像特徴量)
