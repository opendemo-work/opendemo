package main

import (
	"fmt"
)

// mayPanic 模拟一个会触发 panic 的函数
func mayPanic() {
	// 使用 defer 延迟执行一个匿名函数
	// 这个函数将尝试捕获 panic
	defer func() {
		// recover() 只有在 defer 函数中才有效
		if r := recover(); r != nil {
			fmt.Println("recovered:", r)
		}
	}()

	// 主动触发 panic
	// 程序将停止当前函数执行，开始回溯调用栈
	panic("发生了恐慌！")
}

// safeCall 安全调用可能 panic 的函数
func safeCall() {
	fmt.Println("进入 defer 函数")
	mayPanic()
	fmt.Println("这行不会被执行")
}

func main() {
	safeCall()
	fmt.Println("程序继续执行...")
}