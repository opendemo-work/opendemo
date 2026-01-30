package main

import (
	"log"
	"time"

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

	// 声明相同的队列
	_, err = ch.QueueDeclare(
		"hello",
		true,
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "声明队列失败")

	// 设置QoS：一次只处理一条消息（公平分发）
	err = ch.Qos(
		1,       // prefetch count
		0,       // prefetch size
		false,   // global
	)
	failOnError(err, "设置QoS失败")

	// 注册消费者
	msgs, err := ch.Consume(
		"hello",
		"",
		false, // 手动ACK
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "注册消费者失败")

	log.Printf("[*] Waiting for tasks. To exit press CTRL+C")

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			log.Printf("[+] Received task: %s", d.Body)

			// 模拟耗时任务
			dotCount := 0
			for _, b := range d.Body {
				if b == '.' {
					dotCount++
				}
			}
			time.Sleep(time.Duration(dotCount) * time.Second)

			log.Printf("[+] Done processing task")

			// 发送ACK
			d.Ack(false)
		}
	}()

	<-forever
}