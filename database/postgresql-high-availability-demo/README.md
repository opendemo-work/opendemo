# PostgreSQL 高可用架构演示 - 流复制与 Patroni

> 使用 Docker Compose 部署 PostgreSQL 流复制集群，结合 Patroni + etcd 实现自动故障转移和高可用。

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

- ✅ 理解 PostgreSQL 流复制原理
- ✅ 部署 Patroni + etcd + HAProxy 高可用架构
- ✅ 验证主从切换和自动故障转移
- ✅ 使用 pg_basebackup 初始化从库

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL HA 架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   HAProxy ──▶ PostgreSQL Primary                                │
│   :5432        │                                                │
│                ├──▶ Standby 1 (流复制)                          │
│                └──▶ Standby 2 (流复制)                          │
│                                                                 │
│   Patroni ──▶ etcd (DCS 分布式配置存储)                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd database/postgresql-high-availability-demo
./scripts/start.sh
sleep 30
./scripts/check.sh
```

---

## 📖 核心概念

### 1. PostgreSQL 流复制

主库将 WAL（Write-Ahead Log）实时发送给从库，从库重放 WAL 保持数据一致。

### 2. Patroni

Patroni 是 PostgreSQL 高可用模板，提供：

- 自动故障检测
- 主从自动切换
- REST API 管理
- 与 etcd/ZooKeeper/Consul 集成

### 3. etcd

etcd 作为分布式协调服务（DCS），存储集群状态并选举主节点。

---

## 💻 代码示例

### Patroni 配置

```yaml
# configs/patroni.yml
scope: postgres-ha
namespace: /db/
name: node1

restapi:
  listen: 0.0.0.0:8008
  connect_address: node1:8008

etcd:
  hosts: etcd:2379

postgresql:
  listen: 0.0.0.0:5432
  connect_address: node1:5432
  data_dir: /var/lib/postgresql/data
  pgpass: /tmp/pgpass0
  authentication:
    replication:
      username: replicator
      password: repass
    superuser:
      username: postgres
      password: postgres
```

### 查看集群状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker exec patroni-node1 patronictl list
```

### 手动切换主节点

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
docker exec patroni-node1 patronictl switchover --master node1 --candidate node2 --force
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 连接 PostgreSQL
psql -h127.0.0.1 -p5432 -Upostgres -c "SELECT pg_is_in_recovery();"

# 停止主节点，观察自动切换
docker stop patroni-node1
sleep 10
docker exec patroni-node2 patronictl list
```

---

## 📚 扩展学习

- [MySQL 高可用架构](../mysql-high-availability-demo/)
- [Redis 集群](../redis-cluster-demo/)
- [Patroni GitHub](https://github.com/zalando/patroni)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 工作原理

PostgreSQL高可用架构完整指南 的核心机制可以概括为以下几个步骤：

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
