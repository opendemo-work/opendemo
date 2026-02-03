package main

import (
	"fmt"
	"time"
)

// worker 表示一个工作协程，从任务通道中读取任务并处理
func worker(id int, jobs <-chan string, done chan<- bool) {
	for job := range jobs { // 从任务通道中持续获取任务
		fmt.Printf("Worker %d 开始处理任务: %s\n", id, job)
		time.Sleep(time.Second * 1) // 模拟任务处理耗时
		fmt.Printf("Worker %d 完成任务: %s\n", id, job)
	}
	// 当jobs通道被关闭且所有任务处理完毕后，发送完成信号
	done <- true
}

// main 函数演示基础Worker池的使用
func main() {
	// 创建带缓冲的任务通道，最多存放10个任务
	jobs := make(chan string, 10)
	// 创建结果通道，用于接收Worker完成信号
	done := make(chan bool)

	// 启动两个Worker协程
	for w := 1; w <= 2; w++ {
		go worker(w, jobs, done)
	}

	// 生产任务：向通道发送4个任务
	for j := 1; j <= 4; j++ {
		jobs <- fmt.Sprintf("Task-%d", j)
	}
	// 关闭任务通道，表示不再有新任务
	close(jobs)
	fmt.Println("所有任务已分配完毕")

	fmt.Println("等待所有任务完成...")
	// 等待两个Worker都发送完成信号
	for i := 0; i < 2; i++ {
		<-done
	}

	fmt.Println("全部任务执行完毕")
}