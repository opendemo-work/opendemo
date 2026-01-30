package main

import (
	"net/http"
	"strings"

	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
)

var jwtKey = []byte("my_secret_key") // 必须与签发时一致

// JWT认证中间件
func authMiddleware(c *gin.Context) {
	// 从请求头获取Authorization字段
	authHeader := c.GetHeader("Authorization")
	if authHeader == "" {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "缺少Authorization头"})
		c.Abort()
		return
	}

	// 验证格式：Bearer <token>
	parts := strings.Split(authHeader, " ")
	if len(parts) != 2 || parts[0] != "Bearer" {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization头格式错误"})
		c.Abort()
		return
	}

	tokenString := parts[1]
	claims := &Claims{}

	// 解析并验证Token
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		return jwtKey, nil
	})

	// 检查Token有效性
	if err != nil || !token.Valid {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "无效或过期的Token"})
		c.Abort()
		return
	}

	// 将用户名注入上下文，供后续处理器使用
	c.Set("username", claims.Username)
	c.Next() // 继续处理请求
}