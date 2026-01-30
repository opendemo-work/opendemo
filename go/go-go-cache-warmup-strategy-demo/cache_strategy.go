package main

import (
	"github.com/patrickmn/go-cache"
	"fmt"
	"time"
)

// CacheManager 封装缓存操作，提供统一接口
// 使用 github.com/patrickmn/go-cache 实现线程安全的内存缓存
type CacheManager struct {
	cache *gocache.Cache
}

// NewCacheManager 创建并初始化一个新的缓存管理器
// 默认条目5分钟后过期，每10分钟执行一次过期清理
func NewCacheManager() *CacheManager {
	c := &CacheManager{
		cache: gocache.New(5*time.Minute, 10*time.Minute),
	}

	// 启动后台清理任务
	go func() {
		for range time.NewTicker(10 * time.Minute).C {
			stats := c.cache.ItemCount()
			fmt.Printf("[后台] 缓存清理完成，剩余条目数: %d\n", stats)
		}
	}()

	return c
}

// Set 向缓存中添加键值对，使用默认过期时间
func (cm *CacheManager) Set(key string, value interface{}) {
	cm.cache.Set(key, value, gocache.DefaultExpiration)
}

// Get 从缓存中获取指定键的值
// 返回值和是否存在标志
func (cm *CacheManager) Get(key string) (interface{}, bool) {
	value, found := cm.cache.Get(key)
	return value, found
}

// preloadCache 模拟应用启动时的缓存预热过程
// 通常从数据库或其他持久化存储中加载热点数据
func preloadCache(c *CacheManager) {
	fmt.Println("[初始化] 正在预热缓存...")
	users := map[string]string{
		"user_1": "Alice",
		"user_2": "Bob",
	}
	for k, v := range users {
		c.Set(k, v)
		fmt.Printf("[缓存预热] 已加载用户: %s -> %s\n", k, v)
	}
}