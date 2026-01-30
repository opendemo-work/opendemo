package main

import (
	"strings"
)

// CleanAndTitle 清理字符串首尾空格，并将每个单词首字母大写
// 注意：strings.Title 对非ASCII字符支持有限，适合简单场景
func CleanAndTitle(s string) string {
	// TrimSpace 去除前后空白字符
	trimmed := strings.TrimSpace(s)
	// Title 将每个单词首字母转为大写
	return strings.Title(trimmed)
}

// RepeatString 将输入字符串重复n次
// 使用 strings.Repeat 提高性能，避免手动循环拼接
func RepeatString(s string, n int) string {
	if n <= 0 {
		return ""
	}
	return strings.Repeat(s, n)
}

// SafeJoin 使用指定分隔符安全拼接两个字符串
// 避免直接字符串拼接可能带来的空指针或格式问题
func SafeJoin(part1, part2, sep string) string {
	// 确保分隔符不为空
	if sep == "" {
		sep = "_" // 默认使用下划线
	}
	return strings.Join([]string{part1, part2}, sep)
}