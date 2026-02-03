package main

import (
	"context"
	"fmt"
	"time"
)

// monitorTask 模拟一个持续工作的任务
func monitorTask(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			fmt.Println("收到取消信号，停止工作")
			return
		default:
			// 模拟周期性工作
			fmt.Println("正在监控...")
			time.Sleep(500 * time.Millisecond)
		}
	}
}

func main() {
	// 创建可取消的上下文
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 启动监控任务
	go monitorTask(ctx)

	// 模拟主程序运行一段时间后决定取消
	time.Sleep(1 * time.Second)
	fmt.Println("发送取消信号")
	cancel()

	// 给 goroutine 时间退出
	time.Sleep(100 * time.Millisecond)
	fmt.Println("goroutine 成功退出")
}