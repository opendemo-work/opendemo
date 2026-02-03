package main

import (
	"fmt"
	"sync"
	"time"
)

// sync_map.go - 并发安全的map使用示例
func main() {
	// 使用sync.Map来支持并发读写
	var safeMap sync.Map

	// 模拟多个goroutine同时写入数据
	var wg sync.WaitGroup
	items := []string{"apple", "banana", "cherry"}

	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for _, item := range items {
				// 模拟一些处理时间
				time.Sleep(time.Millisecond * 100)
				// 并发安全地增加计数
				safeMap.Compute(item, func(_ interface{}, value interface{}) interface{} {
					if value == nil {
						return 1
					}
					return value.(int) + 1
				})
			}
		}(i)
	}

	// 等待所有goroutine完成
	wg.Wait()

	// 遍历并打印结果
	fmt.Println("最终计数结果（可能顺序不同）：")
	safeMap.Range(func(key, value interface{}) bool {
		fmt.Printf("%s: %d\n", key, value)
		return true // 继续遍历
	})
}