# Go信号处理与优雅关闭Demo

## 简介
本示例演示了在Go语言中如何使用`os/signal`包监听操作系统信号（如SIGINT、SIGTERM），并实现服务器的优雅关闭。适用于Web服务、后台任务等需要安全退出的场景。

## 学习目标
- 理解操作系统信号在Go中的处理机制
- 掌握`signal.Notify`的使用方法
- 实现HTTP服务器的优雅关闭
- 避免请求中断，确保正在处理的任务完成

## 环境要求
- Go 1.19 或更高版本
- 支持终端操作的系统（Windows / Linux / macOS）

## 安装依赖
本项目无外部依赖，仅使用Go标准库。

1. 确保已安装Go：
   ```bash
   go version
   # 预期输出：go version go1.19+ ...
   ```

2. 创建模块（若未初始化）：
   ```bash
   go mod init graceful-shutdown-demo
   ```

## 文件说明
- `main.go`：主程序，启动HTTP服务器并监听中断信号
- `worker.go`：模拟后台任务的优雅停止

## 逐步实操指南

1. 将以下两个代码文件保存到项目目录：
   - `main.go`
   - `worker.go`

2. 构建并运行程序：
   ```bash
   go run main.go
   # 输出：
   # 2023/xx/xx xx:xx:xx 服务已启动在 :8080
   # 等待中断信号...
   ```

3. 打开新终端，发送请求：
   ```bash
   curl http://localhost:8080
   # 输出：Hello, World!
   ```

4. 回到运行程序的终端，按下 Ctrl+C 发送 SIGINT 信号
   ```text
   接收到中断信号，开始优雅关闭...
   正在等待正在进行的请求完成...
   后台任务已停止
   服务已关闭
   ```

## 代码解析

### main.go
- 使用`http.ListenAndServe`启动HTTP服务
- 通过`signal.Notify`监听`SIGINT`和`SIGTERM`
- 关闭`Server`时使用`Shutdown()`方法避免强制终止连接

### worker.go
- 模拟一个周期性执行的后台任务（如日志清理）
- 使用`context.WithCancel`控制其生命周期
- 在主程序关闭时取消任务

## 预期输出示例
```text
2023/xx/xx xx:xx:xx 服务已启动在 :8080
等待中断信号...
接收到中断信号，开始优雅关闭...
正在等待正在进行的请求完成...
后台任务被中断
服务已关闭
```

## 常见问题解答

**Q: 为什么使用`Shutdown()`而不是`Close()`？**
A: `Shutdown()`允许正在处理的请求完成，而`Close()`会立即断开所有连接，可能导致数据丢失或客户端错误。

**Q: 如何测试SIGTERM信号？**
A: 可在Linux/macOS中使用：`kill $(pgrep your-process)`

**Q: Windows下是否支持？**
A: 支持。Windows支持Ctrl+C（SIGINT），但部分信号行为可能略有不同。

## 扩展学习建议
- 结合`sync.WaitGroup`管理多个goroutine的关闭
- 使用`context`传递超时控制给数据库查询等操作
- 将优雅关闭集成到gRPC服务中
- 添加健康检查端点（/healthz）配合Kubernetes使用
