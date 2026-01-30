package main

import "fmt"

// Employee 表示员工信息的结构体
type Employee struct {
	Name   string
	Dept   string
	Salary float64
}

func main() {
	// 使用员工 ID 作为键，Employee 结构体作为值
	employees := map[int]Employee{
		1: {Name: "张三", Dept: "技术部", Salary: 15000},
		2: {Name: "李四", Dept: "销售部", Salary: 12000},
	}

	// 打印原始员工列表
	fmt.Println("员工列表：")
	printEmployees(employees)

	// 修改李四的工资
	if emp, exists := employees[2]; exists {
		emp.Salary = 13000
		employees[2] = emp // 更新 map 中的值
		fmt.Println("李四的工资已调整为 13000")
	}

	// 打印调整后的员工列表
	fmt.Println("调整后员工列表：")
	printEmployees(employees)
}

// printEmployees 遍历并打印所有员工信息
func printEmployees(emps map[int]Employee) {
	for id, emp := range emps {
		fmt.Printf("ID: %d, 姓名: %s, 部门: %s, 工资: %.2f\n", id, emp.Name, emp.Dept, emp.Salary)
	}
}