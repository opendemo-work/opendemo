package main

// 主函数：演示方法接收者的使用差异
func main() {
	// 创建一个Person实例
	person := Person{Name: "Alice"}
	
	fmt.Printf("原始姓名: %s\n", person.Name)
	
	// 调用值接收者方法
	// Go会自动将person复制传入方法
	person.SetValueByValue("Charlie")
	fmt.Printf("调用值接收者方法后: %s\n", person.Name) // 原值不变
	
	// 调用指针接收者方法
	// Go会自动取person的地址传入方法
	person.SetValueByPointer("Bob")
	fmt.Printf("调用指针接收者方法后: %s\n", person.Name) // 原值被修改
	
	// 注意：即使使用指针调用值接收者方法，Go也能正确处理
	// 例如：(&person).SetValueByValue("David") 也是合法的
}