package main

import "fmt"

// sum 是一个可变参数函数，可以接收任意数量的int参数
// nums 在函数内部被视为 []int 类型的切片
func sum(nums ...int) int {
	total := 0
	for _, num := range nums {
		total += num
	}
	return total
}

func main() {
	// 调用可变参数函数
	result := sum(1, 2, 3, 4, 5)
	fmt.Printf("累加和: %d\n", result)
}