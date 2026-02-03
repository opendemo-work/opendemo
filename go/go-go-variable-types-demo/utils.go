package main

import "fmt"

// Swap 交换两个整数的值，演示多返回值
func Swap(a, b int) (int, int) {
	return b, a
}

// GetArrayLength 返回数组长度
func GetArrayLength(arr [3]string) int {
	return len(arr)
}

// 演示工具函数的使用
func useUtils() {
	// 测试交换函数
	a, b := 5, 10
	fmt.Println("\n=== 工具函数演示 ===")
	fmt.Printf("交换前: a=%d, b=%d\n", a, b)
	a, b = Swap(a, b)
	fmt.Printf("交换后: a=%d, b=%d\n", a, b)

	// 测试数组长度
	colors := [3]string{"red", "green", "blue"}
	length := GetArrayLength(colors)
	fmt.Printf("数组长度: %d\n", length)
}