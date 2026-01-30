package main

import "fmt"

// gradeDemo 函数演示 switch 语句的使用
// 功能：根据分数返回对应的等级描述
func gradeDemo() {
	score := 85 // 测试分数

	// 使用 switch 语句进行多分支判断
	// 注意：Go的switch不需要break，自动防止穿透
	// 当没有表达式时，switch true 可用于复杂条件匹配
	switch {
	case score >= 90:
		fmt.Printf("%d 分的等级是：优秀\n", score)
	case score >= 80:
		fmt.Printf("%d 分的等级是：良好\n", score)
	case score >= 70:
		fmt.Printf("%d 分的等级是：中等\n", score)
	case score >= 60:
		fmt.Printf("%d 分的等级是：及格\n", score)
	default:
		fmt.Printf("%d 分的等级是：不及格\n", score)
	}

	// 输出空行分隔
	fmt.Println()
}

// 注意：由于多个文件都有 main 函数，我们将此函数显式调用
func init() {
	gradeDemo()
}