package main

import (
	"fmt"
	"math/rand"
	"time"
)

// 示例1: 基础 select 多路复用
// 展示 select 如何从多个 channel 中选择最先可用的数据
func main() {
	// 设置随机种子，确保每次运行结果可能不同
	rand.Seed(time.Now().UnixNano())

	// 创建两个字符串 channel
	ch1 := make(chan string)
	ch2 := make(chan string)

	// 启动第一个 goroutine，随机延迟后发送消息
	go func() {
		delay := time.Duration(rand.Intn(1000)) * time.Millisecond
		time.Sleep(delay)
		ch1 <- "Hello from channel 1"
	}()

	// 启动第二个 goroutine，随机延迟后发送消息
	go func() {
		delay := time.Duration(rand.Intn(1000)) * time.Millisecond
		time.Sleep(delay)
		ch2 <- "Hello from channel 2"
	}()

	// select 会监听多个 channel，任一有数据即可读时执行对应 case
	// 如果多个同时就绪，runtime 会随机选择一个
	select {
	case msg := <-ch1:
		fmt.Println("Received:", msg)
	case msg := <-ch2:
		fmt.Println("Received:", msg)
	}

	// 注意：程序不会等待另一个 channel，select 执行一次即退出
}