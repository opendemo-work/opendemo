package main

import "fmt"

// main 演示 defer 的基本用法：确保资源释放
func main() {
	fmt.Println("打开资源...")

	// 使用 defer 注册清理函数
	defer fmt.Println("关闭资源...")

	// 模拟主要业务逻辑
	fmt.Println("执行主要逻辑")

	// 即使这里有多次 return，defer 都会执行
	// return
}

// 输出顺序说明：
// 1. 打开资源...
// 2. 执行主要逻辑
// 3. 关闭资源... (defer 在函数 return 前自动调用)