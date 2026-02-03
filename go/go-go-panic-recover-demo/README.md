# Go Panic Recover 实战演示

## 简介
本演示项目展示了在 Go 语言中如何使用 `panic` 和 `recover` 进行错误控制和程序恢复。通过三个不同的场景，帮助开发者理解何时以及如何安全地使用 `panic` 和 `recover`，避免程序意外崩溃。

## 学习目标
- 理解 `panic` 和 `recover` 的工作机制
- 掌握 `defer` 与 `recover` 的配合使用
- 学会在不同场景下合理使用 `recover` 恢复程序执行
- 避免滥用 `panic/recover` 导致代码可读性下降

## 环境要求
- Go 1.19 或更高版本（稳定版）
- 支持终端的系统（Windows / Linux / macOS）

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用 Go 标准库。

1. 确保已安装 Go：
   ```bash
   go version
   ```
   预期输出：`go version go1.19+`

2. 创建模块（如未初始化）：
   ```bash
   go mod init panic-recover-demo
   ```

## 文件说明
- `main.go`：主程序，演示基础 panic 和 recover 的使用
- `http_server.go`：模拟 HTTP 请求处理中的 panic 恢复
- `utils/calc.go`：展示在工具函数中使用 recover 防止崩溃

## 逐步实操指南

### 步骤 1：运行主程序
```bash
go run main.go
```
**预期输出**：
```
进入 defer 函数
recovered: 发生了恐慌！
程序继续执行...
```

### 步骤 2：运行 HTTP 服务示例
```bash
go run http_server.go
```
打开浏览器访问 `http://localhost:8080/bad`，页面显示：`发生错误：runtime error: integer divide by zero`
访问 `http://localhost:8080/good`，显示：`正常响应`
按 Ctrl+C 停止服务。

### 步骤 3：运行工具函数示例
```bash
go run utils/calc.go
```
**预期输出**：
```
计算结果: 10
计算结果: 5
除零错误被恢复
继续执行其他任务...
```

## 代码解析

### main.go 关键代码
```go
func mayPanic() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("recovered:", r)
		}
	}()
	panic("发生了恐慌！")
}
```
- 使用 `defer` 注册匿名函数，在 `panic` 触发时执行
- `recover()` 只在 `defer` 中有效，用于捕获 panic 值

### http_server.go
HTTP 处理器中使用中间件式 `recover`，防止单个请求崩溃导致服务器退出。

### calc.go
工具函数中对可能出错的操作进行封装，使用 `recover` 返回默认值而非中断调用者。

## 预期输出示例
见各步骤中的“预期输出”。

## 常见问题解答

**Q: recover 为什么必须在 defer 中调用？**
A: 因为 `recover` 需要与 `panic` 的堆栈展开过程交互，只有在 `defer` 执行期间才能拦截 panic。

**Q: 是否应该用 panic/recover 替代错误返回？**
A: 不推荐。应优先使用 `error` 返回。`panic` 仅用于不可恢复的错误或内部一致性错误。

**Q: 多层函数调用中 recover 能捕获吗？**
A: 可以，只要在 `goroutine` 的调用栈中有 `defer` + `recover`，就能捕获向上传播的 panic。

## 扩展学习建议
- 阅读《The Go Programming Language》第五章关于错误处理的内容
- 学习使用 `errors.New` 和 `fmt.Errorf` 构建错误
- 了解 `log.Fatal` 和 `panic` 的区别
- 探索 `gin`、`echo` 等框架如何内置 panic 恢复机制