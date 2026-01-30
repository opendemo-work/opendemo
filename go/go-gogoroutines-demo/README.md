# Go并发编程入门：Goroutines实战演示

本项目通过三个具体的代码示例，帮助你理解Go语言中goroutines的基本用法、并发控制以及如何通过channel进行安全的数据通信。

## 学习目标

- 理解什么是goroutine及其在Go中的作用
- 掌握如何启动和管理多个并发任务
- 学会使用channel在goroutine之间安全传递数据
- 了解waitgroup在并发控制中的应用

## 环境要求

- Go 1.19 或更高版本（推荐使用稳定版）
- 支持命令行操作的系统（Windows / Linux / macOS）

## 安装依赖的详细步骤

本项目不依赖第三方库，仅使用Go标准库，因此无需额外安装依赖。

1. 下载并安装Go语言环境：
   访问 [https://golang.org/dl](https://golang.org/dl) 下载对应系统的安装包并安装。

2. 验证安装：
   打开终端或命令提示符，运行以下命令：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.0 linux/amd64
   ```

3. 创建项目目录并复制代码文件（main.go, concurrent_sum.go, worker_pool.go）到项目中。

## 文件说明

- `main.go`：基础goroutine示例，展示如何并发执行简单函数
- `concurrent_sum.go`：使用channel和WaitGroup实现并发求和计算
- `worker_pool.go`：实现一个简单的worker pool模式处理批量任务

## 逐步实操指南

### 步骤1：创建项目目录

```bash
mkdir goroutine-demo
cd goroutine-demo
```

### 步骤2：创建并粘贴代码文件

创建 `main.go`，粘贴第一个示例代码。

运行：
```bash
go run main.go
```

预期输出：
```
主函数开始执行...
你好，来自goroutine！
main函数即将结束
```

> 注意：由于并发调度，可能有时看不到goroutine的输出，因为main可能提前退出。

### 步骤3：运行并发求和示例

创建 `concurrent_sum.go`，粘贴第二个示例代码。

运行：
```bash
go run concurrent_sum.go
```

预期输出：
```
并发计算结果: 5050
```

### 步骤4：运行工作池示例

创建 `worker_pool.go`，粘贴第三个示例代码。

运行：
```bash
go run worker_pool.go
```

预期输出（顺序可能不同）：
```
Worker 1 处理任务: 任务1
Worker 2 处理任务: 任务2
Worker 1 处理任务: 任务3
Worker 2 处理任务: 任务4
Worker 1 处理任务: 任务5
所有任务完成
```

## 代码解析

### main.go - 基础Goroutine

```go
go fmt.Println("你好，来自goroutine！")
```
这一行启动了一个新的goroutine来执行打印语句。但main函数不会等待它，所以需要time.Sleep来避免程序过早退出（仅用于演示）。

### concurrent_sum.go - 使用Channel与WaitGroup

关键点：
- `sync.WaitGroup` 用于等待所有goroutine完成
- 每个goroutine将结果发送到channel
- 主函数从channel接收所有结果并汇总

### worker_pool.go - Worker Pool模式

使用固定数量的worker从任务channel中读取任务，并发处理。这是处理大量任务时的经典模式，能有效控制资源消耗。

## 预期输出示例

见各步骤中的“预期输出”。

## 常见问题解答

**Q: 为什么有时候goroutine没有输出？**
A: 因为main函数执行完后程序立即退出，未等待goroutine。解决方法是使用`sync.WaitGroup`或`time.Sleep`（仅测试用）。

**Q: Goroutine会占用多少内存？**
A: 初始约2KB，Go会自动扩容栈空间，非常轻量。

**Q: Channel是线程安全的吗？**
A: 是的，channel本身就是为并发安全设计的，多个goroutine可安全读写。

## 扩展学习建议

- 学习`context`包以实现goroutine的超时与取消
- 尝试使用`select`语句处理多个channel
- 阅读《The Go Programming Language》第8章
- 实践：构建一个并发爬虫或批量文件处理器