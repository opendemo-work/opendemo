<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# gRPC + Protobuf Go Demo

## 简介
本项目是一个完整的、可运行的Go语言示例，演示了如何使用gRPC框架结合Protocol Buffers（Protobuf）实现高效的远程过程调用（RPC）。包含一个简单的用户信息服务，涵盖定义`.proto`文件、生成Go代码、编写gRPC服务器与客户端的完整流程。

## 学习目标
- 理解gRPC的基本架构和工作原理
- 掌握使用Protobuf定义服务接口和消息结构
- 学会生成并使用gRPC的Go绑定代码
- 实践构建gRPC服务器和客户端通信

## 环境要求
- Go 1.19 或更高版本（支持模块）
- `protoc` 编译器（v3.20+）
- `protoc-gen-go` 和 `protoc-gen-go-grpc` 插件

> 提示：所有命令在 Windows/Linux/Mac 上通用，仅需调整路径分隔符即可。

## 安装依赖步骤

### 1. 安装 Go
确保已安装 Go 并配置好 GOPATH 和 GOBIN。
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
go version
# 预期输出: go version go1.19.x darwin/amd64 (或对应系统)
```

### 2. 安装 protoc 编译器
从 https://github.com/protocolbuffers/protobuf/releases 下载对应平台的 `protoc` 压缩包，并将 `bin/protoc` 加入 PATH。

验证安装：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
protoc --version
# 预期输出: libprotoc 3.20.x
```

### 3. 安装 Go 插件
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.31.0
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2.0
```

确保插件在 $GOBIN 中且在 PATH 内：
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
ls $GOBIN/protoc-gen-go*
# 应看到两个可执行文件
```

## 文件说明
- `user.proto` —— Protobuf 接口定义文件
- `server.go` —— gRPC 服务端实现
- `client.go` —— gRPC 客户端实现

## 逐步实操指南

### 步骤 1: 创建项目目录
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
mkdir grpc-demo && cd grpc-demo
go mod init grpc-demo
```

### 步骤 2: 创建 user.proto
创建文件 `user.proto`，内容如下：
```protobuf
syntax = "proto3";

package proto;

// 用户服务定义
service UserService {
  rpc GetUser (GetUserRequest) returns (User);
}

// 请求消息
message GetUserRequest {
  int32 id = 1;
}

// 用户消息
message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
}
```

### 步骤 3: 生成 Go 代码
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
protoc --go_out=. --go_opt=paths=source_relative \
       --go-grpc_out=. --go-grpc_opt=paths=source_relative \
       user.proto
```

成功后会生成：
- `user.pb.go`
- `user_grpc.pb.go`

### 步骤 4: 编写 server.go
见代码文件。

### 步骤 5: 编写 client.go
见代码文件。

### 步骤 6: 运行服务
打开终端启动服务器：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
go run server.go
# 输出: gRPC server running on port :50051
```

另开终端运行客户端：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
go run client.go
# 预期输出:
# Received: id:1 name:"Alice" email:"alice@example.com"
```

## 代码解析

### server.go 关键点
- 使用 `grpc.NewServer()` 创建gRPC服务器实例
- 注册自定义服务 `UserServiceServer` 实现
- 监听 TCP 端口并启动阻塞服务
- `GetUser` 方法模拟数据库查询返回固定用户

### client.go 关键点
- 使用 `grpc.Dial` 建立到服务器的连接
- 构造客户端桩（stub）`UserServiceClient`
- 调用远程方法如同本地函数调用
- 处理上下文超时以增强健壮性

## 预期输出示例
**服务器端：**
```
gRPC server running on port :50051
Received request for user ID: 1
```

**客户端：**
```
Received: id:1 name:"Alice" email:"alice@example.com"
```

## 常见问题解答

**Q: 报错找不到 protoc-gen-go？**
A: 确保 `$GOBIN` 在系统 PATH 中。可通过 `echo $GOBIN` 查看路径，并添加至环境变量。

**Q: 连接被拒绝？**
A: 检查服务器是否已启动，端口是否冲突，防火墙设置。

**Q: protoc 版本不兼容？**
A: 使用 `protoc --version` 确认版本 ≥ 3.20，否则重新下载安装。

## 扩展学习建议
- 添加 TLS 加密支持
- 使用拦截器实现日志和认证
- 集成 REST 网关（gRPC-Gateway）
- 使用 Etcd 实现服务发现
- 引入 protobuf 的 oneof 和 stream 特性
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
