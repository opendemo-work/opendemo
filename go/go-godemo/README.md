# Go函数编程实践Demo

## 简介
本项目是一个面向初学者的Go语言函数编程教学示例，展示了Go中函数的基本定义、参数传递、返回值、高阶函数以及闭包的使用方式。通过三个独立但递进的代码文件，帮助学习者掌握Go函数的核心概念。

## 学习目标
- 掌握Go中函数的定义与调用
- 理解多返回值的使用场景
- 学会使用高阶函数（函数作为参数和返回值）
- 理解闭包的概念及其在Go中的实现

## 环境要求
- 操作系统：Windows / Linux / macOS（任意）
- Go版本：1.19 或更高稳定版本

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库，因此无需额外安装依赖。

1. 下载并安装Go：访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应系统的Go安装包
2. 安装后验证安装：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.0 darwin/amd64
   ```

## 文件说明
- `main.go`：主程序入口，演示基础函数和多返回值
- `higher_order.go`：展示高阶函数的使用（函数作为参数和返回值）
- `closure.go`：演示闭包的创建与应用

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-functions-demo && cd go-functions-demo
```

### 步骤2：创建并写入代码文件
将以下内容分别保存为对应的文件名。

### 步骤3：初始化Go模块
```bash
go mod init functions-demo
```

### 步骤4：运行程序
```bash
go run main.go higher_order.go closure.go
```

预期输出：
```
加法结果: 15, 是否溢出: false
斐波那契数列前8项: [0 1 1 2 3 5 8 13]
累加器从10开始: 11, 12, 13
计数器: 1, 2, 3
```

## 代码解析

### main.go - 基础函数与多返回值
```go
func add(a, b int) (int, bool) {
    // 返回计算结果和是否溢出的布尔值
}
```
Go支持多返回值，常用于错误处理或状态返回。

### higher_order.go - 高阶函数
```go
func apply(op func(int, int) int, a, b int) int {
    // 函数作为参数传入
}
```
展示了函数式编程思想，提升代码复用性。

### closure.go - 闭包
```go
func makeCounter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}
```
内部函数引用外部变量，形成闭包，实现状态保持。

## 预期输出示例
```
加法结果: 15, 是否溢出: false
斐波那契数列前8项: [0 1 1 2 3 5 8 13]
累加器从10开始: 11, 12, 13
计数器: 1, 2, 3
```

## 常见问题解答

**Q: 运行时报错 `command not found: go`？**
A: 请确认已正确安装Go，并将其添加到系统PATH环境变量中。

**Q: 如何调试Go程序？**
A: 可使用 `fmt.Println` 打印中间值，或使用支持Delve调试器的IDE（如VS Code + Go插件）。

**Q: 为什么Go函数可以返回多个值？**
A: 这是Go语言的设计特性，广泛用于返回结果+错误（error），提高代码清晰度。

## 扩展学习建议
- 阅读《The Go Programming Language》第5章：函数
- 尝试实现一个带缓存的斐波那契函数（记忆化递归）
- 学习使用 `defer`, `panic`, `recover` 控制流程
- 探索Go中函数式编程模式的应用