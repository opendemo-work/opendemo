# Open Demo CLI

一个智能化的编程学习辅助CLI工具,帮助开发者快速获取高质量、可执行的编程语言demo代码。

## 核心功能

- 🚀 **快速获取Demo**: 通过简单命令获取特定编程语言和主题的完整示例代码
- 📚 **AI智能生成**: 本地库未找到时,自动调用AI生成高质量demo
- ✅ **可选验证**: 自动验证生成的代码可执行性,确保质量
- 🔍 **智能搜索**: 在本地demo库中快速搜索相关示例
- 🌍 **社区贡献**: 支持将优质demo贡献到公共库

## 支持的语言

- Python (51个内置Demo)
- Java (待扩充)
- 更多语言即将支持...

## 快速开始

### 安装

```bash
pip install opendemo
```

### 配置

首次使用需要配置AI API密钥:

```bash
opendemo config init
```

### 基本用法

**获取demo:**
```bash
opendemo get python logging      # 优先匹配已有demo
opendemo get python list         # 语义匹配 list-operations
opendemo get python logging new  # 强制重新生成
```

**搜索demo:**
```bash
opendemo search python           # 列出所有Python demo
opendemo search python async     # 按关键字过滤
```

**创建新demo:**
```bash
opendemo new python 异步HTTP请求处理
```

**配置管理:**
```bash
opendemo config set ai.api_key YOUR_API_KEY
opendemo config get ai.model
opendemo config list
```

## 项目结构

```
opendemo/
├── opendemo/              # 主包
│   ├── __init__.py
│   ├── cli.py             # CLI入口
│   ├── core/              # 核心业务逻辑
│   │   ├── demo_manager.py
│   │   ├── search_engine.py
│   │   ├── generator.py
│   │   └── verifier.py
│   ├── services/          # 服务层
│   │   ├── ai_service.py
│   │   ├── config_service.py
│   │   └── storage_service.py
│   ├── utils/             # 工具函数
│   │   ├── logger.py
│   │   └── formatters.py
│   └── builtin_demos/     # 内置demo库
│       ├── python/
│       └── java/
├── tests/                 # 测试文件
├── pyproject.toml         # 项目配置
└── README.md              # 说明文档
```

## 配置说明

配置文件位置:
- 全局配置: `~/.opendemo/config.yaml`
- 项目配置: `./.opendemo.yaml`

主要配置项:
- `output_directory`: demo输出目录
- `user_demo_library`: 用户demo库路径
- `enable_verification`: 是否启用自动验证
- `ai.api_key`: AI服务API密钥
- `ai.model`: 使用的AI模型

## Demo结构

每个demo包含:
- `metadata.json`: demo元数据
- `README.md`: 实操指南文档
- `code/`: 代码文件目录
- `requirements.txt` 或 `pom.xml`: 依赖声明
- `tests/`: 测试文件(可选)

## 开发

### 设置开发环境

```bash
git clone https://github.com/opendemo/opendemo.git
cd opendemo
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black opendemo/
```

## 贡献

欢迎贡献! 请查看贡献指南了解详情。

## 许可证

MIT License

## 联系方式

- 问题反馈: [GitHub Issues](https://github.com/opendemo/opendemo/issues)
- 文档: [项目文档](https://github.com/opendemo/opendemo#readme)
