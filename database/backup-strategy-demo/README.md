# 数据库备份策略演示 - 全量、增量与时间点恢复

> 使用 MySQL 演示全量备份、增量备份、binlog 备份和时间点恢复（PITR），建立完整的数据库备份策略。

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

- ✅ 理解 RTO 和 RPO 的概念
- ✅ 使用 mysqldump 进行逻辑备份
- ✅ 使用 Percona XtraBackup 进行物理备份
- ✅ 配置 binlog 实现增量备份和时间点恢复

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    数据库备份策略                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   业务数据 ──┬──▶ 全量备份（每日）                              │
│             ├──▶ 增量备份（binlog 每小时）                      │
│             └──▶ 异地归档                                       │
│                                                                 │
│   恢复流程：全量备份 + 增量 binlog ──▶ 目标时间点                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd database/backup-strategy-demo
./scripts/start.sh
sleep 20
./scripts/check.sh
```

---

## 📖 核心概念

### 1. RTO 与 RPO

- **RTO（Recovery Time Objective）**：恢复时间目标，业务可容忍的停机时间
- **RPO（Recovery Point Objective）**：恢复点目标，可容忍的数据丢失量

### 2. 备份类型

| 类型 | 工具 | 优点 | 缺点 |
|------|------|------|------|
| 逻辑备份 | mysqldump | 可读、跨版本 | 大库慢 |
| 物理备份 | XtraBackup | 快速、不影响业务 | 依赖版本 |
| 增量备份 | binlog | 精确到秒 | 需要完整链路 |

### 3. 时间点恢复

通过全量备份 + binlog 回放，恢复到指定时间点。

---

## 💻 代码示例

### 启用 binlog

```ini
[mysqld]
log_bin = mysql-bin
server_id = 1
binlog_format = ROW
expire_logs_days = 7
```

### 全量备份

```bash
# 逻辑备份
mysqldump -uroot -prootpass --all-databases --single-transaction > full-backup.sql

# 物理备份（需安装 xtrabackup）
xtrabackup --backup --target-dir=/backup/full
```

### 增量备份（基于 binlog）

```bash
# 刷新 binlog
mysql -uroot -prootpass -e "FLUSH LOGS"

# 复制 binlog
cp /var/lib/mysql/mysql-bin.000002 /backup/binlog/
```

### 时间点恢复

```bash
# 1. 恢复全量备份
mysql -uroot -prootpass < full-backup.sql

# 2. 使用 mysqlbinlog 回放 binlog 到指定时间点
mysqlbinlog --stop-datetime="2026-06-27 12:00:00" mysql-bin.000002 | mysql -uroot -prootpass
```

---

## 🧪 验证测试

```bash
# 检查 binlog 是否启用
mysql -uroot -prootpass -e "SHOW VARIABLES LIKE 'log_bin'"

# 查看 binlog 列表
mysql -uroot -prootpass -e "SHOW BINARY LOGS"
```

---

## 📚 扩展学习

- [MySQL 高可用架构](../mysql-high-availability-demo/)
- [灾难恢复](../disaster-recovery-demo/)
- [MySQL 备份恢复官方文档](https://dev.mysql.com/doc/refman/8.0/en/backup-and-recovery.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 工作原理

backup-strategy-demo 的核心机制可以概括为以下几个步骤：

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
