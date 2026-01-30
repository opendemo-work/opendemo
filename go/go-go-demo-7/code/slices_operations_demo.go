package main

import "fmt"

func main() {
	// 使用字面量创建字符串切片
	slice := []string{"a", "b", "c"}
	fmt.Printf("初始切片: %v\n", slice)

	// 使用 append 添加元素，切片可动态增长
	slice = append(slice, "d")
	slice = append(slice, "e") // 多次 append 演示动态性
	fmt.Printf("追加后: %v\n", slice)

	// 创建子切片 [1:3)，注意左闭右开
	subSlice := slice[1:3]
	fmt.Printf("子切片 s[1:3]: %v\n", subSlice)

	// 修改子切片，由于共享底层数组，原切片也会被修改
	for i := range subSlice {
		subSlice[i] = "999"
	}
	fmt.Println("修改子切片影响原切片")
	fmt.Printf("原切片 now: %v\n", slice)

	// 正确复制切片以避免相互影响
	copied := make([]string, len(slice))
	copy(copied, slice)

	// 修改 copied 不影响原 slice
	copied[0] = "x"
	copied[1] = "y"
	copied[2] = "z"

	fmt.Println("复制切片后的独立操作")
	fmt.Printf("原切片 after copy: %v, 复制切片: %v\n", slice, copied)
}