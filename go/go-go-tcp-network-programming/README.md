# Go TCP网络编程示例

## 简介
本项目是一个简单的Go语言TCP服务器与客户端通信演示，展示了如何使用标准库 `net` 构建并发TCP服务，并实现基本的消息收发功能。

## 学习目标
- 理解Go中基于`net`包的TCP编程模型
- 掌握TCP服务器的监听、接受连接和并发处理机制
- 实现TCP客户端连接、发送消息与接收响应
- 理解Goroutine在并发网络编程中的应用

## 环境要求
- Go 1.19 或更高版本（稳定版）
- 支持命令行操作的系统（Windows / Linux / macOS）

## 安装依赖
此项目仅使用Go标准库，无需额外安装依赖。只需确保已正确安装Go环境：

```bash
# 检查Go版本
go version
# 预期输出：go version go1.19+ ...
```

## 文件说明
- `server.go`：TCP服务器，监听端口并处理多个客户端连接
- `client.go`：TCP客户端，连接服务器并发送消息

## 逐步实操指南

### 步骤1：打开终端，进入项目目录
```bash
cd path/to/your/project
```

### 步骤2：启动TCP服务器
在第一个终端窗口运行：
```bash
go run server.go
```

**预期输出**：
```
服务器启动，监听 :8080...
```

### 步骤3：启动TCP客户端
在第二个终端窗口运行：
```bash
go run client.go
```

**预期输出（客户端）**：
```
已连接到服务器
收到: Hello from server!
```

**服务器输出变化**：
```
客户端 127.0.0.1:xxxx 已连接
向客户端发送响应
```

## 代码解析

### server.go 关键代码段
```go
listener, err := net.Listen("tcp", ":8080")
```
- 使用 `net.Listen` 在本地8080端口启动TCP监听

```go
go handleConnection(conn)
```
- 使用 `go` 关键字启动新Goroutine处理每个连接，实现并发

```go
io.WriteString(conn, "Hello from server!\n")
```
- 向客户端发送字符串响应

### client.go 关键代码段
```go
conn, err := net.Dial("tcp", "localhost:8080")
```
- 连接到本地8080端口的TCP服务器

```go
fmt.Fscanln(os.Stdin, &input)
```
- （可选扩展）读取用户输入发送给服务器

## 预期输出示例
**服务器端**：
```
服务器启动，监听 :8080...
客户端 127.0.0.1:54321 已连接
向客户端发送响应
```

**客户端**：
```
已连接到服务器
收到: Hello from server!
```

## 常见问题解答

**Q: 提示端口被占用？**
A: 更换端口号，如改为 ":9000"，需同步修改客户端连接地址。

**Q: 运行报错 'command not found: go'？**
A: 需先安装Go环境，访问 https://golang.org/dl/ 下载并配置PATH。

**Q: 客户端无法连接？**
A: 确保服务器已启动；检查防火墙设置；确认使用同一网络接口（localhost）。

## 扩展学习建议
- 添加JSON消息编解码支持
- 实现聊天室多客户端广播功能
- 使用TLS加密通信（`crypto/tls`）
- 引入超时控制与连接池管理
- 结合WebSocket进行对比学习