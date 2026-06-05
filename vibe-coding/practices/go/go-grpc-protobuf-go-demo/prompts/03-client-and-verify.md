# Prompt 03: Client 实现 + 验证

实现 client.go：
- 用 grpc.Dial 连接 localhost:50051（insecure credentials）
- 创建 UserServiceClient
- 调用 GetUser({Id: 1})
- 打印响应

验证：
终端 1: go run server.go
终端 2: go run client.go
预期输出: Received: id:1 name:"Alice" email:"alice@example.com"

---
## 背景
- 工具：Claude Code
- 阶段：第 4-5 轮
- 结果：全部通过
