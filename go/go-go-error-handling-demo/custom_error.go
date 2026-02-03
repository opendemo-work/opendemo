package main

import (
	"fmt"
)

// ValidationError 是一个自定义错误类型，用于验证失败场景
type ValidationError struct {
	Field   string  // 出错的字段名
	Value   int     // 实际值
	Message string  // 错误描述
}

// 实现 error 接口的 Error() 方法
func (e *ValidationError) Error() string {
	return fmt.Sprintf("自定义错误：%s：%s，当前值：%d", e.Field, e.Message, e.Value)
}

// validateAge 验证年龄是否合法，演示自定义错误的使用
func validateAge(age int) error {
	if age < 0 || age > 150 {
		return &ValidationError{
			Field:   "年龄",
			Value:   age,
			Message: "必须在 0 到 150 之间",
		}
	}
	return nil
}

func runCustomErrorExample() {
	// 模拟无效输入
	err := validateAge(-5)
	if err != nil {
		fmt.Println(err)
	}

	// 错误类型断言示例
	if validationErr, ok := err.(*ValidationError); ok {
		fmt.Printf("验证失败字段: %s, 值: %d\n", validationErr.Field, validationErr.Value)
	}

	// 模拟文件操作错误
	fmt.Println("文件读取失败模拟：文件未找到")
}