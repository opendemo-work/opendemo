package main

import (
	"fmt"
	"io"
	"net/http"
)

// MakeRequest 封装通用的HTTP请求函数
// 参数: 方法, URL, 可选的BodyReader
// 返回: 响应体字符串, 状态码, 错误
func MakeRequest(method, url string, body io.Reader) (string, int, error) {
	// 创建请求
	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return "", 0, fmt.Errorf("创建请求失败: %w", err)
	}

	// 可在此处统一添加认证头等
	// req.Header.Set("Authorization", "Bearer xxx")

	// 创建客户端
	client := &http.Client{}

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		return "", 0, fmt.Errorf("发送请求失败: %w", err)
	}
	// 确保关闭响应体
	defer func() {
		_ = resp.Body.Close() // 错误忽略，但生产环境应记录日志
	}()

	// 读取响应体
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", 0, fmt.Errorf("读取响应失败: %w", err)
	}

	return string(respBody), resp.StatusCode, nil
}

// GetJSON 封装常用的JSON GET请求
func GetJSON(url string) (string, error) {
	result, statusCode, err := MakeRequest(http.MethodGet, url, nil)
	if err != nil {
		return "", err
	}
	if statusCode != http.StatusOK {
		return "", fmt.Errorf("HTTP错误: 状态码 %d", statusCode)
	}
	return result, nil
}