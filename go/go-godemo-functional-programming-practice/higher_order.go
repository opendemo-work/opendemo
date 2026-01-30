package main

import (
	"fmt"
	"strings"
)

// mapInts 是一个高阶函数，接受一个整数切片和一个函数
// 对每个元素应用该函数并返回新切片
func mapInts(nums []int, f func(int) int) []int {
	result := make([]int, len(nums))
	for i, v := range nums {
		result[i] = f(v)
	}
	return result
}

// filterInts 是另一个高阶函数，根据谓词函数筛选元素
func filterInts(nums []int, pred func(int) bool) []int {
	var result []int
	for _, v := range nums {
		if pred(v) {
			result = append(result, v)
		}
	}
	return result
}

func main() {
	numbers := []int{1, 2, 3, 4, 5}
	fmt.Printf("原始数字: %v\n", numbers)

	// 使用匿名函数计算平方
	squares := mapInts(numbers, func(x int) int {
		return x * x
	})
	fmt.Printf("平方后: %v\n", squares)

	// 筛选偶数
	evens := filterInts(numbers, func(x int) bool {
		return x%2 == 0
	})
	fmt.Printf("偶数筛选: %v\n", evens)

	// 字符串操作示例
	words := []string{"hello", "world", "go", "code"}
	
	// 计算每个单词长度
	lengths := mapInts([]int{len(words[0]), len(words[1]), len(words[2]), len(words[3])}, func(x int) int {
		return x
	})
	fmt.Printf("字符串长度: %v\n", lengths)

	// 转换为大写（使用strings.ToUpper）
	upperWords := make([]string, len(words))
	for i, word := range words {
		upperWords[i] = strings.ToUpper(word)
	}
	fmt.Printf("大写转换: %v\n", upperWords)
}