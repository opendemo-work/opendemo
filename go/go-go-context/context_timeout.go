package main

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

// exampleWithTimeout 展示如何使用 context.WithTimeout 防止 HTTP 请求无限等待
func exampleWithTimeout() {
	// 设置最大等待时间为 2 秒
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel() // 必须调用以释放资源

	// 创建带 context 的请求
	req, err := http.NewRequestWithContext(ctx, "GET", "https://httpbin.org/delay/5", nil)
	if err != nil {
		fmt.Printf("创建请求失败: %v\n", err)
		return
	}

	// 发起请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		// 超时会返回 context.DeadlineExceeded 错误
		fmt.Printf("请求因超时被取消: %v\n", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("请求成功，状态码: %s\n", resp.Status)
}