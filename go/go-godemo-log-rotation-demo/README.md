# Go日志轮转文件管理Demo

## 简介
本示例展示了如何在Go语言中使用 `lumberjack` 库实现日志轮转（Log Rotation），包括按文件大小和时间自动切割日志文件，并保留历史日志。

## 学习目标
- 理解日志轮转的基本概念和应用场景
- 掌握使用 `lumberjack` 实现日志切割的方法
- 学会配置日志文件的最大大小、备份数量和压缩选项
- 熟悉跨平台的日志文件管理实践

## 环境要求
- Go 1.19 或更高版本
- 支持的平台：Windows、Linux、macOS

## 安装依赖的详细步骤
1. 打开终端或命令行工具
2. 进入项目目录（如 `cd log-rotation-demo`）
3. 执行以下命令安装依赖：
   ```bash
   go mod init log-rotation-demo
   go get github.com/natefinch/lumberjack/v2
   ```

## 文件说明
- `main.go`：主程序，演示按大小轮转日志
- `time_rotation.go`：扩展示例，演示结合时间进行日志轮转（逻辑模拟）
- `go.mod`：模块依赖声明文件

## 逐步实操指南

### 步骤1：创建项目目录并初始化
```bash
mkdir log-rotation-demo && cd log-rotation-demo
```

### 步骤2：创建并运行主程序
将 `main.go` 内容保存到文件中，然后执行：
```bash
go run main.go
```

**预期输出**：
- 在当前目录下生成 `logs/app.log`
- 控制台输出写入日志的消息
- 当日志超过1MB时，自动重命名并创建新文件（最多保留3个旧文件）

### 步骤3：查看日志文件
```bash
ls -l logs/
```
应看到类似：
```
app.log
app.log.1
app.log.2.gz
```

## 代码解析

### main.go 关键部分
```go
&lumberjack.Logger{
    Filename:   "logs/app.log",
    MaxSize:    1, // MB
    MaxBackups: 3,
    MaxAge:     7, // 天
    Compress:   true,
}
```
- `MaxSize`: 单个日志文件最大1MB后触发轮转
- `MaxBackups`: 最多保留3个旧日志文件
- `MaxAge`: 超过7天的备份将被删除
- `Compress`: 启用gzip压缩旧日志

## 预期输出示例
```
写入日志: [INFO] 这是一条测试日志消息 (序号: 1)
写入日志: [INFO] 这是一条测试日志消息 (序号: 2)
...
```
并在 `logs/` 目录中观察到自动轮转和压缩行为。

## 常见问题解答

**Q: 日志没有轮转？**
A: 检查是否写入的数据足够大（>1MB），可临时将 `MaxSize` 改为 `1` 测试。

**Q: Windows 下路径错误？**
A: Go 的 `/` 路径在Windows上兼容，无需修改。

**Q: 如何按每天轮转？**
A: `lumberjack` 不直接支持时间轮转，但可通过外部定时任务（如 cron）配合文件名日期实现。

## 扩展学习建议
- 结合 `zap` 或 `logrus` 使用 lumberjack 作为输出writer
- 实现自定义日志轮转器以支持更复杂策略
- 添加日志清理定时任务（如每日扫描删除超过30天的日志）
- 将日志发送到ELK或Loki等集中式系统