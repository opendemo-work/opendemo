package main

import (
	"fmt"
	"strings"
)

// demoFormatting 演示字符串的格式化处理
func demoFormatting() {
	// 字符串转为大写
	s := "Hello World"
	upper := strings.ToUpper(s)
	fmt.Printf("大写：%s\n", upper)

	// 将所有空格替换为连字符
	replaced := strings.ReplaceAll(strings.ToLower(s), " ", "-")
	fmt.Printf("替换空格为 '-'：%s\n", replaced)
}