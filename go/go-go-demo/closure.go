package main

import "fmt"

// newCounter 创建一个计数器闭包
// 演示闭包如何捕获并保持对外部函数局部变量的引用
func newCounter() func() int {
	count := 0 // 此变量被闭包捕获

	// 返回一个匿名函数，它能访问并修改 count
	return func() int {
		count++ // 修改捕获的变量
		return count
	}
}

// 在main函数中演示闭包使用
func demonstrateClosure() {
	counter := newCounter()

	fmt.Printf("计数器: %d\n", counter()) // 输出: 1
	fmt.Printf("计数器: %d\n", counter()) // 输出: 2
	fmt.Printf("计数器: %d\n", counter()) // 输出: 3
}