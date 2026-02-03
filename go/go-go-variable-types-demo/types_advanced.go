package main

import (
	"fmt"
	"time"
)

// Point 表示二维坐标点
type Point struct {
	X, Y int
}

// User 表示用户信息
type User struct {
	ID       int
	Username string
	LoggedIn bool
}

// 演示结构体和时间类型的使用
func showAdvancedTypes() {
	// 创建结构体实例
	p := Point{X: 10, Y: 20}
	u := User{
		ID:       1,
		Username: "testuser",
		LoggedIn: true,
	}

	// 使用 time 包获取当前时间
	currentTime := time.Now()

	fmt.Println("\n=== 高级类型用法 ===")
	fmt.Printf("坐标: (%d, %d)\n", p.X, p.Y)
	fmt.Printf("用户信息: ID=%d, 名称=%s, 登录状态=%t\n", u.ID, u.Username, u.LoggedIn)
	fmt.Printf("当前时间: %v\n", currentTime)
}