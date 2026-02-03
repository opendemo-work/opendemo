package main

import (
	"context"
	"fmt"
	"math"
	"time"
)

// MakeHttpRequestWithRetry 模拟带指数退避的HTTP请求重试
func MakeHttpRequestWithRetry(maxRetries int) (string, error) {
	var lastErr error

	for i := 0; i <= maxRetries; i++ {
		fmt.Printf("模拟HTTP请求 - 尝试第%d次...\n", i+1)

		// 创建带超时的上下文，防止请求无限等待
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		// 模拟网络请求
		result, err := doHttpRequest(ctx, i)
		if err == nil {
			return result, nil
		}

		lastErr = err

		// 如果是最后一次尝试，则不再重试
		if i == maxRetries {
			break
		}

		// 计算指数退避延迟时间（最多8秒）
		delaySeconds := math.Min(math.Pow(2, float64(i+1)), 8)
		delay := time.Duration(delaySeconds) * time.Second

		fmt.Printf("请求失败: %v，%v后重试...\n", err, delay)
		time.Sleep(delay)
	}

	return "", fmt.Errorf("所有重试均失败: %w", lastErr)
}

// doHttpRequest 模拟实际的HTTP请求行为
func doHttpRequest(ctx context.Context, attempt int) (string, error) {
	// 模拟网络延迟
	time.Sleep(100 * time.Millisecond)

	// 使用尝试次数代替随机，保证可预测性：前两次失败，第三次成功
	if attempt < 2 {
		select {
		case <-time.After(1 * time.Second):
			return "", fmt.Errorf("连接超时")
		case <-ctx.Done():
			return "", ctx.Err()
		}
	}

	// 成功情况
	return "模拟HTTP请求 - 尝试第" + fmt.Sprintf("%d", attempt+1) + "次: 成功响应", nil
}