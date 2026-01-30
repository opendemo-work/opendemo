package main

import (
	"net/http"
	"middleware-demo/middleware"
)

// homeHandler 是最终的业务处理函数
func homeHandler(w http.ResponseWriter, r *http.Request) {
	// 设置响应内容类型
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	// 返回成功响应
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("Hello, World!"))
}

// main 启动HTTP服务器，注册带有中间件链的路由
func main() {
	// 构建中间件链：先日志 → 再认证 → 最终处理
	handler := middleware.LoggingMiddleware(
		middleware.AuthMiddleware(http.HandlerFunc(homeHandler)),
	)

	// 注册路由处理器
	http.Handle("/", handler)

	// 启动服务器
	println("Server starting on :8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}