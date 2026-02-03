package main

import (
	"fmt"
	"time"
)

// 演示select的基础用法：监听多个channel
func main() {
	// 创建两个字符串类型的channel
	ch1 := make(chan string)
	ch2 := make(chan string)

	// 启动第一个goroutine，1秒后发送消息
	go func() {
		time.Sleep(1 * time.Second)
		ch1 <- "Hello from channel!"
	}()

	// 启动第二个goroutine，2秒后发送消息
	go func() {
		time.Sleep(2 * time.Second)
		ch2 <- "Hi from another channel!"
	}()

	// 使用select监听两个channel
	// 哪个先准备好就执行哪个case
	select {
	case msg := <-ch1:
		fmt.Printf("接收到消息：%s\n", msg)
	case msg := <-ch2:
		fmt.Printf("接收到消息：%s\n", msg)
	}
	// 注意：由于select只执行一次，只会处理最先到达的消息
}