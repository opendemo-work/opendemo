# Go并发控制实战：Mutex与WaitGroup演示

## 简介
本示例演示了在Go语言中如何使用`sync.Mutex`和`sync.WaitGroup`来安全地管理多个goroutine对共享资源的并发访问。通过两个典型场景——计数器并发更新和银行账户转账，帮助理解并发编程中的关键同步机制。

## 学习目标
- 理解`sync.WaitGroup`的作用及用法
- 掌握`sync.Mutex`如何防止数据竞争
- 学会结合WaitGroup与Mutex实现安全的并发操作
- 避免常见的并发错误（如竞态条件）

## 环境要求
- Go 1.19 或更高版本（推荐使用稳定版）
- 支持的操作系统：Windows、Linux、macOS
- 命令行终端（bash / PowerShell / cmd）

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库，无需额外安装依赖。

```bash
# 检查Go版本
go version
```

预期输出：
```
go version go1.19+ linux/amd64
```

## 文件说明
- `main.go`：主程序，演示多个goroutine并发增加计数器，使用WaitGroup等待完成，Mutex保护共享变量。
- `bank_account.go`：模拟银行账户并发转账场景，展示更复杂的Mutex应用。

## 逐步实操指南

### 步骤1：创建项目目录
```bash
git clone https://github.com/example/go-concurrency-demo.git
cd go-concurrency-demo
```

或手动创建：
```bash
mkdir go-concurrency-democd go-concurrency-demo
touch main.go bank_account.go
```

### 步骤2：复制代码内容
将提供的`main.go`和`bank_account.go`内容分别粘贴到对应文件中。

### 步骤3：运行程序
```bash
go run main.go
```

预期输出：
```
最终计数器值: 1000
执行银行账户并发转账...
转账完成后账户余额: 1000
```

### 步骤4：验证无数据竞争
使用Go的竞争检测器重新运行：
```bash
go run -race main.go
```
如果没有输出错误，则表示无数据竞争问题。

## 代码解析

### main.go 关键代码段
```go
var counter int
var mu sync.Mutex
var wg sync.WaitGroup
```
定义共享计数器、互斥锁和等待组。

```go
wg.Add(1)
go func() {
    defer wg.Done()
    // 加锁保护共享变量
    mu.Lock()
    counter++
    mu.Unlock()
}()
```
每个goroutine增加计数前加锁，确保原子性；使用`defer wg.Done()`确保任务完成通知。

```go
wg.Wait()
```
主线程等待所有goroutine完成。

### bank_account.go 关键点
结构体`Account`包含余额和互斥锁，方法内部自动加锁，对外隐藏同步细节，符合封装原则。

## 预期输出示例
```
最终计数器值: 1000
执行银行账户并发转账...
转账完成后账户余额: 1000
```

## 常见问题解答

**Q: 为什么需要WaitGroup？**
A: 主goroutine不会等待其他goroutine结束。WaitGroup用于协调，确保所有子任务完成后再继续。

**Q: 不加Mutex会发生什么？**
A: 多个goroutine同时修改`counter`会导致竞态条件，最终结果可能小于1000。

**Q: Mutex是否会影响性能？**
A: 会轻微影响，但相比数据不一致的代价，这是必要的。应尽量减少锁持有时间。

**Q: 可以用channel代替Mutex吗？**
A: 可以，但适用场景不同。Channel适合goroutine间通信，Mutex适合保护共享状态。

## 扩展学习建议
- 学习`sync.RWMutex`用于读多写少场景
- 尝试使用`atomic`包进行无锁编程
- 阅读《The Go Programming Language》第9章并发
- 实践使用`context.Context`控制goroutine生命周期