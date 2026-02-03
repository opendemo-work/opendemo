package main

import "fmt"

// 演示变量的基本声明方式和零值机制
func main() {
	// 使用 var 声明变量（未初始化时具有零值）
	var isActive bool        // 布尔类型，零值为 false
	var count int            // 整型，零值为 0
	var price float64        // 浮点型，零值为 0.0
	var message string       // 字符串类型，零值为 ""

	// 输出零值
	fmt.Println("布尔类型 (默认):", isActive)
	fmt.Println("整型 (默认):", count)
	fmt.Println("浮点型 (默认):", price)
	fmt.Println("字符串 (默认):", message)

	// 带初始值的变量声明
	var (
		valid   = true
		number  = 42
		cost    = 3.14
		greeting = "Hello Go"
	)

	// 输出初始化后的变量
	fmt.Println("带初始值的变量:", valid, ",", number, ",", cost, ",", greeting)
}
