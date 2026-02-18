# OpenClaw 階層型3体Bot システム

既存のオープンクローBotとは**完全に独立した**3体のOpenClaw Discord Botです。
**Alpha (統括) → Beta, Gamma (ワーカー)** の階層構造で動作します。

## アーキテクチャ

```
  ユーザー (Yukinori)
       │
       ▼
┌──────────────┐
│  Alpha (統括)  │  Claude Opus — 指示・レビュー・改善指示
│  ポート:18789  │
└──┬───────┬───┘
   │       │
   ▼       ▼
┌──────┐ ┌──────┐
│ Beta │ │Gamma │  Claude Sonnet — タスク実行
│:18790│ │:18791│
└──────┘ └──────┘
```

| Bot | 役割 | モデル | ディレクトリ | ポート |
|-----|------|--------|-------------|--------|
| **Alpha** | 統括・レビュー・改善指示 | Claude Opus 4.5 | `bot-alpha/` | 18789 |
| **Beta** | ワーカー (タスク実行) | Claude Sonnet 4.5 | `bot-beta/` | 18790 |
| **Gamma** | ワーカー (タスク実行) | Claude Sonnet 4.5 | `bot-gamma/` | 18791 |

## 各Botの設定ファイル

各Botの `workspace/` にパーソナリティと運用ルールが定義されています:

| ファイル | 内容 |
|---------|------|
| `SOUL.md` | Botの人格・コミュニケーションスタイル・価値観 |
| `AGENTS.md` | 運用ガイドライン・テンプレート・安全ルール |
| `USER.md` | ユーザー情報・指揮系統 |

## 事前準備

### 1. Dockerのインストール

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# ログアウト・ログインし直す
```

### 2. Discord Botアプリケーションの作成 (3つ)

[Discord Developer Portal](https://discord.com/developers/applications) で**3つ**のアプリケーションを作成:

各アプリケーションで以下を実行:
1. **New Application** → 名前を入力 (例: `Alpha統括`, `Betaワーカー`, `Gammaワーカー`)
2. **Bot** タブ → **Reset Token** → トークンをコピー
3. **Bot** タブ → **Privileged Gateway Intents**:
   - ✅ **Message Content Intent** (必須)
   - ✅ **Server Members Intent** (推奨)
4. **OAuth2** → **URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Permissions: `View Channels`, `Send Messages`, `Read Message History`, `Embed Links`, `Attach Files`, `Add Reactions`
5. 生成されたURLでBotをサーバーに招待

### 3. AIプロバイダーのAPIキー

以下のいずれか1つ以上:
- [Anthropic](https://console.anthropic.com/) (Claude) — **推奨**
- [OpenAI](https://platform.openai.com/)
- [OpenRouter](https://openrouter.ai/)

### 4. Discordサーバーとチャンネルの作成

詳細は **[DISCORD_SETUP.md](./DISCORD_SETUP.md)** を参照。

推奨チャンネル構成:
```
#command-center  ← ユーザー + Alpha
#beta-tasks      ← Alpha → Beta への指示
#gamma-tasks     ← Alpha → Gamma への指示
#review          ← Beta/Gamma の成果物 → Alpha がレビュー
#project-log     ← 全Bot の進捗ログ
```

## セットアップ手順

```bash
# 1. セットアップスクリプト実行
cd openclaw-bots
./setup.sh

# 2. 各Botの .env ファイルを編集 (トークンとAPIキーを入力)
nano bot-alpha/.env
nano bot-beta/.env
nano bot-gamma/.env

# 3. 全Bot起動
./start-all.sh

# 4. 各BotにDiscordチャンネルを追加
cd bot-alpha && docker compose run --rm openclaw-cli channels add --channel discord --token "$DISCORD_BOT_TOKEN"
cd ../bot-beta && docker compose run --rm openclaw-cli channels add --channel discord --token "$DISCORD_BOT_TOKEN"
cd ../bot-gamma && docker compose run --rm openclaw-cli channels add --channel discord --token "$DISCORD_BOT_TOKEN"

# 5. (推奨) オンボーディングを実行して初期設定
cd ../bot-alpha && docker compose run --rm openclaw-cli onboard
cd ../bot-beta && docker compose run --rm openclaw-cli onboard
cd ../bot-gamma && docker compose run --rm openclaw-cli onboard
```

## 管理コマンド

```bash
./start-all.sh          # 全Bot起動
./stop-all.sh           # 全Bot停止
./status.sh             # ステータス確認

# 個別操作
cd bot-alpha
docker compose up -d              # 起動
docker compose down                # 停止
docker compose logs -f             # ログ確認
docker compose run --rm openclaw-cli doctor   # 診断
```

## 運用フロー

1. ユーザーが `#command-center` でAlphaにプロジェクトを依頼
2. Alpha がタスクを分析・分割し、`#beta-tasks` / `#gamma-tasks` に指示を投稿
3. Beta / Gamma がそれぞれ作業を実行
4. 完了後、`#review` に成果物を投稿
5. Alpha がレビューし、承認 or 修正指示
6. 全タスク完了後、Alpha が `#command-center` でユーザーに報告

## セキュリティ注意事項

- `.env` ファイルは**絶対にGitにコミットしない**
- Botに Administrator 権限を与えない
- `allowlist` で応答するユーザーを制限することを推奨
- 各Botの `SOUL.md` に「破壊的操作は承認が必要」のルールが組み込み済み
