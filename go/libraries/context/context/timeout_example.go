package main

import (
	"context"
	"fmt"
	"time"
)

// timeoutExample 展示如何使用 context 控制操作超时
func timeoutExample() {
	// 创建一个带有 2 秒超时的 context
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel() // 确保释放资源，即使提前返回也要执行

	// 启动一个模拟长时间任务的 goroutine
	go func() {
		for {
			select {
			case <-time.After(3 * time.Second):
				// 模拟耗时超过 2 秒的任务
				fmt.Println("任务完成")
				return
			case <-ctx.Done():
				// 当 context 被取消时（超时），立即退出
				fmt.Printf("任务因超时被取消: %v\n", ctx.Err())
				return
			}
		}
	}()

	// 等待足够时间让 select 触发超时
	time.Sleep(3 * time.Second)
}