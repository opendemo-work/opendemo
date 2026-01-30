package main

import (
	"strings"
	"testing"
)

// BenchmarkConcatWithPlus 测试使用 + 操作符进行多次字符串拼接的性能
// 该方法因字符串不可变性，每次拼接都会分配新内存，效率较低
func BenchmarkConcatWithPlus(b *testing.B) {
	const part = "hello world "
	// 重置计时器前可执行必要的初始化（此处无）
	b.ResetTimer() // 确保只测量循环内的逻辑

	for i := 0; i < b.N; i++ {
		var s string
		for j := 0; j < 10; j++ {
			s += part // 每次都创建新的字符串对象
		}
		// 防止编译器优化掉无用变量
		if len(s) == 0 {
			b.Fatal("unexpected empty string")
		}
	}
}

// BenchmarkConcatWithBuilder 测试使用 strings.Builder 进行字符串拼接的性能
// Builder 通过内部字节切片缓冲数据，最后统一构建字符串，大幅减少内存分配
func BenchmarkConcatWithBuilder(b *testing.B) {
	const part = "hello world "
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		var builder strings.Builder
		// 预分配足够容量，进一步提升性能
		builder.Grow(len(part) * 10)

		for j := 0; j < 10; j++ {
			builder.WriteString(part)
		}

		// 最终生成字符串
		s := builder.String()
		if len(s) == 0 {
			b.Fatal("unexpected empty string")
		}
	}
}