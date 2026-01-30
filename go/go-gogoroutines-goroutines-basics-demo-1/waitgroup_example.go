package main

import (
	"fmt"
	"sync"
	"time"
)

// worker 模拟一个工作任务
func worker(id int, wg *sync.WaitGroup) {
	// 在函数返回时标记此worker已完成
	defer wg.Done()

	fmt.Printf("正在执行任务 %d\n", id)
	time.Sleep(time.Duration(id) * 100 * time.Millisecond) // 模拟不同耗时的任务
	fmt.Printf("任务 %d 完成\n", id)
}

// main 使用WaitGroup等待所有goroutine完成
func main() {
	var wg sync.WaitGroup

	// 启动3个worker goroutine
	for i := 1; i <= 3; i++ {
		wg.Add(1) // 增加等待计数
		go worker(i, &wg)
	}

	// 等待所有worker完成
	wg.Wait()
	fmt.Println("所有任务已完成")
}

/*
关键知识点：
- sync.WaitGroup 适用于“一群goroutine完成后通知主线程”的场景
- Add(), Done(), Wait() 三者配合使用
- 注意传递WaitGroup指针而非值拷贝
*/