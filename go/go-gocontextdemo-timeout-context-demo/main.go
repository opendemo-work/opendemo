package main

import (
	"context"
	"fmt"
	"time"
)

// simulateRequest 模拟一个可能耗时的外部请求
func simulateRequest(ctx context.Context) (string, error) {
	// 使用select监听context是否被取消
	select {
	case <-time.After(3 * time.Second): // 模拟长时间操作
		return "数据获取完成", nil
	case <-ctx.Done():
		// 当context超时或被取消时，返回对应的错误
		return "", ctx.Err()
	}
}

func main() {
	// 创建一个带有2秒超时的context
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel() // 确保释放资源

	result, err := simulateRequest(ctx)
	if err != nil {
		fmt.Printf("错误: %v\n", err)
		return
	}
	fmt.Printf("请求成功: %s\n", result)
}