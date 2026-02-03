package main

import (
	"fmt"
	"time"
)

// select_channel.go 演示 select 语句的多路复用能力
func main() {
	// 创建两个 channel：一个用于完成通知，一个用于超时控制
	done := make(chan bool)

	// 启动一个 goroutine 模拟长时间任务
	go func() {
		// 假设任务需要 3 秒完成
		time.Sleep(3 * time.Second)
		done <- true // 任务完成时发送信号
	}()

	// 使用 select 监听多个 channel
	// 哪个 case 先准备好就执行哪个
	select {
	case <-done:
		fmt.Println("接收到信号: done")
		fmt.Println("任务成功完成")
	case <-time.After(2 * time.Second): // 2 秒超时
		fmt.Println("接收到信号: timeout")
		fmt.Println("超时发生，退出程序")
	}
}