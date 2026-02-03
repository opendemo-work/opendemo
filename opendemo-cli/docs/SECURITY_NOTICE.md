# 安全注意事项

## ⚠️ 重要提醒

本项目已移除所有硬编码的敏感信息。请按照以下步骤正确配置：

### 1. 生成安全凭据
```bash
# 使用提供的脚本生成安全密码
./scripts/generate_secure_credentials.sh
```

### 2. 配置环境变量
```bash
# 复制模板并填写实际值
cp .env.template .env
# 编辑 .env 文件，填入生成的安全凭据
```

### 3. 验证配置
```bash
# 测试环境变量是否正确加载
python scripts/validate_env_config.py
```

## 🛡️ 安全最佳实践

- 永不在代码中硬编码敏感信息
- 使用环境变量或密钥管理服务
- 定期轮换密码和密钥
- 实施最小权限原则
- 启用审计日志

## 📚 了解更多
请查看 SECURITY_BEST_PRACTICES.md 获取详细的安全部署指南。
