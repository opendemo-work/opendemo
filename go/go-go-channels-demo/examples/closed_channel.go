package examples

import (
	"fmt"
)

// ClosedChannelExample 演示如何安全关闭 channel 并使用 range 遍历
// 关闭 channel 是通知接收者“不再有数据”的标准方式
func ClosedChannelExample() {
	ch := make(chan string)

	// 启动 goroutine 发送多条消息，然后关闭 channel
	go func() {
		// 发送几条数据
		ch <- "item1"
		ch <- "item2"
		ch <- "item3"

		// 显式关闭 channel，表示不会再有数据发送
		// 关闭后仍可从 channel 读取已发送但未接收的数据
		// 再次向已关闭 channel 发送会引发 panic
		close(ch)
	}()

	// 使用 for-range 循环自动接收 channel 中的所有数据
	// 当 channel 关闭且所有数据被接收后，循环自动退出
	// 这是处理 channel 的惯用模式
	for item := range ch {
		fmt.Printf("收到: %s\n", item)
	}

	fmt.Println("channel 已关闭，接收完成。")
}