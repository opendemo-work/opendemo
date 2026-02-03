package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// JSON数据结构用于POST请求
type PostData struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

func main() {
	fmt.Println("=== 基础GET请求 ===")
	basicGetRequest()

	fmt.Println("\n=== POST请求（带JSON）===")
	postJSONRequest()

	fmt.Println("\n=== 带超时的GET请求 ===")
	timeoutRequest()
}

// basicGetRequest 演示最简单的GET请求
func basicGetRequest() {
	// 使用http.Get快速发起请求
	response, err := http.Get("https://httpbin.org/get")
	if err != nil {
		fmt.Printf("请求失败: %v\n", err)
		return
	}
	// 必须关闭响应体以释放资源
	defer response.Body.Close()

	// 读取响应体
	body, err := io.ReadAll(response.Body)
	if err != nil {
		fmt.Printf("读取响应失败: %v\n", err)
		return
	}

	fmt.Printf("响应状态: %s\n", response.Status)
	fmt.Printf("响应长度: %d\n", len(body))
}

// postJSONRequest 演示发送JSON格式的POST请求
func postJSONRequest() {
	// 构造要发送的数据
	data := PostData{
		Name:  "张三",
		Email: "zhangsan@example.com",
	}

	// 将数据编码为JSON
	jsonData, err := json.Marshal(data)
	if err != nil {
		fmt.Printf("JSON编码失败: %v\n", err)
		return
	}

	// 创建请求
	req, err := http.NewRequest(
		http.MethodPost,
		"https://httpbin.org/post",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		fmt.Printf("创建请求失败: %v\n", err)
		return
	}

	// 设置请求头
	req.Header.Set("Content-Type", "application/json")

	// 创建客户端并发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("请求失败: %v\n", err)
		return
	}
	defer resp.Body.Close() // 及时释放资源

	// 读取响应
	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("响应状态: %s\n", resp.Status)
	fmt.Printf("响应体: %s\n", string(body))
}

// timeoutRequest 演示使用超时控制的HTTP客户端
func timeoutRequest() {
	// 创建带超时的客户端
	client := &http.Client{
		Timeout: 10 * time.Second, // 整个请求最多耗时10秒
	}

	start := time.Now()
	resp, err := client.Get("https://httpbin.org/delay/1")
	if err != nil {
		fmt.Printf("请求失败: %v\n", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("响应状态: %s\n", resp.Status)
	fmt.Printf("请求耗时: %v\n", time.Since(start).Truncate(time.Millisecond))
}