package main

import (
	"fmt"
	"math"
	"time"
)

// main 函数演示基础的指数退避重试机制
func main() {
	fmt.Println("开始演示指数退避重试...")

	// 示例1：基本操作重试
	err := RetryWithExponentialBackoff(5, 2*time.Second, func() error {
		return simulateFlakyOperation()
	})
	if err != nil {
		fmt.Printf("最终失败: %v\n", err)
	} else {
		fmt.Println("操作最终成功！")
	}

	// 示例2：模拟HTTP请求重试
	response, err := MakeHttpRequestWithRetry(3)
	if err != nil {
		fmt.Printf("HTTP请求最终失败: %v\n", err)
	} else {
		fmt.Println(response)
	}
}

// simulateFlakyOperation 模拟一个不稳定的操作，有一定概率失败
func simulateFlakyOperation() error {
	staticCounter := 0 // 实际项目中应使用更健壮的状态管理
	staticCounter++

	if staticCounter < 3 { // 前两次失败，第三次成功
		fmt.Printf("尝试第%d次: 操作失败，将在%.0f秒后重试...\n", 
			staticCounter, 
			math.Pow(2, float64(staticCounter)))
		return fmt.Errorf("临时错误")
	}
	fmt.Printf("尝试第%d次: 操作成功！\n", staticCounter)
	return nil
}