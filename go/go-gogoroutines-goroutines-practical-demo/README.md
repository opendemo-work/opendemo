# Go并发编程实战：Goroutines应用示例

本项目通过三个典型场景展示Go语言中goroutines和channel的高效用法，帮助开发者掌握并发编程的核心技巧。

## 学习目标
- 理解goroutine的基本概念和启动方式
- 掌握使用channel进行goroutine间通信
- 学会使用WaitGroup同步多个goroutine
- 避免常见的并发问题（如竞态条件）

## 环境要求
- Go版本：1.19 或更高（推荐使用稳定版1.20+）
- 操作系统：Windows、Linux、macOS 均支持
- 命令行终端

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库，无需额外安装依赖。

确保已安装Go环境：
```bash
go version
```
预期输出示例：
```
go version go1.21.5 linux/amd64
```

## 文件说明
- `main.go`：主程序，演示基本goroutine与channel通信
- `worker_pool.go`：实现一个简单的任务池模式
- `timeout_example.go`：展示如何使用context和超时控制goroutine执行

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir goroutine-demo && cd goroutine-demo
```

### 步骤2：创建并运行 main.go
```bash
go run main.go
```
**预期输出**：
```
发送消息：Hello from goroutine!
接收到的消息：Hello from goroutine!
main函数结束
```

### 步骤3：运行 worker_pool.go
```bash
go run worker_pool.go
```
**预期输出**：
```
Worker 1 正在处理任务: 任务1
Worker 2 正在处理任务: 任务2
Worker 1 正在处理任务: 任务3
Worker 2 正在处理任务: 任务4
所有任务已分配完毕
Worker 1 正在处理任务: 任务5
Worker 2 收到关闭信号，退出
所有worker已完成
```

### 步骤4：运行 timeout_example.go
```bash
go run timeout_example.go
```
**预期输出**：
```
请求正在处理...
操作超时或被取消
```
或（如果修改为短时间）：
```
请求正在处理...
操作成功完成
```

## 代码解析

### main.go 关键代码段
```go
ch := make(chan string)
```
创建一个字符串类型的无缓冲channel，用于主协程与子协程通信。

```go
go func() {
    time.Sleep(1 * time.Second)
    ch <- "Hello from goroutine!"
}()
```
启动一个匿名goroutine，模拟异步任务，并通过channel发送结果。

```go
msg := <-ch
```
从channel接收数据，阻塞直到有值写入。

### worker_pool.go 要点
使用带缓冲的channel作为任务队列，多个worker并发消费任务，体现任务池模型。

### timeout_example.go 核心机制
利用`context.WithTimeout`控制goroutine最长执行时间，避免无限等待，提升程序健壮性。

## 预期输出示例（综合）
参见各步骤中的“预期输出”。

## 常见问题解答

**Q1：为什么程序没有等待goroutine完成就退出了？**
A：请检查是否正确使用了channel或sync.WaitGroup进行同步。未同步时main函数结束会导致所有goroutine终止。

**Q2：什么是channel的死锁？如何避免？**
A：当goroutine试图读写channel但没有其他goroutine响应时发生。避免方法：确保有发送就有接收，或使用带缓冲channel。

**Q3：goroutine泄漏怎么排查？**
A：可通过pprof工具分析堆栈，或确保每个启动的goroutine都有明确的退出路径。

## 扩展学习建议
- 学习`select`语句处理多个channel
- 探索`context`包在大型项目中的应用
- 阅读《Go语言实战》第8章并发模式
- 实践errgroup、semaphore等高级并发原语