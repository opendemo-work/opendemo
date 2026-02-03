package main

import "fmt"

// Status 表示任务状态的枚举类型
type Status int

const (
	// 使用iota定义状态常量
	StatusUnknown Status = iota
	StatusPending
	StatusRunning
	StatusFinished
)

// String 方法为Status类型提供可读的字符串表示
// 实现 fmt.Stringer 接口
func (s Status) String() string {
	switch s {
	case StatusUnknown:
		return "UNKNOWN"
	case StatusPending:
		return "PENDING"
	case StatusRunning:
		return "RUNNING"
	case StatusFinished:
		return "FINISHED"
	default:
		return fmt.Sprintf("Status(%d)", s)
	}
}