package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("示例1: 基本 Goroutine 和 Channel 通信")
	example1()

	fmt.Println("\n示例2: 使用缓冲 Channel 和关闭机制")
	example2()

	fmt.Println("\n示例3: 使用 select 处理多个 Channel")
	example3()
}

// example1 展示最基本的 channel 用于 goroutine 间通信
func example1() {
	// 创建一个字符串类型的无缓冲 channel
	ch := make(chan string)

	// 启动一个 goroutine 执行任务
	go func() {
		fmt.Println("工作协程开始处理任务...")
		// 模拟耗时操作
		time.Sleep(1 * time.Second)
		// 向 channel 发送结果
		ch <- "处理完成!"
	}()

	// 主协程从 channel 接收结果（会阻塞直到有数据）
	result := <-ch
	fmt.Printf("主协程接收到结果: %s\n", result)
}

// example2 展示使用缓冲 channel 和关闭机制进行生产者-消费者模式
func example2() {
	// 创建一个容量为3的缓冲 channel
	ch := make(chan string, 3)

	// 生产者 goroutine
	go func() {
		for i := 1; i <= 3; i++ {
			data := fmt.Sprintf("数据 %d", i)
			fmt.Printf("生产者发送: %s\n", data)
			ch <- data // 发送数据
			time.Sleep(500 * time.Millisecond) // 模拟生产间隔
		}
		// 生产完成，关闭 channel
		close(ch)
		fmt.Println("生产者完成，关闭通道")
	}()

	// 消费者：使用 range 自动接收直到 channel 关闭
	for data := range ch {
		fmt.Printf("消费者接收到: %s\n", data)
	}
	fmt.Println("消费者完成")
}

// example3 展示使用 select 处理多个 channel 操作，包括超时控制
func example3() {
	ch := make(chan string)
	timeout := make(chan bool)

	// 模拟异步任务（可能失败或延迟）
	go func() {
		time.Sleep(3 * time.Second) // 模拟长时间操作
		ch <- "任务成功"
	}()

	// 超时 goroutine
	go func() {
		time.Sleep(2 * time.Second)
		timeout <- true
	}()

	// 使用 select 等待多个 channel
	select {
	case msg := <-ch:
		fmt.Printf("收到消息: %s\n", msg)
	case <-timeout:
		fmt.Println("收到超时信号，退出")
		return
	}
}