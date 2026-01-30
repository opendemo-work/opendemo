package main

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
)

// 定义JWT密钥（实际项目中应从环境变量读取）
var jwtKey = []byte("my_secret_key")

// 用户登录请求结构体
type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// 自定义声明结构体，嵌入标准字段
type Claims struct {
	Username string `json:"username"`
	jwt.StandardClaims
}

// 模拟用户登录处理函数
func loginHandler(c *gin.Context) {
	var req LoginRequest
	// 解析请求体
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "无效的请求参数"})
		return
	}

	// 简单模拟验证（生产环境应查数据库+密码校验）
	if req.Username != "admin" || req.Password != "password" {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "用户名或密码错误"})
		return
	}

	// 设置Token过期时间为24小时
	expirationTime := time.Now().Add(24 * time.Hour)
	claims := &Claims{
		Username: req.Username,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: expirationTime.Unix(),
			Issuer:    "jwt-auth-demo",
		},
	}

	// 创建签名对象并生成Token字符串
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(jwtKey)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "生成Token失败"})
		return
	}

	// 返回Token给客户端
	c.JSON(http.StatusOK, gin.H{"token": tokenString})
}

// 受保护的接口处理器
func protectedHandler(c *gin.Context) {
	// 中间件已验证Token，直接获取上下文中的用户名
	username := c.GetString("username")
	c.JSON(http.StatusOK, gin.H{"message": "Hello " + username + ", this is a protected route"})
}

func main() {
	// 创建Gin引擎
	r := gin.Default()

	// 登录接口（无需认证）
	r.POST("/login", loginHandler)

	// 受保护的路由组
	protected := r.Group("/protected")
	protected.Use(authMiddleware) // 使用JWT中间件
	{
		protected.GET("", protectedHandler)
	}

	// 启动HTTP服务
	println("[INFO] 服务启动中... 访问 http://localhost:8080")
	r.Run(":8080") // 监听在 8080 端口
}