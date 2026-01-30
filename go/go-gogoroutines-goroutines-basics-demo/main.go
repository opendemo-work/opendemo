package main

import (
	"fmt"
	"sync"
	"time"
)

// 示例1: 基础goroutine并发执行
func example1() {
	fmt.Println("[示例1] 启动两个并发任务...")

	// 启动第一个goroutine
	go func() {
		for i := 1; i <= 2; i++ {
			fmt.Printf("任务A: 执行第 %d 次\n", i)
			time.Sleep(100 * time.Millisecond) // 模拟耗时操作
		}
		fmt.Println("任务A 完成")
	}()

	// 启动第二个goroutine
	go func() {
		for i := 1; i <= 2; i++ {
			fmt.Printf("任务B: 执行第 %d 次\n", i)
			time.Sleep(150 * time.Millisecond)
		}
		fmt.Println("任务B 完成")
	}()

	// 主goroutine等待子任务完成（实际中应使用sync.WaitGroup）
	time.Sleep(500 * time.Millisecond)
	fmt.Println()
}

// 示例2: 使用channel在goroutine间通信
func example2() {
	fmt.Println("[示例2] 使用带缓冲channel传递数据...")

	// 创建一个带缓冲的字符串channel，容量为2
	ch := make(chan string, 2)

	// 生产者goroutine
	go func() {
		for i := 1; i <= 2; i++ {
			msg := fmt.Sprintf("数据-%d", i)
			ch <- msg // 发送数据到channel
			fmt.Printf("生产者发送: %s\n", msg)
			time.Sleep(50 * time.Millisecond)
		}
		close(ch) // 关闭channel表示不再发送
		fmt.Println("生产者完成")
	}()

	// 消费者goroutine
	go func() {
		for data := range ch { // 从channel接收数据直到关闭
			fmt.Printf("消费者接收: %s\n", data)
			time.Sleep(100 * time.Millisecond)
		}
		fmt.Println("消费者完成")
	}()

	time.Sleep(400 * time.Millisecond)
	fmt.Println()
}

// 示例3: 并发安全的共享状态访问
func example3() {
	fmt.Println("[示例3] 并发安全计数器...")

	var counter int
	var mu sync.Mutex // 互斥锁保护共享变量
	var wg sync.WaitGroup

	// 启动两个goroutine递增计数器
	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 1; j <= 2; j++ {
				mu.Lock() // 加锁
				counter++
				fmt.Printf("协程 %d: 当前计数 = %d\n", id, counter)
				mu.Unlock() // 解锁
				time.Sleep(50 * time.Millisecond)
			}
		}(i)
	}

	wg.Wait() // 等待所有goroutine完成
	fmt.Printf("最终计数: %d\n", counter)
}

func main() {
	example1()
	example2()
	example3()
}