package main

import (
	"fmt"
	"reflect"
)

// Greeter 结构体包含一个可导出方法，用于反射调用演示
type Greeter struct {
	Name string
}

// Greet 是一个简单的导出方法，将被通过反射调用
func (g Greeter) Greet() {
	fmt.Printf("Hello, I'm %s\n", g.Name)
}

func main() {
	// 创建Greeter实例
	g := Greeter{Name: "Alice"}

	// 获取实例的反射Value
	v := reflect.ValueOf(g)

	// 通过方法名获取方法Value
	method := v.MethodByName("Greet")
	if method.IsValid() {
		fmt.Println("通过反射调用 Greet 方法:")
		// 调用方法，无参数
		method.Call(nil)
	} else {
		fmt.Println("Greet 方法不存在或不可导出")
	}
}