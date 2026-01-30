package main

import (
	"fmt"
	"sync"
)

// worker_pool.go - 工作池模式示例
// 启动固定数量的工作协程，从任务队列中消费任务
func main() {
	// 定义任务类型
	tasks := []string{"任务1", "任务2", "任务3", "任务4", "任务5"}
	taskChan := make(chan string, len(tasks))

	var wg sync.WaitGroup
	numWorkers := 2

	// 启动worker池
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		workerID := i
		go func() {
			defer wg.Done()
			for task := range taskChan {
				fmt.Printf("Worker %d 处理任务: %s\n", workerID, task)
			}
		}()
	}

	// 发送任务到channel
	for _, task := range tasks {
		taskChan <- task
	}
	close(taskChan) // 关闭任务channel，通知workers无新任务

	// 等待所有worker完成
	wg.Wait()
	fmt.Println("所有任务完成")
}