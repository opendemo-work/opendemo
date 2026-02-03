package main

import "fmt"

// 主函数：演示 if-else 控制流
func main() {
	// 示例1: 基本的 if-else 条件判断
	var num int = 10
	fmt.Println("--- if-else 示例 ---")
	if num > 0 {
		fmt.Println("数字是正数")
	} else if num < 0 {
		fmt.Println("数字是负数")
	} else {
		fmt.Println("数字是零")
	}
	fmt.Println()

	// 调用其他文件中的函数
	runSwitchDemo()
	runForDemo()
}