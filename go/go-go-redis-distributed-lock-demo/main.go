package main

import (
	"context"
	"log"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/go-redsync/redsync/v4"
	"github.com/go-redsync/redsync/v4/redis/goredis/v8"
)

// 主函数：演示基础Redis分布式锁用法
func main() {
	// 创建Redis客户端
	client := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379", // 可替换为远程地址
		Password: "",             // 无密码
		DB:       0,
	})

	// 测试连接
	ctx := context.Background()
	if _, err := client.Ping(ctx).Result(); err != nil {
		log.Fatalf("无法连接到Redis: %v", err)
	}
	log.Println("已连接到Redis")

	// 创建Redsync池
	pool := goredis.NewPool(client)
	redsyncClient := redsync.New(pool)

	// 创建指定资源的互斥锁
	mutex := redsyncClient.NewMutex("my-resource-lock")
	mutex.SetExpiry(8 * time.Second)              // 锁最多持有8秒
	mutex.SetRetryDelay(500 * time.Millisecond)  // 重试间隔
	mutex.SetTries(3)                            // 最多重试3次

	log.Println("尝试获取锁...")

	// 获取锁（阻塞直到成功或达到最大重试次数）
	if err := mutex.Lock(); err != nil {
		log.Fatalf("无法获取锁: %v", err)
	}
	log.Println("成功获取锁！")

	// 使用 defer 延迟释放锁
	defer func() {
		if ok, err := mutex.Unlock(); !ok || err != nil {
			log.Printf("警告：锁释放失败，ok=%v, err=%v", ok, err)
		} else {
			log.Println("锁已安全释放。")
		}
	}()

	// 模拟临界区操作
	log.Println("正在执行临界区操作...")
	time.Sleep(2 * time.Second) // 模拟工作耗时
	log.Println("操作完成，释放锁。")
}