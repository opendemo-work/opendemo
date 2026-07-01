# 🔒 Security 安全技术栈

> 企业级终端与数据安全实践，涵盖密钥管理、磁盘加密、身份认证、访问控制、合规审计和灾难恢复等方向。

---

## 📚 技术栈概览

安全是数字化转型的基础保障。本技术栈提供从数据加密到合规审计的完整安全实践，包含 31 个实战案例，覆盖以下主题：

- 密钥管理与 Secrets 托管
- 云磁盘加密（AWS/Azure/GCP）
- 全盘加密（BitLocker/FileVault/LUKS）
- 身份认证与 LDAP/AD 集成
- GDPR 合规与审计
- 安全工具批量部署与回滚
- 灾难恢复与密钥托管
- TPM/Secure Boot/HSM

---

## 🎯 学习目标

完成本技术栈学习后，你将能够：

- ✅ 设计企业级加密策略
- ✅ 使用 Vault 等工具管理敏感凭据
- ✅ 部署终端全盘加密方案
- ✅ 建立合规审计和访问控制体系
- ✅ 制定安全事件响应和恢复流程

---

## 📂 案例目录

| 案例 | 主题 |
|------|------|
| [密钥管理基础](./crypto-key-management/) | HashiCorp Vault |
| [Secrets Management](./secrets-management-vault/) | 应用凭据管理 |
| [GDPR 合规审计](./compliance-audit-gdpr/) | 数据保护与合规 |
| [AWS 云磁盘加密](./cloud-disk-encryption-aws/) | EBS + KMS |
| [BitLocker 管理](./bitlocker-management/) | Windows 磁盘加密 |
| [LUKS 全盘加密](./fde-luks/) | Linux 磁盘加密 |
| [TPM 安全芯片](./tpm-security/) | 可信平台模块 |

... 共 31 个案例，详见各子目录。

---

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd security/crypto-key-management
./scripts/start.sh
./scripts/check.sh
```

---

## 🔗 相关技术栈

- [Database](./../database/) - 数据库安全
- [Cloud CLI](./../cloud-cli/) - 云资源管理
- [SRE](./../sre/) - 安全事件响应

---

*最后更新：2026-07-01*  
*维护者：OpenDemo Team*
