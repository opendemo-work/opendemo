package main

import "fmt"

// sliceExample 演示Go切片的核心特性
// 切片是对数组的抽象，提供动态大小的序列视图
func sliceExample() {
	// 使用字面量创建一个字符串切片
	// 切片语法：[]T{...}，长度由初始化元素数量决定
	s := []string{"a", "b", "c"}
	fmt.Println("\n=== 切片示例 ===")
	fmt.Printf("原始切片: %v\n", s)

	// 使用 append 函数添加新元素
	// 如果底层数组容量不足，Go会自动分配更大的数组
	s = append(s, "d")
	fmt.Printf("追加元素后: %v\n", s)

	// 创建子切片：包含前两个元素
	// 注意：通常 sub := s[0:2] 会共享底层数组
	// 但为了演示清晰，我们使用 make 创建独立副本
	sub1 := make([]string, 2) // 分配新的底层数组
	copy(sub1, s[0:2])         // 复制前两个元素

	fmt.Printf("子切片 sub1 (前两元素): %v\n", sub1)

	// 修改 sub1 的第一个元素
	sub1[0] = "x"
	fmt.Printf("sub1 修改第一个元素为 'x'\n")
	fmt.Printf("现在 sub1: %v，原始切片仍为: %v\n", sub1, s)
	fmt.Println("因为 sub1 是通过 make 独立创建的")
}