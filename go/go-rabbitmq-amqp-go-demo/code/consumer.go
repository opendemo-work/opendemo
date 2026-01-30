package main

import (
	"log"

	"github.com/streadway/amqp"
)

const amqpURL = "amqp://guest:guest@localhost:5672/"

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	conn, err := amqp.Dial(amqpURL)
	failOnError(err, "无法连接到RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "无法打开通道")
	defer ch.Close()

	// 确保队列存在
	_, err = ch.QueueDeclare(
		"hello",
		true,  // 持久化
		false, // 自动删除
		false, // 排他
		false, // 不等待
		nil,
	)
	failOnError(err, "声明队列失败")

	// 设置消费者从队列获取消息
	msgs, err := ch.Consume(
		"hello", // 队列名称
		"",      // 消费者名称（由服务器生成）
		false,   // 自动ACK
		false,   // 非排他
		false,   // 不本地化
		false,   // 不等待
		nil,     // 参数
	)
	failOnError(err, "注册消费者失败")

	log.Printf("[*] Waiting for messages. To exit press CTRL+C")

	// 使用匿名函数处理每条消息
	forever := make(chan bool)

	go func() {
		for d := range msgs {
			log.Printf("[+] Received %s", d.Body)

			// 模拟消息处理时间
			// time.Sleep(time.Second * 1)

			// 手动发送ACK确认
			d.Ack(false)
		}
	}()

	<-forever // 阻塞主协程
}