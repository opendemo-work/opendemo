package main

import (
	"fmt"
	"time"
)

// 示例2: 使用 select 实现超时控制
func main() {
	ch := make(chan string)

	// 模拟可能延迟或失败的数据获取
	go func() {
		// 假设这个操作耗时超过 1 秒
		time.Sleep(2 * time.Second)
		ch <- "处理完成结果"
	}()

	// 使用 select + timeout 避免永久阻塞
	select {
	case result := <-ch:
		fmt.Println("成功获取结果:", result)
	case <-time.After(1 * time.Second): // 1秒超时
		fmt.Println("操作超时，未收到数据")
	}
	// 主程序不会无限等待
}