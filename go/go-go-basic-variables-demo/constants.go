package main

import "fmt"

// constants.go - 演示常量与 iota 枚举的使用
// 常量在编译时确定，不可修改，适合配置和状态定义

// 使用 const 定义一组相关常量，iota 提供自增值
const (
	StatusPending = iota // 0
	StatusApproved         // 1
	StatusRejected         // 2
)

// 其他常量示例
const (
	MaxRetries = 3
	APIVersion = "v1"
)

// init 函数在 main 之前自动执行，用于演示常量输出
func init() {
	// 输出常量值
	fmt.Println("状态:", getStatusName(StatusPending))
	fmt.Println("状态码:", StatusApproved)
	fmt.Println("最大重试次数:", MaxRetries)
}

// 辅助函数：将状态码转换为名称
func getStatusName(status int) string {
	switch status {
	case StatusPending:
		return "Pending"
	case StatusApproved:
		return "Approved"
	case StatusRejected:
		return "Rejected"
	default:
		return "Unknown"
	}
}