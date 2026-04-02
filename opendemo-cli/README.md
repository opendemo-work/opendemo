# OpenDemo CLI v0.3.0

智能化的编程学习辅助CLI工具，支持518+技术案例管理。

---

## 🎯 概述

OpenDemo CLI是一个功能强大的命令行工具，用于管理和操作OpenDemo技术演示平台。它提供了便捷的方式来浏览、搜索、创建和验证各种技术演示案例。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: Python 3.9+, Click框架, Rich终端库
- **架构**: 模块化设计 (60行入口 + 6命令模块)
- **适用场景**: 命令行操作、自动化脚本、开发工具
- **难度等级**: 🟢 初级

### 技术栈
```python
# 核心依赖
click>=8.0.0              # 命令行界面框架
rich>=13.0.0              # 终端美化
requests>=2.25.0          # HTTP客户端
PyYAML>=5.4.0             # YAML配置处理
Jinja2>=3.0.0             # 模板引擎
```

---

## 🚀 快速开始

### 安装部署
```bash
# 进入CLI目录
cd opendemo-cli

# 安装依赖
pip install -r requirements.txt

# 验证安装
python -m opendemo --help
```

### 基本使用
```bash
# 查看帮助
python -m opendemo --help

# 获取已有demo
python -m opendemo get python logging

# 搜索demo
python -m opendemo search kubernetes

# 创建新demo
python -m opendemo new go microservices

# 运行质量检查
python -m opendemo check
```

---

## 📁 项目结构

```
opendemo-cli/
├── cli.py                    # 主CLI入口 (60行)
├── commands/                 # 命令模块
│   ├── base.py              # 公共函数
│   ├── get.py               # 获取demo
│   ├── search.py            # 搜索demo
│   ├── new.py               # 创建demo
│   ├── config.py            # 配置管理
│   └── check.py             # 质量检查
├── core/                     # 核心模块
│   ├── demo_repository.py   # Demo仓库
│   ├── demo_generator.py    # Demo生成器
│   ├── demo_verifier.py     # Demo验证器
│   ├── readme_updater.py    # README更新
│   └── demo_list_updater.py # 列表更新
├── services/                 # 服务层
│   ├── config_service.py    # 配置服务
│   ├── storage_service.py   # 存储服务
│   └── ai_service.py        # AI服务
├── utils/                    # 工具函数
│   ├── formatters.py        # 格式化输出
│   └── logger.py            # 日志管理
└── templates/                # 模板文件
    ├── readme_template.md
    └── metadata_template.json
```

---

## 🔧 核心功能

### 支持的技术栈 (11个)
1. **python** - Python编程
2. **java** - Java编程
3. **go** - Go编程
4. **nodejs** - Node.js编程
5. **kubernetes** - Kubernetes
6. **database** - 数据库
7. **networking** - 网络技术
8. **kvm** - KVM虚拟化
9. **virtualization** - 虚拟化
10. **sre** - SRE实践
11. **security** - 信息安全

### 主要命令

#### get - 获取Demo
```bash
# 获取已有demo
opendemo get python logging

# 强制重新生成
opendemo get python logging --new

# 验证demo
opendemo get python logging --verify
```

#### search - 搜索Demo
```bash
# 搜索关键词
opendemo search kubernetes

# 指定技术栈搜索
opendemo search microservices --language go
```

#### new - 创建新Demo
```bash
# 创建新demo
opendemo new python asyncio

# 指定难度
opendemo new go design-patterns --difficulty advanced

# 创建并验证
opendemo new java spring-boot --verify
```

#### check - 质量检查
```bash
# 运行质量检查
opendemo check

# 检查特定技术栈
opendemo check --language python
```

#### config - 配置管理
```bash
# 查看配置
opendemo config show

# 设置API密钥
opendemo config set ai.api_key YOUR_KEY

# 设置默认输出目录
opendemo config set output.directory ./output
```

---

## 📝 使用示例

### 示例1: 获取Go并发编程Demo
```bash
opendemo get go goroutines

# 输出:
# ✓ 成功生成demo
# 语言: go
# 主题: goroutines
# 路径: output/go/go-goroutines-demo
# 文件:
#   - README.md
#   - code/main.go
#   - metadata.json
```

### 示例2: 搜索K8s相关Demo
```bash
opendemo search kubernetes

# 输出:
# 找到 10 个匹配结果:
#   1. kubernetes-deployment
#   2. kubernetes-service
#   3. kubernetes-ingress
#   ...
```

### 示例3: 创建Python异步编程Demo
```bash
opendemo new python asyncio --difficulty intermediate

# 输出:
# 生成 python - asyncio 的demo (难度: intermediate)
# ✓ 成功生成demo
# 路径: output/python/python-asyncio-demo
```

---

## 🔍 质量检查

CLI工具内置质量检查功能，确保生成的Demo符合五星标准：

```bash
# 检查所有技术栈
opendemo check

# 检查结果示例:
# ┌──────────────────────────────────────────────────────┐
# │                   质量检查报告                        │
# ├──────────────┬───────────┬─────────────────┬─────────┤
# │ 技术栈       │ 案例数    │ README覆盖率    │ 评级    │
# ├──────────────┼───────────┼─────────────────┼─────────┤
# │ go           │ 93        │ 100%            │ ⭐⭐⭐⭐⭐ │
# │ java         │ 70        │ 100%            │ ⭐⭐⭐⭐⭐ │
# │ nodejs       │ 70        │ 100%            │ ⭐⭐⭐⭐⭐ │
# │ python       │ 55        │ 100%            │ ⭐⭐⭐⭐⭐ │
# │ kubernetes   │ 80        │ 100%            │ ⭐⭐⭐⭐⭐ │
# │ ...          │ ...       │ ...             │ ...     │
# └──────────────┴───────────┴─────────────────┴─────────┘
```

---

## 🛠️ 开发指南

### 添加新命令
```python
# commands/mycommand.py
import click

@click.command()
def mycommand():
    """我的新命令"""
    click.echo("Hello, World!")

# cli.py
from commands.mycommand import mycommand
cli.add_command(mycommand)
```

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_cli.py -v
```

---

## 📚 相关文档

- [项目主文档](../README.md)
- [案例列表](../docs/demo-list.md)
- [执行摘要](../EXECUTIVE_SUMMARY.md)

---

## 📄 版本历史

### v0.3.0 (2026-04-01)
- 模块化重构：965行 → 60行入口 + 6命令模块
- 支持11个技术栈
- 质量检查自动化

### v0.2.0
- 基础命令实现
- AI生成集成

### v0.1.0
- 项目初始化
- 基础CLI框架

---

**版本**: v0.3.0  
**支持**: 518+案例 / 11技术栈 / 全五星标准
