# Go控制流演示

## 简介
本示例演示了Go语言中三种基本的控制流结构：`if`、`switch` 和 `for` 循环。通过三个独立的代码文件，帮助初学者理解条件判断和循环的使用方法。

## 学习目标
- 掌握Go中if-else条件语句的写法
- 理解switch语句的多种用法（包括表达式和类型判断）
- 熟悉for循环的不同形式（经典、while-like、range）
- 遵循Go编码规范编写清晰代码

## 环境要求
- 操作系统：Windows、macOS 或 Linux
- Go版本：1.19 及以上（推荐最新稳定版）

## 安装依赖的详细步骤
本项目无需外部依赖，仅使用Go标准库。

1. 下载并安装Go：访问 [https://golang.org/dl/](https://golang.org/dl/) 下载适合你操作系统的安装包。
2. 安装后验证安装：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.0 darwin/amd64
   ```

## 文件说明
- `main.go`：主程序入口，演示if和else用法
- `switch_demo.go`：演示switch语句的各种场景
- `for_demo.go`：展示for循环的三种常见模式

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir control-flow-demo
cd control-flow-demo
```

### 步骤2：初始化Go模块
```bash
go mod init control-flow-demo
```

### 步骤3：创建并粘贴代码文件
将以下三个文件的内容分别保存到对应文件中：
- `main.go`
- `switch_demo.go`
- `for_demo.go`

### 步骤4：运行程序
```bash
go run main.go switch_demo.go for_demo.go
```

预期输出：
```
--- if-else 示例 ---
数字是正数

--- switch 示例 ---
今天是星期一
这是字符串类型

--- for 循环示例 ---
计数: 0
计数: 1
计数: 2
计数: 3
计数: 4
列表中的元素: apple
列表中的元素: banana
列表中的元素: cherry
```

## 代码解析

### main.go
```go
if num > 0 {
    fmt.Println("数字是正数")
} else if num < 0 {
    fmt.Println("数字是负数")
} else {
    fmt.Println("数字是零")
}
```
Go的if语句不需要括号包裹条件，但必须有花括号。支持链式else if。

### switch_demo.go
```go
switch day {
case "Monday":
    fmt.Println("今天是星期一")
...
}
```
Go的switch不需要break，自动防止穿透。也支持类型判断：`switch v := i.(type)`。

### for_demo.go
```go
for i := 0; i < 5; i++ {
    fmt.Printf("计数: %d\n", i)
}
```
Go中唯一的循环结构是`for`，但它可以模拟while和range行为。

## 预期输出示例
见“逐步实操指南”中的输出部分。

## 常见问题解答

**Q: 为什么Go没有while关键字？**
A: Go用`for`关键字统一了所有循环结构。`for condition { }` 就相当于其他语言的while。

**Q: switch语句需要写break吗？**
A: 不需要。Go的switch默认不穿透，除非使用`fallthrough`关键字。

**Q: 如何遍历map或slice？**
A: 使用`for range`语法，如：`for key, value := range myMap`。

## 扩展学习建议
- 阅读《The Go Programming Language》第5章
- 查阅官方文档：https://golang.org/ref/spec#Statements
- 尝试实现FizzBuzz程序来综合练习控制流