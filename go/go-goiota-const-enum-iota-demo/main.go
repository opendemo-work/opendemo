package main

import "fmt"

// 定义一个基础的枚举类型，使用iota自增
const (
	// _ = iota // 可用于跳过初始值
	Unknown = iota // Unknown = 0
	Pending        // Pending = 1
	Running        // Running = 2
	Finished       // Finished = 3
)

func main() {
	// 输出基础状态值
	fmt.Printf("状态值: %d\n", Pending)

	// 调用status.go中定义的方法
	status := Status(Pending)
	fmt.Printf("当前状态: %s\n", status.String())

	// 使用权限枚举
	perm := Read | Execute
	fmt.Printf("用户权限: %d (%s)\n", perm, perm)
}