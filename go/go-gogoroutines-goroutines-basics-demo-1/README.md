# Go并发编程实战：Goroutines入门与应用

## 简介
本示例演示了Go语言中goroutines的基本用法，包括如何启动并发任务、使用channel进行通信以及如何等待多个goroutine完成。通过三个具体场景帮助开发者理解并发编程的核心概念。

## 学习目标
- 理解goroutine的基本概念和启动方式
- 掌握使用channel在goroutine之间传递数据
- 学会使用sync.WaitGroup协调多个goroutine
- 避免常见的并发问题（如竞态条件）

## 环境要求
- Go版本：1.19 或更高（推荐使用最新稳定版）
- 操作系统：Windows、Linux、macOS 均支持
- 命令行工具（终端）

## 安装依赖的详细步骤
本项目无需外部依赖，仅使用Go标准库。只需安装Go即可运行：

1. 访问 [https://golang.org/dl/](https://golang.org/dl/) 下载并安装对应操作系统的Go语言环境。
2. 验证安装：
   ```bash
   go version
   ```
   预期输出类似：
   ```
   go version go1.21.0 linux/amd64
   ```

## 文件说明
- `main.go`：主程序，展示基础goroutine用法和channel通信
- `waitgroup_example.go`：使用sync.WaitGroup等待多个goroutine完成
- `fan_out_fan_in.go`：演示“扇出-扇入”并发模式

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir goroutine-demo && cd goroutine-demo
```

### 步骤2：创建代码文件
将以下三个文件内容复制到对应文件中：
- `main.go`
- `waitgroup_example.go`
- `fan_out_fan_in.go`

### 步骤3：运行每个示例

运行基础goroutine示例：
```bash
go run main.go
```
预期输出：
```
主函数开始执行
Hello from goroutine!
你好，世界！
main结束
```

运行WaitGroup示例：
```bash
go run waitgroup_example.go
```
预期输出：
```
正在执行任务 1
正在执行任务 2
正在执行任务 3
所有任务已完成
```

运行扇出-扇入模式示例：
```bash
go run fan_out_fan_in.go
```
预期输出：
```
平方结果: 1
平方结果: 4
平方结果: 9
平方结果: 16
平方结果: 25
所有计算完成
```

## 代码解析

### main.go 关键点
- 使用 `go func()` 启动一个新goroutine
- 主goroutine不会等待子goroutine完成，需通过channel或time.Sleep避免提前退出
- 使用无缓冲channel同步执行顺序

### waitgroup_example.go 关键点
- `sync.WaitGroup` 用于等待一组goroutine完成
- `Add(n)` 设置要等待的任务数
- `Done()` 表示当前goroutine完成
- `Wait()` 阻塞直到所有任务调用Done()

### fan_out_fan_in.go 关键点
- 扇出（Fan-out）：多个goroutine从同一个channel读取数据并处理
- 扇入（Fan-in）：将多个channel的结果合并到一个channel
- 展示了典型的并发流水线设计模式

## 预期输出示例
参见上述“逐步实操指南”中的输出示例。

## 常见问题解答

**Q: 为什么main函数没等goroutine就退出了？**
A: Go的main goroutine不会自动等待其他goroutine。必须使用channel、WaitGroup等方式显式同步。

**Q: 什么是goroutine泄漏？如何避免？**
A: 当goroutine因无法退出而一直运行时发生泄漏。应确保所有channel都有发送者和接收者，并使用context控制生命周期。

**Q: goroutine和线程有什么区别？**
A: goroutine是Go运行时管理的轻量级线程，开销远小于操作系统线程，可轻松创建成千上万个。

## 扩展学习建议
- 学习使用 `context.Context` 控制goroutine生命周期
- 探索 `select` 语句处理多个channel
- 阅读《The Go Programming Language》第8章
- 实践更复杂的并发模式：worker pool、pipeline等