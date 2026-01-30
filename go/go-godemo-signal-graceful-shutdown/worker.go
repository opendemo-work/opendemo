package main

import (
	"context"
	"log"
	"time"
)

var (
	workerCtx    context.Context
	workerCancel context.CancelFunc
)

// 模拟后台周期性任务（例如日志轮转、缓存刷新）
func init() {
	workerCtx, workerCancel = context.WithCancel(context.Background())
	go func() {
		ticker := time.NewTicker(2 * time.Second)
		defer ticker.Stop()

		for {
			select {
			case <-ticker.C:
				log.Println("后台任务执行中...")
			case <-workerCtx.Done():
				log.Println("后台任务被中断")
				return
			}
		}
	}()
}

// stopWorker 停止后台任务
func stopWorker() {
	workerCancel() // 触发context取消
}