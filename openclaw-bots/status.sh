#!/bin/bash
# ============================================
# OpenClaw 3体Bot ステータス確認スクリプト
# ============================================

BOTS=("bot-alpha" "bot-beta" "bot-gamma")
PORTS=("18789" "18790" "18791")
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🦞 OpenClaw 3体Bot ステータス"
echo "================================================"
echo ""

for i in "${!BOTS[@]}"; do
    bot="${BOTS[$i]}"
    port="${PORTS[$i]}"
    BOT_DIR="$SCRIPT_DIR/$bot"

    echo "--- $bot (ポート: $port) ---"

    if [ ! -f "$BOT_DIR/.env" ]; then
        echo "  ⚠️  .env 未設定"
    else
        echo "  ✅ .env 設定済み"
    fi

    # Dockerコンテナの状態
    container_name="openclaw-${bot#bot-}"
    status=$(docker inspect --format='{{.State.Status}}' "$container_name" 2>/dev/null || echo "stopped")
    if [ "$status" = "running" ]; then
        echo "  🟢 稼働中"
    else
        echo "  🔴 停止中"
    fi
    echo ""
done
