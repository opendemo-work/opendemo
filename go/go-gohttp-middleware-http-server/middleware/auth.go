package middleware

import "net/http"

// AuthMiddleware 是一个身份验证中间件
// 它检查请求是否包含有效的 Authorization 头
// 如果没有，则返回 401 Unauthorized
func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 检查 Authorization 请求头是否存在
		if r.Header.Get("Authorization") == "" {
			// 如果没有提供认证信息，拒绝访问
			w.WriteHeader(http.StatusUnauthorized)
			_, _ = w.Write([]byte("Unauthorized: missing token"))
			return
		}

		// 认证通过，继续调用下一个处理器
		next.ServeHTTP(w, r)
	})
}