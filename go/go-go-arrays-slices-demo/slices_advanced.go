package main

import "fmt"

// demonstrateSliceSharing 演示切片的共享底层数组行为及扩容机制
func main() {
	// 创建一个字符串切片
	original := []string{"a", "b", "c", "d"}
	fmt.Printf("原始切片: %v\n", original)

	// 创建子切片，共享底层数组
	sub1 := original[1:3] // ["b", "c"]
	fmt.Printf("子切片 sub1: %v, 长度: %d, 容量: %d\n", sub1, len(sub1), cap(sub1))

	// 向 sub1 追加元素，直到触发扩容
	// 初始容量为3（从index1到末尾共3个位置），已有2个元素，最多可容纳1个而不扩容
	sub1 = append(sub1, "e") // 容量够，直接追加
	sub1 = append(sub1, "f") // 超出容量，触发扩容（通常加倍）

	fmt.Printf("sub1追加后: %v, 长度: %d, 容量: %d\n", sub1, len(sub1), cap(sub1))

	// 检查原切片是否受影响
	// 由于扩容导致底层数组被复制，original不再受影响
	fmt.Printf("注意：原切片仍为: %v（已发生复制）\n", original)

	// 验证 sub1 是否与 original 共享内存（扩容前会共享，扩容后不会）
	// 打印地址可进一步验证（此处省略）
}
