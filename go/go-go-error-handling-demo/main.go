package main

import (
	"fmt"
)

// divide 是一个简单的除法函数，演示基本错误返回
func divide(a, b float64) (float64, error) {
	// 检查除数是否为零
	if b == 0 {
		return 0, fmt.Errorf("不能除以零")
	}
	return a / b, nil // 成功时返回结果和 nil 错误
}

func main() {
	// 示例1: 正常情况
	result, err := divide(5, 2)
	if err != nil {
		fmt.Printf("错误：%s\n", err)
	} else {
		fmt.Printf("除法运算成功: 5 / 2 = %.1f\n", result)
	}

	// 示例2: 错误情况
	result, err = divide(5, 0)
	if err != nil {
		fmt.Printf("错误：%s\n", err)
	} else {
		fmt.Printf("除法运算成功: %.1f\n", result)
	}

	// 继续执行其他函数
	runCustomErrorExample()
	runPanicRecoverExample()
}