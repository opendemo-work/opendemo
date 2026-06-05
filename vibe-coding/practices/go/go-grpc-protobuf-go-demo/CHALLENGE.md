# 挑战：Go gRPC + Protobuf

## 难度：advanced | 预计用时：40 分钟 | 推荐工具：Claude Code / Cursor

## 目标

构建一个 gRPC 微服务，实现用户查询功能：

1. 定义 `.proto` 文件 — UserService 服务 + GetUser RPC 方法
2. 生成 Go 代码 — `user.pb.go` + `user_grpc.pb.go`
3. 实现 Server — 监听 50051 端口，根据 ID 返回用户信息
4. 实现 Client — 连接 server，查询 ID=1 的用户并打印结果

## 约束

- Go 1.19+，gRPC v1.59.0，Protobuf v1.31.0
- Proto 文件：`package proto`，消息字段包括 `id(int32)`、`name(string)`、`email(string)`
- Server 的 `GetUser` 方法：接收 ID，返回硬编码的用户信息（name: "Alice", email: "alice@example.com"）
- Client 使用 `insecure.NewCredentials()`（开发环境）
- 代码注释使用中文

## 环境准备（Vibe Coding 时可以跳过，让 AI 帮你做）

```bash
# 安装 protoc 编译器
# 安装 Go 插件
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.31.0
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2.0
```

## 验证

```bash
# 生成代码
protoc --go_out=. --go_opt=paths=source_relative \
       --go-grpc_out=. --go-grpc_opt=paths=source_relative \
       user.proto

# 终端 1：启动 server
go run server.go
# 输出：gRPC server running on port :50051

# 终端 2：运行 client
go run client.go
# 输出：Received: id:1 name:"Alice" email:"alice@example.com"
```

## 提示（卡住时再看）

<details>
<summary>提示 1：Proto 文件结构</summary>

需要定义 `service UserService`、`message GetUserRequest`（含 int32 id）、`message User`（含 id、name、email）。

</details>

<details>
<summary>提示 2：Server 实现</summary>

结构体嵌入 `pb.UnimplementedUserServiceServer`，实现 `GetUser` 方法。使用 `grpc.NewServer()` 创建服务器并注册。

</details>

<details>
<summary>提示 3：常见坑 — protoc 路径</summary>

如果 import 路径不对，在 proto 文件中使用 `option go_package = "grpc-demo/proto";` 指定输出包路径。

</details>

<details>
<summary>提示 4：关键 Prompt（分步）</summary>

第一步："创建 user.proto 文件，定义 UserService 服务和 GetUser 方法，请求包含 int32 id，响应包含 id、name、email"

第二步："基于 proto 生成 Go 代码后，实现 gRPC server 监听 :50051，GetUser 方法返回 ID 对应的硬编码用户"

第三步："实现 gRPC client，连接 localhost:50051，调用 GetUser 查询 ID=1 的用户"

</details>

## 对应原 Demo

完成后对比参考实现：`go/go-grpc-protobuf-go-demo/`
