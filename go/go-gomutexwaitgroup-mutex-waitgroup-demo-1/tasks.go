package main

import (
	"fmt"
	"sync"
)

// simulateTask 模拟一个耗时任务
func simulateTask(id int, wg *sync.WaitGroup) {
	defer wg.Done() // 任务完成时通知WaitGroup
	fmt.Printf("正在执行任务 #%d\n", id)
	// 这里可以添加实际的工作逻辑
}

// processTasks 使用WaitGroup协调多个并发任务
func processTasks() {
	var wg sync.WaitGroup

	// 启动10个任务
	for i := 1; i <= 10; i++ {
		wg.Add(1)
		go simulateTask(i, &wg)
	}

	// 等待所有任务完成
	wg.Wait()
	fmt.Println("所有任务已完成")
}

// 可以在main函数中调用processTasks()
// 注意：已在main.go中调用wg.Wait()，因此这里只定义函数