package main

import (
	"fmt"
	"time"
)

// 示例3: select 配合 timeout 实现超时控制
// 展示如何防止 goroutine 无限等待 channel 数据
func main() {
	// 创建一个用于通信的 channel
	ch := make(chan string)

	// 启动一个 goroutine，模拟耗时操作（例如网络请求）
	// 它将在 2 秒后返回结果
	go func() {
		time.Sleep(2 * time.Second)
		ch <- "operation result"
	}()

	// 使用 select 设置 1 秒超时
	// 如果 1 秒内 ch 没有数据，则执行 timeout 分支
	select {
	case msg := <-ch:
		fmt.Println("Received:", msg)
	case <-time.After(1 * time.Second):
		fmt.Println("Timeout occurred, stopping...")
		// 实际项目中可结合 context 实现更复杂的取消机制
	}

	// 注意：未被接收的 channel 数据会导致 goroutine 泄漏
	// 生产环境应使用 context 控制生命周期
}