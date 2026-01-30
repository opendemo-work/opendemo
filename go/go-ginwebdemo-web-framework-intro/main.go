package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// User 结构体用于接收POST请求中的JSON数据
type User struct {
	Name string `json:"name" binding:"required"`
	Age  int    `json:"age" binding:"gte=0,lte=150"` // 年龄限制合理范围
}

func main() {
	// 创建一个默认的Gin引擎实例
	// Default() 包含了Logger和Recovery中间件
	r := gin.Default()

	// GET 请求：根路径，返回简单JSON消息
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Hello from Gin!",
		})
	})

	// GET 请求：带路径参数和查询参数的用户信息接口
	// 示例：/user/123?name=Tom
	r.GET("/user/:id", func(c *gin.Context) {
		// 获取URL路径中的参数（如:id）
		id := c.Param("id")

		// 获取查询字符串参数，提供默认值
		name := c.DefaultQuery("name", "Guest")

		// 返回JSON格式响应
		c.JSON(http.StatusOK, gin.H{
			"id":   id,
			"name": name,
		})
	})

	// POST 请求：接收JSON格式的用户数据
	r.POST("/user", func(c *gin.Context) {
		var user User

		// ShouldBindJSON 自动解析请求体并进行结构体验证
		if err := c.ShouldBindJSON(&user); err != nil {
			// 如果绑定失败（如字段缺失、类型错误），返回400错误
			c.JSON(http.StatusBadRequest, gin.H{
				"error": err.Error(),
			})
			return
		}

		// 成功接收数据，返回确认信息
		c.JSON(http.StatusOK, gin.H{
			"status":   "success",
			"received": user,
		})
	})

	// 启动HTTP服务器，默认监听 :8080
	// 可通过 r.Run(":9090") 指定其他端口
	r.Run(":8080")
}