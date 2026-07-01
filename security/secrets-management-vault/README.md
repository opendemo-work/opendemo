# Secrets Management with Vault - 应用凭据安全管理

> 演示如何在应用程序中安全地管理和使用敏感凭据，通过 Vault 实现凭据集中存储、动态签发和自动轮换。

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

- ✅ 理解硬编码凭据的安全风险
- ✅ 使用 Vault 作为应用的 Secrets 管理中心
- ✅ 通过 AppRole 或 Kubernetes 认证让应用获取凭据
- ✅ 实现数据库动态凭据，避免长期有效账号

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    应用凭据管理架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Application ──▶ Vault Agent / SDK ──▶ Vault Server            │
│        │                                      │                 │
│        │                              ┌───────┴───────┐        │
│        │                              │ Database      │        │
│        ▼                              │ Secrets Engine│        │
│   获取临时凭据                        └───────┬───────┘        │
│        │                                      │                 │
│        └──────────────────────────────▶ 数据库连接              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```bash
cd security/secrets-management-vault
./scripts/start.sh
sleep 10
./scripts/check.sh
```

---

## 📖 核心概念

### 1. 硬编码凭据的风险

- 代码泄露导致凭据泄露
- 轮换困难，长期有效凭据风险高
- 权限无法精细化管理

### 2. Vault AppRole

为应用提供身份认证方式，包含 RoleID 和 SecretID：

```bash
vault auth enable approle
vault write auth/approle/role/myapp \
  token_policies="myapp-db-policy" \
  token_ttl=1h \
  token_max_ttl=4h
```

### 3. 动态数据库凭据

Vault 可以按需创建临时数据库用户并自动回收：

```bash
vault secrets enable database
vault write database/config/my-mysql \
  plugin_name=mysql-rotate-root \
  connection_url="{{username}}:{{password}}@tcp(mysql:3306)/" \
  allowed_roles="app-readonly"
```

---

## 💻 代码示例

### Python 应用读取 Vault 凭据

```python
import hvac

client = hvac.Client(url='http://localhost:8200')
client.auth.approle.login(
    role_id='your-role-id',
    secret_id='your-secret-id'
)

secret = client.secrets.kv.v2.read_secret_version(
    path='myapp/database'
)
print(secret['data']['data'])
```

### 数据库动态凭据

```bash
# 读取动态凭据
vault read database/creds/app-readonly

# 输出示例
Key                Value
---                -----
lease_id           database/creds/app-readonly/abc123
lease_duration     1h
username           v-token-app-readonly-abc
password           xxxxxxxxxxxxxxxx
```

---

## 🧪 验证测试

```bash
# 检查 Vault 服务
curl -s http://localhost:8200/v1/sys/health

# 测试 AppRole 登录
vault write auth/approle/login role_id=... secret_id=...
```

---

## 📚 扩展学习

- [密钥管理基础](../crypto-key-management/)
- [Vault 官方文档](https://developer.hashicorp.com/vault/docs)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*


---

## 📖 深入理解

### 工作原理

Secrets Management with Vault 的核心机制可以概括为以下几个步骤：

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
