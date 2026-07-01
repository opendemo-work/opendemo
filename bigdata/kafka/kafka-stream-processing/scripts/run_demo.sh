#!/usr/bin/env bash
# 一键运行 Kafka 流处理演示

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=========================================="
echo "Kafka 流处理演示"
echo "=========================================="

# 检查 Python 依赖
if ! python3 -c "import kafka" 2>/dev/null; then
    echo "安装 Python 依赖..."
    pip install -r requirements.txt
fi

# 创建 topic（如果不存在）
echo "[1/3] 创建 topic 'user-events'..."
docker exec kafka-broker kafka-topics --bootstrap-server localhost:9092 --create --topic user-events --partitions 1 --replication-factor 1 --if-not-exists || true

# 启动消费者（后台）
echo "[2/3] 启动消费者（后台）..."
python3 code/consumer.py &
CONSUMER_PID=$!
sleep 2

# 运行生产者
echo "[3/3] 运行生产者..."
python3 code/producer.py

# 等待消费者处理完消息
sleep 3
kill $CONSUMER_PID 2>/dev/null || true
wait $CONSUMER_PID 2>/dev/null || true

echo ""
echo "✅ 演示完成"
