package main

import (
	"fmt"
)

// newCounter 创建一个计数器闭包
// 返回的函数每次调用都会使内部计数加1
// 演示了闭包如何捕获并维护外部作用域的变量
func newCounter() func() int {
	count := 0 // 此变量被闭包捕获
	return func() int {
		count++
		return count
	}
}

// newAccumulator 创建一个累加器闭包
// 初始值由参数指定，返回的函数可不断累加数值
func newAccumulator(initial int) func(int) int {
	sum := initial
	return func(x int) int {
		sum += x
		return sum
	}
}

func main() {
	// 创建计数器实例
	counter := newCounter()
	fmt.Printf("计数器: %d\n", counter()) // 1
	fmt.Printf("计数器: %d\n", counter()) // 2
	fmt.Printf("计数器: %d\n", counter()) // 3

	// 创建累加器实例
	acc := newAccumulator(9) // 初始值9
	fmt.Printf("累加器: %d\n", acc(1)) // 10
	fmt.Printf("累加器: %d\n", acc(5)) // 15
	fmt.Printf("累加器: %d\n", acc(6)) // 21
}