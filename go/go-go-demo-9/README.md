# Go时间处理实战演示

## 简介
本示例展示了Go语言中`time`包的常用功能，包括当前时间获取、时间格式化、时间计算和定时器使用。适合初学者学习Go的时间处理机制。

## 学习目标
- 掌握如何获取当前时间
- 学会格式化和解析时间字符串
- 理解时间的加减运算
- 使用定时器（Timer）和打点器（Ticker）

## 环境要求
- Go 1.19 或更高版本
- 支持Windows、Linux、MacOS

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库`time`，无需额外安装依赖。

## 文件说明
- `main.go`: 主程序，展示时间的基本操作
- `timer_example.go`: 演示定时器和打点器的使用
- `format_parse.go`: 展示时间格式化与解析

## 逐步实操指南

### 步骤1: 创建项目目录
```bash
mkdir go-time-demo
cd go-time-demo
```

### 步骤2: 初始化Go模块
```bash
go mod init go-time-demo
```

### 步骤3: 创建并粘贴代码文件
将以下三个文件内容分别保存到对应文件中：
- `main.go`
- `timer_example.go`
- `format_parse.go`

### 步骤4: 运行程序
```bash
go run main.go timer_example.go format_parse.go
```

### 预期输出示例
```
当前时间: 2025-04-05 10:30:45
明天此时: 2025-04-06 10:30:45
格式化时间: 2025/04/05 10:30:45
解析后的时间: 2023-01-01 12:00:00 +0000 UTC
定时器触发: 2秒后执行
打点器: 第1次打点
打点器: 第2次打点
打点器: 第3次打点
```

## 代码解析

### main.go
```go
now := time.Now()
```
获取当前本地时间，返回`time.Time`类型。

```go
tomorrow := now.Add(24 * time.Hour)
```
使用`Add()`方法进行时间加法，支持负值做减法。

### format_parse.go
```go
dateStr := now.Format("2006/01/02 15:04:05")
```
Go使用固定的参考时间 `Mon Jan 2 15:04:05 MST 2006` 来定义格式，这个时间是 `2006-01-02T15:04:05Z07:00`。

```go
time.Parse("2006-01-02 15:04:05", "2023-01-01 12:00:00")
```
按指定格式解析字符串为`time.Time`类型。

### timer_example.go
```go
timer := time.NewTimer(2 * time.Second)
<-timer.C
```
创建一个定时器，2秒后通道`C`会发送当前时间。

```go
ticker := time.NewTicker(1 * time.Second)
```
打点器会每隔1秒在通道`C`中发送时间，可用于周期性任务。

## 常见问题解答

**Q: 为什么Go时间格式化用的是2006-01-02？**
A: Go使用一个固定的“参考时间”来定义格式模板，即 `2006-01-02 15:04:05`，这是Go诞生前的一个历史设计决策。

**Q: 如何设置时区？**
A: 使用`time.LoadLocation("Asia/Shanghai")`加载时区，然后用`Time.In(loc)`切换时区显示。

**Q: 定时器和打点器需要手动停止吗？**
A: 是的，长时间运行的应用中应调用`timer.Stop()`或`ticker.Stop()`避免资源泄漏。

## 扩展学习建议
- 学习`time.Location`处理多时区应用
- 尝试`time.Since()`计算耗时
- 使用`context`控制定时器生命周期
- 实现一个简单的cron调度器