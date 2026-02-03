package main

import (
	"math"
	"time"
)

// RetryWithExponentialBackoff 封装通用的指数退避重试逻辑
// maxRetries: 最大重试次数
// initialDelay: 初始延迟时间
// operation: 要执行的操作函数
func RetryWithExponentialBackoff(maxRetries int, initialDelay time.Duration, operation func() error) error {
	var err error

	for i := 0; i <= maxRetries; i++ {
		// 执行操作
		err = operation()
		if err == nil {
			return nil // 成功则退出
		}

		// 如果达到最大重试次数，则不再重试
		if i == maxRetries {
			break
		}

		// 计算指数退避延迟：delay = initialDelay * 2^attempt
		delay := time.Duration(float64(initialDelay) * math.Pow(2, float64(i)))

		// 可选：限制最大延迟时间，例如不超过8秒
		maxDelay := 8 * time.Second
		if delay > maxDelay {
			delay = maxDelay
		}

		// 执行退避
		time.Sleep(delay)
	}

	return fmt.Errorf("重试失败超过最大次数(%d): %w", maxRetries, err)
}