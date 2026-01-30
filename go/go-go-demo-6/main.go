package main

import "fmt"

// main 函数演示 if-else 控制结构
// 功能：判断一个整数是奇数还是偶数
func main() {
	// 定义一个测试数字
	num := 7

	// 使用 if-else 进行条件判断
	// % 是取模运算符，num % 2 == 0 表示能被2整除
	if num%2 == 0 {
		fmt.Printf("%d 是偶数\n", num)
	} else {
		fmt.Printf("%d 是奇数\n", num)
	}

	// 输出空行以便区分不同demo输出
	fmt.Println()
}