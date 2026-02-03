package main

import (
	"context"
	"fmt"
	"time"
)

// simulateRequest 模拟一个可能耗时的请求处理函数
func simulateRequest(ctx context.Context) {
	select {
	case <-time.After(3 * time.Second): // 模拟需要3秒完成的操作
		fmt.Println("操作成功完成")
	case <-ctx.Done(): // 当上下文超时或取消时触发
		fmt.Println("操作超时或被取消")
	}
}

func main() {
	// 创建一个1秒后自动取消的context
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel() // 确保释放资源

	fmt.Println("请求正在处理...")

	// 在goroutine中执行可能长时间运行的操作
	go simulateRequest(ctx)

	// 等待足够时间以观察结果
	time.Sleep(2 * time.Second)
}