# Python 缓存技术 - 提升应用性能

> 学习 Python 中常见的缓存策略和实现，包括内存缓存、LRU 缓存、Redis 缓存和缓存失效模式。

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

- ✅ 理解缓存的收益和成本
- ✅ 使用 functools.lru_cache 实现本地缓存
- ✅ 使用 Redis 实现分布式缓存
- ✅ 处理缓存穿透、击穿和雪崩

---

## 📐 架构图

```
应用 ──▶ 查询缓存 ──▶ 命中？
         │
         ├─▶ 是：返回缓存数据
         └─▶ 否：查询数据库 ──▶ 写入缓存
```

---

## 🚀 快速开始

```bash
cd python/caching
pip install -r requirements.txt
python code/cache_demo.py
```

---

## 📖 核心概念

### 1. LRU Cache

最近最少使用缓存：

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 2. Redis 缓存

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.setex('user:1001', 3600, '{"name":"Alice"}')
```

### 3. 缓存问题

- 穿透：查询不存在的数据
- 击穿：热点 key 过期
- 雪崩：大量 key 同时过期

---

## 🧪 验证测试

```bash
python code/cache_demo.py
pytest tests/
```

---

## 📚 扩展学习

- [Python 异步编程](../async-programming/)
- [数据库缓存策略](../../database/caching-strategy-demo/)
- [Redis 官方文档](https://redis.io/docs/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 核心流程

Caching Demo 从启动到完成主要包含以下环节：

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

## 🌡️ 缓存模式

| 模式 | 说明 |
|------|------|
| Cache-Aside | 应用负责读写缓存 |
| Read-Through | 缓存代理数据库读取 |
| Write-Through | 写操作时同步写缓存 |
| Write-Behind | 异步写缓存，再批量写数据库 |

---

## 🧪 缓存测试

```python
@lru_cache(maxsize=2)
def expensive_function(x):
    return x * x

expensive_function(1)
expensive_function(2)
expensive_function(3)  # 可能淘汰 1
```


---

## 🐍 Python 缓存库

| 库 | 特点 |
|----|------|
| functools.lru_cache | 内置，简单易用 |
| cachetools | 支持 TTL、LRU、LFU |
| diskcache | 本地磁盘缓存 |
| redis-py | 分布式缓存 |

---

## 📝 缓存键设计

```python
def cache_key(user_id, date):
    return f"user:{user_id}:stats:{date}"
```

好的缓存键应该唯一、可读且易于失效。


---

## 🔄 缓存更新策略

| 策略 | 说明 |
|------|------|
| Cache-Aside | 应用管理缓存，常用 |
| Write-Through | 写时同步更新缓存 |
| Write-Behind | 异步批量更新缓存 |
| Refresh-Ahead | 提前刷新即将过期的缓存 |

选择合适的更新策略可以保证数据一致性和系统性能。
