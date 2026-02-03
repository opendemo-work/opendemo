package main

import (
	"context"
	"fmt"
	"time"
)

// exampleWithCancel 展示如何使用 context.WithCancel 主动取消一个正在运行的 goroutine
func exampleWithCancel() {
	// 创建一个基础 context 和对应的取消函数
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel() // 确保函数退出前调用 cancel，释放资源

	// 启动一个长期运行的 goroutine
	go func(ctx context.Context) {
		for {
			select {
			case <-ctx.Done():
				// 当收到取消信号时，执行清理并退出
				fmt.Println("收到取消信号，安全退出。")
				return
			default:
				// 模拟工作进行中
				fmt.Println("工作正在进行中...")
				time.Sleep(500 * time.Millisecond)
			}
		}
	}(ctx)

	// 模拟主程序在一段时间后决定取消操作
	time.Sleep(2 * time.Second)
	cancel() // 触发取消

	// 给 goroutine 一点时间响应取消
	time.Sleep(100 * time.Millisecond)
}