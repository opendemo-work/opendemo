# Go Context 实践演示

## 简介
本示例演示了 Go 语言中 `context` 包的核心功能，包括请求超时控制、goroutine 取消传播以及上下文数据传递。通过三个独立但递进的场景，帮助开发者深入理解如何在实际项目中安全高效地使用 context。

## 学习目标
- 理解 context 的作用：控制 goroutine 生命周期
- 掌握使用 `context.WithTimeout` 实现超时控制
- 学会使用 `context.WithCancel` 主动取消操作
- 了解何时以及如何在上下文中传递数据（避免滥用）
- 遵循最佳实践编写可维护的并发程序

## 环境要求
- Go 1.16 或更高版本（推荐 1.20+）
- 操作系统：Windows、Linux、macOS 均支持
- 终端工具（如 bash、PowerShell 或 CMD）

## 安装依赖的详细步骤
本项目无外部依赖，仅使用 Go 标准库。

1. 确保已安装 Go：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.5 linux/amd64
   ```

2. 创建模块目录并初始化：
   ```bash
   mkdir go-context-demo && cd go-context-demo
   go mod init context-demo
   ```

3. 将以下三个文件复制到项目根目录：
   - `main.go`
   - `timeout_example.go`
   - `cancel_example.go`

## 文件说明
| 文件名             | 功能描述 |
|----------------------|----------|
| main.go              | 入口文件，运行所有示例 |
| timeout_example.go   | 演示带超时的 context 使用 |
| cancel_example.go    | 演示手动取消 context 的行为 |

## 逐步实操指南

### 步骤 1: 创建项目结构
```bash
mkdir go-context-demo
cd go-context-demo
go mod init context-demo
```

### 步骤 2: 创建代码文件
将对应内容写入以下文件：

#### 创建 main.go
```bash
# 内容见 code/main.go
```

#### 创建 timeout_example.go
```bash
# 内容见 code/timeout_example.go
```

#### 创建 cancel_example.go
```bash
# 内容见 code/cancel_example.go
```

### 步骤 3: 运行程序
```bash
go run *.go
```

### 预期输出示例
```
=== 超时场景演示 ===
处理任务中... (模拟耗时操作)
任务因超时被取消: context deadline exceeded

=== 取消信号演示 ===
处理任务中... (等待取消信号)
收到取消信号: context canceled
```

## 代码解析

### `timeout_example.go`
```go
ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
defer cancel() // 必须调用 cancel 释放资源
```
- 创建一个最多持续 2 秒的上下文
- 即使未触发超时也必须调用 `cancel()`，防止内存泄漏

在子 goroutine 中监听 `ctx.Done()` 来感知超时事件。

### `cancel_example.go`
```go
ctx, cancel := context.WithCancel(context.Background())
go func() {
    time.Sleep(1 * time.Second)
    cancel() // 主动发出取消信号
}()
```
- 使用 `WithCancel` 创建可手动取消的 context
- 模拟外部条件满足后主动终止正在进行的操作

## 常见问题解答

**Q: 是否每次都要调用 cancel()？**
A: 是的！无论是否使用完 context，都应调用 `cancel()` 以释放关联的定时器和 Goroutine，否则可能导致内存泄漏。

**Q: 能否在 context 中传递用户认证信息？**
A: 可以，但应使用自定义 key 类型避免键冲突，并仅用于请求生命周期内的元数据传递。

**Q: context 是线程安全的吗？**
A: 是的，同一个 context 可被多个 goroutine 同时访问。

## 扩展学习建议
- 阅读官方博客《Go Concurrency Patterns: Context》
- 学习 net/http 包中 context 的集成方式
- 探索 `context.WithValue` 的合理与不合理用法
- 实践在微服务中通过 context 传递追踪 ID