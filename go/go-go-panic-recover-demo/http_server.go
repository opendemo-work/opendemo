package main

import (
	"fmt"
	"net/http"
)

// recoverMiddleware 是一个中间件，用于从 handler 的 panic 中恢复
func recoverMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 使用 defer 来捕获可能发生的 panic
		defer func() {
			if r := recover(); r != nil {
				// 记录错误日志（这里简化为打印）
				fmt.Printf("发生错误：%v\n", r)
				// 返回友好的错误响应
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			}
		}()

		// 调用实际的处理器
		next(w, r)
	}
}

// badHandler 故意触发 panic
func badHandler(w http.ResponseWriter, r *http.Request) {
	var a, b int = 10, 0
	result := a / b // 触发 runtime panic
	fmt.Fprintf(w, "结果: %d", result)
}

// goodHandler 正常响应
func goodHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "正常响应")
}

func main() {
	// 注册带恢复功能的路由
	http.HandleFunc("/bad", recoverMiddleware(badHandler))
	http.HandleFunc("/good", recoverMiddleware(goodHandler))

	fmt.Println("服务器启动在 :8080... (访问 /bad 或 /good)")
	http.ListenAndServe(":8080", nil)
}