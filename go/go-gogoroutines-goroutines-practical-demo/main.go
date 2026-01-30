package main

import (
	"fmt"
	"time"
)

// main 函数演示最基本的goroutine与channel通信
func main() {
	// 创建一个字符串类型的无缓冲channel
	ch := make(chan string)

	// 启动一个goroutine执行匿名函数
	go func() {
		// 模拟一些耗时操作
		time.Sleep(1 * time.Second)
		// 向channel发送消息
		ch <- "Hello from goroutine!"
	}()

	// 从channel接收消息（主线程会在此阻塞，直到有数据）
	msg := <-ch
	fmt.Printf("接收到的消息：%s\n", msg)

	fmt.Println("main函数结束")
}
