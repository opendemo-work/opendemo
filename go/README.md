# 🐹 Go技术栈完整指南

> Go语言从基础到企业级应用的完整学习体系，包含95个基础案例和1个第三方库案例

## 📋 技术栈概述

Go（又称Golang）是由Google开发的开源编程语言，以其简洁的语法、出色的并发支持和高效的性能而著称。本技术栈提供从基础语法到企业级开发的完整学习路径。

### 🔧 核心技能覆盖

- **基础语法**: 变量、数据类型、控制结构、函数、方法
- **并发编程**: Goroutines、Channels、Select、Mutex
- **Web开发**: HTTP服务、RESTful API、中间件、Web框架
- **数据处理**: JSON处理、数据库操作、ORM框架
- **DevOps工具**: 监控、日志、配置管理、容器化
- **企业级应用**: 微服务、RPC、消息队列、缓存

### 🎯 适用人群

- Go语言初学者
- 后端开发工程师
- 微服务架构师
- DevOps工程师
- 系统程序员

---

## 📚 学习路径

### 基础语法系列 (约70个案例)
从变量类型到并发编程，全面掌握Go语言核心特性。

### 企业级开发系列 (约20个案例)
学习Web开发、微服务、DevOps等企业级应用场景。

### 第三方库系列 (1个案例)
掌握常用的第三方库和工具。

---

## 🚀 快速开始

```bash
# 查看所有Go案例
opendemo search go

# 获取基础语法案例
opendemo get go variables-types

# 获取Web开发案例
opendemo get go http-server
```

---

## 📊 案例统计

| 分类 | 案例数量 | 状态 |
|------|----------|------|
| 基础语法 | ~70 | ✅ 基本完成 |
| 企业级开发 | ~20 | ✅ 基本完成 |
| 第三方库 | 1 | ✅ 完成 |
| 排查工具 | 1 | ✅ 新增 |
| **总计** | **94** | ✅ |

---

## 📚 详细目录

### 基础语法与数据结构
<details>
<summary>点击查看完整列表</summary>

- 变量与类型
- 控制流语句
- Map映射操作
- JSON处理
- 常量与枚举
- 错误处理
- Defer延迟执行
- Panic/Recover机制

</details>

### 并发编程
<details>
<summary>点击查看完整列表</summary>

- Goroutines基础
- Channel通道
- Select多路复用
- Mutex/WaitGroup
- 工作池模式
- Context上下文
- 超时控制

</details>

### Web开发
<details>
<summary>点击查看完整列表</summary>

- HTTP基础
- RESTful API
- HTTP中间件
- Gin Web框架
- GORM ORM框架
- Swagger文档
- WebSocket实时通信

</details>

### DevOps/SRE
<details>
<summary>点击查看完整列表</summary>

- Prometheus指标采集
- 健康检查监控
- 优雅关闭
- Zap结构化日志
- ELK日志聚合
- 日志轮转
- OpenTelemetry分布式追踪
- Consul服务发现
- Istio服务网格
- Docker多阶段构建

</details>

---

## 🛠️ 开发环境配置

```bash
# 安装Go
# 推荐版本: Go 1.19+

# 验证安装
go version

# 设置工作空间
mkdir ~/go-workspace
export GOPATH=~/go-workspace

# 安装常用工具
go install golang.org/x/tools/gopls@latest
go install github.com/go-delve/delve/cmd/dlv@latest
```

---

## 📖 学习建议

1. **重视并发**: Go的并发模型是其核心优势，要重点掌握
2. **接口优先**: 学会使用接口进行抽象和解耦
3. **错误处理**: 掌握Go的错误处理哲学
4. **工具链**: 熟悉Go的工具链和生态系统
5. **实践项目**: 通过实际项目巩固所学知识

---

## 🤝 贡献指南

欢迎提交新的Go案例或改进现有案例：
- 遵循Go语言的最佳实践
- 提供清晰的代码示例和说明
- 确保案例的实用性和教育价值
- 遵循统一的文档格式

---

> **💡 提示**: Go语言特别适合构建高性能的后端服务和微服务架构，在云原生时代具有重要地位。

## 🔗 相关技术栈交叉引用

### 与Java的关联
- [Java基础语法](../java/README.md) - 面向对象编程
- [Java并发编程](../java/java-threading-demo/) - 线程vs Goroutines

### 与Python的关联
- [Python基础语法](../python/README.md) - 动态类型语言对比
- [Python并发](../python/multithreading/) - 多线程vs Goroutines

### 与Node.js的关联
- [Node.js异步编程](../nodejs/nodejs-promises-demo/) - 事件循环机制
- [Node.js并发](../nodejs/nodejs-worker-threads-multithreading-demo/) - 多线程vs Goroutines