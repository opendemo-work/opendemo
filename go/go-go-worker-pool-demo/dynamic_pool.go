package main

import (
	"fmt"
	"sync"
	"time"
)

// Task 表示一个任务结构体，可用于携带更多上下文信息
type Task struct {
	ID    string
	Data  interface{}
}

// DynamicWorker 表示可扩展的Worker函数，使用WaitGroup管理生命周期
func DynamicWorker(id int, tasks <-chan Task, wg *sync.WaitGroup) {
	defer wg.Done() // 在退出时通知WaitGroup
	for task := range tasks {
		fmt.Printf("[动态池] Worker %d 处理任务: %s\n", id, task.ID)
		time.Sleep(800 * time.Millisecond) // 模拟处理时间
		fmt.Printf("[动态池] Worker %d 完成任务: %s\n", id, task.ID)
	}
}

// 演示支持动态Worker数量的协程池
func main() {
	const numWorkers = 2
	const numTasks = 4

	// 任务通道
	tasks := make(chan Task, numTasks)
	var wg sync.WaitGroup

	// 启动指定数量的Worker
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go DynamicWorker(i, tasks, &wg)
	}

	// 发送任务
	for j := 1; j <= numTasks; j++ {
		tasks <- Task{ID: fmt.Sprintf("DynamicTask-%d", j)}
	}
	close(tasks) // 关闭通道触发Worker退出

	// 等待所有Worker完成
	wg.Wait()
	fmt.Println("动态Worker池任务全部完成")
}