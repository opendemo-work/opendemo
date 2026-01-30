package main

// ApplyToEach 接收一个整数切片和一个函数f，将f应用于每个元素
// 这是高阶函数的典型示例：函数作为参数
func ApplyToEach(nums []int, f func(int) int) []int {
	result := make([]int, len(nums))
	for i, n := range nums {
		result[i] = f(n)
	}
	return result
}

// Filter 根据条件函数筛选出满足条件的元素
// 展示了如何将函数用于逻辑抽象
func Filter(nums []int, predicate func(int) bool) []int {
	var result []int
	for _, n := range nums {
		if predicate(n) {
			result = append(result, n)
		}
	}
	return result
}

// Counter 返回一个闭包函数，每次调用时递增内部计数器
// 演示了闭包如何捕获并保持外部作用域的状态
func Counter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}
