package main

import "fmt"

// loopDemo 函数演示 for 循环的三种常见用法
func loopDemo() {
	fmt.Println("计数从1到5：")
	// 经典 for 循环：初始化; 条件; 后置操作
	for i := 1; i <= 5; i++ {
		fmt.Println(i)
	}

	fmt.Println()
	fmt.Println("使用for模拟while：")
	// 类似 while 的用法：只保留条件
	countdown := 3
	for countdown > 0 {
		fmt.Printf("使用for模拟while：当前值: %d\n", countdown)
		countdown--
	}
	fmt.Println("倒计时结束！")

	fmt.Println()
	fmt.Println("遍历字符串切片：")
	// 使用 for-range 遍历 slice
	fruits := []string{"Apple", "Banana", "Cherry"}
	for _, fruit := range fruits { // _ 表示忽略索引
		fmt.Printf("- %s\n", fruit)
	}
}

// 调用 loopDemo
func init() {
	loopDemo()
}