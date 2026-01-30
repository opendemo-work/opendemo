package main

import "fmt"

// makeCounter 返回一个闭包函数
// 该函数“捕获”了外部作用域的 count 变量
// 每次调用都会使 count 自增并返回新值
func makeCounter() func() int {
	count := 0 // 此变量在函数返回后仍被闭包引用
	return func() int {
		count++
		return count
	}
}

func main() {
	// 创建一个计数器
	counter := makeCounter()

	// 多次调用闭包函数
	fmt.Printf("计数器: %d\n", counter())
	fmt.Printf("计数器: %d\n", counter())
	fmt.Printf("计数器: %d\n", counter())
}