package main

import (
	"fmt"
	"go-make-demo/utils"
)

// main 是程序入口点
// 使用Makefile自动化构建可以简化编译和运行流程
func main() {
	fmt.Println("Hello, Makefile!")

	// 调用工具包中的函数展示模块化设计
	result := utils.Add(2, 3)
	fmt.Printf("The result of 2 + 3 is: %d\n", result)
}
