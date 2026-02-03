package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/redis/go-redis/v9"
)

// User 表示用户结构体
type User struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
	Age  int    `json:"age"`
}

// 示例：缓存结构化用户数据
func main() {
	// 复用main.go中的Redis客户端初始化逻辑
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		password: "${GENERIC_PASSWORD}",
		DB:       0,
	})

	ctx := context.Background()

	// 测试连接
	_, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("❌ 无法连接到Redis: %v", err)
	}

	// 创建一个用户对象
	user := User{ID: 1001, Name: "Alice", Age: 30}

	// 将用户序列化为JSON并缓存
	userData, err := json.Marshal(user)
	if err != nil {
		log.Fatalf("❌ 序列化用户失败: %v", err)
	}

	// 使用 SET 命令存储整个用户对象
	_, err = rdb.Set(ctx, "user:1001", userData, 10*time.Second).Result()
	if err != nil {
		log.Fatalf("❌ 缓存用户失败: %v", err)
	}
	fmt.Println("✅ 用户信息已缓存: user:1001")

	// 从Redis读取并反序列化
	val, err := rdb.Get(ctx, "user:1001").Result()
	if err != nil {
		log.Fatalf("❌ 读取用户缓存失败: %v", err)
	}

	var cachedUser User
	err = json.Unmarshal([]byte(val), &cachedUser)
	if err != nil {
		log.Fatalf("❌ 反序列化失败: %v", err)
	}
	fmt.Printf("👤 从缓存读取用户: %+v\n", cachedUser)

	// 使用哈希类型缓存用户字段
	hashKey := "user:profile:1001"
	_, err = rdb.HSet(ctx, hashKey, "name", "Alice", "age", 30).Result()
	if err != nil {
		log.Fatalf("❌ HSet缓存失败: %v", err)
	}
	fmt.Println("✅ 使用HSet缓存用户字段: user:profile:1001")

	// 使用HGetAll读取所有字段
	result, err := rdb.HGetAll(ctx, hashKey).Result()
	if err != nil {
		log.Fatalf("❌ HGetAll失败: %v", err)
	}
	fmt.Printf("📊 HGetAll 获取用户资料: %v\n", result)
}