# Go变量类型演示

## 简介
本示例演示了Go语言中基本变量类型的声明、初始化和使用方法，涵盖布尔型、整型、浮点型、字符串以及短变量声明等核心概念。通过三个独立的代码文件，帮助初学者掌握Go的基础数据类型用法。

## 学习目标
- 理解Go中变量的声明与初始化语法
- 掌握常用基本数据类型（bool, int, float64, string）
- 学会使用`var`和`:=`进行变量定义
- 了解零值（zero value）机制

## 环境要求
- Go 1.19 或更高版本（推荐使用稳定版）
- 操作系统：Windows、Linux 或 macOS 均可
- 终端/命令行工具

## 安装依赖的详细步骤
本项目无需外部依赖库，仅使用Go标准库。

1. 下载并安装Go：访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应平台的安装包
2. 安装完成后，在终端执行以下命令验证安装：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.0 darwin/amd64
   ```

## 文件说明
- `main.go`：演示基本变量类型的声明与零值
- `short_declaration.go`：演示短变量声明语法 `:=`
- `type_inference.go`：演示类型推断与多变量赋值

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-variables-demo
cd go-variables-demo
```

### 步骤2：创建并写入代码文件
将以下内容分别保存为对应的Go文件。

### 步骤3：运行每个示例

运行 main.go：
```bash
go run main.go
```
预期输出：
```
布尔类型 (默认): false
整型 (默认): 0
浮点型 (默认): 0
字符串 (默认): 
带初始值的变量: true, 42, 3.14, Hello Go
```

运行 short_declaration.go：
```bash
go run short_declaration.go
```
预期输出：
```
使用 := 声明的变量: name=张三, age=25, height=1.78
```

运行 type_inference.go：
```bash
go run type_inference.go
```
预期输出：
```
类型推断变量 - x=100, y=hello, z=true
多变量同时声明: a=1, b=2, c=3
交换两个变量: a=2, b=1
```

## 代码解析

### main.go 关键点
- 使用 `var` 声明未初始化的变量，会自动赋予**零值**
- 显示不同类型的零值行为（如字符串为空串，bool为false）
- 展示显式初始化语法

### short_declaration.go 关键点
- `:=` 是短变量声明，只能在函数内部使用
- 编译器自动推断类型，简洁且常用

### type_inference.go 关键点
- Go能根据右侧值自动推断变量类型
- 支持多变量声明与赋值，甚至用于交换变量

## 预期输出示例
完整输出见“逐步实操指南”中的各命令结果。

## 常见问题解答

**Q: `var x int` 和 `x := 0` 有什么区别？**
A: `var` 可在包级作用域使用，而 `:=` 只能在函数内使用；`:=` 自动推导类型，更简洁。

**Q: 为什么未初始化的字符串是空串而不是 nil？**
A: 因为 string 是值类型，其零值就是空字符串 ""，不是指针类型。

**Q: 能否在同一行声明多个不同类型变量？**
A: 不可以直接混合类型，但可通过 `:=` 多重赋值实现：`a, b := 1, "hello"`

## 扩展学习建议
- 阅读官方文档：[https://golang.org/ref/spec#Variables](https://golang.org/ref/spec#Variables)
- 学习复合类型：数组、切片、映射
- 尝试使用 `fmt.Printf` 输出变量类型：`%T`
- 探索常量 `const` 与 iota 枚举