# Go函数编程实践Demo

## 简介
本项目是一个专为Go初学者设计的函数编程教学示例，展示了Go语言中函数的基本用法、多返回值、匿名函数与闭包、以及高阶函数的应用场景。通过三个独立但连贯的代码文件，帮助学习者掌握Go函数的核心概念。

## 学习目标
- 理解Go函数的基本语法和调用方式
- 掌握多返回值函数的设计与使用
- 学会创建和使用闭包
- 理解并应用高阶函数模式
- 遵循Go语言最佳实践进行编码

## 环境要求
- 操作系统：Windows 7+/macOS 10.12+/Linux（任何现代发行版）
- Go版本：1.19 或更高版本（推荐使用稳定版1.21+）

## 安装依赖的详细步骤
本项目不依赖外部库，仅使用Go标准库，因此无需安装额外依赖。

1. 下载并安装Go：
   访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应操作系统的安装包

2. 安装完成后验证安装：
   ```bash
   go version
   ```

   **预期输出**：
   ```
   go version go1.21.x os/arch
   ```

3. 设置工作目录：
   ```bash
   mkdir go-functions-demo && cd go-functions-demo
   ```

## 文件说明
- `main.go`：演示基本函数和多返回值
- `closure.go`：展示闭包和状态保持功能
- `higher_order.go`：演示高阶函数的使用

## 逐步实操指南

### 步骤1：创建项目结构
```bash
mkdir go-functions-demo
cd go-functions-demo
go mod init functions-demo
```

### 步骤2：创建并运行第一个示例
将 `main.go` 内容保存到文件中，然后执行：
```bash
go run main.go
```

**预期输出**：
```
5 + 3 = 8
除法结果: 2.5, 是否成功: true
除法错误: 除数不能为零
```

### 步骤3：运行闭包示例
```bash
go run closure.go
```

**预期输出**：
```
计数器: 1
计数器: 2
计数器: 3
累加器: 10
累加器: 15
累加器: 21
```

### 步骤4：运行高阶函数示例
```bash
go run higher_order.go
```

**预期输出**：
```
原始数字: [1 2 3 4 5]
平方后: [1 4 9 16 25]
偶数筛选: [2 4]
字符串长度: [5 3 5 4]
大写转换: [HELLO WORLD GO CODE]
```

## 代码解析

### main.go 关键点
- `add(a int, b int) int`：基础函数定义，展示参数与返回值类型声明
- `divide(a, b float64) (float64, bool)`：多返回值函数，用于安全除法运算

### closure.go 关键点
- `newCounter()` 返回一个闭包函数，内部变量 `count` 被捕获并持续存在
- `newAccumulator()` 展示如何通过闭包维护可变状态

### higher_order.go 关键点
- `mapInts(nums []int, f func(int) int)`：接受函数作为参数的高阶函数
- `filterInts(nums []int, pred func(int) bool)`：基于条件过滤切片元素
- 匿名函数的现场定义与传递

## 预期输出汇总
所有程序运行成功后，应依次看到上述各部分的输出结果，无编译或运行时错误。

## 常见问题解答

**Q: 运行时报错 `command not found: go`？**
A: 请确认已正确安装Go并配置了环境变量PATH。

**Q: 如何调试这些程序？**
A: 可使用 `fmt.Printf` 输出中间变量，或使用 `delve` 调试器：`go install github.com/go-delve/delve/cmd/dlv@latest`

**Q: 函数参数为何可以省略类型重复？**
A: Go允许在连续相同类型的参数后只写一次类型，如 `a, b int` 等价于 `a int, b int`

**Q: 闭包中的变量生命周期是怎样的？**
A: 即使外层函数返回，被闭包引用的局部变量仍会保留在内存中，直到闭包本身被回收

## 扩展学习建议
- 阅读《The Go Programming Language》第5章 函数
- 尝试实现递归函数如斐波那契数列
- 学习Go中的方法（Methods）与函数的区别
- 探索函数式编程模式在Go中的应用
- 实践使用函数构建简单的DSL（领域特定语言）