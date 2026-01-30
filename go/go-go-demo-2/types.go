package main

import "fmt"

// 演示Go中的基本数据类型
func demonstrateTypes() {
	// 使用变量组声明多个不同类型的变量
	var (
		integer int     = 42
		decimal float64 = 3.14
		active  bool    = true
		text    string  = "Hello"
	)

	// 格式化输出各种类型
	fmt.Printf("整型: %d, 浮点型: %.2f, 布尔型: %t, 字符串: %s\n", integer, decimal, active, text)
}

// 在main中调用
func init() {
	demonstrateTypes()
}