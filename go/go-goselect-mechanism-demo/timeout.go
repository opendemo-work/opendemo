package main

import (
	"fmt"
	"time"
)

// 演示使用select实现超时控制
func main() {
	ch := make(chan string)

	// 模拟一个可能延迟或失败的操作
	// 这里我们故意不发送任何数据来触发超时
	// go func() {
	// 	time.Sleep(500 * time.Millisecond)
	// 	ch <- "operation result"
	// }()

	// 使用select配合time.After设置1秒超时
	select {
	case msg := <-ch:
		fmt.Printf("成功接收到数据：%s\n", msg)
	case <-time.After(1 * time.Second):
		fmt.Println("超时：无法在规定时间内接收数据")
	}
	// 即使channel永远没有数据，程序也会在1秒后继续执行
}