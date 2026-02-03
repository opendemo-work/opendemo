package main

import (
	"fmt"
	"time"
)

// 示例2: 使用 default 实现非阻塞 channel 操作
// 展示如何避免在 channel 操作时阻塞主流程
func main() {
	// 创建一个带缓冲的 channel，容量为1
	ch := make(chan string, 1)

	// 先放入一个数据，使 channel 满
	ch <- "existing data"

	// 尝试非阻塞发送新数据
	select {
	case ch <- "new data":
		fmt.Println("Sent data")
	default:
		fmt.Println("Attempting to send... Non-blocking send failed, doing other work.")
		// 即使发送失败也不阻塞，继续执行其他逻辑
	}

	// 模拟做其他工作
	time.Sleep(100 * time.Millisecond)

	// 尝试非阻塞接收
	select {
	case msg := <-ch:
		fmt.Println("Received without blocking:", msg)
	default:
		fmt.Println("No data ready, not waiting.")
	}
}