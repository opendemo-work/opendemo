package main

import "fmt"

// main 展示map的基础操作：创建、赋值、查询、修改、删除、遍历
func main() {
	fmt.Println("--- 基础Map操作 ---")

	// 使用 make 创建一个空的 string->int 映射
	ages := make(map[string]int)

	// 添加元素
	ages["小明"] = 25
	ages["李华"] = 20
	ages["王五"] = 30

	// 查询元素 - 安全方式：返回值和是否存在标志
	if age, exists := ages["小明"]; exists {
		fmt.Printf("小明的年龄是: %d\n", age)
	}

	// 查询不存在的键
	if age, exists := ages["张三"]; exists {
		fmt.Printf("张三的年龄是: %d\n", age)
	} else {
		fmt.Println("张三不存在")
	}

	// 修改已存在元素
	ages["李华"] = 22
	fmt.Printf("更新后李华的年龄: %d\n", ages["李华"])

	// 删除元素
	delete(ages, "王五")
	fmt.Printf("删除王五后，map大小: %d\n", len(ages))

	// 遍历map
	// 注意：map遍历顺序是随机的
	fmt.Print("当前所有人员：")
	for name, age := range ages {
		fmt.Printf("%s(%d) ", name, age)
	}
	fmt.Println()

	// 调用其他示例
	userCacheExample()
	charCountExample()
}