package main

import (
	"fmt"
)

// divide 安全除法函数，使用 recover 处理除零
func divide(a, b int) int {
	// 延迟函数用于恢复 panic
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("除零错误被恢复")
		}
	}()

	if b == 0 {
		panic("division by zero")
	}
	return a / b
}

func main() {
	// 正常计算
	result1 := divide(10, 1)
	fmt.Printf("计算结果: %d\n", result1)

	result2 := divide(10, 2)
	fmt.Printf("计算结果: %d\n", result2)

	// 会 panic，但被 recover 捕获
	_ = divide(10, 0)

	fmt.Println("继续执行其他任务...")
}