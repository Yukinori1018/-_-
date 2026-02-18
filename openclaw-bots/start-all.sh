#!/bin/bash
# ============================================
# OpenClaw 3体Bot 一括起動スクリプト
# ============================================
set -e

BOTS=("bot-alpha" "bot-beta" "bot-gamma")
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🦞 OpenClaw 3体Bot を起動します..."
echo ""

for bot in "${BOTS[@]}"; do
    BOT_DIR="$SCRIPT_DIR/$bot"

    if [ ! -f "$BOT_DIR/.env" ]; then
        echo "❌ $bot/.env が見つかりません。先に setup.sh を実行してください。"
        continue
    fi

    echo "🚀 $bot を起動中..."
    (cd "$BOT_DIR" && docker compose up -d)
    echo "✅ $bot 起動完了"
    echo ""
done

echo "================================================"
echo "🦞 全Bot起動完了！"
echo ""
echo "状態確認:  ./status.sh"
echo "全停止:    ./stop-all.sh"
echo "ログ確認:  cd bot-alpha && docker compose logs -f"
