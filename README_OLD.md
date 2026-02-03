# OpenDemo 技术演示平台

## 🎯 项目简介
OpenDemo 是一个综合性技术学习和演示平台，涵盖多种主流编程语言和技术栈的实战案例。本项目致力于提供高质量的技术示例和最佳实践指南。

## 🔧 核心功能
- **多语言支持**：Python、Go、Java、Node.js 等主流编程语言
- **全栈技术**：从前端到后端，从数据库到容器化部署
- **企业级实践**：安全配置、CI/CD、监控告警等生产环境必备技能
- **AI 集成**：机器学习、深度学习等前沿技术演示
- **数据管理**：项目元数据和验证报告
- **创意编程**：AI助手集成和创新编程实践

## 🛡️ 安全保障
项目采用严格的安全标准：

- **环境变量管理** - 所有敏感配置通过 `.env` 文件管理
- **Git 安全** - 自动化的安全检查和防护机制
- **密钥轮换** - 定期密钥更新策略
- **持续监控** - CI/CD 集成的安全检查
- **零硬编码** - 代码中无任何硬编码的密码、密钥或令牌
- **自动扫描** - 定期扫描潜在的安全漏洞

## 🚀 快速入门

### 1. 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd opendemo

# 复制环境配置模板
cp .env.example .env

# 编辑配置文件（根据实际需求填写）
nano .env
```

### 2. 安全检查
```bash
# 运行自动化安全扫描
./scripts/security/check_security.sh

# 生成项目所需密钥
./scripts/security/generate_keys.sh
```

### 3. 选择技术栈
根据不同需求选择相应的技术演示：

**Python 开发**
```bash
cd python/
# 查看具体示例目录
ls -la
```

**Go 语言学习**
```bash
cd go/
# 探索 Go 技术示例
ls -la
```

**Java 企业级应用**
```bash
cd java/
# 查看 Java 相关演示
ls -la
```

**Node.js 全栈开发**
```bash
cd nodejs/
# 浏览 Node.js 示例
ls -la
```

**数据管理工具**
```bash
cd data/
# 查看项目元数据和验证报告
ls -la
```

**创意编程实践**
```bash
cd vibe-coding/
# 探索AI助手集成示例
ls -la
```

## 📁 项目结构
```
opendemo/
├── ai-ml/              # 🤖 AI/机器学习技术栈
├── container/          # 🐳 容器化技术示例
├── data/               # 📊 数据管理和映射文件
├── database/           # 🗄️ 数据库相关演示
├── docs/               # 📚 技术文档资料
├── go/                 # 🦫 Go 语言技术栈
├── java/               # ☕ Java 企业级应用
├── kubernetes/         # ☸️ Kubernetes 容器编排
├── linux/              # 🐧 Linux 系统管理
├── nodejs/             # 🟩 Node.js 全栈开发
├── opendemo-cli/       # 💻 CLI 命令行工具
├── python/             # 🐍 Python 数据科学
├── scripts/            # 🛠️ 自动化脚本工具
├── vibe-coding/        # 💫 创意编程和AI助手集成
└── .env.example        # ⚙️ 环境配置模板
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
- [项目元数据映射](data/demo_mapping.json)
- [Java验证报告](data/java_validation_report.json)

## 🤝 参与贡献

欢迎任何形式的贡献！

### 📝 贡献流程
1. Fork 本项目到个人仓库
2. 创建功能分支 `git checkout -b feature/AmazingFeature`
3. 提交更改 `git commit -m 'Add some AmazingFeature'`
4. 推送到分支 `git push origin feature/AmazingFeature`
5. 开启 Pull Request

### 🎯 贡献方向
- 🐛 修复 bug 和问题
- ✨ 添加新的技术示例
- 📚 完善文档和注释
- 🔧 优化项目结构和工具

## ⚠️ 重要提醒

### 🔒 安全规范
- ❌ 禁止在代码中硬编码敏感信息
- 🔁 定期更新密钥和密码
- 🛡️ 提交前务必运行安全检查
- 🔐 严格遵循最小权限原则

### 📋 使用须知
- 本项目仅供学习和演示用途
- 生产环境使用请进行充分测试
- 遵循各技术栈的最佳实践
- 及时关注安全更新和补丁

---
<p align="center">
  <strong>🌟 喜欢这个项目？给个 Star 支持我们！</strong>
</p>

*最后更新：2026年2月3日*

---
*最后更新: 2026年2月3日*