# Go HTTP RESTful API 开发演示

## 简介
本项目是一个使用Go语言编写的简单RESTful API服务器示例，使用标准库和流行的`gorilla/mux`路由器。它实现了对用户资源的增删改查（CRUD）操作，返回JSON格式数据，适合学习Web服务开发基础。

## 学习目标
- 掌握Go中构建HTTP服务器的基本方法
- 理解RESTful API设计原则
- 学会使用gorilla/mux进行路由管理
- 实现JSON请求/响应处理
- 了解结构体与HTTP处理函数的结合使用

## 环境要求
- Go 编程语言：版本 1.19 或更高
- 操作系统：Windows、Linux、macOS 均支持
- 终端工具（如：命令提示符、PowerShell、Terminal）

## 安装依赖步骤
1. 确保已安装Go环境：
   ```bash
   go version
   ```
   预期输出：`go version go1.xx.x os/arch`

2. 初始化Go模块（在项目根目录执行）：
   ```bash
   go mod init rest-api-demo
   ```

3. 添加 gorilla/mux 依赖：
   ```bash
   go get github.com/gorilla/mux
   ```

## 文件说明
- `main.go`：主程序文件，包含HTTP服务器启动、路由配置和API处理逻辑
- `go.mod`：Go模块依赖声明文件（由`go mod init`生成）

## 逐步实操指南

### 步骤1：创建项目目录并进入
```bash
mkdir rest-api-demo && cd rest-api-demo
```

### 步骤2：初始化模块并获取依赖
```bash
go mod init rest-api-demo
go get github.com/gorilla/mux
```

### 步骤3：创建 main.go 并粘贴代码
将 `main.go` 中的代码复制到当前目录下的 `main.go` 文件中。

### 步骤4：运行服务器
```bash
go run main.go
```

预期输出：
```
Server is running on port 8080...
```

### 步骤5：测试API（使用curl或Postman）
- 获取所有用户：
  ```bash
  curl http://localhost:8080/api/users
  ```
  输出：`[{"id":"1","name":"Alice","email":"alice@example.com"}]`

- 获取单个用户：
  ```bash
  curl http://localhost:8080/api/users/1
  ```

- 创建新用户：
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"name":"Bob","email":"bob@example.com"}' http://localhost:8080/api/users
  ```

## 代码解析

### 路由设置
```go
r := mux.NewRouter()
r.HandleFunc("/api/users", GetUsers).Methods("GET")
r.HandleFunc("/api/users/{id}", GetUser).Methods("GET")
r.HandleFunc("/api/users", CreateUser).Methods("POST")
```
使用 `gorilla/mux` 创建严格匹配HTTP方法的路由。

### 结构体定义
```go
type User struct {
    ID    string `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}
```
使用结构体标签控制JSON序列化字段名。

### JSON响应处理
```go
json.NewEncoder(w).Encode(users)
```
标准库编码器自动将Go结构体转换为JSON并写入响应。

## 预期输出示例
启动服务后访问 `http://localhost:8080/api/users` 应返回：
```json
[
    {
        "id": "1",
        "name": "Alice",
        "email": "alice@example.com"
    }
]
```

## 常见问题解答

**Q1: 提示找不到 mux 包？**
A: 请确认是否执行了 `go get github.com/gorilla/mux`，并检查 `go.mod` 是否包含该依赖。

**Q2: 端口被占用怎么办？**
A: 修改 `main.go` 中的监听端口，例如改为 `:9090`。

**Q3: 如何添加PUT或DELETE方法？**
A: 参照现有模式添加 `HandleFunc` 并实现对应处理函数即可。

## 扩展学习建议
- 使用数据库（如SQLite、PostgreSQL）替代内存存储
- 添加中间件（日志、认证）
- 引入Swagger文档生成
- 使用Go Modules管理更复杂的依赖
- 尝试使用标准库 `net/http` 实现相同功能以理解底层机制