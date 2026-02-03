# Go并发编程实战：Goroutines详解

## 简介
本示例展示了Go语言中goroutines在实际开发中的三种典型应用场景：
1. 并发执行独立任务
2. 使用通道（channel）进行goroutine间通信
3. 使用`context`控制goroutine生命周期

通过这些例子，你将掌握Go并发编程的核心模式和最佳实践。

## 学习目标
- 理解goroutine的基本概念和启动方式
- 掌握如何使用channel在goroutine之间安全传递数据
- 学会使用`context`取消长时间运行的goroutine
- 避免常见的并发陷阱（如竞态条件）

## 环境要求
- Go 1.19 或更高版本（推荐使用稳定版）
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖的详细步骤
本项目不依赖第三方库，仅使用Go标准库。只需安装Go即可运行。

1. 下载并安装Go：访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应系统的安装包
2. 安装后验证版本：
   ```bash
   go version
   # 预期输出：go version go1.19+ ...
   ```

## 文件说明
- `main.go`：主程序，包含三个独立的goroutine使用示例

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir goroutine-demo && cd goroutine-demo
```

### 步骤2：创建并编辑 main.go
将 `main.go` 的内容复制到文件中。

### 步骤3：运行程序
```bash
go run main.go
```

### 预期输出
```
[示例1] 启动两个并发任务...
任务A: 进度 1
任务B: 进度 1
任务A: 进度 2
任务B: 进度 2
任务A完成
任务B完成

[示例2] 使用通道传递结果...
接收到计算结果: 42
接收到计算结果: 13
所有任务完成

[示例3] 使用Context取消goroutine...
工作协程正在运行...
收到取消信号，正在退出...
上下文已取消，清理完成
```

## 代码解析

### 示例1：基础Goroutine使用
```go
go func(id string) {
    for i := 1; i <= 2; i++ {
        fmt.Printf("%s: 进度 %d\n", id, i)
        time.Sleep(100 * time.Millisecond)
    }
    fmt.Printf("%s完成\n", id)
}("任务A")
```
- 使用 `go` 关键字启动新goroutine
- 每个goroutine模拟一个耗时任务
- 主函数通过 `time.Sleep` 等待所有goroutine完成（生产环境应使用WaitGroup）

### 示例2：Goroutine + Channel
```go
resultChan := make(chan int)
...
go func() {
    result := heavyComputation()
    resultChan <- result
}()
```
- 创建无缓冲通道用于传递结果
- 每个goroutine完成计算后将结果发送到通道
- 主函数从通道接收并处理结果

### 示例3：Context控制Goroutine
```go
ctx, cancel := context.WithTimeout(context.Background(), 800*time.Millisecond)
defer cancel()
...
select {
case <-ctx.Done():
    fmt.Println("收到取消信号，正在退出...")
    return
}
```
- 使用`context.WithTimeout`创建带超时的上下文
- 在goroutine中监听`ctx.Done()`通道
- 超时后自动触发取消，避免资源泄漏

## 常见问题解答

**Q: 为什么主函数需要sleep？不能自动等待吗？**
A: 是的，在生产环境中应使用`sync.WaitGroup`来等待所有goroutine完成，而不是使用`Sleep`。本示例为简化演示使用了Sleep。

**Q: 通道是否必须关闭？**
A: 不是必须的。只有当你使用`range`遍历通道或需要通知接收方不再有数据时才需要关闭。

**Q: 如何避免goroutine泄漏？**
A: 始终确保goroutine有退出路径，使用`context`进行生命周期管理，并避免无限阻塞操作。

## 扩展学习建议
- 学习 `sync.WaitGroup` 替代 sleep 等待
- 探索 `sync.Mutex` 和原子操作处理共享状态
- 研究 `errgroup` 包简化并发错误处理
- 阅读《Go语言高级编程》并发章节
- 实践：构建一个并发网页爬虫