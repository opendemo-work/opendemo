package main

import "fmt"

// main 函数演示LRU缓存的基本使用场景
// 创建容量为3的缓存，依次插入A、B、C
// 访问B和A使其变为最近使用
// 插入D导致最久未使用的A被淘汰
// 最后验证各键的存在性
func main() {
	// 创建容量为3的LRU缓存
	cache := Constructor(3)

	fmt.Println("Put: A=1")
	cache.Put("A", 1)

	fmt.Println("Put: B=2")
	cache.Put("B", 2)

	fmt.Println("Put: C=3")
	cache.Put("C", 3)

	// 访问B和A，使其成为最近使用
	if val, ok := cache.Get("B"); ok {
		fmt.Printf("Get B: %d, %t\n", val, ok)
	}

	if val, ok := cache.Get("A"); ok {
		fmt.Printf("Get A: %d, %t\n", val, ok)
	}

	// 插入D，由于缓存已满且A是最久未使用，A将被移除
	fmt.Println("Put D=4 （触发A被移除）")
	cache.Put("D", 4)

	// 验证A已被淘汰，其他元素仍存在
	if val, ok := cache.Get("A"); !ok {
		fmt.Printf("Get A: %d, %t\n", val, ok) // 应该返回false
	}

	if val, ok := cache.Get("B"); ok {
		fmt.Printf("Get B: %d, %t\n", val, ok)
	}

	if val, ok := cache.Get("C"); ok {
		fmt.Printf("Get C: %d, %t\n", val, ok)
	}

	if val, ok := cache.Get("D"); ok {
		fmt.Printf("Get D: %d, %t\n", val, ok)
	}
}