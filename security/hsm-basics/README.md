# HSM Basics

硬件安全模块(HSM)基础实践。

## HSM类型

```
HSM部署形式:
┌─────────────────┬─────────────────┬─────────────────┐
│   USB HSM       │  Network HSM    │   Cloud HSM     │
├─────────────────┼─────────────────┼─────────────────┤
│ • YubiKey       │ • Thales Luna   │ • AWS CloudHSM  │
│ • NitroKey      │ • Utimaco       │ • Azure HSM     │
│ • SmartCard     │ • SafeNet       │ • GCP CloudHSM  │
├─────────────────┼─────────────────┼─────────────────┤
│ 适合个人/开发    │  适合企业本地    │  适合云端部署    │
│ 低成本便携      │  高性能高安全    │  弹性扩展       │
└─────────────────┴─────────────────┴─────────────────┘
```

## PKCS#11接口

```bash
# 安装OpenSC
sudo apt install opensc-pkcs11

# 列出HSM槽
pkcs11-tool --module /usr/lib/opensc-pkcs11.so -L

# 生成密钥对 (HSM内)
pkcs11-tool --module /usr/lib/opensc-pkcs11.so \
  --login --pin 123456 \
  --keypairgen --key-type RSA:2048 \
  --label "my-key"

# 列出对象
pkcs11-tool --module /usr/lib/opensc-pkcs11.so -O
```

## CloudHSM示例

```bash
# AWS CloudHSM
# 初始化集群
aws cloudhsmv2 create-cluster --hsm-type hsm1.medium \
  --backup-retention-policy Type=DAYS,Value=30

# 初始化HSM
aws cloudhsmv2 create-hsm --cluster-id <cluster-id> \
  --availability-zone us-east-1a

# 使用CloudHSM客户端
createKeystore mykeystore
loginHSM CU user password
generateRSAKeyPair 2048 myrsakey
```

## 学习要点

1. HSM安全边界
2. PKCS#11编程接口
3. 性能与成本权衡
4. 高可用架构设计
