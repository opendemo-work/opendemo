# Prompt 02: 代码生成 + Server 实现

生成 Go 代码：运行 protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative user.proto

然后初始化 go.mod（module grpc-demo），添加 gRPC 和 protobuf 依赖。

接着实现 server.go：
- 监听 TCP :50051
- 实现 UserServiceServer，GetUser 返回硬编码用户 {Id: req.Id, Name: "Alice", Email: "alice@example.com"}
- 嵌入 UnimplementedUserServiceServer 确保向后兼容
- 注册服务并启动

---
## 背景
- 工具：Claude Code
- 阶段：第 2-3 轮
- 结果：protoc 插件需要手动安装到 PATH，之后正确生成
