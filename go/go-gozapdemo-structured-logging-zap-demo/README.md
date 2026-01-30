# Go结构化日志管理Zap实战Demo

## 简介
本项目演示如何使用 Uber 开源的 `zap` 日志库在 Go 应用中实现高效、结构化的日志记录。zap 是性能极高的日志库，广泛用于生产环境，支持结构化输出（JSON）和简单字符串日志（SugaredLogger）。

## 学习目标
- 掌握 zap 的基本配置与初始化
- 理解 SugaredLogger 与 Logger 的区别
- 学会输出结构化日志到文件和控制台
- 实践日志分级（Debug、Info、Error）和字段添加

## 环境要求
- Go 1.19 或更高版本
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖步骤
1. 确保已安装 Go：
   ```bash
   go version
   # 预期输出：go version go1.19+ linux/amd64 (或其他平台)
   ```

2. 初始化 Go 模块（如果尚未初始化）：
   ```bash
   go mod init zap-demo
   ```

3. 添加 zap 依赖：
   ```bash
   go get -u go.uber.org/zap
   ```

## 文件说明
- `main.go`: 主程序，展示不同日志配置场景
- `advanced_logger.go`: 高级配置，包含日志写入文件和级别控制

## 逐步实操指南

### 步骤1: 创建项目目录并进入
```bash
mkdir zap-demo && cd zap-demo
```

### 步骤2: 创建 main.go
将以下内容保存为 `main.go`。

### 步骤3: 创建 advanced_logger.go
将第二个代码文件保存为 `advanced_logger.go`。

### 步骤4: 运行程序
```bash
go run main.go
```

#### 预期输出（部分）：
```json
{"level":"info","ts":1717034567.123,"msg":"用户登录成功","user_id":1001,"ip":"192.168.1.100"}
{"level":"error","ts":1717034567.124,"msg":"数据库连接失败","error":"connection timeout"}
```

## 代码解析

### main.go
- 使用 `zap.NewProduction()` 快速创建生产级日志器
- 通过 `.Sugar()` 获得易用的格式化接口
- 使用 `Infow`, `Errorw` 输出带字段的结构化日志

### advanced_logger.go
- 使用 `zap.Config` 自定义日志行为
- 将日志同时输出到控制台和文件
- 设置日志级别为 `debug`，并在生产中可动态调整
- 使用 `Sync()` 确保日志写入持久化

## 预期输出示例
运行后应看到类似以下 JSON 格式日志输出：
```json
{"level":"info","ts":1717034567.123,"caller":"main.go:15","msg":"服务启动","port":8080}
{"level":"warn","ts":1717034567.124,"msg":"请求处理缓慢","duration_ms":450,"path":"/api/data"}
```

## 常见问题解答

**Q: zap 和 log 包有什么区别？**
A: zap 是结构化、高性能日志库，log 是标准库中的基础文本日志。zap 更适合生产环境和服务监控。

**Q: 如何将日志写入文件？**
A: 见 `advanced_logger.go`，通过配置 `WriteSyncer` 可将日志写入文件。

**Q: 为什么推荐使用 SugaredLogger？**
A: 它支持类似 `printf` 的格式化，开发更方便；但在性能敏感场景建议使用原始 `Logger`。

## 扩展学习建议
- 学习 zap 的 `Field` 类型优化性能（避免重复字符串拼接）
- 结合 `lumberjack` 实现日志轮转
- 在 Gin/Fiber 框架中集成 zap 作为中间件
- 使用 ELK 或 Loki 收集和分析 zap 生成的结构化日志