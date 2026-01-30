package main

import (
	"context"
	"fmt"
	"log"
	"strings"
	"time"

	"github.com/Shopify/sarama"
)

// MyConsumerGroupHandler 实现消费者组处理器接口
type MyConsumerGroupHandler struct{}

// Setup 在会话开始时调用
func (h MyConsumerGroupHandler) Setup(_ sarama.ConsumerGroupSession) error {
	return nil
}

// Cleanup 在会话结束时调用
func (h MyConsumerGroupHandler) Cleanup(_ sarama.ConsumerGroupSession) error {
	return nil
}

// ConsumeClaim 处理分配给该消费者的每个分区的消息
func (h MyConsumerGroupHandler) ConsumeClaim(
	session sarama.ConsumerGroupSession,
	claim sarama.ConsumerGroupClaim,
) error {
	for msg := range claim.Messages() {
		fmt.Printf(
			"📩 收到消息: %s (来自分区: %d, 偏移量: %d)\n",
			string(msg.Value),
			msg.Partition,
			msg.Offset,
		)
		// 标记消息已处理（自动提交偏移量）
		session.MarkMessage(msg, "")
	}
	return nil
}

func main() {
	config := sarama.NewConfig()
	config.Version = sarama.V2_8_0_0 // 显式设置Kafka版本
	config.Consumer.Group.Rebalance.Strategy = sarama.BalanceStrategyRoundRobin
	config.Consumer.Offsets.Initial = sarama.OffsetOldest // 从最早消息开始

	// 创建消费者组
	consumerGroup, err := sarama.NewConsumerGroup([]string{"localhost:9092"}, "demo-group", config)
	if err != nil {
		log.Fatalf("❌ 创建消费者组失败: %v", err)
	}
	defer func() { _ = consumerGroup.Close() }()

	fmt.Println("✅ 正在连接Kafka...")
	
	// 消费循环
	ctx := context.Background()
	for {
		err := consumerGroup.Consume(ctx, []string{"test-topic"}, MyConsumerGroupHandler{})
		if err != nil {
			log.Printf("⚠️ 消费中断，5秒后重连: %v", err)
			time.Sleep(5 * time.Second)
			continue
		}

		// 检查上下文是否被取消
		if ctx.Err() != nil {
			return
		}
	}
}