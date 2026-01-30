package main

import "fmt"

// 演示短变量声明（:=）的使用场景
func main() {
	// 使用 := 进行短变量声明，编译器自动推断类型
	// 注意：只能在函数内部使用
	name := "张三"
	age := 25
	height := 1.78

	// 输出变量值
	fmt.Printf("使用 := 声明的变量: name=%s, age=%d, height=%.2f\n", name, age, height)

	// 后续可以重新赋值
	age = 26
	height = 1.80
	fmt.Printf("更新后: name=%s, age=%d, height=%.2f\n", name, age, height)
}
