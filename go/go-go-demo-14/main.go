package main

import "fmt"

// main 函数演示闭包作为自增计数器的使用
func main() {
	// 示例1：创建一个计数器闭包
	// 外层匿名函数初始化 count 变量，并返回一个内部函数
	counter := func() func() int {
		count := 0 // 此变量被内部函数捕获
		return func() int {
			count++ // 每次调用都修改外部作用域的 count
			return count
		}
	}() // 立即执行外层函数，返回内部函数

	fmt.Println("计数器从1开始：")
	fmt.Printf("Count: %d\n", counter())
	fmt.Printf("Count: %d\n", counter())
	fmt.Printf("Count: %d\n", counter())

	// 导入其他示例
	runFactoryExample()
	runCallbackExample()
}