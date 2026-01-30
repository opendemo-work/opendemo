package examples

import (
	"fmt"
	"time"
)

// BufferedSelectExample 展示带缓冲 channel 和 select 多路复用
// 缓冲 channel 可以临时存储数据，不立即阻塞发送
// select 允许多个 channel 操作进行监听
func BufferedSelectExample() {
	// 创建两个 channel：一个带缓冲，一个无缓冲
	ch1 := make(chan string, 2) // 缓冲大小为2
	ch2 := make(chan string)    // 无缓冲

	// 向 ch1 发送两条消息（不会阻塞，因为有缓冲空间）
	ch1 <- "message1"
	ch1 <- "message2"

	// 启动 goroutine 向 ch2 发送消息（延迟发送）
	go func() {
		time.Sleep(100 * time.Millisecond)
		ch2 <- "message2"
	}()

	// 使用 select 监听多个 channel 操作
	// select 会随机选择一个就绪的 case 执行
	select {
	case msg := <-ch1:
		fmt.Printf("received from ch1: %s\n", msg)
	case msg := <-ch2:
		fmt.Printf("received from ch2: %s\n", msg)
	case ch1 <- "sent":
		fmt.Println("sent to ch1: sent")
	default:
		// default 分支使 select 非阻塞
		// 如果没有其他 case 就绪，则执行 default
		fmt.Println("no activity on channels")
	}

	// 使用 time.After 实现超时机制
	// 如果在指定时间内没有数据到达，则触发超时
	select {
	case msg := <-ch2:
		fmt.Printf("received from ch2: %s\n", msg)
	case <-time.After(200 * time.Millisecond):
		fmt.Println("timed out: no activity on channels")
	}
}