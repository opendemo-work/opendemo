# Go控制流语句实战演示

## 简介
本项目是一个专为Go初学者设计的控制流语句学习示例，涵盖 `if`、`switch` 和 `for` 三种核心控制结构。通过三个独立但连贯的代码文件，帮助你理解如何在实际场景中使用这些语法。

## 学习目标
- 掌握Go中条件判断（if/else）的基本用法
- 理解switch语句的灵活匹配机制
- 熟悉for循环的多种写法（传统、while-like、range）
- 学会结合控制流实现简单逻辑处理

## 环境要求
- 操作系统：Windows / Linux / macOS（任意）
- Go版本：1.19 或更高（推荐使用稳定版，如1.21）
- 终端工具：任意命令行终端（如 PowerShell、bash、zsh）

## 安装依赖的详细步骤
本项目不依赖第三方库，仅使用Go标准库，因此无需额外安装依赖。

1. 确保已安装Go环境：
   ```bash
   go version
   ```
   预期输出（版本号可能不同）：
   ```
   go version go1.21.0 darwin/amd64
   ```

2. 若未安装，请前往 [https://golang.org/dl/](https://golang.org/dl/) 下载对应系统的安装包并安装。

## 文件说明
- `main.go`：演示 if 和 else 的使用 —— 判断数字奇偶性
- `switch_demo.go`：演示 switch 多分支选择 —— 根据分数评定等级
- `loop_demo.go`：演示 for 循环的各种形式 —— 遍历与计数

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir go-control-flow-demo && cd go-control-flow-demo
```

### 步骤2：创建并粘贴代码文件
将以下三个文件内容分别保存到对应文件中：

创建 `main.go`：
```bash
cat > main.go <<EOF
// 将 main.go 内容粘贴到这里
EOF
```

创建 `switch_demo.go`：
```bash
cat > switch_demo.go <<EOF
// 将 switch_demo.go 内容粘贴到这里
EOF
```

创建 `loop_demo.go`：
```bash
cat > loop_demo.go <<EOF
// 将 loop_demo.go 内容粘贴到这里
EOF
```

### 步骤3：运行程序
执行以下命令运行整个程序（Go会自动编译并运行所有`.go`文件）：
```bash
go run *.go
```

## 代码解析

### main.go
使用 `if-else` 判断一个整数是否为偶数或奇数，展示基本条件判断语法。

### switch_demo.go
使用 `switch` 实现成绩等级划分，演示表达式省略时的灵活条件匹配。

### loop_demo.go
展示 `for` 循环的三种常见用法：
- 经典三段式（初始化；条件；递增）
- 类似 while 的单条件循环
- 使用 `range` 遍历切片

## 预期输出示例
```
7 是奇数

85 分的等级是：良好

计数从1到5：
1
2
3
4
5

使用for模拟while：当前值: 3
使用for模拟while：当前值: 2
使用for模拟while：当前值: 1
倒计时结束！

遍历字符串切片：
- Apple
- Banana
- Cherry
```

## 常见问题解答

**Q: 运行时报错 `command not found: go`？**
A: 表示Go未正确安装或未加入系统PATH，请重新安装Go并确认环境变量配置。

**Q: 可以只运行一个文件吗？**
A: 可以，例如：`go run main.go` 即可单独运行该文件。

**Q: Go中有没有 while 关键字？**
A: 没有。Go使用 `for` 来统一实现循环，省略初始化和递增部分即等价于 while。

## 扩展学习建议
- 尝试修改 `switch_demo.go` 使用带表达式的 switch
- 在 `loop_demo.go` 中添加 `break` 和 `continue` 示例
- 学习 `goto` 语句（虽不推荐，但需了解）
- 阅读官方Effective Go文档：https://golang.org/doc/effective_go