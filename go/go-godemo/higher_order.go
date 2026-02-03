package main

import "fmt"

// apply 是一个高阶函数，接受一个二元操作函数和两个整数参数，并执行该操作
// 这种模式提高了代码的抽象层次和可重用性
func apply(op func(int, int) int, a, b int) int {
	return op(a, b)
}

// multiply 是一个简单的乘法函数，可用于传给 apply
func multiply(a, b int) int {
	return a * b
}

// higherOrderExamples 演示高阶函数的使用
func higherOrderExamples() {
	result := apply(addWithoutOverflow, 5, 6)
	fmt.Printf("通过高阶函数计算: %d\n", result)

	// 使用匿名函数作为参数
	square := apply(func(a, b int) int {
		return a * a
	}, 4, 0)
	fmt.Printf("平方运算结果: %d\n", square)
}

// addWithoutOverflow 封装add函数以便兼容apply签名
func addWithoutOverflow(a, b int) int {
	sum, _ := add(a, b)
	return sum
}