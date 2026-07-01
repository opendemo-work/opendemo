# 🗄️ Database 数据库技术栈

> 企业级数据库全生命周期管理实践，涵盖关系型数据库（MySQL/PostgreSQL）、NoSQL（MongoDB/Redis）以及云数据库、性能优化、高可用架构、安全合规等方向。

---

## 📚 技术栈概览

数据库是现代应用系统的核心组件。本技术栈提供从基础运维到企业级架构的完整学习路径，包含 37 个实战案例，覆盖以下主题：

- 数据库安装与配置
- 用户权限与访问控制
- 查询优化与索引设计
- 备份恢复与灾难恢复
- 主从复制与高可用架构
- 读写分离与负载均衡
- 缓存策略与连接池
- 监控告警与审计日志
- 云数据库与容器化部署
- 安全加固与合规认证

---

## 🎯 学习目标

完成本技术栈学习后，你将能够：

- ✅ 部署和管理主流关系型与 NoSQL 数据库
- ✅ 设计高可用、可扩展的数据库架构
- ✅ 诊断和解决常见数据库性能问题
- ✅ 制定完整的备份、恢复和容灾策略
- ✅ 满足安全合规和审计要求

---

## 📂 案例目录

| 案例 | 主题 |
|------|------|
| [MySQL 高可用架构](./mysql-high-availability-demo/) | 主从复制与故障切换 |
| [PostgreSQL 高可用架构](./postgresql-high-availability-demo/) | Patroni + etcd |
| [Redis 集群](./redis-cluster-demo/) | 分布式缓存 |
| [SQL 查询优化](./query-optimization-demo/) | 执行计划与索引 |
| [数据库备份策略](./backup-strategy-demo/) | 全量/增量/PITR |
| [数据库缓存策略](./caching-strategy-demo/) | 缓存穿透/击穿/雪崩 |
| [数据库安全加固](./security-hardening-demo/) | 访问控制与加密 |
| [数据仓库分层设计](./data-warehouse/dwd-dws-ads-layer-design/) | ODS/DWD/DWS/ADS |

... 共 37 个案例，详见各子目录。

---

## 🚀 快速开始

选择感兴趣的数据库方向，进入对应案例目录：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd database/mysql-high-availability-demo
./scripts/start.sh
./scripts/check.sh
```

---

## 🔗 相关技术栈

- [BigData](./../bigdata/) - 大数据处理与分析
- [Monitoring](./../monitoring/) - 数据库监控与告警
- [Security](./../security/) - 数据安全与合规

---

*最后更新：2026-07-01*  
*维护者：OpenDemo Team*
