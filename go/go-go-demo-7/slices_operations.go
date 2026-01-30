package main

import "fmt"

// 演示切片的动态特性：可扩展、引用传递、截取操作
func main() {
	fmt.Println("=== 切片示例 ===")

	// 使用字面量创建一个字符串切片
	// 切片长度可变，是引用类型
	s := []string{"a", "b", "c"}
	fmt.Printf("初始切片: %v\n", s)

	// 使用 append 函数追加元素
	// append 返回新的切片，可能触发底层数组扩容
	s = append(s, "d")
	fmt.Printf("追加元素后: %v\n", s)

	// 切片截取操作：左闭右开区间 [start:end]
	subset := s[1:3] // 获取索引1到2的元素
	fmt.Printf("切片截取 s[1:3]: %v\n", subset)

	// 使用 range 遍历切片，同时获取索引和值
	fmt.Println("遍历切片:")
	for index, value := range s {
		fmt.Printf("索引 %d -> 值: %s\n", index, value)
	}
}