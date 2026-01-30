# Go Consul 服务注册与发现演示

## 简介
本项目演示如何使用 Go 语言结合 HashiCorp Consul 实现微服务架构中的服务注册与发现。包含服务注册、健康检查和服务发现三个核心功能，适用于构建高可用的分布式系统。

## 学习目标
- 理解服务注册与发现的基本原理
- 掌握 Go 客户端与 Consul 交互的方法
- 实践健康检查机制的实现
- 学会在实际项目中集成服务发现

## 环境要求
- Go 1.20 或更高版本
- Consul 1.15.2（可通过 Docker 运行）
- 操作系统：Windows / Linux / macOS

## 安装依赖
```bash
# 1. 安装 Go 依赖
go mod init consul-demo
go get github.com/hashicorp/consul/api@v1.15.2

# 2. 启动本地 Consul 开发服务器（需安装 Docker）
docker run -d --name consul-dev -p 8500:8500 -p 8600:8600/udp consul:1.15.2 agent -dev -client=0.0.0.0 -ui
```

## 文件说明
- `main.go`：主服务程序，注册自身并定期发送健康检查
- `discovery.go`：服务发现客户端，查询并调用已注册的服务
- `go.mod`：Go 模块依赖声明文件

## 逐步实操指南

### 步骤 1：启动 Consul
```bash
docker run -d --name consul-dev -p 8500:8500 -p 8600:8600/udp consul:1.15.2 agent -dev -client=0.0.0.0 -ui
```
**预期输出**：返回容器ID，访问 http://localhost:8500 可看到 Consul Web UI

### 步骤 2：初始化项目并运行服务注册
```bash
go mod init consul-demo
go run main.go
```
**预期输出**：
```
服务 'demo-service' 已成功注册到 Consul
正在发送健康检查... (按 Ctrl+C 停止)
```

### 步骤 3：运行服务发现
在另一个终端窗口执行：
```bash
go run discovery.go
```
**预期输出**：
```
发现服务实例: demo-service @ 127.0.0.1:8080, 状态: passing
```

## 代码解析

### main.go 关键代码段
```go
// 创建 Consul 客户端配置
config := api.DefaultConfig()
config.Address = "127.0.0.1:8500"

// 注册服务到 Consul
registration := &api.AgentServiceRegistration{
    ID:      "demo-service-1",
    Name:    "demo-service",
    Address: "127.0.0.1",
    Port:    8080,
    Check: &api.AgentServiceCheck{
        HTTP:     "http://127.0.0.1:8080/health", // 健康检查端点
        Interval: "5s",                         // 每5秒检查一次
        Timeout:  "3s",
    },
}
```
> 解释：定义服务元数据和健康检查策略，Consul 将根据此配置监控服务状态。

### discovery.go 关键代码段
```go
// 查询健康的服务实例
serviceEntries, _, err := client.Health().Service("demo-service", "", true, nil)
if err != nil {
    log.Fatalf("服务发现失败: %v", err)
}

for _, entry := range serviceEntries {
    fmt.Printf("发现服务实例: %s @ %s:%d, 状态: %s\n",
        entry.Service.Service,
        entry.Node.Address,
        entry.Service.Port,
        entry.Checks.AggregatedStatus())
}
```
> 解释：通过 Health().Service() 获取处于健康状态的服务实例列表，实现安全的服务调用路由。

## 预期输出示例
### main.go 输出
```
服务 'demo-service' 已成功注册到 Consul
正在发送健康检查... (按 Ctrl+C 停止)
```

### discovery.go 输出
```
发现服务实例: demo-service @ 127.0.0.1:8080, 状态: passing
```

## 常见问题解答

**Q: 运行时报错无法连接到 Consul？**
A: 确保 Consul 容器已启动：`docker ps | grep consul`，若无输出则重新执行启动命令。

**Q: 服务在 Consul UI 中显示为 critical？**
A: 检查健康检查端点是否可达。本示例未实现 HTTP 服务，仅用于演示注册逻辑。生产环境应提供真实 `/health` 接口。

**Q: 如何在不同机器上部署？**
A: 修改 `config.Address` 为 Consul 服务器的实际 IP，并确保网络互通。

## 扩展学习建议
- 集成 gRPC 实现真实服务通信
- 使用 TLS 加密 Consul 客户端通信
- 实现服务注销的优雅关闭（defer deregister）
- 结合 Kubernetes 实现自动服务编排
- 探索 Consul 的 KV 存储用于配置管理