package main

import (
	"fmt"
	"time"
)

// bufferedChannelDemo 演示带缓冲 channel 的使用
// 缓冲区允许一定程度的异步通信，提高并发性能
func main() {
	// 创建一个容量为 2 的带缓冲 channel
	tasks := make(chan string, 2)

	// 启动 worker goroutine 处理任务
	go func() {
		for {
			// 不断尝试从 channel 接收任务
			task, ok := <-tasks
			// 如果 channel 关闭且无数据，则退出
			if !ok {
				fmt.Println("Worker 收到关闭信号，停止工作")
				return
			}
			fmt.Printf("Worker 正在处理: %s\n", task)
			time.Sleep(time.Millisecond * 50) // 模拟处理时间
		}
	}()

	// 主函数作为生产者发送任务
	tasks <- "Task 1"
	fmt.Println("发送任务: Task 1")
	tasks <- "Task 2"
	fmt.Println("发送任务: Task 2")

	// 模拟短暂延迟后关闭 channel
	time.Sleep(time.Millisecond * 100)
	close(tasks)
	fmt.Println("所有任务发送完成")

	// 等待 worker 完成处理
	time.Sleep(time.Second)
}
