# 🟢 Node.js技术栈完整指南

> Node.js从基础到全栈开发的完整学习体系，包含71个核心案例

## 🚀 快速入门

想要快速上手Node.js开发？查看我们的 [Node.js CLI 命令行速查表](./cli/nodejs-cli.md) 获取npm/yarn包管理、调试工具和部署命令！

## 📋 技术栈概述

Node.js是一个基于Chrome V8引擎的JavaScript运行时环境，用于构建快速、可扩展的网络应用。本技术栈提供从前端到后端的完整JavaScript开发生态学习路径。

### 🔧 核心技能覆盖

- **ES6+语法**: 箭头函数、解构赋值、模块系统、Promise
- **核心模块**: HTTP、文件系统、路径处理、Buffer操作
- **Web框架**: Express、NestJS、Koa等主流框架
- **异步编程**: Promise、Async/Await、事件循环
- **DevOps工具**: 集群部署、PM2进程管理、监控
- **数据库集成**: MongoDB、MySQL、Redis等
- **实时通信**: Socket.IO、WebSocket

### 🎯 适用人群

- JavaScript/前端开发者
- 全栈开发工程师
- 后端API开发者
- 实时应用开发者
- 微服务架构师

---

## 📚 学习路径

### ES6+语法系列 (约20个案例)
掌握现代JavaScript语法特性和最佳实践。

### 核心模块系列 (约15个案例)
深入理解Node.js核心API和模块系统。

### Web框架系列 (约15个案例)
学习主流Web框架的使用和最佳实践。

### 企业级开发系列 (约15个案例)
掌握生产环境部署、监控、性能优化等技能。

---

## 🚀 快速开始

```bash
# 查看所有Node.js案例
opendemo search nodejs

# 获取基础语法案例
opendemo get nodejs variables-basics

# 获取Web框架案例
opendemo get nodejs express-restful-api
```

---

## 📊 案例统计

| 分类 | 案例数量 | 状态 |
|------|----------|------|
| ES6+语法 | ~20 | ✅ 基本完成 |
| 核心模块 | ~15 | ✅ 基本完成 |
| Web框架 | ~15 | ✅ 基本完成 |
| 企业级开发 | ~15 | ✅ 基本完成 |
| **总计** | **67** | ✅ |

---

## 📚 详细目录

### ES6+语法特性
<details>
<summary>点击查看完整列表</summary>

- 变量基础(let/const)
- 箭头函数
- 模板字符串
- 类与继承
- Symbol/Iterator
- Map/Set数据结构
- Proxy/Reflect
- 对象操作

</details>

### 异步编程
<details>
<summary>点击查看完整列表</summary>

- Promise异步
- Async/Await
- Generator异步控制
- Stream流

</details>

### 核心模块
<details>
<summary>点击查看完整列表</summary>

- HTTP模块
- 文件系统操作
- Path路径处理
- Buffer缓冲区
- JSON处理
- OS系统监控
- 环境变量

</details>

### Web框架
<details>
<summary>点击查看完整列表</summary>

- Express RESTful API
- NestJS框架
- TypeScript Express
- 中间件链
- GraphQL API
- Swagger/OpenAPI

</details>

### DevOps/SRE
<details>
<summary>点击查看完整列表</summary>

- Prometheus指标采集
- 健康检查
- 优雅关闭
- 日志管理
- Cluster集群负载均衡
- PM2多进程部署
- Worker多线程
- Docker SDK容器管理

</details>

---

## 🛠️ 开发环境配置

```bash
# 安装Node.js
# 推荐版本: Node.js 16+ LTS

# 验证安装
node --version
npm --version

# 安装常用工具
npm install -g nodemon pm2 typescript ts-node

# 初始化项目
npm init -y
```

---

## 📖 学习建议

1. **理解异步**: Node.js的核心是异步I/O，这是学习的重点
2. **掌握生态**: 熟悉npm生态系统和常用包
3. **性能优化**: 学习事件循环、内存管理等性能相关知识
4. **错误处理**: 掌握Node.js的错误处理模式
5. **实践经验**: 通过实际项目加深理解

---

## 🤝 贡献指南

欢迎提交新的Node.js案例或改进现有案例：
- 遵循JavaScript/Node.js最佳实践
- 提供现代化的代码示例
- 确保案例的实用性和时效性
- 遵循统一的文档格式

---

> **💡 提示**: Node.js特别适合构建I/O密集型应用和实时应用，在现代Web开发中占据重要地位。

## 🔗 相关技术栈交叉引用

### 与Java的关联
- [Java基础语法](../java/README.md) - 静态类型vs动态类型
- [Java类与继承](../java/java-inheritance-demo/) - 类继承vs原型继承

### 与Python的关联
- [Python基础语法](../python/README.md) - 动态类型语言对比
- [Python异步编程](../python/async-programming/) - asyncio vs Promise

### 与Go的关联
- [Go基础语法](../go/README.md) - 静态类型语言对比
- [Go并发模型](../go/go-goroutines-demo/) - CSP vs 事件循环