package main

import (
	"context"
	"log"
	"net"

	pb "grpc-demo/proto" // 替换为你的模块路径

	"google.golang.org/grpc"
)

// userServiceServer 实现了 UserServiceServer 接口
type userServiceServer struct {
	pb.UnimplementedUserServiceServer // 嵌入未实现结构体，确保向后兼容
}

// GetUser 实现远程调用方法：根据ID返回用户信息
func (s *userServiceServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
	log.Printf("Received request for user ID: %d", req.Id)

	// 模拟数据库查找逻辑
	user := &pb.User{
		Id:    req.Id,
		Name:  "Alice",
		Email: "alice@example.com",
	}

	return user, nil
}

func main() {
	// 创建监听器，在50051端口监听TCP连接
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	// 创建一个新的gRPC服务器实例
	server := grpc.NewServer()

	// 注册我们的服务实现
	pb.RegisterUserServiceServer(server, &userServiceServer{})

	log.Println("gRPC server running on port :50051")

	// 启动服务器并阻塞等待连接
	if err := server.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}