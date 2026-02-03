package main

import (
	"fmt"
	"sync"
)

// concurrent_sum.go - 并发求和示例
// 将大数组分块，由多个goroutine并发计算部分和，最后合并结果
func main() {
	// 创建一个1到100的数组
	data := make([]int, 100)
	for i := 0; i < 100; i++ {
		data[i] = i + 1
	}

	// 使用channel传递每个goroutine的计算结果
	resultChan := make(chan int, 2) // 缓冲channel，存放两个部分和
	var wg sync.WaitGroup

	// 分成两组并发处理
	wg.Add(2)
	go func() {
		defer wg.Done()
		sum := 0
		for i := 0; i < 50; i++ {
			sum += data[i]
		}
		resultChan <- sum // 发送部分和
	}()

	go func() {
		defer wg.Done()
		sum := 0
		for i := 50; i < 100; i++ {
			sum += data[i]
		}
		resultChan <- sum
	}()

	// 等待所有goroutine完成
	go func() {
		wg.Wait()
		close(resultChan) // 关闭channel表示不再有数据
	}()

	// 收集结果
	total := 0
	for partialSum := range resultChan {
		total += partialSum
	}

	fmt.Printf("并发计算结果: %d\n", total)
}