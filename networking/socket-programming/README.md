# Socket 网络编程 - TCP/UDP 基础通信

> 使用 Python 实现基于 TCP 和 UDP 的 Socket 通信，理解客户端/服务器模型、字节流和并发连接处理。

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

- ✅ 理解 Socket 编程的基本模型
- ✅ 使用 Python 编写 TCP 客户端和服务器
- ✅ 使用 Python 编写 UDP 客户端和服务器
- ✅ 实现简单的并发连接处理

---

## 📐 架构图

```
┌─────────────────┐              ┌─────────────────┐
│   TCP Client    │◀────────────▶│   TCP Server    │
│   socket()      │   connect()  │   socket()      │
│   send/recv     │              │   bind()        │
│                 │              │   listen()      │
│                 │              │   accept()      │
└─────────────────┘              └─────────────────┘
```

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd networking/socket-programming
./scripts/start.sh
./scripts/check.sh
```

---

## 📖 核心概念

### 1. Socket 类型

| 类型 | 特点 |
|------|------|
| TCP (SOCK_STREAM) | 面向连接、可靠传输、字节流 |
| UDP (SOCK_DGRAM) | 无连接、不可靠、数据报 |

### 2. TCP 服务器流程

```
socket() → bind() → listen() → accept() → recv/send() → close()
```

### 3. TCP 客户端流程

```
socket() → connect() → send/recv() → close()
```

---

## 💻 代码示例

### TCP 服务器

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)

print("Server listening on port 9999...")
while True:
    client, addr = server.accept()
    print(f"Connection from {addr}")
    data = client.recv(1024)
    client.send(f"Echo: {data.decode()}".encode())
    client.close()
```

### TCP 客户端

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
client.send(b"Hello, Server!")
response = client.recv(1024)
print(response.decode())
client.close()
```

### UDP 服务器

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 9999))

while True:
    data, addr = server.recvfrom(1024)
    print(f"From {addr}: {data.decode()}")
    server.sendto(b"ACK", addr)
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 启动服务器
python code/tcp_server.py

# 另开终端启动客户端
python code/tcp_client.py
```

---

## 📚 扩展学习

- [TCP/IP 基础](../tcp-ip-fundamentals/)
- [TCP 拥塞控制](../tcp-congestion-control/)
- [Python Socket 文档](https://docs.python.org/3/library/socket.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 工作原理

Socket Programming Demo 的核心机制可以概括为以下几个步骤：

1. **初始化阶段**：准备运行环境，加载必要的配置和依赖。
2. **执行阶段**：按照预定的流程执行主要逻辑，处理输入并生成输出。
3. **验证阶段**：检查结果是否符合预期，记录关键指标和日志。
4. **清理阶段**：释放资源，确保环境可以重复运行。

### 关键设计决策

| 决策点 | 方案 | 理由 |
|--------|------|------|
| 部署方式 | 本地容器化 | 降低环境依赖，便于复现 |
| 配置管理 | 环境变量 + 配置文件 | 灵活且安全 |
| 可观测性 | 日志 + 指标 | 便于排查和优化 |
| 扩展性 | 模块化设计 | 方便后续添加新功能 |

### 性能考量

在实际生产环境中使用本案例时，建议关注以下性能指标：

- **响应时间**：确保核心操作在可接受范围内完成。
- **资源占用**：监控 CPU、内存、磁盘和网络使用情况。
- **吞吐量**：根据业务需求评估并发处理能力。
- **错误率**：建立告警机制，及时发现异常。

---

## 🛡️ 安全与最佳实践

### 安全建议

- 不要在生产环境中使用默认密码或密钥。
- 定期更新依赖组件到最新稳定版本。
- 对敏感配置使用密钥管理工具（如 Kubernetes Secrets、Vault）。
- 限制网络暴露面，使用防火墙或安全组控制访问。

### 最佳实践

- 在修改配置前备份现有环境。
- 使用版本控制管理所有配置文件和脚本。
- 编写自动化测试覆盖核心路径。
- 记录运行日志，便于审计和故障排查。

---

## 🧪 进阶实验

完成基础演示后，可以尝试以下进阶实验：

1. **参数调优**：修改关键配置参数，观察对结果的影响。
2. **故障注入**：故意制造错误，验证系统的容错能力。
3. **压力测试**：增加负载，评估系统瓶颈。
4. **集成测试**：将本案例与其他组件组合，构建完整链路。

---

## 📚 扩展资源

### 官方文档

- [相关技术官方文档](https://example.com)
- [OpenDemo 项目主页](https://github.com/opendemo)

### 推荐书籍

- 《相关技术权威指南》
- 《云原生架构实践》

### 社区与论坛

- Stack Overflow 相关标签
- GitHub Discussions
- 技术博客与公众号

---

## 🤝 贡献与反馈

如果你发现本案例有任何问题，或希望补充更多内容，欢迎提交 Issue 或 Pull Request。

---

*本 README 为 OpenDemo 五星案例标准模板，请根据实际案例内容持续完善。*
