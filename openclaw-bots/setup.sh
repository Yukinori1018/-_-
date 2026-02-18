#!/bin/bash
# ============================================
# OpenClaw 3体Bot 一括セットアップスクリプト
# ============================================
set -e

BOTS=("bot-alpha" "bot-beta" "bot-gamma")
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🦞 OpenClaw 3体Bot セットアップを開始します"
echo "================================================"
echo ""

# Docker確認
if ! command -v docker &> /dev/null; then
    echo "❌ Dockerがインストールされていません。"
    echo "   https://docs.docker.com/get-docker/ からインストールしてください。"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose v2が見つかりません。"
    exit 1
fi

echo "✅ Docker & Docker Compose が確認できました"
echo ""

# 各Botの.envファイルを作成
for bot in "${BOTS[@]}"; do
    BOT_DIR="$SCRIPT_DIR/$bot"
    ENV_FILE="$BOT_DIR/.env"
    EXAMPLE_FILE="$BOT_DIR/.env.example"

    echo "--- $bot のセットアップ ---"

    if [ -f "$ENV_FILE" ]; then
        echo "  ⚠️  .env ファイルが既に存在します。スキップします。"
        echo "     (上書きする場合は $ENV_FILE を削除してから再実行してください)"
    else
        cp "$EXAMPLE_FILE" "$ENV_FILE"
        echo "  📄 .env ファイルを作成しました: $ENV_FILE"
        echo "  ⚠️  $ENV_FILE を編集してトークンとAPIキーを設定してください！"
    fi

    # workspace ディレクトリ作成
    mkdir -p "$BOT_DIR/workspace"
    mkdir -p "$BOT_DIR/data"
    echo "  📁 workspace/ と data/ ディレクトリを作成しました"
    echo ""
done

echo "================================================"
echo "🦞 セットアップ完了！"
echo ""
echo "次のステップ:"
echo "  1. 各Botの .env ファイルを編集してトークンを設定"
echo "     - bot-alpha/.env"
echo "     - bot-beta/.env"
echo "     - bot-gamma/.env"
echo ""
echo "  2. Discord Developer Portal で3つのBotアプリを作成"
echo "     https://discord.com/developers/applications"
echo ""
echo "  3. 起動:"
echo "     全Bot起動:  ./start-all.sh"
echo "     個別起動:    cd bot-alpha && docker compose up -d"
echo ""
echo "  4. Discordチャンネルを追加:"
echo "     cd bot-alpha && docker compose run --rm openclaw-cli channels add --channel discord --token \"<token>\""
echo ""
