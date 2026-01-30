package main

func main() {
	// 使用结构体字面量创建Person实例
	person := Person{
		Name: "张三",
		Age:  25,
	}

	// 调用Person的方法
	person.Greet()
	person.Work()

	// 创建Employee实例，组合了Person
	employee := Employee{
		Person: Person{
			Name: "李四",
			Age:  30,
		},
		Position: "开发工程师",
	}

	// Employee可以直接调用Person的方法
	employee.Display()
	employee.Work() // 直接调用嵌入的Person.Work()
}