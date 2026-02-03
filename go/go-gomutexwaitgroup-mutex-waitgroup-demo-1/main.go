package main

import (
	"fmt"
	"sync"
)

// 全局变量：共享的计数器
var counter int
// mutex用于保护对counter的并发访问
var mutex sync.Mutex

// increment 函数安全地增加计数器值
func increment(wg *sync.WaitGroup) {
	defer wg.Done() // 任务完成时通知WaitGroup
	for i := 0; i < 500; i++ {
		mutex.Lock()         // 获取锁
		counter++            // 安全修改共享变量
		mutex.Unlock()       // 释放锁
	}
}

func main() {
	var wg sync.WaitGroup

	// 启动5个goroutine并发执行increment
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go increment(&wg)
	}

	// 等待所有goroutine完成
	wg.Wait()
	fmt.Printf("最终计数器值: %d\n", counter)
}