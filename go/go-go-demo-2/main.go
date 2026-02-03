package main

import "fmt"

// main.go - 演示Go中基本变量的显式声明
// 展示如何使用 var 关键字声明不同类型的变量
func main() {
	// 显式声明整型变量
	var age int = 42
	// 显式声明浮点型变量
	var price float64 = 3.14
	// 显式声明布尔型变量
	var isActive bool = true
	// 显式声明字符串变量
	var message string = "Hello, Go!"

	// 输出所有变量值
	fmt.Println("整数:", age)
	fmt.Println("浮点数:", price)
	fmt.Println("布尔值:", isActive)
	fmt.Println("字符串:", message)
	fmt.Println() // 空行分隔
}
