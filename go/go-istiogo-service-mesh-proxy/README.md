# Istio代理服务网格Go演示

## 简介
本项目是一个简化的Go语言演示，模拟了Istio服务网格中Envoy代理的部分核心行为，如请求拦截、日志记录和服务路由。通过本Demo，开发者可以理解服务网格中sidecar代理如何在微服务之间透明地处理通信。

## 学习目标
- 理解Istio中sidecar代理的基本职责
- 掌握使用Go实现HTTP请求拦截与转发
- 学会使用Gin框架构建轻量级代理服务
- 了解服务网格中的可观测性（日志）实现方式

## 环境要求
- Go 1.19 或更高版本
- 操作系统：Windows、Linux、macOS 均支持
- curl 或浏览器用于测试

## 安装依赖步骤
1. 安装Go语言环境：
   ```bash
   # 验证安装
   go version
   # 输出应类似：go version go1.21.0 linux/amd64
   ```

2. 初始化Go模块并下载依赖：
   ```bash
   go mod init istio-proxy-demo
   go mod tidy
   ```

## 文件说明
- `main.go`：主代理服务，监听8080端口，拦截并转发请求
- `service.go`：模拟后端服务，运行在8081端口
- `README.md`：本说明文档

## 逐步实操指南

### 步骤1：启动后端服务
```bash
go run service.go
```
**预期输出**：
```
后端服务启动于 :8081
```

### 步骤2：启动代理服务（新终端）
```bash
go run main.go
```
**预期输出**：
```
Istio风格代理启动于 :8080
```

### 步骤3：发送测试请求
```bash
curl http://localhost:8080/api/hello
```

**预期输出**：
```
Hello from backend via Istio proxy!\n```

同时在代理终端中应看到日志输出：
```
[PROXY] 请求被拦截: GET /api/hello -> 转发至 http://localhost:8081/api/hello
```

## 代码解析

### main.go 关键逻辑
- 使用Gin创建中间件，在请求转发前记录日志
- 代理将所有请求转发至本地8081端口的后端服务
- 模拟了Istio中透明流量劫持和可观测性功能

### service.go 功能
- 提供简单的HTTP接口 `/api/hello`
- 模拟微服务中的业务逻辑响应

## 预期输出示例
### 代理输出：
```
Istio风格代理启动于 :8080
[PROXY] 请求被拦截: GET /api/hello -> 转发至 http://localhost:8081/api/hello
```

### 客户端curl输出：
```
Hello from backend via Istio proxy!\n```

## 常见问题解答

**Q: 启动时报错 'cannot find package'？**
A: 请确保已执行 `go mod tidy` 下载依赖。

**Q: curl返回连接拒绝？**
A: 请确认 `service.go` 已先于 `main.go` 启动。

**Q: 如何扩展支持HTTPS？**
A: 可使用 `ListenAndServeTLS` 并配置证书路径，Istio中由Citadel自动管理证书。

## 扩展学习建议
- 尝试添加JWT验证模拟mTLS
- 集成OpenTelemetry实现分布式追踪
- 使用eBPF技术深入理解流量劫持机制
- 阅读Istio官方文档中的Sidecar资源配置