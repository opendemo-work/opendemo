package main

import (
	"bytes"
	"io"
	"net/http"
	"net/http/httputil"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

// ProxyHandler 创建一个反向代理处理器
func ProxyHandler(target string) gin.HandlerFunc {
	return func(c *gin.Context) {
		// 记录请求被代理
		logrus.Infof("[PROXY] 请求被拦截: %s %s -> 转发至 %s%s", 
			c.Request.Method, c.Request.URL.Path, target, c.Request.URL.Path)

		// 构建目标URL
		proxy := httputil.NewSingleHostReverseProxy(&http.URL{
			Scheme: "http",
			Host:   target,
		})

		// 自定义修改请求
		originalReq := c.Request
		body, _ := io.ReadAll(originalReq.Body)
		c.Request.Body = io.NopCloser(bytes.NewBuffer(body))

		// 执行代理
		proxy.ServeHTTP(c.Writer, c.Request)
	}
}

func main() {
	// 使用Gin创建路由引擎
	r := gin.Default()

	// 设置代理路由，模拟Istio sidecar行为
	r.Any("/api/*path", ProxyHandler("localhost:8081"))

	// 启动代理服务
	logrus.Info("Istio风格代理启动于 :8080")
	if err := r.Run(":8080"); err != nil {
		logrus.Fatalf("代理启动失败: %v", err)
	}
}