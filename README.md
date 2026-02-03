# OpenDemo 技术演示项目

## 🚀 项目概述
这是一个综合性的技术演示平台，展示了多种编程语言和现代技术的最佳实践。

## 🔐 安全特性
本项目采用企业级安全标准：

- **环境变量管理** - 所有敏感配置通过 `.env` 文件管理
- **Git 安全** - 自动化的安全检查和防护机制
- **密钥轮换** - 定期密钥更新策略
- **持续监控** - CI/CD 集成的安全检查
- **零硬编码** - 代码中无任何硬编码的密码、密钥或令牌
- **自动扫描** - 定期扫描潜在的安全漏洞

## 🛠️ 快速开始

### 1. 环境设置
```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
nano .env  # 填入实际配置值
```

### 2. 安全验证
```bash
# 运行安全检查
./scripts/security/check_security.sh

# 生成安全密钥
./scripts/security/generate_keys.sh
```

### 3. 启动项目
```bash
# 根据具体技术栈启动
make run  # 或相应的启动命令
```

## 📁 项目结构
```
opendemo/
├── ai-ml/              # AI/机器学习示例
├── cli/                # 命令行工具
├── container/          # 容器化示例
├── database/           # 数据库相关
├── go/                 # Go 语言示例
├── java/               # Java 示例
├── kubernetes/         # K8s 配置
├── nodejs/             # Node.js 示例
├── python/             # Python 示例
├── scripts/            # 脚本工具
├── config/             # 配置文件
└── docs/               # 文档资料
```

## 🔧 开发工具

### 安全工具
- `./scripts/security/check_security.sh` - 安全检查
- `./scripts/security/scan_secrets.py` - 敏感信息扫描
- `./scripts/security/generate_keys.sh` - 密钥生成

### 开发辅助
- `make help` - 查看可用命令
- `make test` - 运行测试
- `make lint` - 代码检查

## 📚 文档资源
- [安全配置指南](SECURITY_CONFIG.md)
- [跨技术栈索引](docs/CROSS-TECH-INDEX.md)
- [技术栈规划](java/JAVA-TECH-STACK-COMPLETION-PLAN.md)

## 🤝 贡献指南
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## ⚠️ 安全提醒
请务必：
- 不要在代码中硬编码敏感信息
- 定期更新密钥和密码
- 运行安全检查后再提交代码
- 遵循最小权限原则

## 🛡️ 安全保证
✅ 所有敏感信息均已从代码中移除
✅ 采用环境变量和密钥管理系统
✅ 通过自动化安全扫描验证
✅ 符合 GitHub 安全上传要求

---
*最后更新: 2026年2月3日*