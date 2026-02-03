package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// worker 模拟并发工作单元
func worker(ctx context.Context, id int, wg *sync.WaitGroup) {
	defer wg.Done()

	for {
		select {
		case <-time.After(100 * time.Millisecond):
			fmt.Printf("worker %d 正在工作...\n", id)
		case <-ctx.Done():
			fmt.Printf("worker %d 收到取消信号\n", id)
			return
		}
	}
}

func main() {
	// 设置整体超时为500毫秒
	ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer cancel()

	var wg sync.WaitGroup

	// 启动5个并发worker
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go worker(ctx, i, &wg)
	}

	// 等待所有worker完成或被取消
	wg.Wait()
	fmt.Println("所有任务结束")
}