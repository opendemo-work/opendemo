package main

import (
	"fmt"
	"time"
)

// main.go - 基础goroutine示例
// 展示如何启动一个简单的goroutine
func main() {
	fmt.Println("主函数开始执行...")

	// 启动一个匿名goroutine
	go func() {
		time.Sleep(100 * time.Millisecond) // 模拟一些工作
		fmt.Println("你好，来自goroutine！")
	}()

	// 主goroutine短暂休眠，确保子goroutine有机会执行
	// 实际开发中应使用sync.WaitGroup而非Sleep
	time.Sleep(200 * time.Millisecond)

	fmt.Println("main函数即将结束")
}