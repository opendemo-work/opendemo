# Go Context 实践示例

## 简介
本示例展示了 Go 语言中 `context` 包的核心用法，包括请求超时控制、goroutine 取消通知以及上下文数据传递。通过三个独立但递进的场景，帮助开发者掌握如何安全地管理并发操作的生命周期。

## 学习目标
- 理解 `context.Context` 的作用与设计哲学
- 掌握使用 `context.WithTimeout` 实现超时控制
- 学会通过 `context.WithCancel` 主动取消 goroutine
- 了解不推荐的 `context.WithValue` 使用方式及其注意事项
- 遵循 Go 最佳实践编写健壮的并发程序

## 环境要求
- Go 1.19 或更高版本（推荐 1.20+）
- 支持终端命令行的操作系统（Windows / Linux / macOS 均可）

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用 Go 标准库。

1. 确保已安装 Go：
```bash
go version
```
预期输出类似：
```
go version go1.21.0 linux/amd64
```

2. 创建模块目录并初始化：
```bash
git clone https://github.com/example/context-demo.git
cd context-demo
go mod init context-demo
go mod tidy
```

## 文件说明
- `main.go`：主程序入口，包含三个演示函数
- `README.md`：本说明文档

## 逐步实操指南

### 步骤 1: 编写代码
创建 `main.go` 并粘贴提供的代码内容。

### 步骤 2: 运行程序
```bash
go run main.go
```

### 预期输出
```
--- 场景一：超时控制 ---
任务执行中...
任务在 2 秒后被取消（超时）

--- 场景二：手动取消 ---
监控启动，5秒后将被取消...
收到取消信号，停止监控

--- 场景三：上下文传值 ---
处理用户请求：user123
```

## 代码解析

### 场景一：超时控制
```go
ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
defer cancel()
```
创建一个 2 秒后自动触发取消的上下文。即使忘记调用 `cancel()`，资源也会被自动释放。

### 场景二：手动取消
```go
ctx, cancel := context.WithCancel(context.Background())
go func() {
    time.Sleep(5 * time.Second)
    cancel() // 主动触发取消
}()
```
启动一个 goroutine，在 5 秒后调用 `cancel()`，通知所有监听此 ctx 的协程退出。

### 场景三：上下文传值
```go
ctx := context.WithValue(context.Background(), "userID", "user123")
```
将数据注入上下文，供下游函数读取。注意：应仅用于请求范围的元数据，避免滥用。

## 常见问题解答

**Q: 为什么必须调用 `defer cancel()`？**
A: 即使使用 `WithTimeout`，也应调用 `cancel()` 来立即释放资源。否则定时器将持续运行直到超时，造成潜在内存泄漏。

**Q: `context.WithValue` 和全局变量有什么区别？**
A: `WithValue` 是请求级别的临时数据传递机制，具有明确的生命周期；而全局变量是进程级的，容易引发竞态条件和测试困难。

**Q: 能否在多个 goroutine 中共享同一个 context？**
A: 可以且推荐这样做。Context 设计为并发安全，可在多个 goroutine 中安全传递和读取。

## 扩展学习建议
- 阅读官方博客文章 [Go Concurrency Patterns: Context](https://blog.golang.org/context)
- 学习 `net/http` 包如何集成 context 实现请求链路追踪
- 尝试结合 `sync.WaitGroup` 与 `context` 构建更复杂的并发控制逻辑
- 探索开源项目如 Kubernetes 或 etcd 中 context 的高级用法