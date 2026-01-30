package main

import (
	"fmt"
	"time"
)

// basicChannelDemo 演示最基本的 channel 通信
// 使用无缓冲 channel 实现两个 goroutine 之间的同步消息传递
func main() {
	// 创建一个字符串类型的无缓冲 channel
	ch := make(chan string)

	// 启动一个新 goroutine 发送消息
	go func() {
		// 模拟一些处理时间
		time.Sleep(time.Millisecond * 100)
		// 向 channel 发送消息
		// 此操作会阻塞，直到有人接收
		ch <- "Hello from goroutine!"
	}()

	// 从 channel 接收消息
	// 主函数会在此处阻塞，直到收到数据
	msg := <-ch
	fmt.Printf("接收到消息: %s\n", msg)
}
