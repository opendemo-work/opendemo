# Go正则表达式文本匹配实战演示

## 简介
本项目是一个完整的Go语言示例，展示了如何使用标准库`regexp`进行各种常见的文本匹配操作。涵盖邮箱验证、日志行解析和批量替换三个实用场景。

## 学习目标
- 掌握Go中`regexp`包的基本用法
- 学会编译和复用正则表达式以提高性能
- 理解命名捕获组与子匹配的提取方法
- 实践字符串替换与批量处理技巧

## 环境要求
- Go 1.16 或更高版本（推荐使用最新稳定版）
- 支持终端/命令行的操作系统（Windows / Linux / macOS 均可）

## 安装依赖
此项目仅使用Go标准库，无需额外安装依赖。

## 文件说明
- `main.go`: 主程序，演示邮箱格式验证
- `log_parser.go`: 解析模拟的日志行，提取时间和请求路径
- `text_replacer.go`: 演示敏感词替换和批量文本处理

## 逐步实操指南

### 步骤1: 创建项目目录
```bash
mkdir go-regexp-demo && cd go-regexp-demo
```

### 步骤2: 初始化Go模块
```bash
go mod init go-regexp-demo
```

### 步骤3: 创建并粘贴代码文件
将以下三个文件内容分别保存到对应路径：
- `main.go`
- `log_parser.go`
- `text_replacer.go`

### 步骤4: 运行程序
```bash
go run main.go log_parser.go text_replacer.go
```

### 预期输出：
```
邮箱 'example@example.com' 格式有效: true
邮箱 'invalid-email' 格式有效: false

解析日志条目:
时间: 14:23:01, 请求路径: /api/users
时间: 14:23:05, 请求路径: /static/image.png

原始文本: 用户提交了包含屏蔽词的内容
替换后: 用户提交了包含***的内容
```

## 代码解析

### main.go - 邮箱验证
使用预编译的正则表达式检查邮箱格式是否合法。注意使用`MustCompile`在初始化时编译，避免重复解析开销。

### log_parser.go - 日志解析
利用命名捕获组 `(？P<name>...)` 提取结构化信息，并通过`.SubexpNames()` 和 `.FindStringSubmatch()` 联合使用来获取字段值。

### text_replacer.go - 文本替换
展示如何使用`ReplaceAllString`进行敏感词过滤，支持多个关键词的连续替换。

## 常见问题解答

**Q: 为什么使用`regexp.MustCompile`而不是`regexp.Compile`？**
A: 因为正则表达式是硬编码的常量，如果出错属于编程错误，应立即panic便于调试；而动态输入才需处理error。

**Q: 如何提升大量文本处理的性能？**
A: 复用已编译的`*regexp.Regexp`对象，不要每次调用都重新编译。

**Q: 是否支持Unicode？**
A: 是的，Go的regexp默认支持UTF-8编码的Unicode文本。

## 扩展学习建议
- 尝试添加URL匹配功能
- 使用正则表达式清洗HTML标签
- 结合`io.Reader`流式处理大文件日志
- 学习更复杂的断言和非贪婪匹配语法