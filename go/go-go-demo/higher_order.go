package main

import "fmt"

// operation 是一个函数类型，表示接受两个int并返回一个int的函数
type operation func(int, int) int

// applyOperation 接受一个操作函数和两个参数，执行该操作
// 演示高阶函数：函数作为参数传递
func applyOperation(op operation, a, b int) int {
	return op(a, b)
}

// makeMultiplier 返回一个乘法函数，其乘数固定为factor
// 演示函数工厂：返回函数的函数
func makeMultiplier(factor int) operation {
	return func(a, b int) int {
		return a * b * factor
	}
}

func demonstrateHigherOrder() {
	// 使用高阶函数应用不同的操作
	add := func(a, b int) int { return a + b }
	multiply := func(a, b int) int { return a * b }

	result1 := applyOperation(add, 4, 6)
	result2 := applyOperation(multiply, 4, 6)

	fmt.Printf("应用加法: %d\n", result1)
	fmt.Printf("应用乘法: %d\n", result2)

	// 使用函数工厂创建特定的乘法器
	doubleMultiply := makeMultiplier(2)
	result3 := doubleMultiply(3, 4) // 相当于 3 * 4 * 2
	fmt.Printf("双倍乘法: %d\n", result3)
}

func main() {
	demonstrateClosure()
	demonstrateHigherOrder()
}