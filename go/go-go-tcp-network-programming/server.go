package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
)

// 主函数：启动TCP服务器
func main() {
	// 监听本地8080端口的TCP连接
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("无法启动服务器: %v", err)
	}
	defer listener.Close()

	fmt.Println("服务器启动，监听 :8080...")

	// 循环接受客户端连接
	for {
		conn, err := listener.Accept()
		if err != nil {
			// 非严重错误才记录，避免关闭时打印
			if netErr, ok := err.(net.Error); ok && netErr.Temporary() {
				log.Printf("临时错误: %v", err)
				continue
			}
			break
		}

		// 使用Goroutine并发处理每个连接
		go handleConnection(conn)
	}
}

// 处理单个客户端连接
func handleConnection(conn net.Conn) {
	// 自动关闭连接
	defer conn.Close()

	// 获取客户端地址用于日志
	clientAddr := conn.RemoteAddr().String()
	fmt.Printf("客户端 %s 已连接\n", clientAddr)

	// 向客户端发送欢迎消息
	_, err := io.WriteString(conn, "Hello from server!\n")
	if err != nil {
		log.Printf("发送数据失败: %v", err)
		return
	}
	fmt.Println("向客户端发送响应")

	// 可选：读取客户端发来的消息（此处只读一行）
	message, err := bufio.NewReader(conn).ReadString('\n')
	if err == nil {
		fmt.Printf("来自客户端的消息: %s", message)
	} else if err != io.EOF {
		log.Printf("读取消息失败: %v", err)
	}
}