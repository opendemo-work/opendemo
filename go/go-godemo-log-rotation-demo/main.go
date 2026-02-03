package main

import (
	"io"
	"log"
	"os"
	"time"

	"github.com/natefinch/lumberjack/v2"
)

// 演示基于大小的日志轮转
func main() {
	// 创建日志输出目录
	if err := os.MkdirAll("logs", 0755); err != nil {
		panic(err)
	}

	// 配置lumberjack日志轮转器
	writer := &lumberjack.Logger{
		Filename:   "logs/app.log",   // 输出文件路径
		MaxSize:    1,              // 每个文件最大1MB
		MaxBackups: 3,              // 最多保留3个备份
		MaxAge:     7,              // 备份最长保留7天
		Compress:   true,           // 启用gzip压缩旧日志
	}

	// 创建多写入器：同时输出到控制台和轮转文件
	multiWriter := io.MultiWriter(os.Stdout, writer)

	// 设置标准日志输出
	log.SetOutput(multiWriter)
	log.SetFlags(log.LstdFlags | log.Lshortfile) // 包含时间和文件信息

	// 模拟持续写入日志
	for i := 1; i <= 10000; i++ {
		log.Printf("[INFO] 这是一条测试日志消息 (序号: %d)", i)
		time.Sleep(10 * time.Millisecond) // 减缓写入速度
	}

	// 关闭writer释放资源（实际生产中通常由defer保证）
	writer.Close()
}