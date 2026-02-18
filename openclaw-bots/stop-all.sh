#!/bin/bash
# ============================================
# OpenClaw 3体Bot 一括停止スクリプト
# ============================================
set -e

BOTS=("bot-alpha" "bot-beta" "bot-gamma")
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🦞 OpenClaw 3体Bot を停止します..."
echo ""

for bot in "${BOTS[@]}"; do
    BOT_DIR="$SCRIPT_DIR/$bot"
    echo "⏹️  $bot を停止中..."
    (cd "$BOT_DIR" && docker compose down) 2>/dev/null || echo "  (起動していません)"
    echo ""
done

echo "✅ 全Bot停止完了"
