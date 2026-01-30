package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

// Redis客户端全局变量
var rdb *redis.Client
var ctx = context.Background()

func main() {
	// 初始化Redis客户端
	rdb = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379", // Redis服务器地址
		Password: "",             // 无密码
		DB:       0,              // 使用默认数据库
	})

	// 测试连接
	_, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("❌ 无法连接到Redis: %v", err)
	}
	fmt.Println("🎉 成功连接到Redis!")

	// 1. 设置一个简单的字符串缓存
	setResult, err := rdb.Set(ctx, "welcome", "Hello from Redis!", 0).Result()
	if err != nil {
		log.Fatalf("❌ 设置缓存失败: %v", err)
	}
	fmt.Printf("✅ 设置缓存成功: key=welcome, value=Hello from Redis! (结果: %s)\n", setResult)

	// 2. 获取缓存值
	getValue, err := rdb.Get(ctx, "welcome").Result()
	if err != nil {
		log.Fatalf("❌ 获取缓存失败: %v", err)
	}
	fmt.Printf("✅ 获取缓存成功: %s\n", getValue)

	// 3. 设置带过期时间的键
	expireResult, err := rdb.Set(ctx, "expiring_key", "I will expire!", 3*time.Second).Result()
	if err != nil {
		log.Fatalf("❌ 设置过期缓存失败: %v", err)
	}
	fmt.Printf("✅ 缓存带过期时间设置成功 (结果: %s)\n", expireResult)

	// 等待键过期
	fmt.Println("💤 等待5秒让键过期...")
	time.Sleep(5 * time.Second)

	// 4. 尝试获取已过期的键
	_, err = rdb.Get(ctx, "expiring_key").Result()
	if err == redis.Nil {
		fmt.Println("❌ 键已过期或不存在: key=expiring_key")
	} else if err != nil {
		log.Fatalf("❌ 获取键时出错: %v", err)
	} else {
		fmt.Println("✅ 键仍然存在 - 可能未正确过期")
	}
}