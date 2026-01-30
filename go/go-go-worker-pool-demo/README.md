# Go Worker Pool 实战演示

## 简介
本项目演示了如何在Go语言中使用Worker池（协程池）模式来高效处理大量并发任务。通过固定数量的工作协程从任务队列中消费任务，避免无限制创建goroutine带来的资源耗尽问题。

## 学习目标
- 理解Worker池的设计模式及其优势
- 掌握Go中goroutine与channel的协同工作方式
- 学会控制并发数量以优化系统资源使用
- 提高对复杂并发场景的编程能力

## 环境要求
- Go 1.19 或更高版本（推荐使用稳定版）
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖
此项目不依赖第三方库，仅使用Go标准库，因此无需额外安装依赖。

### 检查Go环境
```bash
go version
```

预期输出（版本号可能不同）：
```bash
go version go1.21.0 linux/amd64
```

## 文件说明
- `main.go`：主程序，实现了一个基本的Worker池模型，模拟处理多个任务
- `dynamic_pool.go`：进阶示例，支持动态调整Worker数量的协程池

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-worker-pool-demo && cd go-worker-pool-demo
```

### 步骤2：创建代码文件
将以下内容分别保存为 `main.go` 和 `dynamic_pool.go`

### 步骤3：运行基础Worker池示例
```bash
go run main.go
```

预期输出：
```bash
Worker 1 开始处理任务: Task-1
Worker 2 开始处理任务: Task-2
Worker 1 开始处理任务: Task-3
Worker 2 开始处理任务: Task-4
Worker 1 完成任务: Task-1
Worker 2 完成任务: Task-2
Worker 1 完成任务: Task-3
Worker 2 完成任务: Task-4
所有任务已分配完毕
等待所有任务完成...
全部任务执行完毕
```

### 步骤4：运行动态Worker池示例
```bash
go run dynamic_pool.go
```

预期输出：
```bash
[动态池] Worker 1 处理任务: DynamicTask-1
[动态池] Worker 2 处理任务: DynamicTask-2
[动态池] Worker 1 完成任务: DynamicTask-1
[动态池] Worker 2 完成任务: DynamicTask-2
动态Worker池任务全部完成
```

## 代码解析

### `main.go` 关键代码段
```go
// 创建带缓冲的任务通道，最多存放10个任务
jobs := make(chan string, 10)

// 创建结果通道，用于接收完成信号
done := make(chan bool)

// 启动两个Worker协程
for w := 1; w <= 2; w++ {
    go worker(w, jobs, done)
}
```
- 使用`chan string`作为任务队列，实现生产者-消费者模型
- `done`通道用于通知主线程所有任务已完成

```go
// 发送完所有任务后关闭通道，防止goroutine泄漏
close(jobs)
// 等待所有Worker完成
for i := 0; i < 2; i++ {
    <-done
}
```
- 必须关闭`jobs`通道，否则Worker中的range会持续等待
- 通过接收`done`信号确保所有Worker退出

### `dynamic_pool.go` 特点
- 使用`sync.WaitGroup`替代布尔通道，更清晰地管理协程生命周期
- 可轻松扩展Worker数量，适合负载变化的场景

## 预期输出示例
见上文“逐步实操指南”中的输出样例。

## 常见问题解答

### Q1: 为什么不能无限启动goroutine？
A: 每个goroutine占用约2KB栈内存，大量并发可能导致内存耗尽或调度延迟。Worker池能有效控制并发数。

### Q2: 为什么要关闭任务channel？
A: 不关闭会导致Worker中`for job := range jobs`无法退出，造成goroutine泄漏。

### Q3: 如何处理任务执行失败？
A: 可扩展result结构体，加入error字段，由Worker回传错误信息进行集中处理。

## 扩展学习建议
- 尝试添加任务超时机制（使用context.WithTimeout）
- 实现优先级任务队列
- 结合Redis等中间件构建分布式任务池
- 学习开源库如`ants`（高性能协程池库）