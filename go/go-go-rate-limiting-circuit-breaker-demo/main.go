package main

import (
	"fmt"
	"time"

	"golang.org/x/time/rate"
)

// 演示基于令牌桶的限流器
func main() {
	// 创建一个限流器：每秒生成2个令牌，桶大小为3
	limiter := rate.NewLimiter(2, 3)

	// 模拟5个请求
	for i := 1; i <= 5; i++ {
		// Allow 方法返回是否允许该请求
		if limiter.Allow() {
			fmt.Printf("请求通过: %d\n", i)
		} else {
			fmt.Printf("请求被限流: %d\n", i)
		}
		time.Sleep(200 * time.Millisecond) // 模拟请求间隔
	}
}