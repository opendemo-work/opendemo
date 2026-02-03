package main

import "fmt"

// runForDemo 演示 for 循环的三种常见形式
func runForDemo() {
	fmt.Println("--- for 循环示例 ---")

	// 示例4: 经典 for 循环 (init; condition; post)
	for i := 0; i < 5; i++ {
		fmt.Printf("计数: %d\n", i)
	}

	// 示例5: 类似 while 的 for 循环
	n := 1
	for n <= 3 {
		fmt.Printf("while风格循环: %d\n", n)
		n++
	}

	// 示例6: for-range 遍历 slice
	fruits := []string{"apple", "banana", "cherry"}
	for _, fruit := range fruits {
		fmt.Printf("列表中的元素: %s\n", fruit)
	}
	fmt.Println()
}