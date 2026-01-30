package main

import (
	"fmt"
	"log"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var jwtKey = []byte("my_secret_key") // 实际使用应从环境变量读取

// Claims 自定义JWT声明
type Claims struct {
	Name string `json:"name"`
	jwt.RegisteredClaims
}

// generateJWT 生成JWT令牌
func generateJWT() (string, error) {
	claims := &Claims{
		Name: "Alice",
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(24 * time.Hour)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    "go-demo",
		},
	}

	// 创建签名对象并生成token字符串
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtKey)
}

// parseJWT 解析JWT令牌
func parseJWT(tokenStr string) (*Claims, error) {
	claims := &Claims{}
	token, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
		return jwtKey, nil
	})
	if err != nil {
		return nil, err
	}
	if !token.Valid {
		return nil, fmt.Errorf("invalid token")
	}
	return claims, nil
}

func main() {
	// 生成JWT
	token, err := generateJWT()
	if err != nil {
		log.Fatal("生成JWT失败:", err)
	}
	fmt.Printf("JWT令牌生成: %s\n", token)

	// 解析JWT
	claims, err := parseJWT(token)
	if err != nil {
		log.Fatal("解析JWT失败:", err)
	}
	fmt.Printf("JWT解析成功: %+v\n", claims)
}