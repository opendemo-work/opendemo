package main

import (
	"fmt"
	"sync"
)

// 演示多个 goroutine 并发写入共享切片时使用 Mutex 保护

var data []string
var mu sync.Mutex
var wg sync.WaitGroup

func main() {
	data = make([]string, 0)
	const numWrites = 500

	for i := 0; i < numWrites; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			// 安全地向切片添加元素
			mu.Lock()
			data = append(data, fmt.Sprintf("item-%d", id))
			mu.Unlock()
		}(i)
	}

	wg.Wait()
	fmt.Printf("写入完成，总共写入 %d 条数据\n", len(data))
}