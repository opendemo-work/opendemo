# WebSocket实时通信 Gorilla

## 简介
本Demo演示如何使用Go语言和Gorilla WebSocket库构建一个简单的实时双向通信服务。包含一个WebSocket服务器和一个模拟客户端，展示消息的实时发送与广播。

## 学习目标
- 理解WebSocket的基本工作原理
- 掌握Gorilla WebSocket库的核心API用法
- 实现一个可运行的WebSocket服务端与客户端通信示例
- 学会处理连接、消息读写和广播机制

## 环境要求
- Go 1.19 或更高版本（跨平台支持：Windows/Linux/macOS）

## 安装依赖的详细步骤
1. 打开终端或命令行工具
2. 进入项目目录：`cd websocket-demo`
3. 初始化Go模块：`go mod init websocket-demo`
4. 添加Gorilla WebSocket依赖：`go get github.com/gorilla/websocket@v1.5.0`

## 文件说明
- `main.go`：WebSocket服务器，处理客户端连接和消息广播
- `client.go`：模拟WebSocket客户端，用于测试连接和收发消息
- `go.mod`：Go模块依赖声明文件

## 逐步实操指南

### 步骤1：创建项目目录并初始化
```bash
mkdir websocket-demo && cd websocket-demo
go mod init websocket-demo
```

### 步骤2：创建并保存代码文件
将以下内容分别保存为 `main.go` 和 `client.go`

### 步骤3：下载依赖
```bash
go get github.com/gorilla/websocket@v1.5.0
```

### 步骤4：启动服务器
```bash
go run main.go
```
**预期输出**：
```
WebSocket服务器已启动，监听 :8080...
```

### 步骤5：启动客户端（另开终端）
```bash
go run client.go
```
**预期输出**：
```
已连接到服务器
收到消息: 广播: Hello from server!
```

## 代码解析

### main.go 关键代码段
```go
upgrader.CheckOrigin = func(r *http.Request) bool { return true }
```
允许所有来源连接（仅用于开发）。

```go
conn, err := upgrader.Upgrade(w, r, nil)
```
将HTTP连接升级为WebSocket连接。

```go
clients[conn] = true
broadcast <- message
```
注册新连接并将消息推送到广播通道。

### client.go 关键代码段
```go
c, _, err := websocket.DefaultDialer.Dial("ws://localhost:8080/ws", nil)
```
连接到本地WebSocket服务器。

```go
c.WriteMessage(websocket.TextMessage, []byte("Hello from client"))
```
向服务器发送文本消息。

## 预期输出示例
**服务器端**：
```
WebSocket服务器已启动，监听 :8080...
新客户端连接
收到消息: Hello from client
```

**客户端**：
```
已连接到服务器
收到消息: 广播: Hello from client
```

## 常见问题解答

**Q1：连接被拒绝？**
A：确保服务器已启动且端口8080未被占用。

**Q2：出现'bad request'错误？**
A：检查请求路径是否为 `/ws`，且使用`ws://`协议。

**Q3：如何在生产环境使用？**
A：移除`CheckOrigin`的宽松设置，添加身份验证和TLS支持。

## 扩展学习建议
- 添加JWT身份验证
- 使用TLS启用`wss://`安全连接
- 实现私聊功能而非广播
- 集成前端HTML页面进行真实浏览器测试
- 使用Redis扩展多实例间的广播能力