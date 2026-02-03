package main

import "fmt"

// 演示基本变量声明和数据类型
// 使用 var 关键字在函数外部声明包级变量
var (
	// 整数类型
	age int = 25
	// 浮点数类型
	salary float64 = 5000.50
	// 字符串类型
	name string = "张三"
	// 布尔类型
	isActive bool = true
)

func main() {
	// 声明基本类型的局部变量
	var number int = 42
	var pi float64 = 3.14
	var success bool = true
	var greeting string = "Hello Gopher"

	// 使用 fmt.Printf 格式化输出多个变量
	fmt.Printf("整数: %d, 浮点数: %.2f, 布尔值: %t, 字符串: %s\n", 
		number, pi, success, greeting)
	
	// 输出包级变量
	fmt.Printf("姓名: %s, 年龄: %d, 薪资: %.2f\n", name, age, salary)

	// 调用其他文件中的函数
	displayStatus()
	displayColors()
	demonstrateTypeInference()
}