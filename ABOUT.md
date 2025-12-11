# Open Demo CLI - 完整使用手册

## 项目简介

Open Demo CLI 是一个智能化的编程学习辅助命令行工具，帮助开发者快速获取高质量、可执行的编程语言Demo代码。支持本地Demo库搜索和AI智能生成，是学习编程的得力助手。

---

## 目录

1. [项目文件结构](#项目文件结构)
2. [安装与配置](#安装与配置)
3. [CLI命令详解](#cli命令详解)
4. [Demo库说明](#demo库说明)
5. [配置管理](#配置管理)
6. [常见问题](#常见问题)

---

## 项目文件结构

```
opendemo/
│
├── 📄 文档文件
│   ├── ABOUT.md              # 本文件 - 完整使用手册
│   ├── README.md             # 项目简介
│   ├── USAGE_GUIDE.md        # 详细使用指南
│   ├── PROJECT_SUMMARY.md    # 项目开发总结
│   ├── TEST_REPORT.md        # CLI功能测试报告
│   └── LICENSE               # MIT开源许可证
│
├── 📦 核心源码
│   └── opendemo/             # Python主包
│       ├── __init__.py       # 包初始化
│       ├── cli.py            # CLI命令入口 (search/get/new/config)
│       │
│       ├── core/             # 核心业务逻辑
│       │   ├── demo_manager.py    # Demo管理器 - 加载、保存、组织Demo
│       │   ├── search_engine.py   # 搜索引擎 - 关键字匹配和排序
│       │   ├── generator.py       # 生成器 - 协调AI生成Demo
│       │   ├── verifier.py        # 验证器 - 验证Demo可执行性
│       │   └── contribution.py    # 贡献管理 - Demo质量检查
│       │
│       ├── services/         # 服务层
│       │   ├── ai_service.py      # AI服务 - 调用LLM API生成代码
│       │   ├── config_service.py  # 配置服务 - 管理全局/项目配置
│       │   └── storage_service.py # 存储服务 - 文件系统操作
│       │
│       ├── utils/            # 工具模块
│       │   ├── formatters.py      # 输出格式化 - Rich彩色表格
│       │   └── logger.py          # 日志工具
│       │
│       └── builtin_demos/    # 内置Demo库（只读）
│           └── python/       # Python内置Demo
│
├── 📂 Demo输出目录
│   └── opendemo_output/      # 生成的Demo保存位置
│       └── python/           # Python Demo (51个)
│           ├── logging/
│           ├── async-programming/
│           ├── collections-module/
│           └── ...
│
├── ⚙️ 配置文件
│   ├── pyproject.toml        # 项目配置和依赖声明
│   ├── .gitignore            # Git忽略规则
│   └── start.py              # 快速启动脚本
│
└── 🧪 测试
    └── tests/                # 单元测试目录
```

---

## 安装与配置

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/opendemo/opendemo.git
cd opendemo

# 安装（开发模式）
pip install -e .
```

### 2. 验证安装

```bash
python -m opendemo.cli --help
```

### 3. 配置AI服务（可选，用于生成新Demo）

```bash
# 初始化配置
python -m opendemo.cli config init

# 设置API密钥
python -m opendemo.cli config set ai.api_key YOUR_API_KEY

# 设置API端点（如使用阿里云百炼等服务）
python -m opendemo.cli config set ai.api_endpoint https://your-api-endpoint/v1/chat/completions
```

---

## CLI命令详解

### 命令概览

| 命令 | 功能 | 示例 |
|------|------|------|
| `search` | 搜索Demo | `opendemo search python` |
| `get` | 获取Demo | `opendemo get python logging` |
| `new` | 创建新Demo | `opendemo new python 装饰器` |
| `config` | 配置管理 | `opendemo config list` |

### search - 搜索Demo

```bash
# 查看所有支持的语言
python -m opendemo.cli search

# 列出所有Python Demo（扫描opendemo_output/python目录）
python -m opendemo.cli search python

# 按关键字过滤
python -m opendemo.cli search python async
python -m opendemo.cli search python thread
```

**输出示例：**
```
找到 51 个匹配的demo:

┌──────┬───────────────────────┬────────────┬───────────────────────┬──────────────┐
│ #    │ 名称                  │ 语言       │ 关键字                │ 难度         │
├──────┼───────────────────────┼────────────┼───────────────────────┼──────────────┤
│ 1    │ abc-interfaces        │ python     │ abc, interfaces       │ beginner     │
│ 2    │ async-programming     │ python     │ async, programming    │ beginner     │
│ 3    │ logging               │ python     │ logging               │ beginner     │
│ ... │ ...                   │ ...        │ ...                   │ ...          │
└──────┴───────────────────────┴────────────┴───────────────────────┴──────────────┘
```

### get - 获取Demo

**匹配优先级：**
1. **精确匹配** - 关键字完全等于文件夹名称
2. **语义匹配** - 关键字被包含在文件夹名称中
3. **AI生成** - 本地未找到时调用AI生成（需配置API）

```bash
# 精确匹配已有Demo
python -m opendemo.cli get python logging

# 语义匹配（list → list-operations）
python -m opendemo.cli get python list

# 强制重新生成（添加-new后缀）
python -m opendemo.cli get python logging new
```

**输出示例：**
```
>>> 搜索 python - logging 的demo...
[OK] 在输出目录中找到匹配的demo: logging
[OK] Demo已存在!

名称: logging
语言: python
路径: opendemo_output\python\logging
关键字: logging
描述: Python logging demo

包含文件:
  - code/logging_demo.py

快速开始:
  1. cd opendemo_output\python\logging
  2. python code/logging_demo.py

如需重新生成: opendemo get python logging new
```

### new - 创建新Demo

使用AI生成全新的Demo（需要配置API密钥）：

```bash
# 生成新Demo
python -m opendemo.cli new python 网络爬虫

# 指定难度级别
python -m opendemo.cli new python 设计模式 --difficulty intermediate

# 生成并验证
python -m opendemo.cli new python 异步IO --verify
```

### config - 配置管理

```bash
# 初始化配置文件
python -m opendemo.cli config init

# 查看所有配置
python -m opendemo.cli config list

# 获取特定配置
python -m opendemo.cli config get ai.model

# 设置配置项
python -m opendemo.cli config set ai.api_key sk-xxx
python -m opendemo.cli config set output_directory ./my_demos
```

---

## Demo库说明

### 现有Python Demo（51个）

| 分类 | Demo名称 | 说明 |
|------|----------|------|
| **基础语法** | control-flow, comprehensions, lambda-expressions | 控制流、推导式、匿名函数 |
| **数据类型** | list-operations, dict-operations, set-operations, tuple-basics, string-operations | 列表、字典、集合、元组、字符串 |
| **函数与类** | functions-decorators, oop-classes, magic-methods, dataclasses | 函数装饰器、面向对象、魔术方法 |
| **高级特性** | iterators-generators, context-managers, descriptors-property, metaclasses | 迭代器、上下文管理器、描述符 |
| **并发编程** | multithreading, multiprocessing, async-programming, threading-synchronization | 多线程、多进程、异步编程 |
| **标准库** | collections-module, functools-module, itertools-module, operator-module | 常用标准库模块 |
| **文件与IO** | file-operations, pathlib-os, json-yaml, serialization-pickle | 文件操作、路径、序列化 |
| **网络与数据库** | http-requests, socket-networking, database-sqlite | HTTP请求、Socket、SQLite |
| **调试与测试** | logging, debugging, unit-testing, profiling-optimization | 日志、调试、测试、性能 |
| **其他** | regex, datetime, enums, type-hints, exception-handling | 正则、时间、枚举、类型提示 |

### Demo目录结构

每个Demo遵循统一结构：

```
opendemo_output/python/logging/
├── metadata.json       # Demo元数据（名称、关键字、难度等）
├── code/               # 代码文件目录
│   └── logging_demo.py # 可执行的Demo代码
└── requirements.txt    # Python依赖（如需要）
```

### 运行Demo

```bash
# 进入Demo目录
cd opendemo_output/python/logging

# 安装依赖（如果有requirements.txt）
pip install -r requirements.txt

# 运行Demo
python code/logging_demo.py
```

---

## 配置管理

### 配置文件位置

- **全局配置**: `~/.opendemo/config.yaml`
- **项目配置**: `./.opendemo.yaml`（当前目录）

### 主要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `output_directory` | Demo输出目录 | `./opendemo_output` |
| `user_demo_library` | 用户Demo库路径 | `~/.opendemo/demos` |
| `default_language` | 默认编程语言 | `python` |
| `enable_verification` | 是否启用自动验证 | `false` |
| `ai.provider` | AI服务提供商 | `openai` |
| `ai.api_key` | API密钥 | 无 |
| `ai.api_endpoint` | API端点URL | OpenAI默认 |
| `ai.model` | 使用的模型 | `gpt-4` |
| `ai.temperature` | 温度参数 | `0.7` |
| `display.color_output` | 彩色输出 | `true` |

---

## 常见问题

### Q1: 如何使用AI生成功能？

需要配置API密钥和端点：
```bash
python -m opendemo.cli config set ai.api_key YOUR_KEY
python -m opendemo.cli config set ai.api_endpoint YOUR_ENDPOINT
```

### Q2: Demo保存在哪里？

默认保存在 `opendemo_output/<语言>/` 目录下，可通过配置修改：
```bash
python -m opendemo.cli config set output_directory /path/to/output
```

### Q3: 如何查看某个Demo的代码？

```bash
# 方法1: 使用get命令查看路径，然后打开
python -m opendemo.cli get python logging

# 方法2: 直接进入目录查看
cd opendemo_output/python/logging/code
cat logging_demo.py
```

### Q4: 搜索结果为空怎么办？

1. 确认Demo目录存在: `opendemo_output/python/`
2. 确认Demo有 `metadata.json` 文件
3. 尝试使用更宽泛的关键字

### Q5: 如何贡献新的Demo？

使用 `new` 命令创建Demo后，系统会询问是否贡献到公共库：
```bash
python -m opendemo.cli new python 你的主题
# 按提示选择是否贡献
```

---

## 文档索引

| 文档 | 说明 |
|------|------|
| [ABOUT.md](ABOUT.md) | 完整使用手册（本文件） |
| [README.md](README.md) | 项目简介 |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | 详细使用指南 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目开发总结 |
| [TEST_REPORT.md](TEST_REPORT.md) | CLI功能测试报告 |
| [LICENSE](LICENSE) | MIT开源许可证 |

---

## 技术支持

- **问题反馈**: GitHub Issues
- **项目仓库**: https://github.com/opendemo/opendemo

---

*最后更新: 2024-12-10*
