package main

import "strings"

// memoryHog 是一个全局切片，用于累积数据，模拟内存使用增长
var memoryHog []string

// growMemory 模拟内存使用持续增长的场景
// 在实际应用中，这可能由缓存未清理、goroutine泄漏或事件监听器堆积导致
func growMemory() {
	// 每次调用向全局切片添加大量字符串
	for i := 0; i < 10000; i++ {
		// 创建长度为1000的字符串并追加
		memoryHog = append(memoryHog, strings.Repeat("x", 1000))
	}
}

// memoryHandler 提供一个HTTP接口来手动触发内存增长
// 虽然本demo通过goroutine自动调用，但保留接口便于测试
func memoryHandler(w http.ResponseWriter, r *http.Request) {
	growMemory()
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("内存增长已触发，当前元素数量: " + len(memoryHog) + "\n"))
}