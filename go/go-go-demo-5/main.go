package main

import (
	"fmt"
)

// main 函数是程序的入口点
// 演示如何使用接口实现多态行为
func main() {
	fmt.Println("打印测试：")
	// 创建可打印对象的切片（接口类型）
	printables := []Printable{
		&Text{Content: "Hello, Interface!"},
		&Document{Title: "Go Guide", Content: "Go is awesome!"},
	}

	// 遍历并调用每个对象的 Print 方法
	// 虽然类型不同，但都实现了 Printable 接口
	for _, p := range printables {
		p.Print()
	}

	fmt.Println("\n交通工具测试：")
	// 同样方式处理交通工具
	vehicles := []Vehicle{
		&Car{Speed: 60},
		&Bicycle{Speed: 15},
	}

	for _, v := range vehicles {
		v.Drive()
	}
}