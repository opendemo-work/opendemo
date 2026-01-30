package main

import (
	"context"
	"log"

	pb "grpc-demo/proto" // 替换为你的模块路径

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	// 连接到gRPC服务器（忽略TLS用于开发）
	conn, err := grpc.Dial(
		"localhost:50051",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		log.Fatalf("Did not connect: %v", err)
	}
	defer conn.Close()

	// 创建UserService客户端桩（stub）
	client := pb.NewUserServiceClient(conn)

	// 创建请求对象
	request := &pb.GetUserRequest{Id: 1}

	// 发起远程调用，带上下文超时控制（此处使用默认）
	response, err := client.GetUser(context.Background(), request)
	if err != nil {
		log.Fatalf("Error while calling GetUser: %v", err)
	}

	// 输出响应结果
	log.Printf("Received: %v", response)
}