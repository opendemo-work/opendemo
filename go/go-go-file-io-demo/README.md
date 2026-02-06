# Go文件操作实战演示

## 简介
本项目是一个面向初学者的Go语言文件I/O操作教学示例，包含三个典型场景：
1. 创建并写入文件
2. 读取文件内容（非缓冲）
3. 使用缓冲方式高效读取大文件

通过这些例子，学习者可以掌握Go中标准库`os`和`bufio`的基本用法。

## 学习目标
- 掌握使用Go进行基本的文件创建与写入
- 理解如何安全地读取文件内容
- 学会使用缓冲提高大文件处理效率
- 熟悉错误处理和资源清理（defer）的最佳实践

## 环境要求
- Go 1.16 或更高版本（推荐最新稳定版）
- 支持命令行操作的系统（Windows / Linux / macOS）

## 安装依赖的详细步骤
本项目不依赖第三方库，仅使用Go标准库，无需额外安装依赖。

1. 下载并安装Go：[https://golang.org/dl/](https://golang.org/dl/)
2. 验证安装：
   ```bash
   go version
   ```
   预期输出示例：
   ```
   go version go1.21.0 darwin/amd64
   ```

## 文件说明
- `main.go` - 主程序入口，演示文件写入
- `read.go` - 演示普通读取和缓冲读取两种方式
- `go.mod` - Go模块声明文件

## 逐步实操指南

### 步骤1：初始化Go模块
```bash
mkdir file-io-demo && cd file-io-demo
go mod init file-io-demo
```

### 步骤2：创建代码文件
将以下内容分别保存为对应文件名。

### 步骤3：运行程序
```bash
# 运行写入示例
go run main.go

# 运行读取示例
go run read.go
```

预期输出：
```text
文件已成功写入: sample.txt
正在读取文件: sample.txt
--- 普通读取 ---\n这是第一行。\n这是第二行。\n\n--- 缓冲读取 ---\n这是第一行。\n这是第二行。\n```

## 代码解析

### main.go 关键点
```go
file, err := os.Create(filename)
defer file.Close()
```
- 使用 `os.Create` 创建或覆盖文件
- 使用 `defer` 确保文件在函数退出时关闭

```go
ioutil.WriteFile 的替代方式：使用 WriteString 并检查错误
```

### read.go 关键点
```go
scanner := bufio.NewScanner(file)
for scanner.Scan() {
    fmt.Println(scanner.Text())
}
```
- `bufio.Scanner` 是逐行读取大文件的推荐方式
- 自动处理换行符，兼容不同平台

## 预期输出示例
```
文件已成功写入: sample.txt
正在读取文件: sample.txt
--- 普通读取 ---
这是第一行。
这是第二行。

--- 缓冲读取 ---
这是第一行。
这是第二行。
```

## 常见问题解答

**Q: 运行时报错 `command not found: go`？**
A: 请确认已正确安装Go，并将其添加到系统PATH环境变量中。

**Q: 写入的文件在哪里？**
A: 文件会生成在你运行 `go run` 命令的当前目录下。

**Q: 如何读取中文内容？**
A: Go原生支持UTF-8，只要源码保存为UTF-8格式即可正常读写中文。

## 扩展学习建议
- 尝试修改代码实现追加写入模式（使用 `os.OpenFile` 和 `os.O_APPEND`）
- 实现一个统计文件行数的小工具
- 学习 `io/ioutil`（已弃用）与 `os.ReadFile` 的区别（Go 1.16+）
- 探索 `os.Stat` 获取文件信息