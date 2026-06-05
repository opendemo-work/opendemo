# 解决过程：Go gRPC + Protobuf

## 使用的工具：Claude Code（终端模式）

---

### 第 1 轮：Proto 文件

**Prompt：**
> 创建 user.proto 文件，定义：
> - package proto
> - service UserService { rpc GetUser(GetUserRequest) returns(User) }
> - message GetUserRequest { int32 id = 1 }
> - message User { int32 id = 1; string name = 2; string email = 3 }

**AI 生成：** 正确的 proto 文件。

---

### 第 2 轮：代码生成 + go.mod

**Prompt：**
> 生成 Go 代码：运行 protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative user.proto
>
> 然后初始化 go.mod（module grpc-demo），添加 gRPC 和 protobuf 依赖。

**问题：** protoc 命令报错 "protoc-gen-go: program not found"

**修复：**
```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.31.0
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2.0
export PATH=$PATH:$(go env GOPATH)/bin
```

重新运行 protoc 成功，生成了 `user.pb.go` 和 `user_grpc.pb.go`。

**学习点：** protoc 插件必须安装并在 PATH 中。这是 gRPC 开发最常见的环境问题。

---

### 第 3 轮：Server 实现

**Prompt：**
> 实现 server.go：
> - 监听 TCP :50051
> - 实现 UserServiceServer，GetUser 返回硬编码用户 {Id: req.Id, Name: "Alice", Email: "alice@example.com"}
> - 嵌入 UnimplementedUserServiceServer 确保向后兼容
> - 注册服务并启动

**AI 生成：** 正确实现。

---

### 第 4 轮：Client 实现

**Prompt：**
> 实现 client.go：
> - 用 grpc.Dial 连接 localhost:50051（insecure credentials）
> - 创建 UserServiceClient
> - 调用 GetUser({Id: 1})
> - 打印响应

**AI 生成：** 正确，但用了已废弃的 `grpc.Dial`。

**修复：** "把 grpc.Dial 改为 grpc.NewClient" — 但由于新 API 变化较大，保持 `grpc.Dial` 也可接受（gRPC 文档中仍在使用）。

---

### 第 5 轮：验证

```bash
# 终端 1
go run server.go
# gRPC server running on port :50051

# 终端 2
go run client.go
# Received: id:1 name:"Alice" email:"alice@example.com"
```

**结果：** 全部通过 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 5 轮 |
| 实际用时 | ~25 分钟 |
| AI 犯错次数 | 0（环境问题不算 AI 错误） |
| 人工干预 | 安装 protoc 插件 |

### 关键技巧
- **gRPC 必须分步**：proto → 代码生成 → server → client，不能跳步
- **环境准备是最大障碍** — protoc + 插件安装占了一半时间
- **UnimplementedUserServiceServer** — 必须嵌入，否则编译不通过

### 常见坑
- `protoc-gen-go` 不在 PATH 中 — 报错 "program not found"
- import 路径不匹配 — proto 文件需要 `option go_package` 或正确设置 paths
- `+incompatible` 版本 — 某些 gRPC 依赖需要手动处理版本兼容
- Server 必须嵌入 `Unimplemented*` 结构体 — 这是 gRPC 向后兼容的强制要求
