package main

import "fmt"

// Person 表示一个人的基本信息
// 使用结构体封装数据
type Person struct {
	Name string // 姓名字段
}

// SetValueByValue 是一个值接收者方法
// 接收的是Person的副本，因此无法修改原始实例
// 适用于不需要修改状态且结构体较小的场景
func (p Person) SetValueByValue(name string) {
	p.Name = name // 修改的是副本，不影响原始对象
	fmt.Printf("在值接收者方法内: %s\n", p.Name)
}

// SetValueByPointer 是一个指针接收者方法
// 接收的是Person的指针，可以直接修改原始实例
// 适用于需要修改状态或结构体较大的情况
func (p *Person) SetValueByPointer(name string) {
	p.Name = name // 直接修改原始对象
	fmt.Printf("在指针接收者方法内: %s\n", p.Name)
}