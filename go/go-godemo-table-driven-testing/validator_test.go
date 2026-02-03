package main

import (
	"regexp"
	"testing"
)

// ValidateEmail 使用正则表达式验证基础邮箱格式
// 注意：生产环境应使用更严格的验证或第三方库
func ValidateEmail(email string) bool {
	const emailRegex = `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
	return regexp.MustCompile(emailRegex).MatchString(email)
}

// TestValidateEmail 表驱动测试邮箱验证函数
func TestValidateEmail(t *testing.T) {
	// 测试用例包括合法和非法邮箱
	tests := []struct {
		name     string // 自定义测试名称，提高可读性
		email    string
		valid    bool
	}{
		{name: "Valid_Simple", email: "user@example.com", valid: true},
		{name: "Valid_WithDot", email: "first.last@domain.co", valid: true},
		{name: "Valid_WithPlus", email: "user+tag@site.org", valid: true},
		{name: "Invalid_MissingAt", email: "userdomain.com", valid: false},
		{name: "Invalid_MissingDomain", email: "user@", valid: false},
		{name: "Invalid_Empty", email: "", valid: false},
		{name: "Invalid_OnlyAt", email: "@", valid: false},
	}

	// 执行每个测试用例
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got := ValidateEmail(tc.email)
			if got != tc.valid {
				t.Errorf("ValidateEmail(%q) = %v; 期望 %v", tc.email, got, tc.valid)
			}
		})
	}
}