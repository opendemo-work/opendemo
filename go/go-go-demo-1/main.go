package main

import (
	"fmt"
	"reflect"
)

// Person 示例结构体，用于演示反射操作
type Person struct {
	Name string // 可导出字段，可通过反射修改
	age  int   // 不可导出字段，反射无法修改
}

func main() {
	// 创建Person实例
	p := Person{Name: "Alice", age: 30}
	fmt.Printf("原始Name: %s\n", p.Name)

	// 获取结构体的反射Value，注意传入指针并调用Elem()
	v := reflect.ValueOf(&p).Elem()

	// 通过字段名获取Name字段的Value
	nameField := v.FieldByName("Name")
	if nameField.IsValid() {
		fmt.Printf("通过反射读取Name: %s\n", nameField.String())
	}

	// 修改Name字段值
	if nameField.CanSet() {
		nameField.SetString("Bob")
		fmt.Printf("修改后Name: %s\n", p.Name) // 输出 Bob
	} else {
		fmt.Println("Name字段不可设置")
	}

	// 尝试访问不可导出字段age
	ageField := v.FieldByName("age")
	if ageField.IsValid() {
		fmt.Printf("age字段存在，值为: %d\n", ageField.Int())
		// 但无法设置
		if !ageField.CanSet() {
			fmt.Println("age字段不可设置（未导出）")
		}
	}
}