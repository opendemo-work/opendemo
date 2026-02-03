# Go中间件模式HTTP服务器示例

## 简介
本项目演示了如何在Go语言中使用中间件模式构建灵活、可扩展的HTTP服务器。通过组合多个中间件，我们可以实现日志记录、身份验证、请求超时等功能，而无需耦合到具体处理逻辑中。

## 学习目标
- 理解Go中HTTP中间件的基本概念和实现方式
- 掌握函数式中间件的设计与链式调用
- 学会构建可复用的中间件组件
- 实践Go web服务的最佳实践

## 环境要求
- Go 1.19 或更高版本
- 操作系统：Windows / Linux / macOS（跨平台兼容）

## 安装依赖的详细步骤
1. 确保已安装Go环境：
   ```bash
   go version
   # 预期输出：go version go1.19.x 或更高
   ```

2. 初始化Go模块（如果尚未初始化）：
   ```bash
   go mod init middleware-demo
   ```

3. 下载依赖（本项目无外部依赖，仅使用标准库）：
   ```bash
   go mod tidy
   ```

## 文件说明
- `main.go`：主服务器入口，包含路由和中间件链配置
- `middleware/logger.go`：日志记录中间件，打印请求信息
- `middleware/auth.go`：模拟身份验证中间件

## 逐步实操指南

### 步骤1：创建项目目录结构
```bash
mkdir -p middleware-demo/{middleware}
cd middleware-demo
```

### 步骤2：复制代码文件
将提供的 `main.go` 和 `middleware/*.go` 文件复制到对应路径。

### 步骤3：运行程序
```bash
go run main.go
```

### 步骤4：测试接口
打开新终端窗口，执行以下命令：

```bash
# 测试普通请求（带认证头）
curl -H "Authorization: Bearer token123" http://localhost:8080/

# 预期输出：Hello, World!

# 查看控制台日志输出，应包含请求方法、路径、状态码等信息
```

## 代码解析

### `middleware/logger.go`
```go
func LoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("[INFO] %s %s", r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}
```
- 包装下一个处理器，记录进入时间与请求信息
- 调用 `next.ServeHTTP` 继续处理链

### `middleware/auth.go`
```go
func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Authorization") == "" {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}
```
- 检查请求头是否包含 Authorization
- 若缺失则返回401，否则放行

### `main.go`
```go
handler := middleware.LoggingMiddleware(
	middleware.AuthMiddleware(http.HandlerFunc(homeHandler)),
)
```
- 中间件以嵌套方式组合，执行顺序为外层到内层
- 最终由 homeHandler 处理业务逻辑

## 预期输出示例
```bash
2025/04/05 10:00:00 [INFO] GET /
```
同时curl返回：
```text
Hello, World!
```

## 常见问题解答

**Q: 为什么中间件要返回 `http.Handler`？**
A: 因为Go的net/http包基于`http.Handler`接口设计，中间件接收并包装该接口，实现职责链模式。

**Q: 中间件的执行顺序是什么？**
A: 从最外层向最内层执行。例如 `A(B(C))`，执行顺序是 A → B → C，响应时倒序返回。

**Q: 如何添加更多中间件？**
A: 编写新的中间件函数并嵌套调用，或使用第三方库如`alice`简化链式调用。

## 扩展学习建议
- 尝试实现超时中间件（使用 context.WithTimeout）
- 添加 CORS 支持中间件
- 使用 Gorilla Mux 或 Gin 框架集成中间件
- 实现中间件注册管理器，支持命名与启用控制