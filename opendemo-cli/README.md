# OpenDemo CLI 命令行工具

## 🎯 概述

OpenDemo CLI是一个功能强大的命令行工具，用于管理和操作OpenDemo技术演示平台。它提供了便捷的方式来浏览、搜索和运行各种技术演示案例。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: Python 3.8+, Click框架
- **适用场景**: 命令行操作、自动化脚本、开发工具
- **难度等级**: 🟢 初级

### 技术栈
```python
# 核心依赖
click>=8.0.0              # 命令行界面框架
requests>=2.25.0          # HTTP客户端
PyYAML>=5.4.0             # YAML配置处理
Jinja2>=3.0.0             # 模板引擎
colorama>=0.4.4           # 终端颜色支持
```

## 🚀 快速开始

### 安装部署
```bash
# 克隆项目
git clone <repository-url>
cd opendemo-cli

# 安装依赖
pip install -r requirements.txt

# 安装CLI工具
pip install -e .

# 验证安装
opendemo --help
```

### 基本使用
```bash
# 查看帮助
opendemo --help

# 列出所有技术栈
opendemo list stacks

# 搜索特定demo
opendemo search "数据库连接"
```

## 📁 项目结构

```
opendemo-cli/
├── core/                           # 核心模块
│   ├── __init__.py
│   ├── cli.py                     # 主CLI入口
│   ├── commands/                  # 命令实现
│   │   ├── list.py               # 列表命令
│   │   ├── search.py             # 搜索命令
│   │   ├── run.py                # 运行命令
│   │   └── config.py             # 配置命令
│   └── utils/                     # 工具函数
├── services/                       # 服务模块
│   ├── __init__.py
│   ├── demo_manager.py           # Demo管理服务
│   └── config_service.py         # 配置服务
├── config/                         # 配置文件
│   ├── config.yaml               # 主配置文件
│   └── templates/                # 模板文件
├── docs/                           # 文档目录
│   └── usage_guide.md            # 使用指南
├── tests/                          # 测试目录
│   ├── test_cli.py
│   └── test_services.py
├── requirements.txt                # 依赖列表
└── README.md                      # 本文件
```

## 🔧 核心功能

### 主要命令
1. **list**: 列出技术栈和demo
2. **search**: 搜索特定技术演示
3. **run**: 运行指定的demo
4. **config**: 管理配置设置

### 使用示例
```bash
# 列出所有Go语言demo
opendemo list demos --stack go

# 搜索包含"并发"的demo
opendemo search "并发" --stack java

# 运行特定demo
opendemo run go/go-channels-demo

# 查看demo详情
opendemo info nodejs/express-demo
```

## ⚙️ 配置说明

### 配置文件
```yaml
# ~/.opendemo/config.yaml
general:
  demo_path: "/path/to/opendemo"
  default_editor: "vim"
  color_output: true

api:
  base_url: "https://api.opendemo.example.com"
  timeout: 30

logging:
  level: "INFO"
  file: "~/.opendemo/logs/cli.log"
```

### 环境变量
```bash
OPENDEMO_PATH=/path/to/opendemo      # Demo项目路径
OPENDEMO_EDITOR=code                 # 默认编辑器
OPENDEMO_LOG_LEVEL=DEBUG             # 日志级别
```

## 🔍 故障排除

### 常见问题
1. **问题**: 命令未找到
   - **解决方案**: 确认已正确安装并添加到PATH

2. **问题**: 权限被拒绝
   - **解决方案**: 检查demo目录权限，必要时使用sudo

### 调试模式
```bash
# 启用详细输出
opendemo --verbose list stacks

# 启用调试日志
export OPENDEMO_LOG_LEVEL=DEBUG
opendemo search "kubernetes"
```

## 🧪 测试验证

### 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_cli.py::test_list_command

# 生成测试覆盖率报告
pytest --cov=core --cov-report=html tests/
```

### 功能测试脚本
```bash
#!/bin/bash
# test-cli.sh

echo "Testing OpenDemo CLI..."

# 测试基本命令
opendemo --version
opendemo --help

# 测试列表功能
opendemo list stacks
opendemo list demos --stack python

# 测试搜索功能
opendemo search "database" --limit 5

echo "CLI tests completed!"
```

## 📈 性能优化

### 命令响应时间
- **基本命令**: < 100ms
- **列表操作**: < 500ms
- **搜索操作**: < 1s
- **运行操作**: 取决于demo复杂度

### 内存使用
- **基础内存占用**: ~25MB
- **峰值内存使用**: ~50MB

## 🔒 安全考虑

### 安全特性
- 输入验证和清理
- 命令执行沙箱化
- 配置文件权限控制

### 最佳实践
- 定期更新依赖包
- 使用虚拟环境隔离
- 限制文件系统访问权限

## 🚀 高级用法

### 批量操作
```bash
# 批量运行demo
opendemo batch run --file demo_list.txt

# 批量导出配置
opendemo export config --format json
```

### 自定义扩展
```python
# 创建自定义命令
import click
from core.cli import cli

@cli.command()
@click.argument('name')
def hello(name):
    """Say hello to someone"""
    click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    cli()
```

## 📚 相关资源

### 官方文档
- [Click官方文档](https://click.palletsprojects.com/)
- [Python CLI最佳实践](https://docs.python-guide.org/writing/cli/)

### 学习资源
- 《Click权威指南》
- Python命令行应用开发教程

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
# 创建开发环境
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# 运行开发版本
python -m core.cli --help
```

## 📄 许可证

本项目采用 MIT 许可证

---
*最后更新: 2026年2月3日*