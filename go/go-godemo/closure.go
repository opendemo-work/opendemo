package main

import "fmt"

// makeAccumulator 创建一个闭包，返回一个能持续累加的函数
// 外部变量 val 被内部匿名函数捕获，形成闭包
func makeAccumulator(start int) func(int) int {
	val := start
	return func(delta int) int {
		val += delta
		return val
	}
}

// makeCounter 创建一个计数器闭包，每次调用返回递增的整数
func makeCounter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

// closureExamples 演示闭包的实际使用
func closureExamples() {
	// 创建一个从10开始的累加器
	acc := makeAccumulator(10)
	fmt.Printf("累加器从10开始: %d, %d, %d\n", acc(1), acc(1), acc(1))

	// 创建一个计数器
	counter := makeCounter()
	fmt.Printf("计数器: %d, %d, %d\n", counter(), counter(), counter())
}