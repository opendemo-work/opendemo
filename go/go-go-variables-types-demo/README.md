# Go变量与类型演示

## 简介
本演示项目展示了Go语言中变量声明、初始化以及基本数据类型的使用方式。通过三个不同的场景，帮助初学者理解Go中的静态类型系统、变量作用域和类型推断机制。

## 学习目标
- 掌握Go中变量的声明与初始化语法
- 理解基本数据类型（int, float64, bool, string）的使用
- 学会使用短变量声明和类型推断
- 了解常量和iota枚举的用法

## 环境要求
- Go 1.19 或更高版本（推荐使用稳定版）
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖的详细步骤
本项目无需外部依赖，仅使用Go标准库。

1. 下载并安装Go语言环境：
   访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应平台的安装包

2. 验证安装：
   ```bash
   go version
   ```
   预期输出：`go version go1.19.x os/arch`

## 文件说明
- `main.go`：主程序，演示变量声明和基本类型
- `constants.go`：演示常量和枚举类型
- `types_inference.go`：演示类型推断和短变量声明

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-variables-demo
cd go-variables-demo
```

### 步骤2：复制代码文件
将以下三个文件内容分别保存到对应文件中：
- `main.go`
- `constants.go`
- `types_inference.go`

### 步骤3：初始化Go模块
```bash
go mod init variables-demo
```

### 步骤4：运行程序
```bash
go run .
```

预期输出：
```
整数: 42, 浮点数: 3.14, 布尔值: true, 字符串: Hello Gopher
姓名: 张三, 年龄: 25, 薪资: 5000.50
工作状态: 工作中
颜色: Green, 数值: 1
x=10, y=20, z=30 (自动推断为int类型)
a=hello, b=3.14159 (自动推断为string和float64)
```

## 代码解析

### main.go
演示了标准变量声明方式，使用 `var` 关键字显式指定类型，适合在函数外声明包级变量。

### constants.go
展示了 `const` 的用法，特别是 `iota` 自动生成递增常量值，常用于定义枚举类型。

### types_inference.go
使用 `:=` 短变量声明，Go编译器会根据右侧值自动推断变量类型，这是Go中最常见的局部变量声明方式。

## 预期输出示例
```
整数: 42, 浮点数: 3.14, 布尔值: true, 字符串: Hello Gopher
姓名: 张三, 年龄: 25, 薪资: 5000.50
工作状态: 工作中
颜色: Green, 数值: 1
x=10, y=20, z=30 (自动推断为int类型)
a=hello, b=3.14159 (自动推断为string和float64)
```

## 常见问题解答

**Q: 为什么有些变量用 var，有些用 := ?**
A: `var` 可以在任何地方使用，而 `:=` 只能在函数内部使用，且必须同时声明和赋值。

**Q: Go 是静态类型语言吗？**
A: 是的，Go 是静态类型语言，所有变量在编译时都必须有确定的类型。

**Q: 如何查看变量的实际类型？**
A: 使用 `fmt.Printf("%T", variable)` 可打印变量类型。

## 扩展学习建议
- 学习复合类型：数组、切片、映射
- 了解结构体和方法
- 探索接口和多态性
- 阅读《The Go Programming Language》第3章