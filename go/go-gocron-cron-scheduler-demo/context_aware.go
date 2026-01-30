package main

import (
	"context"
	"log"
	"time"

	"github.com/robfig/cron/v3"
)

// 上下文感知任务示例
// 演示如何结合context实现可取消的定时任务
func main() {
	// 创建可取消的context
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	c := cron.New()
	c.Start()
	defer c.Stop()

	// 添加一个每2秒执行的任务，该任务能响应context取消
	c.AddFunc("*/2 * * * * *", func() {
		// 模拟任务执行过程
		select {
		case <-time.After(1 * time.Second):
			log.Println("[上下文任务] 正在执行...")
		case <-ctx.Done():
			log.Println("[上下文任务] 收到取消信号，停止执行")
			return
		}
	})

	// 5秒后取消所有任务
	time.AfterFunc(5*time.Second, func() {
		cancel()
		log.Println("[系统] 已发送取消信号")
	})

	// 保持运行
	time.Sleep(8 * time.Second)
}