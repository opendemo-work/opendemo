package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

// simpleHandler 返回预设消息，模拟后端服务响应
func simpleHandler(message string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 模拟一些处理延迟（50-150ms）
		delay := time.Duration(50+randInt(100)) * time.Millisecond
		time.Sleep(delay)

		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "%s | Time: %s | Path: %s\n", message, time.Now().Format("15:04:05"), r.URL.Path)
	}
}

// randInt 生成 0 到 max 之间的随机整数
func randInt(max int) int {
	return int(time.Now().UnixNano()%int64(max)) + 1
}

func main() {
	// 从命令行参数读取端口和消息
	port := ":8081"
	message := "Hello from Backend"
	if len(os.Args) > 1 {
		port = os.Args[1]
	}
	if len(os.Args) > 2 {
		message = os.Args[2]
	}

	log.Printf("Backend server starting on %s with message: %s", port, message)

	http.HandleFunc("/", simpleHandler(message))
	log.Fatal(http.ListenAndServe(port, nil))
}