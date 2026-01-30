package main

import (
	"fmt"
	"time"
)

// main 函数演示最基础的goroutine用法
func main() {
	fmt.Println("主函数开始执行")

	// 启动一个goroutine执行匿名函数
	go func() {
		time.Sleep(100 * time.Millisecond) // 模拟耗时操作
		fmt.Println("Hello from goroutine!")
	}()

	// 另一个goroutine
	done := make(chan bool)
	go func() {
		fmt.Println("你好，世界！")
		done <- true // 通知完成
	}()

	// 等待第二个goroutine完成
	<-done

	// 给第一个goroutine足够时间完成
	time.Sleep(200 * time.Millisecond)
	fmt.Println("main结束")
}

/*
关键知识点：
- 使用 go keyword 启动新goroutine
- 主goroutine退出会导致整个程序终止，即使其他goroutine仍在运行
- channel可用于goroutine间通信和同步
*/