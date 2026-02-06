package main

import "fmt"

// Employee 表示员工，通过组合Person扩展功能
type Employee struct {
	Person  // 匿名嵌入Person，自动获得其字段和方法
	Position string // 职位
}

// Display 显示员工完整信息
func (e Employee) Display() {
	fmt.Printf("员工: %s, 职位: %s, 年龄: %d\n", e.Name, e.Position, e.Age)
}