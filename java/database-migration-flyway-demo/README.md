# Flyway 数据库迁移 - 版本化管理 Schema

> 使用 Flyway 管理 Spring Boot 应用的数据库 Schema 版本，演示迁移脚本编写、执行和回滚策略。

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

- ✅ 理解数据库版本迁移的重要性
- ✅ 使用 Flyway 编写和执行迁移脚本
- ✅ 配置 Spring Boot 集成 Flyway
- ✅ 管理迁移的版本号和命名规范

---

## 📐 架构图

```
应用启动 ──▶ Flyway ──▶ 检查 Schema 版本 ──▶ 执行未应用迁移
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 |
|------|----------|
| JDK | >= 17 |
| Maven | >= 3.8 |
| MySQL/PostgreSQL/H2 | - |

### 启动

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd java/database-migration-flyway-demo
mvn spring-boot:run
```

---

## 📖 核心概念

### 1. 迁移脚本命名

```
V1__create_users_table.sql
V2__add_email_index.sql
V3__insert_initial_data.sql
```

- `V`：版本化迁移
- 数字：版本号
- 双下划线：分隔符
- 描述：脚本功能

### 2. Flyway 表

Flyway 自动创建 `flyway_schema_history` 表记录已执行的迁移。

### 3.  repeatable 迁移

以 `R__` 开头的脚本，在 checksum 变化时重复执行，适合视图、存储过程。

---

## 💻 代码示例

### application.yml 配置

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/demo
    username: root
    password: rootpass
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
```

### 迁移脚本

```sql
-- db/migration/V1__create_users_table.sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- db/migration/V2__add_email_index.sql
CREATE INDEX idx_users_email ON users(email);
```

### 查看迁移状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn flyway:info
```

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 执行迁移
mvn flyway:migrate

# 查看数据库
mysql -uroot -prootpass demo -e "SELECT * FROM flyway_schema_history"
```

---

## 📚 扩展学习

- [Spring Cloud Gateway](../spring-cloud-gateway-demo/)
- [MySQL 高可用架构](../../database/mysql-high-availability-demo/)
- [Flyway 官方文档](https://documentation.red-gate.com/flyway/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 核心流程

database-migration-flyway-demo 从启动到完成主要包含以下环节：

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

## 🔄 Flyway 迁移最佳实践

1. 每个迁移脚本只做一件事
2. 不要修改已执行的迁移脚本
3. 使用有意义的描述命名
4. 生产环境先备份数据库
5. 将迁移纳入 CI/CD 流程

---

## 🛠️ 修复错误迁移

如果迁移失败，需要先修复脚本，然后：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 修复失败记录（谨慎使用）
mvn flyway:repair

# 重新执行
mvn flyway:migrate
```
