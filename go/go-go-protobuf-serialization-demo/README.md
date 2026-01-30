# Go Protobuf 序列化 Demo

## 简介
本项目演示了如何在 Go 中使用 Protocol Buffers（简称 Protobuf）进行高效的二进制序列化和反序列化。Protobuf 是一种语言中立、平台中立的机制，用于序列化结构化数据，常用于微服务通信和数据存储。

## 学习目标
- 理解 Protobuf 的基本概念与优势
- 掌握 `.proto` 文件定义消息格式的方法
- 学会使用 `protoc` 编译器生成 Go 代码
- 实践序列化与反序列化操作
- 比较 Protobuf 与其他格式（如 JSON）的空间效率

## 环境要求
- Go 1.19 或更高版本
- protoc 编译器（v3.20+）
- git（用于下载依赖）

## 安装依赖的详细步骤

### 1. 安装 Go
请访问 [https://golang.org/dl/](https://golang.org/dl/) 下载并安装适合你系统的 Go 版本。

验证安装：
```bash
go version
# 预期输出: go version go1.19.x linux/amd64 (或对应系统架构)
```

### 2. 安装 protoc 编译器
#### macOS:
```bash
brew install protobuf
```

#### Linux (Ubuntu):
```bash
sudo apt-get update
sudo apt-get install -y protobuf-compiler
```

#### Windows:
从 GitHub 下载预编译二进制文件：
[https://github.com/protocolbuffers/protobuf/releases](https://github.com/protocolbuffers/protobuf/releases)
解压后将 `protoc.exe` 添加到 PATH。

验证安装：
```bash
protoc --version
# 预期输出: libprotoc 3.20.x
```

### 3. 安装 Go Protobuf 插件
```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.31.0
```
确保 `$GOPATH/bin` 在你的 `PATH` 环境变量中。

## 文件说明
- `person.proto`: 定义 Person 消息结构的 Protobuf schema 文件
- `main.go`: 主程序，演示序列化与反序列化流程
- `go.mod`: Go 模块依赖声明文件

## 逐步实操指南

### 步骤 1: 初始化模块
```bash
go mod init protobuf-demo
```

### 步骤 2: 生成 Go 代码
```bash
protoc --go_out=. --go_opt=paths=source_relative person.proto
```
此命令会生成 `person.pb.go` 文件。

### 步骤 3: 运行程序
```bash
go run main.go
```

### 预期输出：
```
原始对象: name:"Alice" age:30 email:"alice@example.com"
序列化后的字节长度: 28
反序列化后对象: name:"Alice" age:30 email:"alice@example.com"
```

## 代码解析

### person.proto
```protobuf	syntax = "proto3";
package main;

message Person {
  string name = 1;
  int32 age = 2;
  string email = 3;
}
```
- `proto3` 语法更简洁，默认字段不为 null
- 字段编号用于二进制编码，不能重复

### main.go
- 使用 `proto.Marshal()` 将结构体编码为二进制
- 使用 `proto.Unmarshal()` 解码回结构体
- 输出字节长度以体现空间效率

## 常见问题解答

**Q: 报错找不到 protoc-gen-go？**
A: 确保 `$GOPATH/bin` 在 PATH 中，并重新运行 `go install` 命令。

**Q: 反序列化失败？**
A: 检查 proto 结构是否匹配，字段类型和编号必须一致。

**Q: 能否跨语言使用？**
A: 可以！Protobuf 支持 C++, Java, Python, JavaScript 等多种语言。

## 扩展学习建议
- 尝试添加嵌套消息（如 Address）
- 使用 gRPC 构建远程调用服务
- 对比 JSON 和 Protobuf 的性能差异
- 探索 `oneof`、`enum` 等高级特性