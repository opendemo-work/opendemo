package main

import "fmt"

// closingChannelDemo 演示如何安全关闭 channel
// 并检测 channel 的关闭状态，避免无限等待或错误读取
func main() {
	// 创建一个整型 channel
	ch := make(chan int)

	// 启动 goroutine 发送有限数据并关闭 channel
	go func() {
		ch <- 1
		ch <- 2
		ch <- 3
		// 显式关闭 channel，表示不再有数据发送
		close(ch)
	}()

	// 使用 for 循环持续接收数据，直到 channel 关闭
	for {
		// 使用逗号 ok 语法判断 channel 是否关闭
		value, ok := <-ch
		if !ok {
			// ok 为 false 表示 channel 已关闭且无数据
			fmt.Println("channel 已关闭，不再有数据")
			break
		}
		fmt.Printf("接收到数值: %d\n", value)
	}
}
