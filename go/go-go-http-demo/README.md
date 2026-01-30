# Go HTTP客户端实战演示

## 简介
本示例演示了在Go语言中如何使用标准库`net/http`发送HTTP请求的三种常见场景：
- 基础GET请求
- 带自定义Header的POST请求
- 使用超时控制的客户端配置

所有代码均使用Go标准库，无需第三方依赖。

## 学习目标
- 掌握Go中发起HTTP请求的基本方法
- 理解http.Client和http.Request的使用
- 学会处理响应和错误
- 了解如何设置请求超时和自定义头信息

## 环境要求
- Go 1.19 或更高版本
- 操作系统：Windows、Linux、macOS（跨平台兼容）

## 安装依赖的详细步骤
本项目仅使用Go标准库，无需额外安装依赖。只需确保已安装Go环境：

```bash
# 检查Go版本
go version
# 预期输出：go version go1.19.x os/arch
```

## 文件说明
- `main.go` - 主程序，包含三个HTTP请求示例
- `client.go` - 封装的HTTP客户端工具

## 逐步实操指南

### 步骤1: 创建项目目录
```bash
mkdir go-http-demo && cd go-http-demo
```

### 步骤2: 初始化Go模块
```bash
go mod init http-demo
```

### 步骤3: 创建代码文件
将以下内容分别保存为对应文件名。

### 步骤4: 运行程序
```bash
go run main.go
```

**预期输出**：
```
=== 基础GET请求 ===
响应状态: 200 OK
响应长度: 13 (示例)

=== POST请求（带JSON）===
响应状态: 201 Created
响应体: {\"id\":101}

=== 带超时的GET请求 ===
响应状态: 200 OK
请求耗时: 45ms
```

## 代码解析

### main.go
- 使用`http.Get()`快速发起GET请求
- 使用`http.NewRequest()`构建自定义POST请求
- 设置`Content-Type: application/json`头
- 使用`http.Client{Timeout: time.Second * 10}`设置超时

### client.go
- 封装通用的HTTP请求函数
- 统一处理错误和资源释放
- 使用`defer response.Body.Close()`防止内存泄漏

## 常见问题解答

**Q: 运行时报错`command not found: go`？**
A: 请先安装Go语言环境，访问 https://golang.org/dl/ 下载安装。

**Q: 请求总是超时？**
A: 检查网络连接，或尝试更换测试API地址（如https://httpbin.org/get）。

**Q: 如何添加更多Header？**
A: 使用`req.Header.Set("Key", "Value")`继续添加即可。

## 扩展学习建议
- 学习使用`context.Context`控制请求取消
- 尝试使用第三方库如`resty`简化HTTP操作
- 实现重试机制和日志记录
- 学习HTTPS证书处理和自定义Transport