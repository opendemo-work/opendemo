package main

import "fmt"

// 演示类型推断与多变量操作
func main() {
	// 编译器根据右侧值自动推断类型
	x := 100           // int 类型
	y := "hello"         // string 类型
	z := true           // bool 类型

	fmt.Printf("类型推断变量 - x=%d, y=%s, z=%t\n", x, y, z)

	// 多变量声明与初始化
	a, b, c := 1, 2, 3
	fmt.Printf("多变量同时声明: a=%d, b=%d, c=%d\n", a, b, c)

	// 利用多重赋值交换两个变量的值
	a, b = b, a
	fmt.Printf("交换两个变量: a=%d, b=%d\n", a, b)
}
