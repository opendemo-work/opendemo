package main

import (
	"fmt"
	"strings"
)

// runAdvancedExample 演示前缀判断与大小写转换
func runAdvancedExample() {
	// 示例3：前缀检查
	language := "Go is awesome"
	// HasPrefix 判断字符串是否以指定前缀开始
	startsWithGo := strings.HasPrefix(language, "Go")
	fmt.Printf("【示例3】是否以Go开头: %v\n", startsWithGo)

	// 示例3：大小写转换
	text := "hello world"
	// ToUpper 将所有字符转为大写
	upperText := strings.ToUpper(text)
	fmt.Printf("【示例3】大写转换: %s\n", upperText)
	// 类似地，ToLower 可将字符串转为小写
}