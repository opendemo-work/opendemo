package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"time"

	// docs 是由 swag 生成的包，必须导入以注册 Swagger 处理程序
	_ "swagger-demo/docs"
	"github.com/swaggo/gin-swagger" // gin-swagger middleware
	"github.com/swaggo/files"        // swagger embed files
)

// @title           Swagger Demo API
// @version         1.0
// @description     一个简单的Go API 示例，用于演示 Swagger 文档生成
// @termsOfService  http://swagger.io/terms/

// @contact.name   API 支持
// @contact.url    http://www.example.com/support
// @contact.email  support@example.com

// @license.name  Apache 2.0
// @license.url   http://www.apache.org/licenses/LICENSE-2.0.html

// @host      localhost:8080
// @BasePath  /api
// @schemes   http
func main() {
	// 创建默认的 Gin 引擎
	r := gin.Default()

	// 分组 API 路由
	api := r.Group("/api")
	{
		// @Summary 健康检查
		// @Description 返回 pong 表示服务正常运行
		// @Tags 基础
		// @Success 200 {object} map[string]string
		// @Router /ping [get]
		api.GET("/ping", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{
				"message": "pong",
			})
		})

		// @Summary 获取用户信息
		// @Description 根据用户ID返回模拟的用户数据
		// @Tags 用户管理
		// @Param id path int true "用户ID"
		// @Success 200 {object} map[string]interface{}
		// @Failure 400 {object} map[string]string
		// @Router /user/{id} [get]
		api.GET("/user/:id", func(c *gin.Context) {
			id := c.Param("id")
			c.JSON(http.StatusOK, gin.H{
				"id":   id,
				"name": "张三",
				"createdAt": time.Now().Format(time.RFC3339),
			})
		})
	}

	// 自动注入 Swagger UI 路由
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// 启动服务器
	gin.Print("Starting server on :8080\n")
	gin.Print("Swagger UI available at http://localhost:8080/swagger/index.html\n")
	_ = r.Run(":8080") // 监听并在 0.0.0.0:8080 上启动服务
}