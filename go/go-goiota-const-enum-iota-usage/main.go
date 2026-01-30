package main

import "fmt"

// 定义状态枚举类型
// 使用iota从0开始自动递增
// iota在每个const块开始时重置为0
// 每行iota自动加1

type Status int

const (
	StatusPending = iota // 值为0
	StatusApproved         // 值为1
	StatusRejected         // 值为2
)

// 为Status类型实现String方法
// 这样在打印时能显示有意义的字符串
func (s Status) String() string {
	switch s {
	case StatusPending:
		return "PENDING"
	case StatusApproved:
		return "APPROVED"
	case StatusRejected:
		return "REJECTED"
	default:
		return "UNKNOWN"
	}
}

func main() {
	// 使用枚举值
	currentStatus := StatusPending
	
	fmt.Printf("状态：%v\n", currentStatus)
	fmt.Printf("状态字符串：%s\n", currentStatus.String())
}