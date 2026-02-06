package main

import (
	"fmt"
	"sync"
	"time"
)

// 模拟多个任务并发执行，并使用 WaitGroup 等待全部完成
func main() {
	var wg sync.WaitGroup

	// 启动3个worker
	for i := 0; i < 3; i++ {
		wg.Add(1) // 增加计数器
		go func(id int) {
			defer wg.Done() // 任务完成时通知
			fmt.Printf("Worker %d 开始工作...\n", id)
			time.Sleep(time.Second * 1) // 模拟工作耗时
		}(i)
	}

	// 等待所有 worker 完成
	wg.Wait()
	fmt.Println("所有 worker 已完成")
}