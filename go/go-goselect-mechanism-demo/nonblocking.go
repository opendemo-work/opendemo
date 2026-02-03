package main

import (
	"fmt"
	"time"
)

// 演示非阻塞的channel操作
func main() {
	ch := make(chan string)

	// 模拟周期性检查是否有消息，但不阻塞
	for i := 0; i < 3; i++ {
		select {
		case msg := <-ch:
			fmt.Printf("接收到消息：%s\n", msg)
		default:
			// 如果channel中没有数据，立即执行default分支
			fmt.Println("无可用消息，执行其他任务...")
			time.Sleep(500 * time.Millisecond) // 模拟做其他事情
		}
	}

	// 稍后发送一条消息
	go func() {
		time.Sleep(1 * time.Second)
		ch <- "delayed message"
	}()

	// 再次尝试非阻塞读取（可能仍读不到，取决于调度）
	time.Sleep(200 * time.Millisecond)
	select {
	case msg := <-ch:
		fmt.Printf("最终接收到延迟消息：%s\n", msg)
	default:
		fmt.Println("仍然没有消息到来")
	}
}