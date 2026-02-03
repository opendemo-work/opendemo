package main

import (
	"log"
	"time"

	"github.com/robfig/cron/v3"
)

// 动态任务管理示例
// 演示如何在运行时动态添加和删除定时任务
func main() {
	c := cron.New()
	c.Start()
	defer c.Stop()

	// 添加一个每3秒执行一次的动态任务
	id, _ := c.AddFunc("*/3 * * * * *", func() {
		log.Printf("[动态任务] 执行于 %s", time.Now().Format("2006-01-02 15:04:05"))
	})

	log.Printf("[系统] 已添加动态任务，ID: %d", id)

	// 模拟运行一段时间后移除任务
	time.AfterFunc(10*time.Second, func() {
		c.Remove(id)
		log.Println("[系统] 已移除动态任务")
	})

	// 保持程序运行足够长时间以观察效果
	time.Sleep(15 * time.Second)
}