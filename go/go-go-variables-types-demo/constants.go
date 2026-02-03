package main

import "fmt"

// 常量声明 - 值在编译时确定且不可更改
const (
	StatusUnknown = 0
	StatusWorking = iota // iota 自动递增，值为1
	StatusResting          // 值为2
	StatusOff              // 值为3
)

// 使用 iota 创建颜色枚举
const (
	Red Color = iota   // 0
	Green              // 1
	Blue               // 2
)

// 定义新类型 Color，基于 int
type Color int

// 实现 String 方法以便格式化输出
func (c Color) String() string {
	colors := []string{"Red", "Green", "Blue"}
	if int(c) < len(colors) {
		return colors[c]
	}
	return "Unknown"
}

// 显示工作状态的函数
func displayStatus() {
	currentStatus := StatusWorking
	fmt.Printf("工作状态: ")
	
	switch currentStatus {
	case StatusWorking:
		fmt.Println("工作中")
	case StatusResting:
		fmt.Println("休息中")
	case StatusOff:
		fmt.Println("已关闭")
	default:
		fmt.Println("未知状态")
	}
}

// 显示颜色枚举
func displayColors() {
	favoriteColor := Green
	fmt.Printf("颜色: %s, 数值: %d\n", favoriteColor, favoriteColor)
}