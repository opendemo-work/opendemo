package main

import "fmt"

func main() {
	// 示例1：使用 switch 判断季节（基于月份）
	month := 3
	var season string
	switch month {
	case 3, 4, 5:
		season = "春季"
	case 6, 7, 8:
		season = "夏季"
	case 9, 10, 11:
		season = "秋季"
	case 12, 1, 2:
		season = "冬季"
	default:
		season = "无效月份"
	}
	fmt.Printf("月份: %d 对应季节是%s\n", month, season)

	// 示例2：使用 switch 进行值匹配（如颜色分类）
	color := "blue"
	switch color {
	case "red", "blue", "yellow":
		fmt.Printf("颜色 '%s' 是原色之一\n", color)
	case "green", "orange", "purple":
		fmt.Printf("颜色 '%s' 是间色\n", color)
	default:
		fmt.Printf("颜色 '%s' 未分类\n", color)
	}

	// 示例3：使用 type switch 判断接口类型
	var any interface{} = "hello world"
	switch v := any.(type) {
	case string:
		fmt.Println("x的类型是字符串")
	case int:
		fmt.Println("x的类型是整数")
	case bool:
		fmt.Println("x的类型是布尔值")
	default:
		fmt.Println("未知类型")
	}
}