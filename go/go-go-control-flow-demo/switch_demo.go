package main

import "fmt"

// runSwitchDemo 演示 switch 语句的多种用法
func runSwitchDemo() {
	fmt.Println("--- switch 示例 ---")

	// 示例2: 基于值的 switch 判断
	day := "Monday"
	switch day {
	case "Monday":
		fmt.Println("今天是星期一")
	case "Tuesday":
		fmt.Println("今天是星期二")
	case "Wednesday":
		fmt.Println("今天是星期三")
	default:
		fmt.Println("其他日子")
	}

	// 示例3: 类型 switch，用于接口类型的判断
	var i interface{} = "hello"
	switch v := i.(type) {
	case string:
		fmt.Println("这是字符串类型")
	case int:
		fmt.Println("这是整数类型")
	case bool:
		fmt.Println("这是布尔类型")
	default:
		fmt.Println("未知类型")
	}
	fmt.Println()
}