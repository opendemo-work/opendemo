package main

import (
	"context"
	"fmt"
	"time"
)

// cancelExample 展示如何通过 cancel 函数主动终止 context
func cancelExample() {
	// 创建一个可取消的 context
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel() // 保证 cancel 被调用，符合最佳实践

	// 启动工作 goroutine
	go func() {
		for {
			select {
			case <-ctx.Done():
				// 收到取消信号，清理并退出
				fmt.Printf("收到取消信号: %v\n", ctx.Err())
				return
			default:
				fmt.Println("处理任务中... (等待取消信号)")
				time.Sleep(500 * time.Millisecond)
			}
		}
	}()

	// 模拟一秒钟后决定取消任务
	time.Sleep(1 * time.Second)
	cancel() // 发出取消指令，触发 ctx.Done()

	// 给 goroutine 时间响应取消
	time.Sleep(100 * time.Millisecond)
}