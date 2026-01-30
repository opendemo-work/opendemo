package examples

import (
	"fmt"
)

// BasicChannelExample 演示最基本的 channel 通信
// 创建一个无缓冲 channel，启动 goroutine 发送消息，主线程接收
func BasicChannelExample() {
	// 创建一个字符串类型的无缓冲 channel
	// 无缓冲意味着发送和接收必须同时就绪，否则阻塞
	ch := make(chan string)

	// 启动一个新的 goroutine
	go func() {
		// 向 channel 发送一条消息
		// 此处会阻塞，直到有人从 channel 接收
		ch <- "Hello from goroutine!"
	}()

	// 从 channel 接收消息
	// 这里会等待 goroutine 发送数据
	msg := <-ch
	fmt.Printf("接收到消息: %s\n", msg)

	// 注意：实际开发中应考虑使用 sync.WaitGroup
	// 确保 goroutine 执行完成，此处因有 channel 通信而自然同步
}