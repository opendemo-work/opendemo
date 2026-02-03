package main

import (
	"fmt"
	"time"
)

// main 函数是程序入口点
// 演示缓存预热的过程：在系统启动时预先加载常用数据到缓存中
func main() {
	// 创建缓存管理器实例
	cache := NewCacheManager()

	// 执行缓存预热
	preloadCache(cache)

	// 模拟运行时查询
	value, exists := cache.Get("user_1")
	fmt.Printf("[查询] 从缓存获取 user_1: %s, 存在: %v\n", value, exists)

	value, exists = cache.Get("user_3")
	fmt.Printf("[查询] 从缓存获取 user_3: %s, 存在: %v\n", value, exists)

	// 等待清理goroutine执行一次
	time.Sleep(11 * time.Second)
}