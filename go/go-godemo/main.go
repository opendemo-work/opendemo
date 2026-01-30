package main

import "fmt"

// add 函数接收两个整数，返回它们的和以及是否发生溢出的标志
// Go支持多返回值，这是其区别于其他语言的重要特性之一
func add(a, b int) (int, bool) {
	// 检查是否可能发生整数溢出（简化版）
	if a > 0 && b > 0 && a > int(^uint(0)>>1)-b {
		return 0, true // 溢出
	}
	return a + b, false
}

// fibonacci 生成前n个斐波那契数
func fibonacci(n int) []int {
	if n <= 0 {
		return []int{}
	}
	if n == 1 {
		return []int{0}
	}
	result := make([]int, n)
	result[0], result[1] = 0, 1
	for i := 2; i < n; i++ {
		result[i] = result[i-1] + result[i-2]
	}
	return result
}

func main() {
	// 示例1：使用基础函数和多返回值
	sum, overflow := add(7, 8)
	if overflow {
		fmt.Println("计算溢出")
	} else {
		fmt.Printf("加法结果: %d, 是否溢出: %v\n", sum, overflow)
	}

	// 示例2：调用斐波那契函数
	fmt.Printf("斐波那契数列前8项: %v\n", fibonacci(8))

	// 导出函数供其他文件使用
	higherOrderExamples()
	closureExamples()
}