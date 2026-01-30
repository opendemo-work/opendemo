package main

import "fmt"

// HTTP状态码枚举
// 演示如何从特定值开始并跳过某些值

type HTTPStatus int

const (
	HTTPStatusOK = iota + 200 // 从200开始计数
	_                           // 跳过201，但我们显式定义下一个
	HTTPStatusCreated           // 201
	HTTPStatusAccepted          // 202
	HTTPStatusNoContent         // 204
)

// 为HTTPStatus类型实现String方法
func (h HTTPStatus) String() string {
	switch h {
	case HTTPStatusOK:
		return "OK"
	case HTTPStatusCreated:
		return "Created"
	case HTTPStatusAccepted:
		return "Accepted"
	case HTTPStatusNoContent:
		return "No Content"
	default:
		return "Unknown"
	}
}

func main() {
	status := HTTPStatusOK
	
	fmt.Printf("HTTP状态码：%d\n", status)
	fmt.Printf("状态文本：%s\n", status)
}