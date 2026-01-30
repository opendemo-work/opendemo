package main

import (
	"fmt"
	"time"
)

// formatAndParseExample 演示时间的格式化与解析
func formatAndParseExample() {
	now := time.Now()

	// 格式化时间为自定义字符串
	dateStr := now.Format("2006/01/02 15:04:05")
	fmt.Printf("格式化时间: %s\n", dateStr)

	// 解析字符串为时间对象
	parsedTime, err := time.Parse("2006-01-02 15:04:05", "2023-01-01 12:00:00")
	if err != nil {
		fmt.Printf("解析时间失败: %v\n", err)
		return
	}
	fmt.Printf("解析后的时间: %v\n", parsedTime)
}