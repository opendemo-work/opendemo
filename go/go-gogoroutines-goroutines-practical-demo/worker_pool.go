package main

import (
	"fmt"
	"time"
)

// worker 启动一个工作协程，从任务channel中获取任务并处理
func worker(id int, jobs <-chan string, done chan<- bool) {
	for job := range jobs { // 当jobs channel关闭时，循环自动退出
		fmt.Printf("Worker %d 正在处理任务: %s\n", id, job)
		time.Sleep(500 * time.Millisecond) // 模拟处理时间
	}
	// 处理完成后通知主协程
	done <- true
}

func main() {
	// 创建一个可容纳4个任务的带缓冲channel
	jobs := make(chan string, 4)
	// 创建一个用于通知完成的channel
	done := make(chan bool, 2)

	// 启动两个worker goroutine
	go worker(1, jobs, done)
	go worker(2, jobs, done)

	// 发送任务到channel
	for i := 1; i <= 5; i++ {
		jobs <- fmt.Sprintf("任务%d", i)
	}
	fmt.Println("所有任务已分配完毕")

	// 关闭channel表示不再有新任务
	close(jobs)

	// 等待两个worker都完成
	for i := 0; i < 2; i++ {
		<-done
	}

	fmt.Println("所有worker已完成")
}
