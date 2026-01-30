package main

import (
	"fmt"
	"strings"
)

// main 函数演示 strings 包的基础用法
func main() {
	fmt.Println("=== 字符串基础操作 ===")

	// 定义一个原始字符串
	text := "Hello, 世界! Welcome to Golang."
	fmt.Printf("原始文本: %s\n", text)

	// 转换为大写
	upperText := strings.ToUpper(text)
	fmt.Printf("转为大写: %s\n", upperText)

	// 判断是否包含特定子串
	contains := strings.Contains(text, "Golang")
	fmt.Printf("是否包含\"Golang\": %t\n", contains)

	// 替换子串
	replaced := strings.ReplaceAll(text, "Golang", "Go")
	fmt.Printf("替换\"Golang\"为\"Go\": %s\n", replaced)

	// 按分隔符分割字符串
	parts := strings.Split(text, " ")
	fmt.Printf("按空格分割: %v\n", parts)

	fmt.Println()
	// 调用工具函数
	demoUtils()
}

// demoUtils 演示如何使用自定义字符串工具函数
func demoUtils() {
	fmt.Println("=== 字符串工具函数演示 ===")

	// 使用 CleanAndTitle 清理并格式化字符串
	cleaned := CleanAndTitle("  hello world  ")
	fmt.Printf("清理并标题化: %s\n", cleaned)

	// 使用 RepeatString 重复字符串
	repeated := RepeatString("Test", 3)
	fmt.Printf("重复三次: %s\n", repeated)

	// 使用 SafeJoin 安全拼接字符串
	joined := SafeJoin("Part1", "Part2", "_")
	fmt.Printf("安全拼接: %s\n", joined)
}