package main

import (
	"context"
	"fmt"
	"time"
)

// 示例1: 基础goroutine并发执行
func exampleBasicGoroutines() {
	fmt.Println("[示例1] 启动两个并发任务...")

	// 启动第一个goroutine
	go func(id string) {
		for i := 1; i <= 2; i++ {
			fmt.Printf("%s: 进度 %d\n", id, i)
			time.Sleep(100 * time.Millisecond) // 模拟耗时操作
		}
		fmt.Printf("%s完成\n", id)
	}("任务A")

	// 启动第二个goroutine
	go func(id string) {
		for i := 1; i <= 2; i++ {
			fmt.Printf("%s: 进度 %d\n", id, i)
			time.Sleep(150 * time.Millisecond)
		}
		fmt.Printf("%s完成\n", id)
	}("任务B")

	// 等待足够时间让goroutines完成（实际应使用WaitGroup）
	time.Sleep(500 * time.Millisecond)
}

// 示例2: 使用通道在goroutines间通信
func exampleChannelCommunication() {
	fmt.Println("\n[示例2] 使用通道传递结果...")

	// 创建一个整型通道
	resultChan := make(chan int)

	// 模拟耗时计算函数
	heavyComputation := func(delay time.Duration) int {
		time.Sleep(delay)
		return 42 // 模拟计算结果
	}

	// 启动多个goroutine执行任务并将结果发送到通道
	for i := 0; i < 2; i++ {
		go func(taskID int) {
			var result int
			if taskID == 0 {
				result = heavyComputation(200 * time.Millisecond)
			} else {
				result = heavyComputation(300 * time.Millisecond)
				result = 13 // 第二个任务返回不同结果
			}
			resultChan <- result // 发送结果到通道
		}(i)
	}

	// 从通道接收结果（顺序可能不同）
	for i := 0; i < 2; i++ {
		result := <-resultChan
		fmt.Printf("接收到计算结果: %d\n", result)
	}

	fmt.Println("所有任务完成")
}

// 示例3: 使用Context控制goroutine生命周期
func exampleContextCancellation() {
	fmt.Println("\n[示例3] 使用Context取消goroutine...")

	// 创建一个带超时的context（800毫秒后自动取消）
	ctx, cancel := context.WithTimeout(context.Background(), 800*time.Millisecond)
	defer cancel() // 确保释放资源

	// 启动一个长时间运行的goroutine
	go func(ctx context.Context) {
		for {
			select {
			case <-ctx.Done():
				fmt.Println("收到取消信号，正在退出...")
				return
			default:
				fmt.Println("工作协程正在运行...")
				time.Sleep(300 * time.Millisecond)
			}
		}
	}(ctx)

	// 等待context被取消
	<-ctx.Done()
	fmt.Printf("上下文已取消，清理完成 (%v)\n", ctx.Err())
}

func main() {
	// 设置更精确的时间格式显示
	exampleBasicGoroutines()
	exampleChannelCommunication()
	exampleContextCancellation()

	fmt.Println("\n演示结束")
}