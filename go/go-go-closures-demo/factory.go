package main

import "fmt"

// createLogger 是一个工厂函数，返回一个带前缀的日志打印函数
// 演示闭包如何封装配置信息，生成定制化行为
func createLogger(prefix string) func(message string) {
	return func(message string) {
		fmt.Printf("%s: %s\n", prefix, message)
	}
}

// runFactoryExample 执行工厂模式示例
func runFactoryExample() {
	fmt.Println("\n创建带前缀的日志函数：")

	// 创建不同类型的日志函数
	infoLog := createLogger("INFO")
	errorLog := createLogger("ERROR")

	// 使用闭包函数打印消息
	infoLog("系统启动")
	errorLog("文件未找到")
}