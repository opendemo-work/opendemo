package main

import "fmt"

// Person 表示一个人的基本信息
type Person struct {
	Name string
}

// Greet 返回问候语
func (p Person) Greet() string {
	return fmt.Sprintf("你好，我是%s", p.Name)
}

// Department 表示部门信息（用于嵌入）
type Department struct {
	DeptName string
}

// Employee 表示员工，通过嵌入Person和Department实现组合
// 注意：Person是匿名字段，将自动提升其字段和方法
type Employee struct {
	Person        // 匿名嵌入Person，实现属性和行为复用
	Position string // 当前职位
	Department     // 匿名嵌入部门
}

// Animal 表示动物基础结构
type Animal struct {
	Name string
	Kind string
}

// Speak 让动物发出声音
func (a Animal) Speak() {
	fmt.Printf("动物名称: %s, 种类: %s, 发出声音: ", a.Name, a.Kind)
}

// Dog 狗，嵌入Animal并添加具体行为
type Dog struct {
	Animal // 嵌入动物通用属性
}

// Bark 实现狗的叫声
func (d Dog) Bark() {
	d.Speak()
	fmt.Println("汪汪！")
}

func main() {
	// 创建员工实例
	e := Employee{
		Person:     Person{Name: "张三"},
		Position:   "开发工程师",
		Department: Department{DeptName: "技术部"},
	}

	// 直接访问嵌入字段和方法
	fmt.Printf("员工姓名: %s, 职位: %s, 部门: %s\n", e.Name, e.Position, e.DeptName)

	// 方法被自动提升
	fmt.Println(e.Greet())

	// 创建狗实例并调用
	dog := Dog{
		Animal: Animal{Name: "小黑", Kind: "狗"},
	}
	dog.Bark()
}