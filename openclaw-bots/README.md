# OpenClaw 独立3体Bot セットアップ

既存のオープンクローBotとは**完全に独立した**3体のOpenClaw Discord Botです。
各Botは個別のDockerコンテナ・Discordトークン・AIプロバイダーキーで動作します。

## 構成

| Bot | ディレクトリ | ポート | コンテナ名 |
|-----|-------------|--------|-----------|
| Alpha | `bot-alpha/` | 18789 | openclaw-alpha |
| Beta | `bot-beta/` | 18790 | openclaw-beta |
| Gamma | `bot-gamma/` | 18791 | openclaw-gamma |

## 事前準備

### 1. Dockerのインストール

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# ログアウト・ログインし直す
```

### 2. Discord Botアプリケーションの作成 (3つ)

[Discord Developer Portal](https://discord.com/developers/applications) で**3つ**のアプリケーションを作成します:

各アプリケーションで以下を実行:
1. **New Application** をクリック → 名前を入力 (例: `OpenClaw Alpha`)
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
- [Anthropic](https://console.anthropic.com/) (Claude)
- [OpenAI](https://platform.openai.com/)
- [OpenRouter](https://openrouter.ai/)

## セットアップ手順

```bash
# 1. セットアップスクリプト実行
cd openclaw-bots
./setup.sh

# 2. 各Botの .env ファイルを編集
#    Discord Bot トークンとAPIキーを入力
nano bot-alpha/.env
nano bot-beta/.env
nano bot-gamma/.env

# 3. 全Bot起動
./start-all.sh

# 4. 各BotにDiscordチャンネルを追加
cd bot-alpha && docker compose run --rm openclaw-cli channels add --channel discord --token "$DISCORD_BOT_TOKEN"
cd ../bot-beta && docker compose run --rm openclaw-cli channels add --channel discord --token "$DISCORD_BOT_TOKEN"
cd ../bot-gamma && docker compose run --rm openclaw-cli channels add --channel discord --token "$DISCORD_BOT_TOKEN"
```

## 管理コマンド

```bash
# 全Bot起動
./start-all.sh

# 全Bot停止
./stop-all.sh

# ステータス確認
./status.sh

# 個別Bot操作
cd bot-alpha
docker compose up -d        # 起動
docker compose down          # 停止
docker compose logs -f       # ログ確認
docker compose run --rm openclaw-cli doctor  # 診断

# 個別Botのオンボーディング(初回設定ウィザード)
cd bot-alpha && docker compose run --rm openclaw-cli onboard
```

## サーバー分離について

3体のBotは以下のどちらでも運用できます:

- **同一サーバー**: 3体全てを1つのDiscordサーバーに招待
- **別サーバー**: 各Botを異なるDiscordサーバーに招待 (推奨)

別サーバーにする場合はDiscordで新しいサーバーを作成し、各Botを個別に招待してください。

## セキュリティ注意事項

- `.env` ファイルには機密情報が含まれるため、**絶対にGitにコミットしない**こと
- Botに Administrator 権限を与えないこと
- `allowlist` で応答するユーザーを制限することを推奨
