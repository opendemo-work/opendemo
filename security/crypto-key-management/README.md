# Cryptographic Key Management

密钥生命周期管理最佳实践。

## 密钥管理层次

```
密钥层级 (CKMS):
┌─────────────────────────────────────────────────────────┐
│  Master Key (KEK) - 密钥加密密钥                         │
│  存储于HSM，永不离开安全边界                              │
├─────────────────────────────────────────────────────────┤
│  Intermediate Key - 中间层密钥                           │
│  用于加密数据密钥，定期轮换                               │
├─────────────────────────────────────────────────────────┤
│  Data Key (DEK) - 数据加密密钥                           │
│  用于实际数据加密，高频生成/销毁                          │
├─────────────────────────────────────────────────────────┤
│  Encrypted Data - 加密数据                               │
│  DEK与密文一起存储，DEK由上层密钥加密                     │
└─────────────────────────────────────────────────────────┘
```

## 密钥生命周期

| 阶段 | 操作 | 最佳实践 |
|------|------|----------|
| 生成 | 随机数生成 | HSM内生成，熵池充足 |
| 分发 | 安全传输 | TLS 1.3，信封加密 |
| 存储 | 安全保存 | HSM/KMS，访问审计 |
| 使用 | 加密操作 | HSM内运算，密钥不导出 |
| 轮换 | 定期更换 | 自动轮换，双密钥并行 |
| 归档 | 历史保存 | 加密归档，保留恢复 |
| 销毁 | 安全删除 | HSM删除，物理销毁 |

## OpenSSL密钥操作

```bash
# 生成RSA密钥对
openssl genrsa -aes256 -out private.pem 4096
openssl rsa -in private.pem -pubout -out public.pem

# 生成ECC密钥
openssl ecparam -genkey -name prime256v1 -out ec-private.pem
openssl ec -in ec-private.pem -pubout -out ec-public.pem

# 生成对称密钥
openssl rand -base64 32 > symmetric.key

# 密钥派生 (PBKDF2)
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 \
  -pass pass:password123 -P
```

## 密钥轮换策略

```bash
# AWS KMS密钥轮换
aws kms enable-key-rotation --key-id alias/my-key

# 手动轮换流程
# 1. 生成新密钥
# 2. 重新加密数据 (双写)
# 3. 验证新密钥工作
# 4. 停用旧密钥 (保留用于解密历史数据)
# 5. 完全删除旧密钥 (达到保留期后)
```

## 学习要点

1. 密钥层级设计
2. 生命周期管理
3. HSM与软件密钥权衡
4. 合规要求 (FIPS 140-2/3)
