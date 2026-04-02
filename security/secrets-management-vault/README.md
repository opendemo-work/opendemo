# Secrets Management with Vault

HashiCorp Vault密钥管理实践演示。

## Vault架构

```
Vault架构:
┌─────────────────────────────────────────────────────────┐
│                    Vault API                            │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │  Auth   │ │  Token  │ │  Lease  │ │  Policy │      │
│  │ Methods │ │ Manager │ │ Manager │ │ Engine  │      │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘      │
├───────┴───────────┴───────────┴───────────┴───────────┤
│                   Secret Engines                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │   KV    │ │Database │ │   PKI   │ │ Transit │      │
│  │  v1/v2  │ │ Secrets │ │  (TLS)  │ │Encrypt  │      │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
├─────────────────────────────────────────────────────────┤
│                   Storage Backend                       │
│         (Consul/etcd/S3/PostgreSQL/MySQL)               │
└─────────────────────────────────────────────────────────┘
```

## 安装与初始化

```bash
# 安装Vault
wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip
unzip vault_1.15.0_linux_amd64.zip
sudo mv vault /usr/local/bin/

# 开发模式启动
vault server -dev -dev-root-token-id="root"

# 生产模式配置
vault server -config=vault.hcl

# vault.hcl配置
storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls.crt"
  tls_key_file = "/opt/vault/tls.key"
}

api_addr = "https://vault.example.com:8200"
cluster_addr = "https://10.0.0.1:8201"
```

## 初始化与解封

```bash
# 初始化 (生成5个解封密钥，需要3个解封)
vault operator init \
  -key-shares=5 \
  -key-threshold=3

# 输出:
# Unseal Key 1: xxx
# ...
# Initial Root Token: xxx

# 解封Vault
vault operator unseal <Unseal Key 1>
vault operator unseal <Unseal Key 2>
vault operator unseal <Unseal Key 3>

# 自动解封 (使用云KMS)
seal "awskms" {
  region = "us-east-1"
  kms_key_id = "alias/vault-unseal"
}
```

## KV Secrets引擎

```bash
# 启用KV v2
vault secrets enable -version=2 kv

# 存储密钥
vault kv put secret/api \
  db_host=prod-db.example.com \
  db_user=app_user \
  db_pass=super_secret_password

# 读取密钥
vault kv get secret/api

# 读取特定字段
vault kv get -field=db_pass secret/api

# 版本控制
vault kv put secret/api db_pass=new_password
vault kv get -version=1 secret/api  # 历史版本
vault kv delete secret/api          # 软删除
vault kv destroy secret/api         # 永久删除
```

## 数据库动态凭证

```bash
# 启用数据库引擎
vault secrets enable database

# 配置PostgreSQL
vault write database/config/postgres \
  plugin_name=postgresql-database-plugin \
  allowed_roles="app" \
  connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
  username="vaultadmin" \
  password="vaultadmin_password"

# 创建角色
vault write database/roles/app \
  db_name=postgres \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# 获取动态凭证
vault read database/creds/app
# 自动生成用户名/密码，1小时后自动过期
```

## Kubernetes集成

```yaml
# Vault Agent Injector
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vault-agent-injector
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "app"
        vault.hashicorp.com/agent-inject-secret-db: "database/creds/app"
        vault.hashicorp.com/agent-inject-template-db: |
          {{ with secret "database/creds/app" -}}
          export DB_USER="{{ .Data.username }}"
          export DB_PASS="{{ .Data.password }}"
          {{- end }}
    spec:
      serviceAccountName: app-sa
      containers:
      - name: app
        image: myapp:latest
```

## 学习要点

1. Vault安全模型与解封机制
2. Secret Engines选择
3. 动态凭证与自动轮换
4. Kubernetes集成模式
5. 高可用与灾难恢复
