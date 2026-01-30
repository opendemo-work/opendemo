package main

import (
	"fmt"
	"time"
)

// main 函数演示基本时间操作
func main() {
	// 获取当前时间
	now := time.Now()
	fmt.Printf("当前时间: %s\n", now.Format("2006-01-02 15:04:05"))

	// 时间加减：计算明天此时
	tomorrow := now.Add(24 * time.Hour)
	fmt.Printf("明天此时: %s\n", tomorrow.Format("2006-01-02 15:04:05"))

	// 调用格式化与解析示例
	formatAndParseExample()

	// 调用定时器示例
	timerExample()
}