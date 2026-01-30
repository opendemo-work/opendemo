package main

import (
	"log"
	"time"

	"github.com/streadway/amqp"
)

// 连接URL格式：amqp://用户名:密码@主机:端口/
const amqpURL = "amqp://guest:guest@localhost:5672/"

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	// 建立与RabbitMQ服务器的连接
	conn, err := amqp.Dial(amqpURL)
	failOnError(err, "无法连接到RabbitMQ")
	defer conn.Close()

	// 创建一个通道
	ch, err := conn.Channel()
	failOnError(err, "无法打开通道")
	defer ch.Close()

	// 声明一个队列，确保其存在
	queue, err := ch.QueueDeclare(
		"hello",  // 队列名称
		true,   // 持久化
		false,  // 自动删除
		false,  // 排他性
		false,  // 不等待
		nil,    // 额外参数
	)
	failOnError(err, "声明队列失败")

	// 发送消息
	body := "Hello World!"
	publishErr := ch.Publish(
		"",        // exchange，默认交换机
		queue.Name, // routing key
		false,     // mandatory
		false,     // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(body),
			Timestamp:   time.Now(),
			DeliveryMode: amqp.Persistent, // 消息持久化
		},
	)
	failOnError(publishErr, "发送消息失败")
	log.Printf("[+] Sent '%s'\n", body)
}