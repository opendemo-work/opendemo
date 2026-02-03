package main

import "fmt"

// 演示数组的值类型特性和固定长度
func main() {
	fmt.Println("=== 数组示例 ===")

	// 声明并初始化一个长度为3的整型数组
	var arr [3]int = [3]int{10, 20, 30}
	fmt.Printf("原始数组: %v\n", arr)

	// 调用函数尝试修改数组
	modifyArray(arr)

	// 输出原数组，验证是否被修改
	fmt.Printf("函数调用后原数组: %v （数组是值类型，拷贝传递）\n", arr)
}

// modifyArray 接收一个数组副本，修改不影响原始数组
// 参数是 [3]int 类型，表示固定长度为3的数组
func modifyArray(arr [3]int) {
	arr[0] = 100 // 只修改副本
	fmt.Printf("函数内修改后: %v\n", arr)
}