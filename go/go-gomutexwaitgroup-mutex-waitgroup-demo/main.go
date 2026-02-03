package main

import (
	"fmt"
	"sync"
)

// 全局变量：共享计数器
var counter int
var mu sync.Mutex   // 互斥锁保护counter
var wg sync.WaitGroup // 用于等待所有goroutine完成

func main() {
	const numGoroutines = 1000

	// 启动1000个goroutine，每个增加counter一次
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1) // 每次启动goroutine前增加WaitGroup计数
		go func() {
			defer wg.Done() // 确保函数退出时调用Done()
			mu.Lock()       // 进入临界区前加锁
			counter++       // 安全地修改共享变量
			mu.Unlock()     // 退出临界区后解锁
		}()
	}

	// 等待所有goroutine完成
	wg.Wait()
	fmt.Printf("最终计数: %d\n", counter)

	// 运行其他示例
	bankTransferExample()
	workerPoolExample()
}