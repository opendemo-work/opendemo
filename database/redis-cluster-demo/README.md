# Redis 集群模式演示 - 分布式缓存高可用

> 使用 Docker Compose 部署 Redis Cluster（6 节点，3 主 3 从），演示数据分片、主从复制、故障转移和集群扩缩容。

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

- ✅ 理解 Redis Cluster 的数据分片原理
- ✅ 部署 3 主 3 从的 Redis Cluster
- ✅ 验证主从复制和自动故障转移
- ✅ 使用 redis-cli 进行集群操作
- ✅ 了解集群扩缩容的基本流程

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Redis Cluster 架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   客户端 ──▶ Redis Cluster (CRC16 槽位映射)                     │
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                   │
│   │ Master 1│    │ Master 2│    │ Master 3│                   │
│   │ 0-5460  │    │ 5461-10922│   │10923-16383│                │
│   │ Replica │    │ Replica │    │ Replica │                   │
│   │ Slave 1 │    │ Slave 2 │    │ Slave 3 │                   │
│   └─────────┘    └─────────┘    └─────────┘                   │
│                                                                 │
│        16384 个槽位均匀分配到 3 个主节点                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Redis 节点 |
| Docker Compose | >= 1.29 | 编排 6 个节点 |
| 内存 | >= 2GB | 6 个 Redis 实例 |

### 启动集群

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd database/redis-cluster-demo
./scripts/start.sh
sleep 10
./scripts/check.sh
```

### 创建集群

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 进入第一个 Redis 节点容器
docker exec -it redis-node-1 redis-cli --cluster create \
  172.20.0.11:6379 172.20.0.12:6379 172.20.0.13:6379 \
  172.20.0.14:6379 172.20.0.15:6379 172.20.0.16:6379 \
  --cluster-replicas 1 --cluster-yes
```

---

## 📖 核心概念

### 1. 数据分片（Sharding）

Redis Cluster 将 16384 个槽位（slot）分配到不同主节点：

- 每个 key 通过 `CRC16(key) % 16384` 计算槽位
- 客户端根据槽位路由到对应主节点
- 使用 `{tag}` 实现相关 key 的强制同槽位

### 2. 主从复制

每个主节点可以有多个从节点，当主节点故障时，从节点可以提升为主节点。

### 3. 故障转移

- 主节点之间通过 Gossip 协议通信
- 当某个主节点不可达时，其从节点发起选举
- 选举成功后，从节点晋升为主节点

### 4. MOVED 和 ASK 重定向

- **MOVED**：槽位已永久迁移到另一个节点
- **ASK**：槽位正在迁移中，需要临时访问目标节点

---

## 💻 代码示例

### 查看集群信息

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 连接任意节点
docker exec -it redis-node-1 redis-cli -c -p 6379

# 查看集群节点
CLUSTER NODES

# 查看集群槽位分配
CLUSTER SLOTS

# 查看集群状态
CLUSTER INFO
```

### 数据写入与读取

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用 -c 参数支持自动重定向
docker exec -it redis-node-1 redis-cli -c -p 6379

127.0.0.1:6379> SET user:1001 "Alice"
-> Redirected to slot [8325] located at 172.20.0.12:6379
OK

127.0.0.1:6379> GET user:1001
-> Redirected to slot [8325] located at 172.20.0.12:6379
"Alice"
```

### 使用 Hash Tag

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
127.0.0.1:6379> SET {user:1001}:name "Alice"
127.0.0.1:6379> SET {user:1001}:age 25
# 两个 key 会落在同一槽位
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `docker-compose.yml` | 定义 6 个 Redis 节点 |
| `configs/redis.conf` | Redis 集群配置 |
| `scripts/create-cluster.sh` | 创建集群脚本 |

### Redis 集群配置关键项

```conf
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 检查集群状态
docker exec redis-node-1 redis-cli -c CLUSTER INFO

# 2. 测试故障转移：停止一个主节点
docker stop redis-node-1
sleep 10

# 3. 查看是否自动故障转移
docker exec redis-node-2 redis-cli -c CLUSTER NODES

# 4. 恢复节点
docker start redis-node-1
```

---

## 📊 运行结果

```
$ docker exec redis-node-1 redis-cli -c CLUSTER INFO
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_known_nodes:6
cluster_size:3
```

---

## 🐛 常见问题

### Q1：集群创建失败？

**A**：确保所有节点都已启动并可以互相通信，检查 `cluster-announce-ip` 配置是否正确。

### Q2：客户端连接报错 CLUSTERDOWN？

**A**：说明部分槽位没有分配或节点不可用，检查 `CLUSTER SLOTS` 输出。

### Q3：故障转移没有自动发生？

**A**：检查 `cluster-node-timeout` 是否太短或太长，以及从节点是否正常运行。

---

## 📚 扩展学习

- [MySQL 高可用架构](../mysql-high-availability-demo/)
- [PostgreSQL 高可用架构](../postgresql-high-availability-demo/)
- [Redis 官方集群教程](https://redis.io/docs/management/scaling/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
