package main

import (
	"fmt"
)

// add 是一个基础函数，接收两个整数并返回它们的和
// 参数格式: name type
// 返回值格式: type
func add(a, b int) int {
	return a + b
}

// divide 演示多返回值函数
// 返回除法结果和一个表示是否成功的布尔值
// 处理除零错误的安全除法
func divide(a, b float64) (float64, bool) {
	if b == 0 {
		return 0, false
	}
	return a / b, true
}

// main 函数是程序入口点
func main() {
	// 调用基础函数
	result := add(5, 3)
	fmt.Printf("5 + 3 = %d\n", result)

	// 演示多返回值处理
	if val, ok := divide(5, 2); ok {
		fmt.Printf("除法结果: %.1f, 是否成功: %t\n", val, ok)
	} else {
		fmt.Println("除法错误: 除数不能为零")
	}

	// 测试除零情况
	if val, ok := divide(5, 0); ok {
		fmt.Printf("除法结果: %.1f\n", val)
	} else {
		fmt.Println("除法错误: 除数不能为零")
	}
}