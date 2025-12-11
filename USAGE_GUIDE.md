# Open Demo CLI 使用指南

## 快速上手

### 1. 安装

```bash
pip install -e .
```

### 2. 配置AI API密钥(可选,用于AI生成功能)

如果您想使用AI生成新demo的功能,需要配置API密钥:

```bash
python -m opendemo.cli config init
```

或者直接设置:

```bash
python -m opendemo.cli config set ai.api_key YOUR_API_KEY
```

### 3. 使用命令

#### 搜索demo

列出所有Python demo（扫描 `opendemo_output/python/` 目录）:

```bash
python -m opendemo.cli search python
```

输出示例:
```
找到 51 个匹配的demo:

┌──────┬──────────────────────┬────────────┬──────────────────────┬──────────────┐
│ #    │ 名称                 │ 语言       │ 关键字               │ 难度         │
├──────┼──────────────────────┼────────────┼──────────────────────┼──────────────┤
│ 1    │ abc-interfaces       │ python     │ abc, interfaces      │ beginner     │
│ 2    │ async-programming    │ python     │ async, programming   │ beginner     │
│ 3    │ logging              │ python     │ logging              │ beginner     │
│ ... │ ...                  │ ...        │ ...                  │ ...          │
└──────┴──────────────────────┴────────────┴──────────────────────┴──────────────┘
```

按关键字搜索过滤:

```bash
python -m opendemo.cli search python async
python -m opendemo.cli search python logging
```

#### 获取demo

获取已有的demo（优先匹配 `opendemo_output` 目录）:

```bash
python -m opendemo.cli get python logging
```

输出示例:
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

**强制重新生成已有demo**（文件夹名添加 `-new` 后缀）:

```bash
python -m opendemo.cli get python logging new
```

如果本地未找到匹配,会自动使用AI生成(需要配置API密钥):

```bash
python -m opendemo.cli get python 新主题
```

#### 创建新demo

使用AI生成新的demo:

```bash
python -m opendemo.cli new python 装饰器
python -m opendemo.cli new python 上下文管理器 --difficulty intermediate
```

#### 配置管理

查看所有配置:

```bash
python -m opendemo.cli config list
```

获取特定配置:

```bash
python -m opendemo.cli config get ai.model
```

设置配置:

```bash
python -m opendemo.cli config set enable_verification true
python -m opendemo.cli config set ai.temperature 0.7
```

## 实际演示

### 示例1: 搜索所有Python demo

```bash
$ python -m opendemo.cli search python

找到 51 个匹配的demo:

┌──────┬──────────────────────┬────────────┬──────────────────────┬──────────────┐
│ #    │ 名称                 │ 语言       │ 关键字               │ 难度         │
├──────┼──────────────────────┼────────────┼──────────────────────┼──────────────┤
│ 1    │ abc-interfaces       │ python     │ abc, interfaces      │ beginner     │
│ 2    │ async-programming    │ python     │ async, programming   │ beginner     │
│ 3    │ bitwise-operations   │ python     │ bitwise, operations  │ beginner     │
│ 4    │ caching              │ python     │ caching              │ beginner     │
│ 5    │ collections-module   │ python     │ collections, module  │ beginner     │
│ ... │ ...                  │ ...        │ ...                  │ ...          │
│ 51  │ unit-testing         │ python     │ unit, testing        │ beginner     │
└──────┴──────────────────────┴────────────┴──────────────────────┴──────────────┘

使用 'opendemo get <语言> <关键字>' 获取具体demo
```

### 示例2: 获取已有demo

```bash
$ python -m opendemo.cli get python logging

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

### 示例3: 强制重新生成demo

```bash
$ python -m opendemo.cli get python logging new

[i] 强制重新生成: logging
>>> 使用AI生成demo...
[OK] 成功生成demo

语言: python
主题: logging-new
输出位置: opendemo_output\python\logging-new
...
```

### 示例4: 执行demo

```bash
$ cd opendemo_output\python\logging
$ python code/logging_demo.py

==================================================
1. 基础日志配置
==================================================
2024-01-01 12:00:00 - INFO - 这是一条INFO日志
2024-01-01 12:00:00 - WARNING - 这是一条警告
...

所有日志示例完成!
```

## 项目结构说明

```
opendemo/
├── opendemo/                    # 主包
│   ├── __init__.py
│   ├── cli.py                   # CLI入口
│   ├── core/                    # 核心业务逻辑
│   │   ├── demo_manager.py      # Demo管理器
│   │   ├── search_engine.py     # 搜索引擎
│   │   ├── generator.py         # Demo生成器
│   │   ├── verifier.py          # 验证器
│   │   └── contribution.py      # 贡献管理
│   ├── services/                # 服务层
│   │   ├── ai_service.py        # AI服务
│   │   ├── config_service.py    # 配置服务
│   │   └── storage_service.py   # 存储服务
│   ├── utils/                   # 工具函数
│   │   ├── logger.py            # 日志工具
│   │   └── formatters.py        # 输出格式化
│   └── builtin_demos/           # 内置demo库
│       └── python/              # Python demo
├── opendemo_output/             # Demo输出目录
│   └── python/                  # Python demo (51个)
│       ├── abc-interfaces/      # 抽象基类
│       ├── async-programming/   # 异步编程
│       ├── logging/             # 日志记录
│       ├── collections-module/  # collections模块
│       └── ...                  # 更多demo
├── pyproject.toml               # 项目配置
├── README.md                    # 项目说明
└── USAGE_GUIDE.md              # 本文件
```

## 配置说明

配置文件位于 `~/.opendemo/config.yaml`,主要配置项:

### 通用配置

- `output_directory`: demo输出目录,默认 `./opendemo_output`
- `user_demo_library`: 用户demo库路径,默认 `~/.opendemo/demos`
- `default_language`: 默认编程语言,默认 `python`
- `enable_verification`: 是否启用自动验证,默认 `false`
- `verification_method`: 验证方法,默认 `venv`
- `verification_timeout`: 验证超时时间(秒),默认 `300`

### AI配置

- `ai.provider`: LLM服务提供商,默认 `openai`
- `ai.api_key`: API密钥(必须配置才能使用AI生成功能)
- `ai.api_endpoint`: API端点URL
- `ai.model`: 使用的模型,默认 `gpt-4`
- `ai.temperature`: 温度参数,默认 `0.7`
- `ai.max_tokens`: 最大token数,默认 `4000`

### 贡献配置

- `contribution.auto_prompt`: new命令后是否自动询问贡献,默认 `true`
- `contribution.author_name`: 贡献者名称
- `contribution.author_email`: 贡献者邮箱

### 显示配置

- `display.color_output`: 是否使用彩色输出,默认 `true`
- `display.page_size`: 搜索结果分页大小,默认 `10`
- `display.verbose`: 是否显示详细信息,默认 `false`

## 验证功能

如果启用验证功能,系统会在生成demo后自动:

1. 创建Python虚拟环境
2. 安装demo的依赖
3. 执行demo代码
4. 检查是否有错误

启用验证:

```bash
python -m opendemo.cli config set enable_verification true
```

或在执行命令时添加 `--verify` 标志:

```bash
python -m opendemo.cli get python 元组 --verify
python -m opendemo.cli new python 装饰器 --verify
```

## 贡献demo到公共库

使用 `new` 命令创建demo后,系统会询问是否贡献到公共库:

```bash
$ python -m opendemo.cli new python 生成器

# ... demo生成 ...

是否将此demo贡献到公共库? (y/n): y
✓ 已将demo保存到用户库: ~/.opendemo/demos/python/python-generator
```

贡献的demo会:
1. 保存到用户本地库
2. 通过验证检查
3. 生成贡献信息
4. 等待手动提交到GitHub仓库

## 常见问题

### Q1: 如何使用AI生成功能?

**A:** 需要先配置OpenAI API密钥:
```bash
python -m opendemo.cli config set ai.api_key sk-xxx
```

### Q2: 生成的demo在哪里?

**A:** 默认在当前目录的 `opendemo_output` 文件夹中,可通过配置修改:
```bash
python -m opendemo.cli config set output_directory /path/to/output
```

### Q3: 如何添加更多内置demo?

**A:** 在 `opendemo/builtin_demos/<language>/` 目录下创建新的demo目录,包含:
- `metadata.json` - 元数据
- `README.md` - 实操文档
- `code/` - 代码文件目录
- `requirements.txt` 或 `pom.xml` - 依赖声明

### Q4: 验证失败怎么办?

**A:** 查看详细错误信息,可能的原因:
- Python版本不兼容
- 依赖安装失败
- 代码有bug

可以手动检查生成的demo,或禁用验证功能。

## 下一步

1. 尝试搜索和获取内置demo
2. 配置AI API密钥体验AI生成功能
3. 创建自己的demo并贡献到社区
4. 查看设计文档了解更多技术细节

## 技术支持

- GitHub Issues: https://github.com/opendemo/opendemo/issues
- 文档: README.md
- 设计文档: .qoder/quests/open-demo-cli-development.md
