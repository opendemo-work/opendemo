package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	// 创建HTTP服务器
	server := &http.Server{Addr: ":8080"}
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// 模拟处理时间
		time.Sleep(100 * time.Millisecond)
		w.Write([]byte("Hello, World!\n"))
	})

	// 在goroutine中启动服务器
	go func() {
		log.Printf("服务已启动在 %s", server.Addr)
		er := server.ListenAndServe()
		if er != nil && er != http.ErrServerClosed {
			log.Fatalf("服务器启动失败: %v", er)
		}
	}()

	// 设置信号监听
	quit := make(chan os.Signal, 1)
	// 监听中断信号：Ctrl+C (SIGINT) 和 kill命令 (SIGTERM)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	log.Println("等待中断信号...")

	// 阻塞直到收到信号
	<-quit
	log.Println("接收到中断信号，开始优雅关闭...")

	// 创建上下文用于限制关闭超时
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// 停止后台任务
	stopWorker()

	// 优雅关闭服务器
	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("服务器关闭出错: %v", err)
	}

	log.Println("正在等待正在进行的请求完成...")
	// 等待上下文完成或超时
	<-ctx.Done()
	log.Println("服务已关闭")
}