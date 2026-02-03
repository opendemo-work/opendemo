package main

import "fmt"

// 主函数：演示结构体的综合使用
func main() {
	// 创建Person实例
	p := Person{
		Name: "张三",
		Age:  25,
	}

	// 调用结构体方法
	fmt.Printf("姓名: %s, 年龄: %d, 是否成年: %t\n", p.Name, p.Age, p.IsAdult())

	// 使用嵌套结构体
	car := Car{
		Person: p,
		Vehicle: Vehicle{
			Brand: "Tesla",
			Model: "Model 3",
		},
	}
	fmt.Printf("汽车品牌: %s, 型号: %s\n", car.Brand, car.Model)

	// 匿名结构体示例
	anonymousCar := struct {
		Brand string
		Model string
	}{
		Brand: "BMW",
		Model: "X5",
	}
	fmt.Printf("匿名车辆: %s %s\n", anonymousCar.Brand, anonymousCar.Model)
}