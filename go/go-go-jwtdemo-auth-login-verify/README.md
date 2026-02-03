# Go-JWT认证用户登录验证Demo

## 简介
本项目是一个使用Go语言实现的JWT（JSON Web Token）用户登录与认证的完整可运行示例。通过 Gin Web 框架和 jwt-go 库，展示如何安全地处理用户登录、生成 JWT Token，并保护受限制的API接口。

## 学习目标
- 理解JWT的基本原理与结构
- 掌握在Go中使用Gin框架实现用户认证流程
- 学会生成和验证JWT Token
- 实践中间件在权限控制中的应用

## 环境要求
- Go 1.18 或更高版本
- 支持终端操作（Windows/Linux/Mac均可）

## 安装依赖的详细步骤
1. 打开终端或命令行工具
2. 进入项目根目录
3. 执行以下命令安装所需依赖：

```bash
go mod init jwt-auth-demo
```

此命令将根据项目中的 import 自动创建 go.mod 文件并下载依赖。

## 文件说明
- `main.go`：主程序入口，包含路由设置、用户登录处理和受保护接口
- `middleware.go`：JWT认证中间件，用于验证请求中的Token
- `README.md`：本说明文档

## 逐步实操指南

### 步骤1：创建项目目录并进入
```bash
mkdir jwt-auth-demo && cd jwt-auth-demo
```

### 步骤2：初始化Go模块
```bash
go mod init jwt-auth-demo
```

### 步骤3：复制代码文件
将以下两个文件内容分别保存为 `main.go` 和 `middleware.go`

### 步骤4：运行程序
```bash
go run main.go middleware.go
```

预期输出：
```
[GIN-debug] POST   /login                    --> main.loginHandler (3 handlers)
[GIN-debug] GET    /protected                --> main.protectedHandler (3 handlers)
[GIN-debug] Listening and serving HTTP on :8080
```

### 步骤5：测试登录接口（使用curl）
```bash
curl -X POST http://localhost:8080/login -H "Content-Type: application/json" -d '{"username":"admin","password: "${GENERIC_PASSWORD}"}'
```

预期输出（Token会不同）：
```json
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjMwNDM1MjAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}
```

### 步骤6：访问受保护接口
```bash
curl -X GET http://localhost:8080/protected -H "Authorization: Bearer <your_token>"
```
替换 `<your_token>` 为上一步返回的 token。

预期输出：
```json
{"message":"Hello admin, this is a protected route"}
```

## 代码解析

### `main.go`
- 定义了简单的用户结构体和登录处理函数
- 使用 `jwt-go` 创建带有用户名和过期时间的 Token
- `/login` 接口验证固定账号密码并返回 Token
- `/protected` 接口由 JWT 中间件保护

### `middleware.go`
- `authMiddleware` 函数从请求头提取 `Authorization: Bearer <token>`
- 使用预定义密钥解析并验证 Token 的有效性
- 验证成功则放行，失败返回 401 错误

## 预期输出示例
启动服务后，按上述步骤操作，最终应能成功获取 Token 并访问受保护资源。

## 常见问题解答

**Q1: 启动时报错找不到 gin 包？**
A: 确保已执行 `go mod init` 并检查网络是否正常。可尝试 `go get -u github.com/gin-gonic/gin`

**Q2: 访问 /protected 返回 401？**
A: 检查是否正确设置了 Authorization 头，且 Token 未过期（有效期为24小时）

**Q3: 可以用其他密钥吗？**
A: 可以，修改 `jwtKey` 变量即可，但需保证签发和验证使用相同密钥

## 扩展学习建议
- 将用户信息存储到数据库（如MySQL或MongoDB）
- 添加刷新Token机制
- 使用更安全的哈希算法存储密码（如bcrypt）
- 集成Swagger文档展示API