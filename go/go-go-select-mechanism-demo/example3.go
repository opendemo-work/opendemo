package main

import (
	"fmt"
)

// 示例3: 使用 default 实现非阻塞 select
func main() {
	ch := make(chan string, 1) // 缓冲 channel

	// 尝试读取 channel，但不阻塞
	select {
	case msg := <-ch:
		fmt.Println("读取到消息:", msg)
	default:
		fmt.Println("无数据可读，执行默认操作")
	}

	// 向 channel 写入数据，但不阻塞
	select {
	case ch <- "新消息":
		fmt.Println("成功写入消息")
	default:
		fmt.Println("channel 满，跳过写入")
	}

	// 该模式常用于轮询或状态检查
}