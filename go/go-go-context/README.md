# Go Context 实践演示

## 简介
本项目是一个简洁的 Go 语言演示程序，展示了 `context` 包在实际开发中的三种典型应用场景：
- 使用 `context.WithTimeout` 实现 HTTP 请求超时控制
- 使用 `context.WithCancel` 手动取消长时间运行的 goroutine
- 在函数调用链中传递 context 以实现统一的取消机制

通过本 demo，您将深入理解 context 如何帮助我们构建健壮、可取消且响应迅速的并发程序。

## 学习目标
- 掌握 context 的基本结构与生命周期管理
- 学会使用超时和手动取消来控制 goroutine
- 理解 context 在多层函数调用中传递的重要性
- 避免 goroutine 泄露的最佳实践

## 环境要求
- Go 1.19 或更高版本（推荐 1.20+）
- 操作系统：Windows、Linux、macOS 均支持
- 网络连接（用于测试 HTTP 超时场景）

## 安装依赖
该项目仅使用 Go 标准库，无需额外安装依赖。

```bash
# 确保已安装 Go 并配置好环境变量
go version
# 输出应类似：go version go1.21.0 linux/amd64
```

## 文件说明
- `main.go` - 主程序入口，包含三个独立示例
- `context_cancel.go` - 展示 WithCancel 的使用
- `context_timeout.go` - 展示 WithTimeout 的使用

## 逐步实操指南

### 步骤 1：创建项目目录
```bash
mkdir go-context-demo && cd go-context-demo
```

### 步骤 2：复制代码文件
将以下三个文件内容分别保存到对应路径：
- `main.go`
- `context_cancel.go`
- `context_timeout.go`

### 步骤 3：初始化模块
```bash
go mod init context-demo
```

### 步骤 4：运行程序
```bash
go run .
```

### 预期输出示例
```
【示例1】开始执行带取消的 goroutine...
工作正在进行中...
收到取消信号，安全退出。
【示例1】goroutine 已成功取消。

【示例2】发起一个最多等待2秒的HTTP请求...
请求因超时被取消: Get \"https://httpbin.org/delay/5\": context deadline exceeded
【示例2】HTTP请求超时处理完成。
```

## 代码解析

### `context.WithCancel`
```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel() // 确保释放资源
```
- 创建可取消的上下文，调用 `cancel()` 可通知所有监听者停止工作
- `defer cancel()` 是最佳实践，防止 goroutine 泄露

### `context.WithTimeout`
```go
ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
defer cancel()
```
- 设置自动超时，时间一到自动触发取消
- 常用于网络请求、数据库查询等可能阻塞的操作

### 在调用链中传递 ctx
所有下游函数都接收 `ctx context.Context` 参数，持续监听取消信号

## 常见问题解答

**Q: 为什么必须调用 `cancel()`？**
A: 即使不主动调用，GC 最终也会回收，但显式调用能立即释放资源，避免潜在的内存或 goroutine 泄露。

**Q: context 能携带数据吗？**
A: 可以，使用 `context.WithValue()`，但建议只传请求域的元数据（如用户ID），不要用于传递可选参数。

**Q: 超时不等于错误吗？**
A: 是的。超时是控制流的一部分，应作为正常逻辑处理，而非异常。

## 扩展学习建议
- 阅读官方博客《Go Concurrency Patterns: Context》
- 学习 gRPC 和 net/http 如何集成 context
- 尝试使用 `context.WithDeadline` 控制定时任务
- 实践中间件中 context 的传递（如 Gin/Echo 框架）