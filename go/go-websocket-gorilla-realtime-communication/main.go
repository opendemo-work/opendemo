package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

// 升级器配置，将HTTP连接升级为WebSocket
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		// 允许所有CORS请求，生产环境应限制具体来源
		return true
	},
}

// 存储所有活跃的WebSocket连接
var clients = make(map[*websocket.Conn]bool)

// 广播通道，用于向所有客户端发送消息
var broadcast = make(chan []byte)

func main() {
	// 设置WebSocket路由
	http.HandleFunc("/ws", handleConnections)

	// 启动广播监听器
	go handleMessages()

	// 启动HTTP服务器
	log.Println("WebSocket服务器已启动，监听 :8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// 处理新的WebSocket连接
func handleConnections(w http.ResponseWriter, r *http.Request) {
	// 将HTTP连接升级为WebSocket
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("连接升级失败: %v", err)
		return
	}
	// 确保函数退出时关闭连接
	defer conn.Close()

	// 将新连接加入客户端列表
	clients[conn] = true
	log.Println("新客户端连接")

	// 持续读取消息
	for {
		_, message, err := conn.ReadMessage()
		if err != nil {
			log.Printf("读取消息错误: %v", err)
			delete(clients, conn)
			break
		}
		log.Printf("收到消息: %s", message)
		// 将消息发送到广播通道
		broadcast <- message
	}
}

// 处理广播消息
func handleMessages() {
	for {
		// 从通道接收消息
		message := <-broadcast
		// 遍历所有客户端并发送消息
		for client := range clients {
			err := client.WriteMessage(websocket.TextMessage, append([]byte("广播: "), message...))
			if err != nil {
				log.Printf("发送消息失败: %v", err)
				client.Close()
				delete(clients, client)
			}
		}
	}
}