package main

import (
	"fmt"
	"sync"
	"time"
)

// 演示并发环境下使用mutex保护map
func main() {
	// 共享map，记录每个键被增加的次数
	counter := make(map[string]int)
	var mu sync.Mutex // 互斥锁，保护counter
	var wg sync.WaitGroup

	// 启动多个goroutine并发修改map
	keys := []string{"a", "b", "c"}
	for _, key := range keys {
		for i := 0; i < 3; i++ { // 每个key增加3次
			wg.Add(1)
			go func(k string) {
				defer wg.Done()
				// 模拟一些处理时间
				time.Sleep(time.Millisecond * 10)
				// 加锁保护共享资源
				mu.Lock()
				counter[k]++
				mu.Unlock()
			}(key)
		}
	}

	// 等待所有goroutine完成
	wg.Wait()

	fmt.Printf("最终计数: a=%d, b=%d, c=%d\n", counter["a"], counter["b"], counter["c"])
	fmt.Println("所有goroutine执行完成")
}