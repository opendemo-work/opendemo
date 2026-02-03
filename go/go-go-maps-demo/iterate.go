package main

import (
	"fmt"
	"slices"
	"sort"
)

// iterate.go - map遍历与排序输出示例
func main() {
	// 初始化成绩map
	scores := map[string]int{
		"bob":   92,
		"alice": 85,
		"david": 96,
	}

	fmt.Println("原始成绩：")
	// 直接遍历map（顺序不确定）
	for name, score := range scores {
		fmt.Printf("%s: %d\n", name, score)
	}

	// 实现有序输出：先提取所有键，排序后再遍历
	var names []string
	for name := range scores {
		names = append(names, name)
	}

	// 使用sort包对字符串切片排序
	sort.Strings(names) // 或使用 slices.Sort(names)

	fmt.Println("按名字排序输出：")
	for _, name := range names {
		fmt.Printf("%s: %d\n", name, scores[name])
	}
}