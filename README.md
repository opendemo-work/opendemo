# Open Demo CLI

一个智能化的编程学习辅助CLI工具,帮助开发者快速获取高质量、可执行的编程语言demo代码。

## 核心功能

- 🚀 **快速获取Demo**: 通过简单命令获取特定编程语言和主题的完整示例代码
- 📚 **AI智能生成**: 本地库未找到时,自动调用AI生成高质量demo
- 📦 **第三方库支持**: AI智能识别第三方库，自动组织到libraries目录
- ✅ **可选验证**: 自动验证生成的代码可执行性,确保质量
- 🔍 **智能搜索**: 在本地demo库中快速搜索相关示例
- 🌍 **社区贡献**: 支持将优质demo贡献到公共库

## 支持的语言

- Python (51个内置Demo)
- **Go (89个内置Demo)** - 包含DevOps/SRE完整支持
- **Node.js (67个内置Demo)** - 包含DevOps/SRE完整支持
- Java (待扩充)

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
# Python Demo
opendemo get python logging      # 优先匹配已有demo
opendemo get python list         # 语义匹配 list-operations
opendemo get python logging new  # 强制重新生成

# Go Demo
opendemo get go goroutines       # 获取Go并发编程demo
opendemo get go prometheus       # 获取Prometheus监控demo
opendemo get go grpc             # 获取gRPC服务demo
opendemo get go health           # 获取健康检查demo

# Node.js Demo
opendemo get nodejs express      # 获取Express框架demo
opendemo get nodejs cluster      # 获取Cluster集群demo
opendemo get nodejs jwt          # 获取JWT认证demo
```

**搜索demo:**
```bash
opendemo search                  # 显示所有支持的语言
opendemo search python           # 列出所有Python demo
opendemo search python async     # 按关键字过滤
opendemo search go               # 列出所有Go demo
opendemo search nodejs           # 列出所有Node.js demo
```

**创建新demo:**
```bash
opendemo new python 异步HTTP请求处理
opendemo new go 并发编程 --difficulty intermediate
opendemo new nodejs async-await --difficulty intermediate
```

**第三方库Demo（自动识别并组织到libraries目录）:**
```bash
# AI会自动识别第三方库，并将demo输出到 libraries 目录
opendemo new python numpy                    # → opendemo_output/python/libraries/numpy/
opendemo new python requests HTTP请求       # → opendemo_output/python/libraries/requests/
opendemo new python pandas 数据分析          # → opendemo_output/python/libraries/pandas/
opendemo new java spring-boot web服务       # → opendemo_output/java/libraries/spring-boot/
opendemo new go gin 中间件                   # → opendemo_output/go/libraries/gin/
opendemo new nodejs express 路由             # → opendemo_output/nodejs/libraries/express/

# 普通编程主题（中文或标准库）输出到语言根目录
opendemo new python 数据处理               # → opendemo_output/python/
opendemo new python logging                 # → opendemo_output/python/ (标准库)
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
│   │   ├── verifier.py
│   │   ├── library_detector.py  # 库名检测器
│   │   └── library_manager.py   # 库管理器
│   ├── services/          # 服务层
│   │   ├── ai_service.py
│   │   ├── config_service.py
│   │   └── storage_service.py
│   ├── utils/             # 工具函数
│   │   ├── logger.py
│   │   └── formatters.py
│   └── builtin_demos/     # 内置demo库
│       ├── python/
│       ├── go/
│       ├── nodejs/
│       └── java/
├── scripts/               # 工具脚本
│   ├── start.py           # 交互式启动脚本
│   └── ...                # 其他脚本
├── data/                  # 数据文件目录
│   └── demo_mapping.json  # Demo映射配置
├── opendemo_output/       # 输出目录
│   ├── python/
│   │   ├── libraries/         # 第三方库Demo
│   │   │   ├── numpy/
│   │   │   ├── requests/
│   │   │   └── pandas/
│   │   └── <普通主题demo>/    # 编程主题Demo
│   ├── go/
│   │   └── libraries/
│   └── nodejs/
│       └── libraries/
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
- `requirements.txt` 或 `pom.xml` 或 `go.mod` 或 `package.json`: 依赖声明
- `tests/`: 测试文件(可选)

## 开发

### 设置开发环境

```bash
git clone https://github.com/opendemo/opendemo.git
cd opendemo
pip install -e ".[dev]"
```

### 交互式启动（可选）

如果你更喜欢菜单式的交互方式，可以使用交互式启动脚本：

```bash
python scripts/start.py
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
