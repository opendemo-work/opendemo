package main

import (
	"context"
	"fmt"
)

// 自定义上下文 key 类型，避免字符串冲突
type contextKey string

const UserIDKey contextKey = "userID"

// authenticate 模拟权限检查，从上下文中获取用户ID
func authenticate(ctx context.Context) error {
	userID, ok := ctx.Value(UserIDKey).(string)
	if !ok || userID == "" {
		return fmt.Errorf("未找到用户身份")
	}
	fmt.Printf("处理用户请求: %s\n", userID)
	// 模拟验证逻辑
	fmt.Println("用户权限验证通过")
	return nil
}

// handleRequest 模拟 HTTP 请求处理流程
func handleRequest(ctx context.Context) {
	if err := authenticate(ctx); err != nil {
		fmt.Printf("认证失败: %v\n", err)
		return
	}
	fmt.Println("请求完成")
}

func main() {
	// 创建根上下文并注入用户ID
	ctx := context.WithValue(context.Background(), UserIDKey, "user123")

	// 处理请求
	handleRequest(ctx)
}