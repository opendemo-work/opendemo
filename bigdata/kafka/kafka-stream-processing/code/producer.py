"""
Kafka 生产者示例。

向指定 topic 发送模拟用户行为事件（JSON 格式）。
"""

import json
import random
import time
from datetime import datetime

from kafka import KafkaProducer


def create_event(user_id: int) -> dict:
    """生成一条模拟事件。"""
    return {
        "user_id": f"user_{user_id:04d}",
        "event_type": random.choice(["click", "view", "purchase"]),
        "page": random.choice(["/home", "/product", "/cart", "/checkout"]),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "value": round(random.uniform(0, 100), 2),
    }


def main():
    topic = "user-events"
    bootstrap_servers = ["localhost:9092"]

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
    )

    print(f"开始向 topic '{topic}' 发送消息...")
    try:
        for i in range(20):
            event = create_event(i)
            key = event["user_id"]
            future = producer.send(topic, key=key, value=event)
            record_metadata = future.get(timeout=10)
            print(
                f"✅ 已发送: partition={record_metadata.partition}, "
                f"offset={record_metadata.offset}, event={event['event_type']}"
            )
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n收到中断信号，停止发送")
    finally:
        producer.flush()
        producer.close()
        print("生产者已关闭")


if __name__ == "__main__":
    main()
