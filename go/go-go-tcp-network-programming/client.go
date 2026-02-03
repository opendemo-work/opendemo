package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
	"os"
)

// 主函数：启动TCP客户端
func main() {
	// 连接到本地运行的TCP服务器
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		log.Fatalf("无法连接到服务器: %v", err)
	}
	defer conn.Close()

	fmt.Println("已连接到服务器")

	// 读取服务器发来的消息
	response, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil && err != io.EOF {
		log.Printf("读取响应失败: %v", err)
	} else {
		fmt.Printf("收到: %s", response)
	}

	// 可选：向服务器发送一条消息
	_, err = io.WriteString(conn, "Hello Server!\n")
	if err != nil {
		log.Printf("发送消息失败: %v", err)
	}

	// 等待用户输入任意键退出（防止立即断开）
	fmt.Println("按回车键断开连接...")
	bufio.NewReader(os.Stdin).ReadString('\n')
}