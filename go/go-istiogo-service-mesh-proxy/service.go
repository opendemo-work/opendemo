package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func main() {
	// 创建一个简单的Gin引擎作为后端服务
	r := gin.Default()

	// 定义一个API端点，模拟业务服务
	r.GET("/api/hello", func(c *gin.Context) {
		logrus.Info("[SERVICE] 收到请求: GET /api/hello")
		c.String(http.StatusOK, "Hello from backend via Istio proxy!\n")
	})

	// 启动后端服务
	logrus.Info("后端服务启动于 :8081")
	if err := r.Run(":8081"); err != nil {
		logrus.Fatalf("服务启动失败: %v", err)
	}
}