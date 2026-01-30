# Go并发编程实战：Mutex与WaitGroup详解

## 简介
本示例演示了在Go语言中如何使用`sync.Mutex`和`sync.WaitGroup`来安全地处理并发访问共享资源的场景。包含两个典型用例：计数器并发更新和批量任务处理。

## 学习目标
- 理解`sync.WaitGroup`的作用及其使用方法
- 掌握`sync.Mutex`在保护共享数据中的应用
- 学会避免Go中的竞态条件（race condition）
- 实践Go并发编程的最佳实践

## 环境要求
- Go 1.19 或更高版本（推荐使用稳定版）
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖
本项目不依赖外部库，仅使用Go标准库，无需额外安装依赖。

## 文件说明
- `main.go`: 主程序，展示使用Mutex保护共享计数器
- `tasks.go`: 演示使用WaitGroup协调多个并发任务

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-concurrency-demo
cd go-concurrency-demo
```

### 步骤2：初始化Go模块
```bash
go mod init concurrency-demo
```

### 步骤3：创建并复制代码文件
将以下两个文件内容分别保存到对应路径：
- 创建 `main.go` 并粘贴第一个代码示例
- 创建 `tasks.go` 并粘贴第二个代码示例

### 步骤4：运行程序
```bash
go run main.go tasks.go
```

### 预期输出
```
最终计数器值: 5000
所有任务已完成
```

## 代码解析

### main.go 关键点
- 使用 `sync.Mutex` 确保对共享变量 `counter` 的访问是线程安全的
- 多个goroutine并发执行时，通过 `mutex.Lock()` 和 `mutex.Unlock()` 保证原子性操作
- `defer mutex.Unlock()` 确保即使发生panic也能释放锁

### tasks.go 关键点
- 使用 `sync.WaitGroup` 等待所有goroutine完成
- `wg.Add(1)` 增加等待计数，每个goroutine完成后调用 `wg.Done()`
- `wg.Wait()` 阻塞主线程直到所有任务结束

## 预期输出示例
```
正在执行任务 #1
正在执行任务 #3
正在执行任务 #2
正在执行任务 #4
正在执行任务 #5
...（共10条类似日志）
最终计数器值: 5000
所有任务已完成
```

## 常见问题解答

**Q: 为什么需要Mutex？**
A: 当多个goroutine同时读写同一变量时，会发生竞态条件。Mutex确保同一时间只有一个goroutine能访问临界区。

**Q: WaitGroup的作用是什么？**
A: 它用于等待一组并发操作完成，常用于主函数等待所有子goroutine结束。

**Q: 如何检测竞态条件？**
A: 使用 `go run -race main.go tasks.go` 启用竞态检测器，可发现潜在的数据竞争问题。

## 扩展学习建议
- 尝试移除Mutex，观察结果变化，并使用 `-race` 标志检测问题
- 将任务数量增加到100，观察性能表现
- 学习使用`channel`替代WaitGroup/Mutex实现同步
- 阅读官方文档 [https://pkg.go.dev/sync](https://pkg.go.dev/sync)
