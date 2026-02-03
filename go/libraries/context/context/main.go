package main

import (
	"context"
	"fmt"
	"time"
)

// main 函数是程序入口，依次运行两个 context 使用场景
func main() {
	fmt.Println("=== 超时场景演示 ===")
	timeoutExample()

	time.Sleep(1 * time.Second) // 分隔输出

	fmt.Println("\n=== 取消信号演示 ===")
cancelExample()
}