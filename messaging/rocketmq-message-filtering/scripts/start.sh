#!/usr/bin/env bash
# 风险等级：🟡 中风险
# 说明：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
# 生产安全提示：
#   - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
#   - 注意检查依赖版本、端口占用和目标资源配置。
#   - 生产环境执行前请经过变更评审和备份确认。

# 启动 RocketMQ 消息过滤演示

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "启动 RocketMQ 消息过滤演示..."

if command -v docker-compose &>/dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo "等待服务就绪..."
sleep 10

echo "✅ RocketMQ 消息过滤演示 已启动"
