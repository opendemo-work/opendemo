"""
Kafka 消费者示例。

从指定 topic 消费消息，并按 event_type 统计数量。
"""

import json
import signal
import sys
from collections import Counter

from kafka import KafkaConsumer


def create_consumer(topic: str, group_id: str, bootstrap_servers: list):
    return KafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        key_deserializer=lambda m: m.decode("utf-8") if m else None,
    )


def main():
    topic = "user-events"
    group_id = "event-processor"
    bootstrap_servers = ["localhost:9092"]

    consumer = create_consumer(topic, group_id, bootstrap_servers)

    shutdown = False

    def handle_signal(signum, frame):
        nonlocal shutdown
        print("\n收到关闭信号，正在优雅退出...")
        shutdown = True

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    stats = Counter()
    print(f"开始消费 topic '{topic}'...")

    try:
        for message in consumer:
            event = message.value
            event_type = event.get("event_type", "unknown")
            stats[event_type] += 1
            print(
                f"📩 partition={message.partition}, offset={message.offset}, "
                f"key={message.key}, event_type={event_type}"
            )

            if shutdown:
                break
    finally:
        consumer.close()
        print("\n消费统计:")
        for event_type, count in sorted(stats.items()):
            print(f"  {event_type}: {count}")
        print("消费者已关闭")


if __name__ == "__main__":
    main()
