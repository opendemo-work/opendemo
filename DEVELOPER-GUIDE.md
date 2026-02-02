# OpenDemo 开发者指南

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Git
- 对应技术栈的运行环境（Java、Go、Node.js等）

### 开发环境设置
```bash
# 克隆项目
git clone <repository-url>
cd opendemo

# 安装依赖
make setup

# 运行完整构建
make all
```

## 📁 项目结构说明

### 核心目录
```
opendemo/
├── cli/           # CLI工具核心代码
├── languages/     # 编程语言技术栈
├── infrastructure/ # 基础设施技术栈
├── ai-ml/        # AI/机器学习技术栈
├── dev-tools/    # 开发工具链
├── applications/ # 应用场景分类
├── docs/         # 项目文档
└── scripts/      # 自动化脚本
```

### 案例目录结构标准
每个技术案例应包含以下文件：
```
technology-demo-name/
├── README.md          # 详细说明文档
├── metadata.json      # 元数据配置
├── code/             # 示例代码目录
├── config/           # 配置文件目录
└── docs/             # 附加文档目录
```

## 🔧 开发工作流程

### 1. 新增案例流程
```bash
# 1. 创建案例目录
mkdir -p languages/python/new-python-demo

# 2. 生成基础模板
python scripts/generate_demos.py --template python --name "new-python-demo"

# 3. 编写代码和文档
# 编辑 README.md 和代码文件

# 4. 验证案例质量
make validate

# 5. 更新索引
make update-index
```

### 2. 代码质量要求
- 遵循对应语言的最佳实践
- 提供完整的错误处理
- 包含必要的注释说明
- 确保可执行性和环境兼容性

### 3. 文档编写标准
README.md 应包含：
- 学习目标和适用人群
- 环境准备和依赖安装
- 详细的代码解释
- 实际应用场景
- 常见问题解答

## 🧪 测试和验证

### 自动化测试
```bash
# 运行所有测试
make test

# 特定技术栈测试
make java-test
make go-test
make python-test

# 代码质量检查
make check
```

### 手动验证
1. 确认代码在标准环境中可运行
2. 验证文档内容准确完整
3. 检查跨平台兼容性
4. 确认示例具有实际参考价值

## 📝 贡献指南

### Pull Request 流程
1. Fork 项目仓库
2. 创建功能分支
3. 实现功能并添加测试
4. 确保所有测试通过
5. 提交 Pull Request

### 代码审查标准
- 代码风格一致性
- 功能完整性和正确性
- 文档质量和完整性
- 性能和安全性考虑

## 🛠️ 常用开发工具

### CLI 工具使用
```bash
# 搜索案例
python cli/cli.py search python logging

# 获取案例
python cli/cli.py get python logging

# 生成新案例
python cli/cli.py new java "spring-boot-example"
```

### 自动化脚本
- `generate_demos.py` - 批量生成案例模板
- `java_demo_validator.py` - Java案例质量验证
- `update_readme.py` - 自动更新文档索引

## 🔒 质量保证

### 持续集成
- 自动化测试执行
- 代码质量扫描
- 文档完整性检查
- 案例可执行性验证

### 质量门禁
- 测试覆盖率 > 80%
- 代码质量评分 > 85分
- 文档完整性 100%
- 案例可执行性 100%

## 🎯 最佳实践

### 案例设计原则
1. **实用性**: 解决真实的开发问题
2. **渐进性**: 从基础到进阶的完整路径
3. **完整性**: 提供端到端的解决方案
4. **可复用**: 代码具有良好的复用价值

### 技术选型建议
- 优先选择稳定成熟的方案
- 考虑企业级应用场景
- 关注技术的发展趋势
- 平衡学习成本和实用价值

## 🆘 获取帮助

### 社区支持
- GitHub Issues: 报告bug和功能请求
- Discussions: 技术讨论和经验分享
- Documentation: 详细的使用文档

### 维护团队
项目由专业的技术团队维护，定期更新内容和技术栈覆盖。

---
*最后更新: 2026-01-31*