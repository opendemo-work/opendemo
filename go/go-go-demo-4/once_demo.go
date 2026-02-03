package main

import (
	"fmt"
	"sync"
)

var (
	initialized bool
	once       sync.Once
)

// 模拟只执行一次的初始化操作
func initialize() {
	once.Do(func() {
		fmt.Println("第一次调用：初始化开始")
		// 模拟初始化逻辑
		initialized = true
		fmt.Println("初始化完成")
	})
}

func main() {
	// 第一次调用会触发初始化
	initialize()

	// 第二次调用不会执行初始化逻辑
	fmt.Println("第二次调用：无操作（已初始化）")
	initialize()
}