package main

import "fmt"

// types_inferred.go - 演示Go的类型推断与短变量声明
// 使用 := 让编译器自动推断变量类型，提高编码效率
func demonstrateTypeInference() {
	// 使用短声明并让Go自动推断为 int
	count := 100
	// 自动推断为 float64
	pi := 2.718
	// 自动推断为 string
	text := "变量已自动推断类型"

	// 输出推断后的变量
	fmt.Println("推断整数:", count)
	fmt.Println("推断浮点数:", pi)
	fmt.Println("消息:", text)
}

// 注意：main 函数已在 main.go 中定义
// 这里我们添加一个 init 函数来自动调用演示
func init() {
	demonstrateTypeInference()
	fmt.Println() // 添加空行
}