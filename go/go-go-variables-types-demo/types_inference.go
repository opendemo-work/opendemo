package main

import "fmt"

// 演示类型推断和短变量声明
// 这是Go中最常见的局部变量声明方式
func demonstrateTypeInference() {
	// 使用 := 进行短变量声明，编译器自动推断类型
	x, y, z := 10, 20, 30 // 推断为 int 类型
	
	// 多重赋值和类型推断
	a, b := "hello", 3.14159 // a 为 string, b 为 float64
	
	// 输出变量及其类型
	fmt.Printf("x=%d, y=%d, z=%d (自动推断为int类型)\n", x, y, z)
	fmt.Printf("a=%s, b=%.5f (自动推断为string和float64)\n", a, b)
	
	// 演示类型不能更改
	// x = "new" // 这行会编译错误：cannot use "new" (type string) as type int
	
	// 使用空标识符 _ 忽略不需要的返回值
	_, result := calculate(5, 3)
	fmt.Printf("计算结果: %d\n", result)
}

// 示例函数，返回两个值
func calculate(a, b int) (int, int) {
	sum := a + b
	product := a * b
	return sum, product // 返回和与积
}