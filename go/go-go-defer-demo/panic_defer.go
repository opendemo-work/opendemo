package main

import "fmt"

// riskyFunction 演示即使发生 panic，defer 依然会执行
func riskyFunction() {
	fmt.Println("进入函数")

	// 注册延迟执行的清理函数
	defer func() {
		fmt.Println("defer 执行：清理工作完成")
	}()

	// 故意引发 panic
	panic("触发一个错误")
}

func main() {
	// 注意：recover 可用于捕获 panic，但本例不使用以展示 defer 行为
	riskyFunction()

	// 这行不会执行
	fmt.Println("这行不会打印")
}

// 关键点：尽管函数 panic，defer 中的清理代码仍然运行