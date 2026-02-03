package main

import (
	"fmt"
	"time"
)

// main 函数演示 context 的两个主要用途：取消和超时
func main() {
	fmt.Println("【示例1】开始执行带取消的 goroutine...")
	exampleWithCancel()
	fmt.Println("【示例1】goroutine 已成功取消。\n")

	time.Sleep(1 * time.Second) // 分隔输出

	fmt.Println("【示例2】发起一个最多等待2秒的HTTP请求...")
	exampleWithTimeout()
	fmt.Println("【示例2】HTTP请求超时处理完成。\n")
}
