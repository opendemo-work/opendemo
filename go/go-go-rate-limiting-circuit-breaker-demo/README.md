# Go限流与熔断机制实战演示

## 简介
本项目演示如何在Go语言中使用`golang.org/x/time/rate`实现请求限流，以及使用`github.com/sony/gobreaker`实现熔断机制。这两个模式是构建高可用微服务系统的核心组件，能有效防止系统雪崩和过载。

## 学习目标
- 掌握限流（Rate Limiting）的基本原理与实现方式
- 理解熔断器（Circuit Breaker）的工作机制
- 学会在Go项目中集成并使用限流与熔断
- 提升对微服务容错设计的理解

## 环境要求
- Go 1.19 或更高版本
- Git（用于下载依赖）

## 安装依赖的详细步骤
1. 打开终端
2. 进入项目目录：`cd path/to/demo`
3. 初始化模块并下载依赖：
   ```bash
   go mod init rate-circuit-demo
   go get golang.org/x/time/rate
   go get github.com/sony/gobreaker
   ```

## 文件说明
- `main.go`：主程序，演示限流功能
- `circuit_breaker.go`：演示熔断器的使用
- `go.mod`：Go模块依赖声明文件

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir rate-circuit-demo && cd rate-circuit-demo
```

### 步骤2：创建并运行限流示例
将`main.go`内容复制到文件中：
```bash
cat > main.go <<EOF
// 内容见下方代码文件
EOF
```
运行程序：
```bash
go run main.go
```

**预期输出**：
```
请求通过: 1
请求通过: 2
请求被限流: 3
请求被限流: 4
请求通过: 5
```

### 步骤3：运行熔断器示例
将`circuit_breaker.go`内容复制并运行：
```bash
go run circuit_breaker.go
```

**预期输出**：
```
调用成功: 调用正常服务
调用失败: 服务异常
...（多次失败后）...
熔断器已打开，拒绝请求
...
熔断器半开，尝试恢复
调用成功: 调用正常服务
```

## 代码解析

### main.go 关键代码段
```go
limiter := rate.NewLimiter(2, 3)
```
- 创建一个每秒最多2个令牌，突发容量为3的限流器。
- 使用`limiter.Allow()`判断是否允许请求通过。

### circuit_breaker.go 关键代码段
```go
var cb = gobreaker.NewCircuitBreaker(gobreaker.Settings{
    Name:        "example",
    MaxRequests: 1,
    Timeout:     5 * time.Second,
    ReadyToTrip: func(counts gobreaker.Counts) bool {
        return counts.ConsecutiveFailures > 2
    },
})
```
- 当连续失败超过2次时触发熔断
- 熔断持续5秒后进入半开状态尝试恢复
- `MaxRequests: 1` 表示半开状态下只允许1个请求试探

## 常见问题解答

**Q: 为什么需要限流？**
A: 防止系统因突发流量而崩溃，保护后端资源。

**Q: 熔断器有哪几种状态？**
A: 三种：关闭（Closed）、打开（Open）、半开（Half-Open）。

**Q: 如何调整限流速率？**
A: 修改`rate.NewLimiter(r, b)`中的`r`（速率）和`b`（突发值）。

## 扩展学习建议
- 尝试结合HTTP服务器实现API级限流
- 使用Redis实现分布式限流（如滑动窗口）
- 探索Hystrix、Resilience4j等其他熔断库的设计理念
- 学习服务网格（如Istio）中的限流与熔断配置