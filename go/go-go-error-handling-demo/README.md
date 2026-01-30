# Go 错误处理演示

## 简介
本项目是一个简单的 Go 程序，用于演示 Go 语言中的错误处理机制，包括基本错误检查、自定义错误类型和 panic/recover 的使用。

## 学习目标
- 理解 Go 中 error 类型的基本用法
- 学会创建和使用自定义错误
- 掌握 panic 和 recover 的正确使用场景
- 遵循 Go 的错误处理最佳实践

## 环境要求
- Go 1.16 或更高版本（推荐使用最新稳定版）
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用 Go 标准库。只需安装 Go 即可运行。

1. 下载并安装 Go：https://golang.org/dl/
2. 验证安装：
   ```bash
   go version
   ```
   预期输出：`go version go1.xx.x os/arch`

## 文件说明
- `main.go`：主程序，演示基础错误处理
- `custom_error.go`：定义自定义错误类型及其使用
- `panic_recover.go`：演示 panic 和 recover 的使用

## 逐步实操指南

### 步骤 1: 创建项目目录
```bash
mkdir go-error-demo && cd go-error-demo
```

### 步骤 2: 创建代码文件
将以下三个文件创建到项目目录中：`main.go`、`custom_error.go`、`panic_recover.go`

### 步骤 3: 初始化 Go 模块
```bash
go mod init go-error-demo
```

### 步骤 4: 运行程序
```bash
go run main.go custom_error.go panic_recover.go
```

预期输出：
```
除法运算成功: 5 / 2 = 2.5
错误：不能除以零
自定义错误：年龄必须在 0 到 150 之间，当前值：-5
文件读取失败模拟：文件未找到
Panic 被 recover：发生严重错误
程序继续执行...
```

## 代码解析

### main.go
展示了标准的错误返回模式。函数通过返回 `error` 类型来通知调用方是否出错。

### custom_error.go
定义了一个实现 `error` 接口的结构体 `ValidationError`，用于提供更丰富的错误信息。

### panic_recover.go
演示了如何使用 `defer` 和 `recover()` 来捕获 panic，防止程序崩溃。适用于不可恢复的错误场景。

## 常见问题解答

**Q: 应该使用 error 还是 panic？**
A: 正常业务逻辑中的错误应使用 `error` 返回；只有在程序无法继续运行时才使用 `panic`，例如配置加载失败。

**Q: recover 能捕获所有 panic 吗？**
A: 只能在 defer 函数中使用 `recover()` 才能捕获当前 goroutine 的 panic。

**Q: 如何跨平台运行？**
A: Go 编译为静态二进制文件，只要编译目标匹配操作系统和架构即可。

## 扩展学习建议
- 阅读《The Go Programming Language》第五章关于错误处理的内容
- 学习 `errors.Is` 和 `errors.As`（Go 1.13+）进行错误比较
- 探索 `log/slog` 包进行结构化日志记录
- 实践在 HTTP 服务中统一错误处理中间件