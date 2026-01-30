package main

import "fmt"

// modifyArray 演示数组作为参数是值传递
func modifyArray(arr [3]int) {
	arr[0] = 100 // 修改的是副本
	fmt.Printf("修改后的副本: %v\n", arr)
}

func main() {
	// 声明并初始化一个长度为3的整型数组
	var nums [3]int
	nums[0] = 10
	nums[1] = 20
	nums[2] = 30

	fmt.Printf("原始数组: %v\n", nums)

	// 传递数组给函数
	modifyArray(nums)

	// 原数组未受影响
	fmt.Printf("原数组未变: %v\n", nums)

	// 输出数组的长度和容量（数组两者相等）
	fmt.Printf("数组长度: %d, 容量: %d\n", len(nums), cap(nums))
}