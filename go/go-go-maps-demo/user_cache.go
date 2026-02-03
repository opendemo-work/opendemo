package main

import "fmt"

// UserCache 模拟一个简单的用户信息缓存结构
type UserCache struct {
	data map[string]string // key: 用户ID, value: 用户名
}

// NewUserCache 创建一个新的用户缓存实例
func NewUserCache() *UserCache {
	return &UserCache{
		data: make(map[string]string),
	}
}

// Get 获取用户名称，返回值和是否命中的标志
func (uc *UserCache) Get(userID string) (string, bool) {
	name, exists := uc.data[userID]
	return name, exists
}

// Set 设置用户名称到缓存
func (uc *UserCache) Set(userID, name string) {
	uc.data[userID] = name
}

// Size 返回缓存中条目数量
func (uc *UserCache) Size() int {
	return len(uc.data)
}

// userCacheExample 演示如何使用map实现简单缓存
func userCacheExample() {
	fmt.Println("\n--- 用户缓存示例 ---")

	cache := NewUserCache()
	cache.Set("user1", "Alice")
	cache.Set("user2", "Bob")

	// 模拟缓存命中
	if name, ok := cache.Get("user1"); ok {
		fmt.Printf("命中缓存: user1 -> %s\n", name)
	}

	// 模拟缓存未命中
	if name, ok := cache.Get("user3"); ok {
		fmt.Printf("命中缓存: user3 -> %s\n", name)
	} else {
		fmt.Println("未命中缓存: user3")
	}

	fmt.Printf("缓存大小: %d\n", cache.Size())
}