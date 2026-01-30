# Go并发编程实战：Goroutines入门

## 简介
本示例演示了Go语言中goroutines的三种典型使用场景，包括基础并发执行、带缓冲通道的数据传递以及并发安全的计数器实现。通过这些例子，您将理解如何高效地利用Go的轻量级线程（goroutines）来编写并发程序。

## 学习目标
- 理解goroutine的基本概念和启动方式
- 掌握使用channel在goroutine之间通信
- 学会控制并发执行的同步机制
- 了解并发安全的常见模式

## 环境要求
- Go语言版本：1.19 或更高（推荐使用稳定版）
- 操作系统：Windows、Linux、macOS（跨平台兼容）
- 命令行终端

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库。请确保已安装Go环境：

1. 访问 [https://golang.org/dl/](https://golang.org/dl/) 下载并安装对应系统的Go发行版。
2. 验证安装：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.0 linux/amd64
   ```
3. 设置工作目录，例如：
   ```bash
   mkdir goroutine-demo && cd goroutine-demo
   ```

## 文件说明
- `main.go`：主程序文件，包含三个独立的goroutine使用示例
- `go.mod`：Go模块声明文件

## 逐步实操指南

### 步骤1：初始化Go模块
```bash
go mod init goroutine-demo
```

### 步骤2：创建并编辑 main.go
将 `main.go` 文件内容复制到本地文件中。

### 步骤3：运行程序
```bash
go run main.go
```

**预期输出：**
```
[示例1] 启动两个并发任务...
任务A: 执行第 1 次
任务B: 执行第 1 次
任务A: 执行第 2 次
任务B: 执行第 2 次
任务A 完成
任务B 完成

[示例2] 使用带缓冲channel传递数据...
生产者发送: 数据-1
消费者接收: 数据-1
生产者发送: 数据-2
消费者接收: 数据-2
生产者完成
消费者完成

[示例3] 并发安全计数器...
协程 1: 当前计数 = 1
协程 2: 当前计数 = 2
协程 1: 当前计数 = 3
协程 2: 当前计数 = 4
最终计数: 4
```

## 代码解析

### 示例1：基础Goroutine使用
```go
go func() {
    for i := 1; i <= 2; i++ {
        fmt.Printf("任务A: 执行第 %d 次\n", i)
        time.Sleep(100 * time.Millisecond)
    }
    fmt.Println("任务A 完成")
}()
```
- 使用 `go` 关键字启动匿名函数作为goroutine
- 主函数通过 `time.Sleep` 等待子goroutine完成（实际中应使用sync.WaitGroup）

### 示例2：Channel通信
```go
ch := make(chan string, 2)
```
- 创建容量为2的带缓冲channel，避免发送阻塞
- 生产者向channel发送数据，消费者从channel接收

### 示例3：并发安全计数器
```go
var mu sync.Mutex
mu.Lock()
counter++
mu.Unlock()
```
- 使用 `sync.Mutex` 保证对共享变量 `counter` 的访问是线程安全的
- 防止竞态条件（race condition）

## 预期输出示例
见“逐步实操指南”中的输出部分。

## 常见问题解答

**Q1: 为什么main函数需要sleep？**
A: 因为主goroutine不会等待其他goroutine自动完成。在生产环境中，应使用 `sync.WaitGroup` 来协调。

**Q2: 如何检测竞态条件？**
A: 使用 `go run -race main.go` 启用竞态检测器。

**Q3: channel无缓冲和有缓冲的区别？**
A: 无缓冲channel要求发送和接收同时就绪；有缓冲channel可在缓冲未满时立即发送。

## 扩展学习建议
- 学习使用 `sync.WaitGroup` 替代 sleep 实现精确同步
- 探索 `context.Context` 在超时和取消中的应用
- 阅读《Go语言实战》或官方Effective Go文档
- 尝试实现一个并发的Web爬虫