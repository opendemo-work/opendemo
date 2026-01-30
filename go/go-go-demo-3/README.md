# Go字符串处理实战演示

## 简介
本项目是一个面向初学者的Go语言字符串（strings）操作演示程序，通过两个具体的使用场景展示Go标准库中`strings`包的常见用法，包括字符串搜索、替换、分割与大小写转换等。

## 学习目标
- 掌握Go中`strings`包的基本函数使用
- 理解不可变字符串的处理方式
- 学会格式化输出和字符串构建
- 培养良好的Go编码习惯

## 环境要求
- 操作系统：Windows、Linux 或 macOS
- Go版本：1.19 或更高（推荐使用稳定版如1.20+）

## 安装依赖的详细步骤
本项目仅使用Go标准库，无需额外安装依赖。

1. 下载并安装Go语言环境：
   访问 [https://golang.org/dl/](https://golang.org/dl/) 下载对应系统的安装包并安装。

2. 验证安装：
   打开终端或命令行，运行：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.0 linux/amd64
   ```

3. 设置工作目录：
   ```bash
   mkdir go-strings-demo && cd go-strings-demo
   ```

## 文件说明
- `main.go`：主程序，演示字符串基本操作
- `utils.go`：工具函数，演示字符串处理的封装方法
- `go.mod`：模块声明文件，定义项目模块名

## 逐步实操指南

### 步骤1：初始化Go模块
在项目根目录执行：
```bash
go mod init strings-demo
```

预期输出：
```bash
go: creating new go.mod: module strings-demo
```

### 步骤2：创建代码文件
将`main.go`、`utils.go`和`go.mod`内容复制到对应文件中。

### 步骤3：运行程序
执行以下命令：
```bash
go run main.go utils.go
```

预期输出：
```text
=== 字符串基础操作 ===
原始文本: Hello, 世界! Welcome to Golang.
转为大写: HELLO, 世界! WELCOME TO GOLANG.
是否包含"Golang": true
替换"Golang"为"Go": Hello, 世界! Welcome to Go.
按空格分割: [Hello, 世界! Welcome to Golang.]

=== 字符串工具函数演示 ===
清理并标题化: Hello World
重复三次: TestTestTest
安全拼接: Part1_Part2
```

## 代码解析

### main.go 关键代码段
```go
strings.ToUpper(text) // 将字符串转为大写
```
说明：Go中字符串是不可变的，该函数返回新字符串，原字符串不变。

```go
strings.Contains(text, "Golang")
```
说明：判断子串是否存在，返回布尔值，性能高。

### utils.go 中的`CleanAndTitle`函数
```go
return strings.Title(strings.TrimSpace(s))
```
说明：链式调用多个`strings`函数，先去空格再转为首字母大写格式（注意：`Title`对Unicode支持有限，生产环境建议用`golang.org/x/text`）。

## 预期输出示例
见“逐步实操指南”中的输出部分。

## 常见问题解答

**Q1: 运行时报错 `command not found: go`？**
A: 请确认已正确安装Go并配置了环境变量PATH。

**Q2: `strings.Title` 对中文无效？**
A: 是的，`Title`主要用于ASCII字符。处理多语言文本时建议使用第三方库如`golang.org/x/text/cases`。

**Q3: 能否修改原字符串？**
A: 不可以。Go的字符串是只读的，所有操作都返回新字符串。

## 扩展学习建议
- 学习`strconv`包进行字符串与基本类型转换
- 探索`fmt.Sprintf`进行格式化字符串拼接
- 了解正则表达式 `regexp` 包
- 阅读官方文档：[https://pkg.go.dev/strings](https://pkg.go.dev/strings)
