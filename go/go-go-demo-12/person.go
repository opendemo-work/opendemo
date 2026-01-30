package main

import "fmt"

// Person 表示一个人的基本信息
type Person struct {
	Name string // 姓名
	Age  int   // 年龄
}

// Greet 打招呼方法，使用值接收者
func (p Person) Greet() {
	fmt.Printf("姓名: %s, 年龄: %d\n", p.Name, p.Age)
}

// Work 工作方法，使用指针接收者（符合修改场景的规范）
func (p *Person) Work() {
	fmt.Printf("%s正在工作...\n", p.Name)
}