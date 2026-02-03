package main

import (
	"log"
	"net/http"
	"os"
)

// main 是程序入口点
// 设置HTTP路由并启动服务器
func main() {
	// 设置/hello路由处理函数
	http.HandleFunc("/hello", helloHandler)
	
	// 设置/healthz健康检查端点
	// 符合Kubernetes等平台的探针规范
	http.HandleFunc("/healthz", healthCheckHandler)
	
	// 从环境变量获取端口，默认8080
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	
	// 记录启动日志
	log.Printf("Starting server on :%s", port)
	
	// 启动HTTP服务器
	// 使用nil表示使用DefaultServeMux
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

// helloHandler 处理/hello请求
// 返回友好的问候消息，包含构建方式信息
func helloHandler(w http.ResponseWriter, r *http.Request) {
	// 设置响应头内容类型
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	// 返回成功状态码
	w.WriteHeader(http.StatusOK)
	// 写入响应体
	w.Write([]byte("Hello from Go in Docker! Built with multi-stage build."))
}

// healthCheckHandler 处理健康检查请求
// 用于容器编排平台的存活/就绪探针
func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}