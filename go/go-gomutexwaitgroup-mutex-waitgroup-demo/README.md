# Go并发编程实战：Mutex与WaitGroup

## 简介
本示例演示如何在Go语言中使用`sync.Mutex`保护共享资源，以及使用`sync.WaitGroup`协调多个goroutine的执行。通过三个典型场景展示并发编程中的关键同步机制。

## 学习目标
- 理解`sync.Mutex`的作用及使用场景
- 掌握`sync.WaitGroup`的基本用法
- 学会避免竞态条件（race condition）
- 实践Go并发编程的最佳实践

## 环境要求
- Go 1.19 或更高版本（推荐使用稳定版）
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖
本项目不依赖外部库，仅使用Go标准库。

确保已安装Go环境：
```bash
go version
```
预期输出类似：
```
go version go1.21.0 linux/amd64
```

## 文件说明
- `main.go`：主程序，演示多个goroutine对共享计数器的安全访问
- `bank_account.go`：模拟银行账户转账，展示Mutex在实际业务中的应用
- `worker_pool.go`：使用WaitGroup协调工作池中的任务完成

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-concurrency-demo && cd go-concurrency-demo
```

### 步骤2：创建代码文件
将以下内容分别保存为对应文件名。

### 步骤3：运行程序
```bash
go run main.go
```
预期输出：
```
最终计数: 1000
账户A余额: 500, 账户B余额: 500
所有工作任务已完成
```

### 步骤4：检测竞态条件（可选）
使用Go的竞态检测器重新运行：
```bash
go run -race main.go
```
若无输出错误，则说明同步正确。

## 代码解析

### main.go
使用`WaitGroup`等待1000个goroutine完成，并用`Mutex`保护共享变量`counter`，防止竞态条件。

### bank_account.go
模拟两个账户间并发转账，每个转账操作都通过Mutex锁定涉及的账户，保证数据一致性。

### worker_pool.go
展示如何使用WaitGroup等待一组后台任务全部完成，常用于批量处理场景。

## 预期输出示例
```
最终计数: 1000
账户A余额: 500, 账户B余额: 500
所有工作任务已完成
```

## 常见问题解答

**Q: 为什么需要Mutex？**
A: 多个goroutine同时读写同一变量会导致数据竞争。Mutex确保同一时间只有一个goroutine能访问临界区。

**Q: WaitGroup的作用是什么？**
A: 它让主goroutine等待其他goroutine完成任务，避免程序提前退出。

**Q: 是否可以在defer中调用WaitGroup.Done()？**
A: 可以，且是推荐做法，确保即使发生panic也能正确释放。

## 扩展学习建议
- 学习`sync.RWMutex`以提高读多写少场景的性能
- 探索`channel`替代Mutex实现同步
- 阅读《The Go Programming Language》第9章并发
- 使用`go tool trace`分析并发程序行为