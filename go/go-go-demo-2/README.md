# Go变量类型实战演示

## 简介
本示例通过三个具体的Go程序，帮助初学者理解Go语言中变量的声明方式、基本数据类型及其使用场景。涵盖显式声明、短变量声明、类型推断等核心概念。

## 学习目标
- 掌握Go中变量的多种声明方式
- 理解常见基本数据类型（int, float64, bool, string）
- 学会使用`var`和`:=`进行变量初始化
- 了解Go的类型推断机制

## 环境要求
- 操作系统：Windows / Linux / macOS（任意）
- Go版本：1.19 或更高（推荐使用稳定版，如1.21）
- 命令行终端

## 安装依赖步骤
本项目无需外部依赖，仅使用Go标准库。

1. 下载并安装Go：访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应系统的安装包
2. 安装后验证版本：
   ```bash
   go version
   ```
   预期输出：`go version go1.21.x os/arch`

## 文件说明
- `main.go`：主程序，演示基本变量声明和类型使用
- `types_inferred.go`：展示类型推断与短变量声明
- `constants.go`：介绍常量与iota枚举用法

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-variables-demo && cd go-variables-demo
```

### 步骤2：复制代码文件
将以下三个文件内容分别保存到对应文件中：
- `main.go`
- `types_inferred.go`
- `constants.go`

### 步骤3：运行程序
```bash
go run main.go types_inferred.go constants.go
```

预期输出：
```
整数: 42
浮点数: 3.14
布尔值: true
字符串: Hello, Go!

推断整数: 100
推断浮点数: 2.718
消息: 变量已自动推断类型

状态: Pending
状态码: 1
最大重试次数: 3
```

## 代码解析

### main.go
使用标准 `var` 关键字显式声明变量，并指定类型，适合在包级别或需要明确类型的场景。

### types_inferred.go
使用 `:=` 进行短变量声明，Go会根据右侧值自动推断类型，适用于函数内部快速声明。

### constants.go
展示 `const` 和 `iota` 的使用，`iota` 在常量组中自增，常用于定义状态码或枚举值。

## 预期输出示例
见“逐步实操指南”中的输出部分。

## 常见问题解答

**Q: `var x int = 10` 和 `x := 10` 有什么区别？**
A: 前者是显式声明，可在函数外使用；后者是短声明，只能在函数内使用，且类型由Go自动推断。

**Q: 为什么不能在函数外使用 `:=`？**
A: `:=` 是短变量声明，仅限局部作用域，函数外必须使用 `var` 或 `const`。

**Q: 如何查看变量的实际类型？**
A: 使用 `fmt.Printf("%T", variable)` 可打印变量类型。

## 扩展学习建议
- 阅读官方文档：[https://golang.org/doc/tutorial/getting-started](https://golang.org/doc/tutorial/getting-started)
- 学习复合类型：数组、切片、映射
- 尝试使用 `type` 定义自定义类型