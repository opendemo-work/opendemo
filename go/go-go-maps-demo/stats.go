package main

import "fmt"

// countChars 统计字符串中每个字符出现的次数
// 使用map[rune]int作为计数器，rune支持Unicode字符
func countChars(s string) map[rune]int {
	// 初始化一个空map用于存储字符计数
	counts := make(map[rune]int)

	// 遍历字符串中的每一个字符（rune）
	for _, char := range s {
		// 如果键不存在，Go会自动赋予零值0，因此可以直接递增
		counts[char]++
	}

	return counts
}

// charCountExample 演示map作为计数器的使用场景
func charCountExample() {
	fmt.Println("\n--- 字符统计示例 ---")

	text := "aaabbc"
	result := countChars(text)

	// 注意：由于map遍历无序，输出顺序可能不同
	fmt.Printf("字符统计结果: %v\n", result)
}