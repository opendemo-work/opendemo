package main

import (
	"fmt"
	"log"
	"time"

	"github.com/Shopify/sarama"
)

// 主函数：Kafka生产者示例
func main() {
	// 配置生产者
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true // 启用成功通知
	config.Producer.Retry.Max = 3           // 失败重试次数

	// 创建同步生产者实例
	producer, err := sarama.NewSyncProducer([]string{"localhost:9092"}, config)
	if err != nil {
		log.Fatalf("❌ 创建生产者失败: %v", err)
	}
	defer func() { _ = producer.Close() }()

	fmt.Println("✅ 生产者启动成功，开始发送消息...")

	// 发送10条测试消息
	for i := 1; i <= 10; i++ {
		message := fmt.Sprintf("Hello Kafka! [序号: %d]", i)
		msg := &sarama.ProducerMessage{
			Topic: "test-topic",
			Value: sarama.StringEncoder(message),
		}

		// 发送消息并等待确认
		partition, offset, err := producer.SendMessage(msg)
		if err != nil {
			log.Printf("❌ 发送消息失败 #%d: %v", i, err)
		} else {
			fmt.Printf("✅ 消息已发送：%s (分区: %d, 偏移量: %d)\n", message, partition, offset)
		}

		time.Sleep(500 * time.Millisecond) // 控制发送频率
	}
}