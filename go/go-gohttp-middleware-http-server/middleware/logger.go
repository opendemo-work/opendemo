package middleware

import (
	"log"
	"net/http"
)

// LoggingMiddleware 是一个日志记录中间件
// 它在每个请求开始时打印基本信息：方法和路径
// 然后将控制权交给下一个处理器
func LoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 在处理请求前记录日志
		log.Printf("[INFO] %s %s", r.Method, r.URL.Path)

		// 调用链中的下一个处理器
		next.ServeHTTP(w, r)
	})
}