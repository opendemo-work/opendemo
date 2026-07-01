# 密钥管理基础 - HashiCorp Vault 实战

> 使用 Docker 部署 HashiCorp Vault，演示密钥的创建、轮换、访问控制和动态凭据签发，理解现代密钥管理的核心实践。

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

- ✅ 理解密钥管理的核心原则和威胁模型
- ✅ 使用 Vault 部署 Dev 模式进行学习和测试
- ✅ 创建和管理 KV 凭据引擎
- ✅ 配置策略（Policy）实现最小权限访问
- ✅ 理解动态凭据和自动轮换的价值

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Vault 密钥管理架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   应用/运维人员 ──▶ Vault Server ──▶ 存储后端                   │
│        │                │                                       │
│        │                ├─▶ KV Secrets Engine                   │
│        │                ├─▶ Database Secrets Engine             │
│        │                ├─▶ PKI Secrets Engine                  │
│        │                └─▶ Transit Encryption Engine           │
│        │                                                        │
│        ▼                                                        │
│   认证方式（Token/Kubernetes/AppRole/LDAP）                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 Vault 容器 |
| Docker Compose | >= 1.29 | 编排服务 |
| Vault CLI | >= 1.13 | 可选，用于命令行操作 |

### 启动 Vault

```bash
cd security/crypto-key-management
./scripts/start.sh
sleep 5
./scripts/check.sh
```

### 初始化 Vault（Dev 模式已自动解封）

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

vault status
```

---

## 📖 核心概念

### 1. Secret Engine

Vault 通过 Secret Engine 管理不同类型的秘密：

- **KV**：键值对凭据存储
- **Database**：动态数据库凭据
- **PKI**：证书签发
- **Transit**：加密即服务
- **AWS/Azure/GCP**：云厂商动态凭据

### 2. 认证方法

Vault 支持多种认证方式：

- Token（开发测试）
- Kubernetes（K8s 工作负载）
- AppRole（应用集成）
- LDAP/ OIDC（人员访问）

### 3. Policy

基于路径的访问控制策略，采用最小权限原则：

```hcl
path "secret/data/myapp/*" {
  capabilities = ["read"]
}
```

### 4. 动态凭据

Vault 可以按需签发临时数据库账号、云 IAM 凭据等，并自动到期回收，降低凭据泄露风险。

---

## 💻 代码示例

### 启用 KV 引擎并写入凭据

```bash
# 启用 KV v2 引擎
vault secrets enable -version=2 kv

# 写入凭据
vault kv put kv/myapp/database username=app_user password=StrongP@ssw0rd

# 读取凭据
vault kv get kv/myapp/database

# 更新凭据
vault kv put kv/myapp/database username=app_user password=NewP@ssw0rd

# 查看历史版本
vault kv metadata get kv/myapp/database
```

### 配置访问策略

```bash
# 创建策略文件
cat > myapp-policy.hcl <<EOF
path "kv/data/myapp/*" {
  capabilities = ["read"]
}
EOF

# 写入策略
vault policy write myapp myapp-policy.hcl

# 创建 Token 并关联策略
vault token create -policy=myapp
```

### 使用策略 Token 读取凭据

```bash
export VAULT_TOKEN="<generated-token>"
vault kv get kv/myapp/database
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `docker-compose.yml` | Vault 服务编排 |
| `configs/vault.hcl` | Vault 服务端配置 |
| `scripts/start.sh` | 启动脚本 |

### Dev 模式配置

```hcl
disable_mlock = true
ui = true

storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}
```

⚠️ 生产环境必须启用 TLS 和高可用存储后端（如 Consul、etcd、Raft）。

---

## 🧪 验证测试

```bash
# 检查 Vault 状态
vault status

# 列出 Secret Engine
vault secrets list

# 测试策略访问
curl -H "X-Vault-Token: $VAULT_TOKEN" \
  $VAULT_ADDR/v1/kv/data/myapp/database
```

---

## 📊 运行结果

```bash
$ vault kv get kv/myapp/database
====== Metadata ======
Key              Value
---              -----
created_time     2026-06-27T10:00:00.000000000Z
custom_metadata  <nil>
destroyed        false
version          1

====== Data ======
Key         Value
---         -----
password    StrongP@ssw0rd
username    app_user
```

---

## 🐛 常见问题

### Q1：Vault 启动后无法访问？

**A**：Dev 模式下 Vault 监听 0.0.0.0:8200，确认端口未被占用。

### Q2：Token 权限不足？

**A**：检查 Policy 路径和 capabilities 是否匹配访问请求。

### Q3：生产环境如何部署？

**A**：使用 Raft 集成存储、启用 TLS、配置自动解封（如 AWS KMS、Azure Key Vault）。

---

## 📚 扩展学习

- [Secrets Management with Vault](../secrets-management-vault/)
- [云磁盘加密 AWS](../cloud-disk-encryption-aws/)
- [HashiCorp Vault 官方文档](https://developer.hashicorp.com/vault/docs)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
