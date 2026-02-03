package main

import (
	"fmt"
	"math/rand"
	"time"
)

// 示例1: 基础 select - 从多个 channel 中选择一个接收
func main() {
	// 创建两个字符串 channel
	chA := make(chan string)
	chB := make(chan string)

	// 启动两个 goroutine，分别向 channel 发送消息
	go func() {
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // 随机延迟
		chA <- "Hello from channel A"
	}()

	go func() {
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // 随机延迟
		chB <- "Hello from channel B"
	}()

	// 使用 select 等待任意一个 channel 返回数据
	select {
	case msg := <-chA:
		fmt.Println("收到消息:", msg)
	case msg := <-chB:
		fmt.Println("收到消息:", msg)
	}
	// 注意：一旦某个 case 执行，select 结束
}