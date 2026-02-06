package main

import "fmt"

// createUserClickHandler 模拟生成用户点击事件的回调函数
// 每个返回的函数都捕获了特定的 userID，体现闭包的状态保持能力
func createUserClickHandler(userID int) func() {
	return func() {
		fmt.Printf("按钮被点击了！用户ID: %d\n", userID)
	}
}

// runCallbackExample 执行回调闭包示例
func runCallbackExample() {
	fmt.Println("\n模拟按钮点击事件：")

	// 模拟多个用户的事件处理器
	userIDs := []int{1001, 1002}
	var handlers []func()

	for _, uid := range userIDs {
		// 注意：此处必须使用局部变量副本，否则所有闭包将共享最后一个值
		handlers = append(handlers, createUserClickHandler(uid))
	}

	// 触发事件
	for _, handler := range handlers {
		handler()
	}
}