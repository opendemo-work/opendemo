package main

import "fmt"

// add 计算两个整数的和，并检测是否溢出
// Go支持多返回值，常用于返回结果和错误/状态
func add(a, b int) (int, bool) {
	result := a + b
	// 简单的溢出检测（仅用于演示）
	if a > 0 && b > 0 && result < 0 {
		return 0, true // 溢出
	}
	return result, false
}

// divide 执行整数除法，返回商和余数
// 演示命名返回值的用法，让代码更清晰
func divide(dividend, divisor int) (quotient int, remainder int) {
	if divisor == 0 {
		return 0, 0 // 实际项目中应返回错误
	}
	quotient = dividend / divisor
	remainder = dividend % divisor
	return // 使用裸返回，自动返回命名的返回值
}

func main() {
	// 调用具有多返回值的函数
	sum, overflow := add(10, 5)
	if overflow {
		fmt.Println("加法运算溢出")
	} else {
		fmt.Printf("加法结果: %d, 是否溢出: %v\n", sum, overflow)
	}

	// 调用命名返回值函数
	q, r := divide(13, 4)
	fmt.Printf("除法结果: %d, 余数: %d\n", q, r)
}