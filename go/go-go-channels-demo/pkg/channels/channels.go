// Package channels 提供 Go channel 核心用法的可复用示例函数。
//
// 每个函数都专注于一个具体场景：
//   - BasicChannel：无缓冲 channel 的同步通信
//   - BufferedChannel：带缓冲 channel 的生产者-消费者模式
//   - ClosingChannel：安全关闭 channel 并检测关闭状态
//   - SelectChannel：使用 select 实现超时控制
//
// 这些函数返回字符串切片，便于在测试和主程序中统一校验输出。
package channels

import (
	"fmt"
	"time"
)

// BasicChannel 演示无缓冲 channel 的同步通信。
// 发送方会阻塞，直到接收方就绪。
func BasicChannel() []string {
	ch := make(chan string)
	var out []string

	go func() {
		out = append(out, "工作协程开始处理任务...")
		time.Sleep(100 * time.Millisecond)
		ch <- "处理完成!"
	}()

	result := <-ch
	out = append(out, fmt.Sprintf("主协程接收到结果: %s", result))
	return out
}

// BufferedChannel 演示带缓冲 channel 和 close 机制。
// 缓冲区允许一定程度的异步，close 用于通知消费者不再有数据。
func BufferedChannel() []string {
	ch := make(chan string, 3)
	var out []string

	go func() {
		for i := 1; i <= 3; i++ {
			data := fmt.Sprintf("数据 %d", i)
			out = append(out, fmt.Sprintf("生产者发送: %s", data))
			ch <- data
			time.Sleep(50 * time.Millisecond)
		}
		close(ch)
		out = append(out, "生产者完成，关闭通道")
	}()

	for data := range ch {
		out = append(out, fmt.Sprintf("消费者接收到: %s", data))
	}
	out = append(out, "消费者完成")
	return out
}

// ClosingChannel 演示使用逗号 ok 语法判断 channel 是否已关闭。
func ClosingChannel() []string {
	ch := make(chan int)
	var out []string

	go func() {
		for i := 1; i <= 3; i++ {
			ch <- i
		}
		close(ch)
	}()

	for {
		value, ok := <-ch
		if !ok {
			out = append(out, "channel 已关闭，不再有数据")
			break
		}
		out = append(out, fmt.Sprintf("接收到数值: %d", value))
	}
	return out
}

// SelectChannel 演示使用 select 监听多个 channel，实现超时控制。
// timeoutAfter 指定超时时间，taskDelay 指定模拟任务耗时。
func SelectChannel(timeoutAfter, taskDelay time.Duration) []string {
	ch := make(chan string)
	timeout := time.After(timeoutAfter)
	var out []string

	go func() {
		time.Sleep(taskDelay)
		ch <- "任务成功"
	}()

	select {
	case msg := <-ch:
		out = append(out, fmt.Sprintf("收到消息: %s", msg))
	case <-timeout:
		out = append(out, "收到超时信号，退出")
	}
	return out
}
