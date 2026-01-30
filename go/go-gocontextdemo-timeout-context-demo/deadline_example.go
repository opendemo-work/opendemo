package main

import (
	"context"
	"fmt"
	"time"
)

// timedTask 模拟一个受截止时间控制的任务
func timedTask(ctx context.Context) {
	for {
		select {
		case <-time.After(500 * time.Millisecond):
			fmt.Println("任务仍在运行...")
		case <-ctx.Done():
			fmt.Println("任务因截止时间到达被取消")
			return
		}
	}
}

func main() {
	// 设置一个1秒后的截止时间
	deadline := time.Now().Add(1 * time.Second)
	ctx, cancel := context.WithDeadline(context.Background(), deadline)
	defer cancel()

	// 启动任务
	go timedTask(ctx)

	// 主协程等待足够时间以观察取消行为
	time.Sleep(2 * time.Second)
}