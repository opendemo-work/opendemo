package main

import (
	"log"

	"github.com/gorilla/websocket"
)

func main() {
	// 设置WebSocket连接地址
	url := "ws://localhost:8080/ws"

	// 拨号连接到服务器
	c, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		log.Fatalf("连接失败: %v", err)
	}
	defer c.Close()

	log.Println("已连接到服务器")

	// 发送一条消息到服务器
	message := []byte("Hello from client")
	err = c.WriteMessage(websocket.TextMessage, message)
	if err != nil {
		log.Fatalf("发送消息失败: %v", err)
	}

	// 持续接收来自服务器的消息
	for {
		_, msg, err := c.ReadMessage()
		if err != nil {
			log.Printf("读取消息错误: %v", err)
			break
		}
		log.Printf("收到消息: %s", msg)
	}
}