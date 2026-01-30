package main

import "fmt"

// demonstrateSlice 展示切片的强大功能和引用特性
// 切片是对数组的动态引用，支持自动扩容
func demonstrateSlice() {
	// 使用字面量创建字符串切片
	slice := []string{"a", "b", "c"}
	fmt.Println("=== 切片演示 ===")
	fmt.Printf("初始切片: %v\n", slice)

	// append 添加元素，切片可动态增长
	slice = append(slice, "d")
	fmt.Printf("追加元素后: %v\n", slice)

	// 创建子切片 [1:3)，左闭右开区间
	sub := slice[1:3]
	fmt.Printf("子切片 [1:3]: %v\n", sub)

	// 修改子切片会影响原切片（共享底层数组）
	sub[0] = "x"
	sub[1] = "y"
	fmt.Printf("修改子切片影响原切片: %v\n", slice)

	// 查看当前长度和容量
	fmt.Printf("切片容量变化: len=%d, cap=%d\n", len(slice), cap(slice))

	// 继续添加元素直到触发扩容
	oldCap := cap(slice)
	slice = append(slice, "e")
	newCap := cap(slice)
	fmt.Printf("扩容后的切片: %v, cap=%d\n", slice, newCap)
	if newCap > oldCap {
		fmt.Println("注意：append 导致底层数组重新分配")
	}
}