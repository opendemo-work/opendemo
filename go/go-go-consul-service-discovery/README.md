# Go 服务注册与发现 - Consul

> 使用 Go 语言和 Consul 实现微服务的服务注册、发现和健康检查。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解服务注册与发现的作用
- ✅ 使用 Consul 作为服务注册中心
- ✅ 使用 Go 客户端注册和发现服务
- ✅ 配置健康检查

---

## 📐 架构图

```
Service A ──▶ Consul Server ◀── Service B
                │
                ▼
           健康检查 / KV 存储
```

---

## 🚀 快速开始

```bash
cd go/go-go-consul-service-discovery
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. 服务注册

启动时向 Consul 注册服务信息（IP、端口、健康检查）。

### 2. 服务发现

通过 Consul API 或 DNS 查询可用服务实例。

### 3. 健康检查

Consul 定期检查服务健康状态，剔除不健康实例。

---

## 💻 代码示例

### 注册服务

```go
import "github.com/hashicorp/consul/api"

config := api.DefaultConfig()
client, _ := api.NewClient(config)

agent := client.Agent()
agent.ServiceRegister(&api.AgentServiceRegistration{
    ID:      "user-service-1",
    Name:    "user-service",
    Port:    8080,
    Tags:    []string{"v1"},
    Check: &api.AgentServiceCheck{
        HTTP:     "http://localhost:8080/health",
        Interval: "10s",
    },
})
```

### 发现服务

```go
services, _, _ := client.Health().Service("user-service", "", true, nil)
for _, svc := range services {
    fmt.Println(svc.Service.Address, svc.Service.Port)
}
```

---

## 🧪 验证测试

```bash
curl http://localhost:8500/v1/catalog/services
go test ./...
```

---

## 📚 扩展学习

- [Go Web 框架 Gin](../go-ginwebdemo-web-framework-intro/)
- [Go Channels](../go-go-channels-demo/)
- [Consul 官方文档](https://developer.hashicorp.com/consul/docs)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 核心流程

Go Consul 服务注册与发现演示 从启动到完成主要包含以下环节：

1. **环境准备**：配置运行所需的依赖、网络和存储资源。
2. **主流程执行**：运行案例的核心逻辑并产出结果。
3. **结果验证**：通过日志、命令输出或测试用例确认正确性。
4. **资源回收**：停止服务并清理临时数据，保证可重复执行。

### 设计要点

| 方面 | 做法 | 说明 |
|------|------|------|
| 部署方式 | 本地容器化 | 减少环境差异，便于复现 |
| 配置管理 | 配置文件 + 环境变量 | 兼顾可读性与灵活性 |
| 可观测性 | 日志 + 健康检查 | 方便定位问题 |
| 扩展方式 | 模块化组织 | 后续可按需增加功能 |

### 需要关注的指标

在生产环境中落地类似方案时，建议留意：

- 关键路径的响应延迟
- CPU、内存、磁盘和网络资源使用
- 并发量与吞吐量变化
- 错误率和异常告警

---

## 🛡️ 安全与最佳实践

### 安全建议

- 生产环境不要使用默认密码、密钥或令牌。
- 定期将依赖升级到稳定的最新版本。
- 敏感配置优先使用密钥管理工具或环境变量注入。
- 通过防火墙、安全组或网络策略限制访问范围。

### 操作建议

- 修改配置前备份现有环境。
- 将配置文件和脚本纳入版本控制。
- 为核心路径补充自动化测试。
- 保留运行日志以便审计和排障。

---

## 🧪 进阶实验

基础流程跑通后，可以尝试：

1. 调整关键参数，观察对结果的影响。
2. 模拟异常场景，验证容错能力。
3. 增加负载，分析系统瓶颈。
4. 与其他组件组合，形成完整链路。

---

## 📚 扩展资源

- 相关技术的官方文档
- [OpenDemo 项目主页](https://github.com/opendemo)
- GitHub Discussions 与技术社区

---

## 🤝 贡献与反馈

如发现内容有误或希望补充，欢迎提交 Issue 或 Pull Request。

---

*本 README 由 OpenDemo 自动生成并持续维护，欢迎根据实际案例补充细节。*


---

## 🏥 健康检查类型

Consul 支持多种健康检查：

| 类型 | 说明 |
|------|------|
| HTTP | 检查 HTTP 端点 |
| TCP | 检查 TCP 端口 |
| Script | 执行脚本检查 |
| TTL | 服务主动上报 |
| gRPC | gRPC 健康检查 |

---

## 🔄 服务发现模式

- **客户端发现**：客户端直接查询 Consul 选择实例
- **服务端发现**：通过 API Gateway 或 Load Balancer 代理


---

## 🛡️ Consul 安全

生产环境应启用 ACL 和 TLS：

```hcl
acl {
  enabled = true
  default_policy = "deny"
}

tls {
  defaults {
    ca_file = "consul-ca.pem"
    cert_file = "consul.pem"
    key_file = "consul-key.pem"
    verify_incoming = true
    verify_outgoing = true
  }
}
```
