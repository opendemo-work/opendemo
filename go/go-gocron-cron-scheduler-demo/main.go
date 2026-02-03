package main

import (
	"log"
	"time"

	"github.com/robfig/cron/v3"
)

// 基础定时任务示例
// 演示如何使用Cron表达式定期执行函数
func main() {
	// 创建一个新的cron调度器
	c := cron.New()

	// 添加一个每5秒执行一次的任务
	// Cron表达式格式：秒 分 时 日 月 星期
	// */5 表示每5秒执行一次
	c.AddFunc("*/5 * * * * *", func() {
		log.Printf("[基础任务] 当前时间: %s", time.Now().Format("2006-01-02 15:04:05"))
	})

	// 启动调度器
	c.Start()
	defer c.Stop() // 确保程序退出时释放资源

	// 阻塞主线程，保持程序运行
	// 在实际应用中，这里可能是HTTP服务器或其他长期运行的服务
	log.Println("调度器已启动，等待任务执行...")
	time.Sleep(30 * time.Second) // 运行30秒后自动退出
}