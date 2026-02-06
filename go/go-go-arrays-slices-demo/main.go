package main

import "fmt"

// main 函数演示数组和切片的基础操作
func main() {
	// 定义一个长度为5的整型数组
	arr := [5]int{1, 2, 3, 4, 5}
	fmt.Printf("数组 arr: %v\n", arr)

	// 从数组创建切片：包含索引1到3的元素（左闭右开）
	s := arr[1:4] // 取出 [2, 3, 4]
	fmt.Printf("切片 s: %v\n", s)

	// 输出切片的长度和容量
	// 长度是当前元素个数，容量是从起始位置到底层数组末尾的可用空间
	fmt.Printf("切片长度: %d, 容量: %d\n", len(s), cap(s))

	// 使用 append 向切片追加元素
	// 如果超出容量，Go会自动分配更大的底层数组
	s = append(s, 6, 7)
	fmt.Printf("追加后的切片: %v\n", s)

	// 注意：此时原数组arr不会被改变，因为append可能导致了新数组分配
	fmt.Printf("原数组仍为: %v（未受影响）\n", arr)
}
