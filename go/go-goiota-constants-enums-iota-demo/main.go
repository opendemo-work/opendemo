package main

import "fmt"

// 定义方向类型，基于int
type Direction int

// 使用iota定义四个方向常量
// iota在const块中从0开始自动递增
const (
	Up Direction = iota    // 值为0
	Down                    // 值为1
	Left                    // 值为2
	Right                   // 值为3
)

// 定义颜色类型
type Color int

// 颜色常量，从1开始以避免0值混淆
const (
	Red Color = iota + 1  // 值为1
	Green                 // 值为2
	Blue                  // 值为3
)

func main() {
	// 打印方向常量值
	fmt.Printf("方向：Up=%d, Down=%d, Left=%d, Right=%d\n", Up, Down, Left, Right)

	// 打印颜色常量值
	fmt.Printf("颜色：Red=%d, Green=%d, Blue=%d\n", Red, Green, Blue)

	// 使用color.go中定义的String()方法
	fmt.Printf("详细颜色：%s, %s, %s\n", Red.String(), Green.String(), Blue.String())

	// 测试未知值
	var unknown Color = 99
	fmt.Printf("未知颜色显示为：%s\n", unknown.String())
}