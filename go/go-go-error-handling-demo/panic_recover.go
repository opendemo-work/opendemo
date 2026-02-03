package main

import (
	"fmt"
)

// riskyOperation 模拟一个可能 panic 的操作
func riskyOperation() {
	defer func() {
		// defer 中使用 recover 捕获 panic
		if r := recover(); r != nil {
			fmt.Printf("Panic 被 recover：%v\n", r)
		}
	}()

	// 故意触发 panic
	panic("发生严重错误")
}

func runPanicRecoverExample() {
	riskyOperation()
	fmt.Println("程序继续执行...")
}