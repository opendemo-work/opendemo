# Go定时任务调度Cron示例

## 简介
本项目演示如何在Go语言中使用`robfig/cron/v3`库实现灵活的定时任务调度。通过三个不同的场景，展示基础定时、动态任务管理和带上下文的任务执行。

## 学习目标
- 掌握Go中使用Cron表达式进行任务调度的方法
- 理解如何添加、删除和管理定时任务
- 学会结合context实现优雅的任务控制

## 环境要求
- Go 1.19 或更高版本
- 支持跨平台（Windows/Linux/Mac）

## 安装依赖的详细步骤

1. 初始化Go模块：
   ```bash
   go mod init cron-demo
   ```

2. 添加robfig/cron依赖：
   ```bash
   go get github.com/robfig/cron/v3
   ```

## 文件说明
- `main.go`：主程序，展示基本Cron任务调度
- `dynamic_scheduler.go`：演示动态添加/删除任务
- `context_aware.go`：展示带context的可取消任务

## 逐步实操指南

### 步骤1：创建项目目录并初始化
```bash
mkdir cron-demo && cd cron-demo
go mod init cron-demo
```

### 步骤2：创建代码文件
将以下三个文件内容分别保存到对应路径：
- `main.go`
- `dynamic_scheduler.go`
- `context_aware.go`

### 步骤3：安装依赖
```bash
go get github.com/robfig/cron/v3
```

### 步骤4：运行示例

运行基础定时任务：
```bash
go run main.go
```
预期输出（每5秒打印一次）：
```
[基础任务] 当前时间: 2025-04-05 10:00:05
```

运行动态任务管理：
```bash
go run dynamic_scheduler.go
```
预期输出：
```
[动态任务] 执行于 2025-04-05 10:00:05
[系统] 已移除动态任务
```

运行上下文感知任务：
```bash
go run context_aware.go
```
预期输出：
```
[上下文任务] 正在执行...
[上下文任务] 收到取消信号，停止执行
```

## 代码解析

### main.go - 基础Cron用法
使用标准Cron表达式 `*/5 * * * * *` 表示“每5秒”执行一次任务，这是robfig/cron支持的扩展格式（包含秒字段）。

### dynamic_scheduler.go - 动态管理
通过`cron.EntryID`记录任务ID，调用`c.Remove(id)`实现运行时动态删除任务，适用于配置驱动的调度系统。

### context_aware.go - 上下文控制
利用`context.WithCancel`创建可取消的context，在任务函数中监听`ctx.Done()`实现优雅退出，避免goroutine泄漏。

## 预期输出示例
```
[基础任务] 当前时间: 2025-04-05 10:00:05
[基础任务] 当前时间: 2025-04-05 10:00:10
[动态任务] 执行于 2025-04-05 10:00:15
[系统] 已移除动态任务
[上下文任务] 正在执行...
[上下文任务] 收到取消信号，停止执行
```

## 常见问题解答

**Q: Cron表达式`*/5 * * * * *`是什么意思？**
A: 这是六字段格式（秒 分 时 日 月 周），表示“每5秒”触发一次。注意robfig/cron默认支持秒字段。

**Q: 如何让任务只在特定条件下运行？**
A: 可以在任务函数内部添加条件判断逻辑，或封装一个条件执行包装器。

**Q: 为什么任务没有按预期执行？**
A: 检查Cron表达式格式是否正确；确保main函数没有立即退出（可通过channel阻塞）。

## 扩展学习建议
- 尝试集成日志库（如zap）记录任务执行情况
- 实现持久化任务列表（使用JSON或数据库存储）
- 结合HTTP服务提供REST API来增删定时任务
- 使用`cron.WithSeconds()`显式启用秒级调度