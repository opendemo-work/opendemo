package main

import (
	"fmt"
	"regexp"
)

// 邮箱验证正则表达式
// 解释：
// ^[a-zA-Z0-9._%+-]+ : 开头，用户名部分，允许字母数字及常见符号
// @                  : 必须包含@符号
// [a-zA-Z0-9.-]+     : 域名主体
// \.[a-zA-Z]{2,}$    : 顶级域名，至少两个字母
var emailRegex = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

// IsValidEmail 检查给定字符串是否为有效邮箱格式
func IsValidEmail(email string) bool {
	return emailRegex.MatchString(email)
}

func main() {
	// 示例：验证邮箱地址
	fmt.Printf("邮箱 'example@example.com' 格式有效: %t\n", IsValidEmail("example@example.com"))
	fmt.Printf("邮箱 'invalid-email' 格式有效: %t\n", IsValidEmail("invalid-email"))

	// 调用其他模块功能
	parseLogLines()
	performTextReplacement()
}