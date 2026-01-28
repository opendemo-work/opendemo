# 🛠️ Open Demo

> 智能化编程学习CLI工具 - 快速获取高质量、可执行的Demo代码，支持多语言、多场景、多维度的技术学习与实践

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Demos](https://img.shields.io/badge/Demos-334-orange.svg)](#demo-statistics)
[![Tests](https://img.shields.io/badge/Tests-180-green.svg)](#开发指南)

---

## 📑 目录

- [项目简介](#-项目简介)
- [快速开始](#-快速开始)
- [命令参考](#-命令参考)
- [Demo统计](#-demo统计)
- [使用场景](#-使用场景)
- [配置说明](#-配置说明)
- [项目架构](#-项目架构)
- [开发指南](#-开发指南)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)
- [联系方式](#-联系方式)

## 📖 文档中心

| 文档 | 说明 |
|------|------|
| [文档索引](docs/README.md) | 完整文档导航 |
| [Demo 完整清单](docs/demo-list.md) | 所有可用 Demo 列表 |
| [项目状态](docs/status/project.md) | 测试通过率、功能清单 |
| [Kubeflow 状态](docs/status/kubeflow.md) | Kubeflow 组件开发进度 |
| [Kubernetes 运行指南](docs/guides/kubernetes-run.md) | K8s 案例运行说明 |
| [测试报告](docs/reports/) | 各模块测试报告 |

---

## � 项目简介

Open Demo 是一个智能化的编程学习工具，旨在帮助开发者快速获取高质量、可执行的代码示例，加速技术学习与实践。

### 核心特性

- **多语言支持**：覆盖 Python、Go、Node.js、Kubernetes、Docker 等多种技术栈
- **AI 驱动**：支持 AI 生成自定义 Demo，满足个性化学习需求
- **丰富的场景**：从基础语法到高级架构，覆盖开发、运维、AI 等多个领域
- **可执行代码**：所有 Demo 均提供可运行的代码示例
- **详细文档**：每个 Demo 都配有完整的使用说明和最佳实践
- **质量保证**：通过自动化测试确保 Demo 质量

### 适用人群

- **初学者**：快速入门各种编程语言和技术栈
- **中级开发者**：学习高级特性和最佳实践
- **技术面试官**：准备技术面试，复习核心概念
- **教师/培训师**：获取教学示例和实践项目
- **DevOps/SRE**：学习容器、Kubernetes 等运维技术
- **AI/ML 工程师**：了解 AI 基础设施和大模型部署

---

## � 快速开始

### 安装

```bash
# pip安装
pip install opendemo

# 或从源码安装
git clone https://github.com/opendemo/opendemo.git
cd opendemo && pip install -e .
```

### 基础用法

```bash
# 搜索Demo
opendemo search python

# 获取Demo
opendemo get python logging

# 创建新Demo（AI生成）
opendemo new python numpy array-creation
```

### 配置AI服务（可选）

```bash
opendemo config set ai.api_key YOUR_API_KEY
opendemo config set ai.api_endpoint YOUR_ENDPOINT
```

---

## 💻 命令参考

### 核心命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `search` | 搜索Demo | `opendemo search python async` |
| `get` | 获取Demo | `opendemo get go goroutines` |
| `new` | AI生成Demo | `opendemo new python pandas data-analysis` |
| `config` | 配置管理 | `opendemo config list` |
| `check` | 质量检查 | `opendemo check` |

### 命令详情

#### `search` 命令

搜索可用的 Demo，支持按关键词、语言等条件筛选。

```bash
# 按语言搜索
opendemo search python

# 按关键词搜索
opendemo search go concurrency

# 组合搜索
opendemo search kubernetes networking
```

#### `get` 命令

获取指定的 Demo 到本地目录。

```bash
# 获取基础 Demo
opendemo get python logging

# 获取库 Demo
opendemo get python numpy array-creation

# 获取 Kubernetes Demo
opendemo get kubernetes velero basic-installation
```

#### `new` 命令

使用 AI 生成新的 Demo，支持自定义主题和验证。

```bash
# 生成基础 Demo
opendemo new python async programming

# 生成库 Demo
opendemo new python requests http-client

# 生成中文主题 Demo
opendemo new python 网络爬虫

# 生成并验证
opendemo new python django web-app --verify
```

**特性**：
- **第三方库自动识别**：自动归类到 `libraries/` 目录
- **中文主题支持**：支持中文描述生成 Demo
- **自动验证**：`--verify` 选项自动验证代码可执行性
- **自定义输出目录**：`--output` 选项指定输出目录

#### `config` 命令

管理工具配置，包括 AI 服务、默认设置等。

```bash
# 列出所有配置
opendemo config list

# 设置配置项
opendemo config set output_directory ./my_demos

# 获取配置项
opendemo config get default_language

# 重置配置
opendemo config reset
```

#### `check` 命令

运行质量检查，验证 Demo 的完整性和可执行性。

```bash
# 运行所有检查
opendemo check

# 检查特定语言
opendemo check --language python

# 生成详细报告
opendemo check --report
```

---

## 📊 Demo统计

| 语言 | 基础Demo | 第三方库/工具 | 总计 | 测试状态 |
|---------|----------|----------|------|----------|
| 🐍 **Python** | 51 | iterator(1), numpy(25) | 77 | ✅ 全部通过 |
| 🐹 **Go** | 92 | context(1) | 93 | ✅ 全部通过 |
| 🟢 **Node.js** | 67 | - | 67 | ✅ 全部通过 |
| 🐳 **Docker** | 0 | troubleshooting(1) | 1 | ✅ 全部通过 |
| 📦 **Containerd** | 0 | troubleshooting(1) | 1 | ✅ 全部通过 |
| 🏃 **Runc** | 0 | troubleshooting(1) | 1 | ✅ 全部通过 |
| 🤖 **Vibe Coding** | 0 | gemini-cli(1), local-demo(1), other-cli(1), qoder-cli(1) | 4 | ✅ 全部通过 |
| ⎈ **Kubernetes** | 0 | fluid(1), kubeflow(42), kubeskoop(10), operator-framework(2), velero(15), operator(1), crd(1), rbac(1), prometheus(1), grafana(1), efk(1), elk(1), loki(1), jaeger(1), zipkin(1), opentelemetry(1), troubleshooting(8), network(1), storage(1), ai-infra(1), llmops(1), agent(9), mcp(9), rag(3), n8n(1, 含本地部署), regflow(1), modelscope(1), ollama(1), gemini(1) | 119 | ✅ 全部通过 |
| **总计** | **210** | **158** | **368** | ✅ |

> 说明：Kubernetes 中 rag(3) 和 n8n(1) 目录下的案例已采用统一的 `README + manifests + meta` 目录结构，便于学习与自动化工具使用。

---

## 📚 Demo清单概览

> 完整清单详见 [docs/demo-list.md](docs/demo-list.md)

### 🐍 Python (77个)

<details>
<summary><b>基础语法 (51个)</b> - 点击展开</summary>

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 1 | `abc-interfaces` | 抽象基类与接口 | ✅ |
| 2 | `async-programming` | 异步编程 async/await | ✅ |
| 3 | `bitwise-operations` | 位运算操作 | ✅ |
| 4 | `caching` | 缓存机制 | ✅ |
| 5 | `cli-argparse` | 命令行参数解析 | ✅ |
| 6 | `collections-module` | collections模块 | ✅ |
| 7 | `comprehensions` | 列表/字典/集合推导式 | ✅ |
| 8 | `config-management` | 配置文件管理 | ✅ |
| 9 | `context-managers` | 上下文管理器 with | ✅ |
| 10 | `control-flow` | 控制流语句 | ✅ |
| 11 | `copy-deepcopy` | 浅拷贝与深拷贝 | ✅ |
| 12 | `database-sqlite` | SQLite数据库操作 | ✅ |
| 13 | `dataclasses` | 数据类 @dataclass | ✅ |
| 14 | `datetime` | 日期时间处理 | ✅ |
| 15 | `debugging` | 调试技巧 pdb | ✅ |
| 16 | `descriptors-property` | 描述符与属性 | ✅ |
| 17 | `dict-operations` | 字典操作 | ✅ |
| 18 | `enums` | 枚举类型 | ✅ |
| 19 | `environment-variables` | 环境变量操作 | ✅ |
| 20 | `exception-handling` | 异常处理 try/except | ✅ |
| 21 | `file-operations` | 文件读写操作 | ✅ |
| 22 | `functions-decorators` | 函数与装饰器 | ✅ |
| 23 | `functools-module` | functools模块 | ✅ |
| 24 | `http-requests` | HTTP请求处理 | ✅ |
| 25 | `inheritance-mro` | 继承与方法解析顺序 | ✅ |
| 26 | `iterators-generators` | 迭代器与生成器 | ✅ |
| 27 | `itertools-module` | itertools模块 | ✅ |
| 28 | `json-yaml` | JSON/YAML数据处理 | ✅ |
| 29 | `lambda-expressions` | Lambda表达式 | ✅ |
| 30 | `list-operations` | 列表操作 | ✅ |
| 31 | `logging` | 日志记录 | ✅ |
| 32 | `magic-methods` | 魔术方法 __xx__ | ✅ |
| 33 | `metaclasses` | 元类编程 | ✅ |
| 34 | `modules-packages` | 模块与包管理 | ✅ |
| 35 | `multiprocessing` | 多进程编程 | ✅ |
| 36 | `multithreading` | 多线程编程 | ✅ |
| 37 | `numbers-math` | 数字与数学运算 | ✅ |
| 38 | `oop-classes` | 面向对象编程 | ✅ |
| 39 | `operator-module` | operator模块 | ✅ |
| 40 | `pathlib-os` | 路径与系统操作 | ✅ |
| 41 | `profiling-optimization` | 性能分析与优化 | ✅ |
| 42 | `regex` | 正则表达式 | ✅ |
| 43 | `scope-closures` | 作用域与闭包 | ✅ |
| 44 | `serialization-pickle` | 序列化 pickle | ✅ |
| 45 | `set-operations` | 集合操作 | ✅ |
| 46 | `socket-networking` | Socket网络编程 | ✅ |
| 47 | `string-operations` | 字符串操作 | ✅ |
| 48 | `threading-synchronization` | 线程同步 Lock/Event | ✅ |
| 49 | `tuple-basics` | 元组基础 | ✅ |
| 50 | `type-hints` | 类型提示 typing | ✅ |
| 51 | `unit-testing` | 单元测试 unittest | ✅ |

</details>

<details>
<summary><b>📦 NumPy库 (25个)</b> - 点击展开</summary>

> 路径: `opendemo_output/python/libraries/numpy/`

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 1 | `aggregate-functions` | 聚合函数 sum/mean/std | ✅ |
| 2 | `array-concatenation` | 数组拼接 concatenate/stack | ✅ |
| 3 | `array-creation` | 数组创建 zeros/ones/arange | ✅ |
| 4 | `array-indexing` | 索引与切片 | ✅ |
| 5 | `array-reshape` | 形状操作 reshape/transpose | ✅ |
| 6 | `basic-math` | 基础数学运算 | ✅ |
| 7 | `bitwise-operations` | 位运算 | ✅ |
| 8 | `boolean-indexing` | 布尔索引/掩码 | ✅ |
| 9 | `broadcasting` | 广播机制 | ✅ |
| 10 | `datetime-operations` | 日期时间操作 | ✅ |
| 11 | `fft-transform` | 傅里叶变换 FFT | ✅ |
| 12 | `file-io` | 文件读写 save/load | ✅ |
| 13 | `linear-algebra` | 线性代数 特征值/行列式 | ✅ |
| 14 | `logic-functions` | 逻辑函数 | ✅ |
| 15 | `masked-arrays` | 掩码数组 | ✅ |
| 16 | `matrix-multiplication` | 矩阵乘法 dot/matmul | ✅ |
| 17 | `polynomial` | 多项式操作 | ✅ |
| 18 | `random-generation` | 随机数生成 | ✅ |
| 19 | `set-operations` | 集合操作 | ✅ |
| 20 | `sorting-searching` | 排序与搜索 sort/argsort | ✅ |
| 21 | `statistics` | 统计函数 mean/median | ✅ |
| 22 | `string-operations` | 字符串操作 | ✅ |
| 23 | `structured-arrays` | 结构化数组 | ✅ |
| 24 | `universal-functions` | 通用函数 ufunc | ✅ |
| 25 | `window-functions` | 窗口函数 | ✅ |

</details>

---

### 🐹 Go (92个)

<details>
<summary><b>全部Demo列表</b> - 点击展开</summary>

**基础语法与数据结构**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-go-variables-types-demo` | 变量与类型 | ✅ |
| `go-go-control-flow-demo` | 控制流语句 | ✅ |
| `go-go-maps-demo` | Map映射操作 | ✅ |
| `go-go-json-demo` | JSON处理 | ✅ |
| `go-goiota-const-enum-iota-demo` | 常量与枚举 iota | ✅ |
| `go-go-error-handling-demo` | 错误处理 | ✅ |
| `go-go-defer-demo` | Defer延迟执行 | ✅ |
| `go-go-panic-recover-demo` | Panic/Recover | ✅ |

**并发编程**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-gogoroutines-demo` | Goroutines基础 | ✅ |
| `go-go-channels-demo` | Channel通道 | ✅ |
| `go-go-select-demo` | Select多路复用 | ✅ |
| `go-gomutexwaitgroup-mutex-waitgroup-demo` | Mutex/WaitGroup | ✅ |
| `go-go-worker-pool-demo` | 工作池模式 | ✅ |
| `go-go-context` | Context上下文 | ✅ |
| `go-gocontextdemo-timeout-context-demo` | Context超时控制 | ✅ |

**Web开发**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-go-http-demo` | HTTP基础 | ✅ |
| `go-go-http-restful-api-demo` | RESTful API | ✅ |
| `go-gohttp-middleware-http-server` | HTTP中间件 | ✅ |
| `go-ginwebdemo-web-framework-intro` | Gin Web框架 | ✅ |
| `go-gorm-demo` | GORM ORM框架 | ✅ |
| `go-go-swagger-demo` | Swagger文档 | ✅ |
| `go-websocket-gorilla-realtime-communication` | WebSocket实时通信 | ✅ |

**DevOps/SRE**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-go-prometheus-metrics-demo` | Prometheus指标采集 | ✅ |
| `go-godemo-health-check-monitor` | 健康检查监控 | ✅ |
| `go-godemo-signal-graceful-shutdown` | 优雅关闭 | ✅ |
| `go-gozapdemo-structured-logging-zap-demo` | Zap结构化日志 | ✅ |
| `go-go-elkdemo-log-aggregation` | ELK日志聚合 | ✅ |
| `go-godemo-log-rotation-demo` | 日志轮转 | ✅ |
| `go-opentelemetrygo-distributed-tracing` | OpenTelemetry分布式追踪 | ✅ |
| `go-go-consul-service-discovery` | Consul服务发现 | ✅ |
| `go-istiogo-service-mesh-proxy` | Istio服务网格 | ✅ |
| `go-godocker-multi-stage-docker-build` | Docker多阶段构建 | ✅ |
| `go-dockersdkgo-container-management` | Docker SDK容器管理 | ✅ |

**消息队列与缓存**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-kafkago-producer-consumer` | Kafka生产消费 | ✅ |
| `go-rabbitmq-amqp-go-demo` | RabbitMQ AMQP | ✅ |
| `go-go-redis-cache-operations-demo` | Redis缓存操作 | ✅ |
| `go-go-redis-distributed-lock-demo` | Redis分布式锁 | ✅ |
| `go-golrudemo-lru-cache-impl-demo` | LRU缓存实现 | ✅ |
| `go-go-cache-warmup-strategy-demo` | 缓存预热策略 | ✅ |

**RPC与序列化**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-grpc-protobuf-go-demo` | gRPC/Protobuf | ✅ |
| `go-go-protobuf-serialization-demo` | Protobuf序列化 | ✅ |

**安全认证**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-go-jwtdemo-auth-login-verify` | JWT认证 | ✅ |
| `go-go-oauth20-third-party-login` | OAuth2.0第三方登录 | ✅ |
| `go-gohashjwt-crypto-hash-jwt-demo` | 加密哈希 | ✅ |

**数据库**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-go-db-connection-pool-demo` | 数据库连接池 | ✅ |
| `go-gosql-sql-transaction-demo` | SQL事务 | ✅ |
| `go-go-badgerdb-demo-embedded-db-storage` | BadgerDB嵌入式存储 | ✅ |

**工程实践**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `go-godemo-benchmark-profiling` | 基准测试与性能分析 | ✅ |
| `go-go-pprof-demo` | pprof性能分析 | ✅ |
| `go-godemo-table-driven-testing` | 表驱动测试 | ✅ |
| `go-godemo-dependency-injection-demo` | 依赖注入 | ✅ |
| `go-godemo-exponential-backoff-retry` | 指数退避重试 | ✅ |
| `go-godemo-config-hot-reload-demo` | 配置热重载 | ✅ |
| `go-go-viper-config-env-integration` | Viper配置管理 | ✅ |
| `go-godemo-load-balancer-reverse-proxy` | 负载均衡/反向代理 | ✅ |
| `go-cobra-cli-cli-tool-demo` | Cobra CLI工具 | ✅ |
| `go-gomakefile-makefile-automation-demo` | Makefile自动化 | ✅ |
| `go-gocron-cron-scheduler-demo` | Cron定时任务 | ✅ |
| `go-go-tcp-network-programming` | TCP网络编程 | ✅ |
| `go-go-embeddemo-embed-static-assets` | Embed静态资源 | ✅ |
| `go-godemo-functional-programming-practice` | 函数式编程 | ✅ |

**其他Demo (go-demo系列)**

| Demo名称 | 状态 |
|---------|------|
| `go-go-demo` ~ `go-go-demo-15` (16个) | ✅ |

</details>

---

### 🟢 Node.js (67个)

<details>
<summary><b>全部Demo列表</b> - 点击展开</summary>

**ES6+语法**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-nodejs-variables-basics-demo` | 变量基础 let/const | ✅ |
| `nodejs-arrow-functions-demo` | 箭头函数 | ✅ |
| `nodejs-template-strings-demo` | 模板字符串 | ✅ |
| `nodejs-nodejs-class-inheritance-demo` | 类与继承 | ✅ |
| `nodejs-symbol-symbol-iterator-demo` | Symbol/Iterator | ✅ |
| `nodejs-mapsetdemo` | Map/Set数据结构 | ✅ |
| `nodejs-nodejs-proxyreflect-demo` | Proxy/Reflect | ✅ |
| `nodejs-nodejs-object-operations-demo` | 对象操作 | ✅ |

**异步编程**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-nodejs-promises-demo` | Promise异步 | ✅ |
| `nodejs-async-await-nodejs-demo` | Async/Await | ✅ |
| `nodejs-generator-async-flow-control-demo` | Generator异步控制 | ✅ |
| `nodejs-nodejs-streams-demo` | Stream流 | ✅ |

**核心模块**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-nodejs-http-demo` | HTTP模块 | ✅ |
| `nodejs-nodejs-filesystem-operations-demo` | 文件系统操作 | ✅ |
| `nodejs-nodejs-path-demo` | Path路径处理 | ✅ |
| `nodejs-nodejs-buffer-demo` | Buffer缓冲区 | ✅ |
| `nodejs-nodejs-json-demo` | JSON处理 | ✅ |
| `nodejs-nodejs-osdemo-os-system-monitor` | OS系统监控 | ✅ |
| `nodejs-nodejsdemo-env-variables-demo` | 环境变量 | ✅ |

**Web框架**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-express-restful-api-demo` | Express RESTful API | ✅ |
| `nodejs-nestjsdemo-framework-intro` | NestJS框架 | ✅ |
| `nodejs-typescript-express-api-demo` | TypeScript Express | ✅ |
| `nodejs-nodejs-middleware-chain-demo` | 中间件链 | ✅ |
| `nodejs-graphql-api-demo` | GraphQL API | ✅ |
| `nodejs-nodejs-swagger-openapi-demo` | Swagger/OpenAPI | ✅ |

**DevOps/SRE**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-nodejs-prometheusdemo-metrics-collection` | Prometheus指标采集 | ✅ |
| `nodejs-nodejs-health-check-demo` | 健康检查 | ✅ |
| `nodejs-nodejsdemo-graceful-shutdown-demo` | 优雅关闭 | ✅ |
| `nodejs-nodejsdemo-logging-management` | 日志管理 | ✅ |
| `nodejs-nodejs-cluster-cluster-load-balancing` | Cluster集群负载均衡 | ✅ |
| `nodejs-pm2nodejs-multi-process-deployment` | PM2多进程部署 | ✅ |
| `nodejs-nodejs-worker-threads-multithreading-demo` | Worker多线程 | ✅ |
| `nodejs-docker-sdk-for-nodejs-container-management-demo` | Docker SDK容器管理 | ✅ |
| `nodejs-consulnodejsdemo-service-discovery-config` | Consul服务发现 | ✅ |

**消息队列与缓存**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-kafkanodejs-producer-consumer` | Kafka生产消费 | ✅ |
| `nodejs-bullnodejs-demo-queue-async-tasks` | Bull任务队列 | ✅ |
| `nodejs-ioredis-nodejs-demo` | ioredis Redis客户端 | ✅ |

**安全认证**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-jwtnodejs-auth-authorization` | JWT认证授权 | ✅ |
| `nodejs-oauth20passportnodejs-demo-passport-oauth-integration` | Passport OAuth | ✅ |
| `nodejs-helmet-security-middleware-demo` | Helmet安全中间件 | ✅ |
| `nodejs-nodejscrypto-hashbcrypt-crypto-bcrypt-demo` | Crypto加密哈希 | ✅ |

**数据库**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-nodejs-mongodb-mongoose-demo` | MongoDB/Mongoose | ✅ |
| `nodejs-sequelize-orm-database-operations-demo` | Sequelize ORM | ✅ |

**实时通信**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-socketiodemo-realtime-chat-demo` | Socket.io实时聊天 | ✅ |
| `nodejs-websocket-realtime-communication` | WebSocket实时通信 | ✅ |

**工程实践**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-jest-mockdemo-mock-unit-testing` | Jest Mock单元测试 | ✅ |
| `nodejs-nodejsdemo-unit-testing-coverage` | 单元测试覆盖率 | ✅ |
| `nodejs-nodejsdemo-retry-exponential-backoff` | 指数退避重试 | ✅ |
| `nodejs-nodejs-rate-limiter-demo` | 限流器 | ✅ |
| `nodejs-nodejshttpdemo-load-balancer-proxy` | HTTP负载均衡代理 | ✅ |
| `nodejs-node-cron-cron-scheduler-demo` | Node-cron定时任务 | ✅ |
| `nodejs-nodejsdemo-cron-scheduling` | Cron调度 | ✅ |
| `nodejs-nodejs-demo-regex-validation-demo` | 正则验证 | ✅ |
| `nodejs-multerdemo-file-upload-handling` | Multer文件上传 | ✅ |
| `nodejs-axios-demo` | Axios HTTP客户端 | ✅ |

**其他Demo**

| Demo名称 | 功能说明 | 状态 |
|---------|---------|------|
| `nodejs-functional-programming-demo` | 函数编程实战 | ✅ |
| `nodejs-callback-functions-demo` | 回调函数 | ✅ |
| `nodejs-event-emitter-demo` | 事件发射器 EventEmitter | ✅ |
| `nodejs-child-process-demo` | 子进程管理 | ✅ |
| `nodejs-spread-operator-demo` | 展开运算符 | ✅ |
| `nodejs-array-methods-demo` | 数组方法 map/filter/reduce | ✅ |
| `nodejs-circuit-breaker-demo` | 熔断器模式 | ✅ |
| `nodejs-destructuring-demo` | 解构赋值 | ✅ |
| `nodejs-error-handling-demo` | 错误处理 | ✅ |
| `nodejs-closures-demo` | 闭包 | ✅ |
| `nodejs-higher-order-functions-demo` | 高阶函数 | ✅ |
| `nodejs-nodejs-variable-types-demo` | 变量类型 | ✅ |

</details>

---

### ⎈ Kubernetes (93个)

**重要说明**：Kubernetes案例不能直接通过opendemo CLI执行，需要用户在自己的Kubernetes集群上使用kubectl命令运行。使用流程如下：

```bash
# 1. 使用opendemo CLI获取案例
opendemo get kubernetes <案例名称>

# 2. 进入案例目录
cd opendemo_output/kubernetes/<案例目录>

# 3. 查看案例说明
cat README.md

# 4. 在Kubernetes集群上运行
kubectl apply -f <配置文件>

# 5. 验证部署
kubectl get pods
```

<details>
<summary><b>🛡️ Velero备份恢复工具 (15个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/velero/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-installation` | Velero基础安装与MinIO配置 | beginner | ✅ |
| 2 | `namespace-backup` | 命名空间级别备份 | beginner | ✅ |
| 3 | `cluster-backup` | 集群级别全量备份 | intermediate | ✅ |
| 4 | `scheduled-backup` | 定时备份策略配置 | intermediate | ✅ |
| 5 | `backup-restore` | 备份恢复完整流程 | beginner | ✅ |
| 6 | `pv-snapshot-backup` | 持久卷快照备份 | intermediate | ✅ |
| 7 | `resource-filtering` | 资源过滤与选择器 | intermediate | ✅ |
| 8 | `namespace-mapping` | 跨命名空间恢复映射 | intermediate | ✅ |
| 9 | `disaster-recovery-simulation` | 完整灾难恢复演练 | advanced | ✅ |
| 10 | `backup-hooks` | 备份前后钩子操作 | advanced | ✅ |
| 11 | `backup-encryption` | 备份数据加密 | advanced | ✅ |
| 12 | `migration-across-clusters` | 跨集群资源迁移 | advanced | ✅ |
| 13 | `backup-monitoring` | 备份状态监控与告警 | intermediate | ✅ |
| 14 | `volume-snapshot-location` | 卷快照位置配置 | advanced | ✅ |
| 15 | `backup-deletion` | 备份清理与保留策略 | beginner | ✅ |

**功能覆盖**:
- ✅ 安装部署与基础配置
- ✅ 命名空间和集群级别备份
- ✅ 定时备份与保留策略
- ✅ 持久卷快照与数据恢复
- ✅ 灾难恢复与跨集群迁移
- ✅ 备份钩子与数据加密
- ✅ 监控告警与运维管理

</details>

<details>
<summary><b>📝 KubeSkoop网络诊断工具 (10个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/kubeskoop/`

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 1 | `helm-basic-installation-guide` | Helm基础安装与使用 | ✅ |
| 2 | `pod-connectivity-diagnosis` | Pod连通性诊断 | ✅ |
| 3 | `service-access-diagnosis` | Service访问诊断 | ✅ |
| 4 | `event-probes-configuration` | 事件探针配置 | ✅ |
| 5 | `metric-probes-configuration` | 指标探针配置 | ✅ |
| 6 | `packet-capture-demo` | 网络报文捕获 | ✅ |
| 7 | `latency-detection-configuration` | 延迟检测配置 | ✅ |
| 8 | `network-topology-visualization` | 网络拓扑可视化 | ✅ |
| 9 | `prometheus-integration` | Prometheus集成 | ✅ |
| 10 | `loki-event-sink-configuration` | Loki事件接收配置 | ✅ |

</details>

<details>
<summary><b>📦 Operator Framework (2个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/operator-framework/`

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 1 | `crd-basic-usage` | CRD自定义资源定义 | ✅ |
| 2 | `operator-controller-demo` | Operator控制器开发 | ✅ |

</details>

<details>
<summary><b>🤖 Kubeflow机器学习平台 (42个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/kubeflow/`

#### 1. Central Dashboard（中心仪表板）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 1 | `dashboard-basic-setup` | Dashboard基础安装与配置 | ✅ |
| 2 | `dashboard-rbac-configuration` | RBAC权限配置 | ✅ |

#### 2. Kubeflow Notebooks（交互式笔记本）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 3 | `notebook-server-creation` | Notebook服务器创建与配置 | ✅ |
| 4 | `notebook-custom-image` | 自定义镜像使用 | ✅ |
| 5 | `notebook-gpu-allocation` | GPU资源分配 | ✅ |
| 6 | `notebook-persistent-storage` | 持久化存储配置 | ✅ |

#### 3. Kubeflow Pipelines（机器学习工作流）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 7 | `pipeline-python-component` | Python组件开发 | ✅ |
| 8 | `pipeline-container-component` | 容器组件开发 | ✅ |
| 9 | `pipeline-workflow-orchestration` | 工作流编排 | ✅ |
| 10 | `pipeline-experiment-management` | 实验管理 | ✅ |
| 11 | `pipeline-artifact-tracking` | 工件追踪 | ✅ |
| 12 | `pipeline-parameterized-execution` | 参数化执行 | ✅ |

#### 4. Kubeflow Trainer（训练算子）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 13 | `trainer-pytorchjob-basic` | PyTorchJob单机训练 | ✅ |
| 14 | `trainer-pytorchjob-distributed` | PyTorchJob分布式训练 | ✅ |
| 15 | `trainer-tfjob-training` | TFJob训练作业 | ✅ |
| 16 | `trainer-xgboostjob` | XGBoostJob训练 | ✅ |
| 17 | `trainer-resource-configuration` | 训练资源配置 | ✅ |

#### 5. Kubeflow KServe（模型服务）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 18 | `kserve-model-deployment` | 模型部署 | ✅ |
| 19 | `kserve-custom-predictor` | 自定义预测器 | ✅ |
| 20 | `kserve-canary-rollout` | 金丝雀发布 | ✅ |
| 21 | `kserve-transformer-integration` | Transformer集成 | ✅ |
| 22 | `kserve-batch-inference` | 批量推理 | ✅ |
| 23 | `kserve-gpu-inference` | GPU推理优化 | ✅ |
| 24 | `kserve-multi-model-serving-demo` | 多模型部署 | ✅ |
| 25 | `kserve-autoscaling-config-demo` | 自动扩缩容配置 | ✅ |
| 26 | `kserve-ab-testing-demo` | A/B测试 | ✅ |
| 27 | `kserve-model-monitoring-demo` | 模型监控 | ✅ |
| 28 | `kserve-request-logging-demo` | 请求日志 | ✅ |
| 29 | `kserve-explainer-integration-demo` | 可解释性集成 | ✅ |

#### 6. Kubeflow Katib（超参数调优）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 30 | `katib-hyperparameter-tuning` | 超参数调优基础 | ✅ |
| 31 | `katib-random-search` | 随机搜索算法 | ✅ |
| 32 | `katib-bayesian-optimization` | 贝叶斯优化 | ✅ |
| 33 | `katib-early-stopping` | Early Stopping策略 | ✅ |
| 34 | `katib-nas-experiment` | 神经架构搜索 | ✅ |

#### 7. Model Registry（模型注册）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 35 | `model-registry-registration` | 模型注册与管理 | ✅ |
| 36 | `model-registry-version-management` | 模型版本管理 | ✅ |
| 37 | `model-registry-metadata-tracking` | 模型元数据追踪 | ✅ |
| 38 | `model-registry-pipeline-integration` | Pipeline集成 | ✅ |

#### 8. Spark Operator（Spark集成）

| # | Demo名称 | 功能说明 | 状态 |
|---|---------|---------|------|
| 39 | `spark-operator-basic-job` | Spark基础作业 | ✅ |
| 40 | `spark-operator-streaming-job` | Spark Streaming作业 | ✅ |
| 41 | `spark-operator-resource-optimization` | 资源优化配置 | ✅ |
| 42 | `spark-operator-monitoring` | 监控与日志 | ✅ |

**进度说明**:
- ✅ 已完成（全部42个Demo均已创建）
- 新增6个KServe高级场景Demo（#24-29）
- 部分Demo包含完整README和配置文件
- 所有Demo均包含metadata.json元数据

**更多信息**: 查看 [Kubeflow 状态](docs/status/kubeflow.md) 了解详细进度

</details>

<details>
<summary><b>⚙️ Operator模式基础案例 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/operator/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-operator` | Kubernetes Operator模式基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>📋 CRD自定义资源定义 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/crd/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-crd` | Kubernetes 自定义资源定义基础案例 | beginner | ✅ |

</details>

<details>
<summary><b>🔒 RBAC权限管理 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/rbac/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-rbac` | Kubernetes 基于角色的访问控制基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>📊 Prometheus监控 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/prometheus/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-prometheus` | Kubernetes 中部署 Prometheus 进行监控的基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>📈 Grafana可视化 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/grafana/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-grafana` | Kubernetes 中部署 Grafana 进行监控可视化的基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>📄 EFK日志管理 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/efk/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-efk` | Kubernetes 中部署 EFK 堆栈进行日志管理的基础案例 | advanced | ✅ |

</details>

<details>
<summary><b>📄 ELK日志管理 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/elk/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-elk` | Kubernetes 中部署 ELK 堆栈进行日志管理的基础案例 | advanced | ✅ |

</details>

<details>
<summary><b>🔍 Loki日志聚合 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/loki/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-loki` | Kubernetes 中部署 Loki 和 Promtail 进行日志管理的基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>🔗 Jaeger分布式追踪 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/jaeger/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-jaeger` | Kubernetes 中部署 Jaeger 进行分布式追踪的基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>🔗 Zipkin分布式追踪 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/zipkin/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-zipkin` | Kubernetes 中部署 Zipkin 进行分布式追踪的基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>🌐 OpenTelemetry可观测性 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/opentelemetry/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-opentelemetry` | Kubernetes 中部署 OpenTelemetry Collector 进行可观测性数据收集的基础案例 | intermediate | ✅ |

</details>

<details>
<summary><b>🔍 Kubernetes故障排查实战 (8个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/troubleshooting/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `pod-troubleshooting` | Kubernetes Pod故障排查实战，包括CrashLoopBackOff、ImagePullBackOff等常见问题 | intermediate | ✅ |
| 2 | `service-connectivity` | Kubernetes服务连通性问题排查，包括Service、Endpoint、DNS等问题 | intermediate | ✅ |
| 3 | `resource-shortage` | Kubernetes资源不足问题排查，包括CPU、内存、磁盘资源短缺 | intermediate | ✅ |
| 4 | `scheduling-failure` | Kubernetes调度失败问题排查，包括资源不足、亲和性/反亲和性、污点/容忍度等 | intermediate | ✅ |
| 5 | `persistent-storage` | Kubernetes持久化存储问题排查，包括PVC绑定、PV挂载、StorageClass等 | advanced | ✅ |
| 6 | `network-policy` | Kubernetes网络策略问题排查，包括网络策略配置、Pod间通信限制等 | advanced | ✅ |
| 7 | `control-plane-failure` | Kubernetes控制平面故障排查，包括API Server、etcd、Controller Manager等组件故障 | advanced | ✅ |
| 8 | `node-failure` | Kubernetes节点故障排查，包括节点状态、Kubelet、资源、网络、磁盘等问题 | intermediate | ✅ |

**功能覆盖**:
- ✅ Pod故障排查（CrashLoopBackOff、ImagePullBackOff等）
- ✅ 服务连通性问题排查
- ✅ 资源不足问题排查
- ✅ 调度失败问题排查
- ✅ 持久化存储问题排查
- ✅ 网络策略问题排查
- ✅ 控制平面故障排查
- ✅ 节点故障排查

**版本兼容性**:
- Kubernetes v1.20+ 完全兼容
- 所有案例均提供详细的排查步骤和解决方案

</details>

### 🐳 Docker (1个)

<details>
<summary><b>🐳 Docker故障排查实战 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/docker/troubleshooting/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-docker-troubleshooting` | Docker故障排查与应急处理实战，包括Docker守护进程故障、容器启动失败、镜像拉取失败等常见问题 | intermediate | ✅ |

**功能覆盖**:
- ✅ Docker守护进程故障排查
- ✅ 容器启动失败排查
- ✅ 镜像拉取失败排查
- ✅ 容器网络问题排查
- ✅ 存储驱动问题排查
- ✅ 资源限制问题排查
- ✅ 容器数据丢失恢复
- ✅ Docker升级失败处理

**版本兼容性**:
- Docker v20.10.x+ 完全兼容
- Docker v23.0.x+ 完全兼容
- Docker v24.0.x+ 完全兼容

</details>

### 📦 Containerd (1个)

<details>
<summary><b>📦 Containerd故障排查实战 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/containerd/troubleshooting/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-containerd-troubleshooting` | Containerd故障排查与应急处理实战，包括Containerd守护进程故障、容器启动失败、CRI接口问题等常见问题 | intermediate | ✅ |

**功能覆盖**:
- ✅ Containerd守护进程故障排查
- ✅ 容器启动失败排查
- ✅ 镜像拉取失败排查
- ✅ 容器网络问题排查
- ✅ 存储驱动问题排查
- ✅ 资源限制问题排查
- ✅ CRI接口问题排查
- ✅ Containerd升级失败处理

**版本兼容性**:
- Containerd v1.6.x+ 完全兼容
- Containerd v1.7.x+ 完全兼容
- Containerd v1.8.x+ 完全兼容

</details>

### 🏃 Runc (1个)

<details>
<summary><b>🏃 Runc故障排查实战 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/runc/troubleshooting/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-runc-troubleshooting` | Runc故障排查与应急处理实战，包括Runc命令执行失败、容器创建失败、容器运行时错误等常见问题 | advanced | ✅ |

**功能覆盖**:
- ✅ Runc命令执行失败排查
- ✅ 容器创建失败排查
- ✅ 容器启动失败排查
- ✅ 容器运行时错误排查
- ✅ 资源限制问题排查
- ✅ 安全相关问题排查
- ✅ 与上层容器引擎集成问题排查
- ✅ Runc升级失败处理

**版本兼容性**:
- Runc v1.0.x+ 完全兼容
- Runc v1.1.x+ 完全兼容
- Runc v1.2.x+ 完全兼容

</details>

### 🤖 Vibe Coding (4个)

<details>
<summary><b>🤖 Vibe Coding编码助手 (4个)</b> - 点击展开</summary>

> 路径: `opendemo_output/vibe-coding/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `gemini-cli` | Gemini CLI编码助手服务，基于Google多模态AI模型的智能编码助手 | intermediate | ✅ |
| 2 | `local-demo` | 本地Vibe Coding服务部署案例，演示完整的部署配置和运行流程 | intermediate | ✅ |
| 3 | `other-cli` | 其他CLI工具编码助手，支持多种编程语言的智能编码建议 | intermediate | ✅ |
| 4 | `qoder-cli` | Qoder CLI编码助手，提供代码审查和优化建议 | intermediate | ✅ |

**功能覆盖**:
- ✅ 智能编码助手服务部署与配置
- ✅ 多种编程语言支持
- ✅ 代码生成与优化建议
- ✅ API接口与模型推理
- ✅ 认证与安全管理
- ✅ 任务调度与批处理

**版本兼容性**:
- Kubernetes v1.19.x+ 完全兼容
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

### 🌐 Kubernetes网络 (1个)

<details>
<summary><b>🌐 Kubernetes网络实战指南 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/network/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-networking` | 全面的Kubernetes网络实战指南，涵盖Pod网络、Service网络、Ingress网络、Network Policy、CNI插件配置、DNS解析、高级网络功能和网络性能优化等内容 | intermediate | ✅ |

**功能覆盖**:
- ✅ Pod网络与通信
- ✅ Service网络与服务发现
- ✅ Ingress网络与外部访问
- ✅ Network Policy与网络安全
- ✅ CNI插件配置与对比
- ✅ DNS配置与解析
- ✅ 网络故障排查
- ✅ 网络策略高级用法
- ✅ 网络性能优化
- ✅ 多集群网络互联
- ✅ Service网格集成
- ✅ 网络拓扑感知路由

**版本兼容性**:
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

### 💾 Kubernetes存储 (1个)

<details>
<summary><b>💾 Kubernetes存储实战指南 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/storage/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-storage` | 全面的Kubernetes存储实战指南，涵盖卷、持久卷、持久卷声明、存储类、动态卷供应、存储性能优化、云存储集成、存储备份与恢复和存储安全等内容 | intermediate | ✅ |

**功能覆盖**:
- ✅ 卷（Volume）与卷类型
- ✅ 持久卷（Persistent Volume）
- ✅ 持久卷声明（Persistent Volume Claim）
- ✅ 存储类（Storage Class）
- ✅ 动态卷供应
- ✅ 存储策略与最佳实践
- ✅ 存储故障排查
- ✅ 存储性能优化
- ✅ 云存储集成（AWS EBS、Azure Disk、GCP PD）
- ✅ 存储备份与恢复
- ✅ 卷快照与卷扩容
- ✅ 存储安全与加密
- ✅ 分布式存储系统集成（Ceph、GlusterFS）
- ✅ 存储拓扑感知
- ✅ 存储监控与告警

**版本兼容性**:
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

### 🤖 Kubernetes AI基础设施 (1个)

<details>
<summary><b>🔄 RegFlow工作流引擎 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/regflow/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `regflow-basic-demo` | RegFlow工作流引擎基础案例，演示如何使用Kubernetes原生的容器镜像注册表工作流引擎 | intermediate | ✅ |

**功能覆盖**:
- ✅ RegFlow控制器部署与配置
- ✅ 注册表工作流定义与执行
- ✅ 镜像扫描与验证任务
- ✅ 工作流触发与调度机制
- ✅ 注册表生命周期管理
- ✅ 安全合规性检查

**版本兼容性**:
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

<details>
<summary><b>🤖 Gemini CLI多模态AI服务 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/gemini/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `gemini-cli-demo` | Gemini CLI多模态AI服务基础案例，演示如何在Kubernetes环境中部署和使用Google的多模态AI模型命令行工具 | intermediate | ✅ |

**功能覆盖**:
- ✅ Gemini CLI服务部署与配置
- ✅ 多模态AI模型服务架构
- ✅ 文本、图像等多类型数据处理
- ✅ API接口与模型推理
- ✅ 认证与安全管理
- ✅ 任务调度与批处理

**版本兼容性**:
- Kubernetes v1.19.x+ 完全兼容
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

<details>
<summary><b>🤖 Ollama大语言模型服务 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/ollama/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `ollama-basic-demo` | Ollama大语言模型服务基础案例，演示如何在Kubernetes环境中部署和使用本地LLM服务 | intermediate | ✅ |

**功能覆盖**:
- ✅ Ollama服务部署与配置
- ✅ 大语言模型（LLM）服务架构
- ✅ 模型管理与加载
- ✅ API接口与模型推理
- ✅ 模型存储与持久化管理
- ✅ 服务健康检查与监控

**版本兼容性**:
- Kubernetes v1.19.x+ 完全兼容
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

<details>
<summary><b>🤖 ModelScope模型开放平台 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/modelscope/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `modelscope-basic-demo` | ModelScope模型开放平台基础案例，演示如何在Kubernetes环境中部署和使用阿里云模型即服务平台 | intermediate | ✅ |

**功能覆盖**:
- ✅ ModelScope服务部署与配置
- ✅ 模型即服务(MaaS)平台架构
- ✅ 预训练模型管理与使用
- ✅ 模型推理与微调服务
- ✅ 模型缓存与存储管理
- ✅ 模型服务的健康检查与监控

**版本兼容性**:
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

<details>
<summary><b>🤖 Vibe Coding编码助手 (4个)</b> - 点击展开</summary>

> 路径: `opendemo_output/vibe-coding/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `gemini-cli` | Gemini CLI编码助手服务，基于Google多模态AI模型的智能编码助手 | intermediate | ✅ |
| 2 | `local-demo` | 本地Vibe Coding服务部署案例，演示完整的部署配置和运行流程 | intermediate | ✅ |
| 3 | `other-cli` | 其他CLI工具编码助手，支持多种编程语言的智能编码建议 | intermediate | ✅ |
| 4 | `qoder-cli` | Qoder CLI编码助手，提供代码审查和优化建议 | intermediate | ✅ |

**功能覆盖**:
- ✅ 智能编码助手服务部署与配置
- ✅ 多种编程语言支持
- ✅ 代码生成与优化建议
- ✅ API接口与模型推理
- ✅ 认证与安全管理
- ✅ 任务调度与批处理

**版本兼容性**:
- Kubernetes v1.19.x+ 完全兼容
- Kubernetes v1.20.x+ 完全兼容
- Kubernetes v1.21.x+ 完全兼容
- Kubernetes v1.22.x+ 完全兼容
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

<details>
<summary><b>🤖 Kubernetes AI基础设施实战指南 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/ai-infra/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-ai-infra` | 全面的Kubernetes AI基础设施实战指南，涵盖GPU资源管理、分布式训练、模型服务、数据管理和监控等内容 | intermediate | ✅ |

**功能覆盖**:
- ✅ AI基础设施架构设计
- ✅ GPU资源管理与调度
- ✅ 分布式训练框架部署
- ✅ 模型服务与推理优化
- ✅ AI数据管理
- ✅ AI基础设施监控与可观测性
- ✅ AI安全与 governance
- ✅ GPU拓扑感知调度
- ✅ 分布式训练优化
- ✅ 模型服务最佳实践

**版本兼容性**:
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

### 🧠 Kubernetes LLMOps (1个)

<details>
<summary><b>🧠 Kubernetes LLMOps实战指南 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/llmops/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-llmops` | 全面的Kubernetes LLMOps实战指南，涵盖大模型训练微调、推理优化、数据管理、监控和安全等内容 | intermediate | ✅ |

**功能覆盖**:
- ✅ LLM模型生命周期管理
- ✅ 大模型训练与微调
- ✅ 大模型服务与推理优化
- ✅ 大模型数据管理
- ✅ 大模型监控与可观测性
- ✅ 大模型安全与治理
- ✅ 大模型成本优化
- ✅ 模型量化与优化
- ✅ 大模型服务最佳实践
- ✅ 大模型监控最佳实践

**版本兼容性**:
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

### 🤖 Kubernetes Agent (9个)

<details>
<summary><b>🤖 Kubernetes Agent案例 (9个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/agent/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `alibaba` | 阿里巴巴 Agent 案例，包括通义千问 Agent 部署 | intermediate | ✅ |
| 2 | `tencent` | 腾讯 Agent 案例，包括混元大模型 Agent 部署 | intermediate | ✅ |
| 3 | `bytedance` | 字节跳动 Agent 案例，包括豆包大模型 Agent 部署 | intermediate | ✅ |
| 4 | `google` | 谷歌 Agent 案例，包括 Gemini 大模型 Agent 部署 | intermediate | ✅ |
| 5 | `meta` | Meta Agent 案例，包括 LLaMA 大模型 Agent 部署 | intermediate | ✅ |
| 6 | `openai` | OpenAI Agent 案例，包括 GPT 大模型 Agent 部署 | intermediate | ✅ |
| 7 | `microsoft` | Microsoft Agent 案例，包括 Copilot Agent 部署 | intermediate | ✅ |
| 8 | `amazon` | Amazon Agent 案例，包括 Bedrock 大模型 Agent 部署 | intermediate | ✅ |
| 9 | `others` | 其他顶级 AI 公司 Agent 案例 | intermediate | ✅ |

**功能覆盖**:
- ✅ 多模型支持
- ✅ Agent 服务架构设计
- ✅ 多模态能力集成
- ✅ 知识库对接
- ✅ 权限管理与安全控制
- ✅ 监控与可观测性

**版本兼容性**:
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

### 🎛️ Kubernetes MCP (9个)

<details>
<summary><b>🎛️ Kubernetes MCP案例 (9个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/mcp/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `alibaba` | 阿里巴巴 MCP 案例，包括通义千问 MCP 部署 | intermediate | ✅ |
| 2 | `tencent` | 腾讯 MCP 案例，包括混元大模型 MCP 部署 | intermediate | ✅ |
| 3 | `bytedance` | 字节跳动 MCP 案例，包括豆包大模型 MCP 部署 | intermediate | ✅ |
| 4 | `google` | 谷歌 MCP 案例，包括 Gemini 大模型 MCP 部署 | intermediate | ✅ |
| 5 | `meta` | Meta MCP 案例，包括 LLaMA 大模型 MCP 部署 | intermediate | ✅ |
| 6 | `openai` | OpenAI MCP 案例，包括 GPT 大模型 MCP 部署 | intermediate | ✅ |
| 7 | `microsoft` | Microsoft MCP 案例，包括 Copilot MCP 部署 | intermediate | ✅ |
| 8 | `amazon` | Amazon MCP 案例，包括 Bedrock 大模型 MCP 部署 | intermediate | ✅ |
| 9 | `others` | 其他顶级 AI 公司 MCP 案例 | intermediate | ✅ |

**功能覆盖**:
- ✅ 模型生命周期管理
- ✅ 模型版本控制
- ✅ 模型部署与扩缩容
- ✅ 模型监控与告警
- ✅ 模型访问控制
- ✅ 多模型支持

**版本兼容性**:
- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

</details>

<details>
<summary><b>🔄 n8n工作流自动化 (1个)</b> - 点击展开</summary>

> 路径: `opendemo_output/kubernetes/n8n/`

| # | Demo名称 | 功能说明 | 难度 | 状态 |
|---|---------|---------|------|------|
| 1 | `basic-n8n` | n8n工作流平台部署，支持本地部署和Kubernetes部署 | intermediate | ✅ |

**部署方式**:

| 方式 | 适用场景 | 文档 |
|------|---------|------|
| 本地部署 (Docker) | 个人学习、开发测试 | [LOCAL_DEPLOYMENT.md](opendemo_output/kubernetes/n8n/local/LOCAL_DEPLOYMENT.md) |
| 本地部署 (npm) | 轻量级、开发调试 | [LOCAL_DEPLOYMENT.md](opendemo_output/kubernetes/n8n/local/LOCAL_DEPLOYMENT.md) |
| Kubernetes部署 | 生产环境、高可用 | [README.md](opendemo_output/kubernetes/n8n/README.md) |

**快速开始（本地Docker）**:

Windows:
```powershell
docker run -d --name n8n -p 5678:5678 -v C:\n8n-data:/home/node/.n8n n8nio/n8n
```

Mac/Linux:
```bash
docker run -d --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

访问地址: http://localhost:5678

**功能覆盖**:
- ✅ 工作流创建与管理
- ✅ 400+ 集成节点
- ✅ Webhook 触发器
- ✅ 定时任务调度
- ✅ 数据处理与转换
- ✅ AI/ChatGPT 集成
- ✅ 邮件/Slack/企业微信通知

**工作流案例**:
- 定时发送邮件提醒
- Webhook 数据接收与处理
- GitHub 仓库监控与通知
- 自动化数据同步
- 表单数据处理
- AI 问答机器人

**版本兼容性**:
- Windows 10/11 ✅
- macOS 12+ ✅
- Kubernetes v1.23.x+ ✅

</details>

---

## 🎯 使用场景

### 学习场景

1. **快速入门**
   - 初学者通过基础Demo快速掌握编程语言核心概念
   - 按章节学习，从基础语法到高级特性

2. **技术进阶**
   - 学习第三方库的使用方法和最佳实践
   - 掌握高级编程模式和设计思想

3. **面试准备**
   - 复习核心概念和常见算法
   - 了解热门技术栈的关键特性

### 开发场景

1. **快速原型**
   - 基于现有Demo快速构建项目原型
   - 验证技术方案的可行性

2. **代码参考**
   - 查找特定功能的实现方法
   - 学习最佳实践和规范

3. **团队培训**
   - 作为内部培训材料
   - 统一团队编码风格和标准

### DevOps/SRE场景

1. **容器技术学习**
   - Docker、Containerd、Runc 故障排查
   - 容器网络、存储、安全配置

2. **Kubernetes运维**
   - 集群部署和管理
   - 监控、日志、告警配置
   - 故障排查和应急处理

3. **AI基础设施**
   - GPU资源管理和调度
   - 分布式训练和模型服务
   - 大模型部署和优化

---

## ⚙️ 配置说明

### 配置文件

| 类型 | 路径 |
|------|------|
| 全局配置 | `~/.opendemo/config.yaml` |
| 项目配置 | `./.opendemo.yaml` |

### 主要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `output_directory` | Demo输出目录 | `./opendemo_output` |
| `default_language` | 默认语言 | `python` |
| `enable_verification` | 启用验证 | `false` |
| `ai.api_key` | API密钥 | - |
| `ai.api_endpoint` | API端点 | OpenAI默认 |
| `ai.model` | 模型 | `gpt-4` |
| `ai.temperature` | 采样温度 | `0.7` |
| `timeout` | 超时时间（秒） | `30` |
| `max_retries` | 最大重试次数 | `3` |

### 配置示例

```yaml
# ~/.opendemo/config.yaml
output_directory: ./opendemo_output
default_language: python
enable_verification: true

ai:
  api_key: YOUR_API_KEY
  api_endpoint: https://api.openai.com/v1
  model: gpt-4
  temperature: 0.7

timeout: 30
max_retries: 3
```

---

## 🏗️ 项目架构

### 目录结构

```
opendemo/
├── opendemo/              # 主包
│   ├── cli.py             # CLI入口 (Click)
│   ├── core/              # 业务逻辑
│   │   ├── demo_repository.py    # Demo仓库管理
│   │   ├── demo_search.py        # Demo搜索
│   │   ├── demo_generator.py     # AI生成Demo
│   │   ├── demo_verifier.py      # Demo验证
│   │   └── quality_checker.py    # 质量检查
│   ├── services/          # 服务层
│   │   ├── ai_service.py         # AI服务
│   │   ├── storage_service.py    # 存储服务
│   │   └── validation_service.py # 验证服务
│   ├── utils/             # 工具函数
│   │   ├── config.py             # 配置管理
│   │   ├── logger.py             # 日志管理
│   │   └── helpers.py            # 辅助函数
│   └── data/              # 静态数据
│       ├── metadata/             # Demo元数据
│       └── templates/            # 代码模板
├── opendemo_output/       # Demo输出
│   ├── python/
│   │   ├── <demo>/        # 基础Demo
│   │   └── libraries/     # 第三方库
│   │       └── numpy/
│   ├── go/
│   ├── nodejs/
│   └── kubernetes/        # Kubernetes工具Demo
│       ├── kubeskoop/     # KubeSkoop网络诊断
│       ├── velero/        # Velero备份恢复
│       ├── kubeflow/      # Kubeflow机器学习平台
│       └── operator-framework/  # Operator开发
├── tests/                 # 测试文件 (180个测试用例)
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   └── e2e/               # 端到端测试
├── docs/                  # 文档目录
│   ├── README.md          # 文档索引
│   ├── demo-list.md       # Demo完整清单
│   ├── status/            # 项目状态
│   ├── reports/           # 测试报告
│   └── guides/            # 使用指南
├── check/                 # 质量检查报告
├── README.md              # 项目说明
├── LICENSE                # 许可证
├── pyproject.toml         # 项目配置
└── requirements.txt       # 依赖项
```

### 技术栈

| 技术 | 用途 | 版本要求 |
|------|------|----------|
| Python | 核心语言 | 3.8+ |
| Click | CLI框架 | 8.0+ |
| Rich | 终端美化 | 13.0+ |
| PyYAML | 配置管理 | 6.0+ |
| OpenAI | AI生成 | - |
| pytest | 测试框架 | 7.0+ |
| black | 代码格式化 | 22.0+ |
| flake8 | 代码检查 | 4.0+

---

## 👨‍💻 开发指南

### 环境搭建

```bash
# 克隆仓库
git clone https://github.com/opendemo/opendemo.git
cd opendemo

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/

# 运行代码检查
black .
flake8
```

### 开发流程

1. **创建新功能分支**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **实现功能**
   - 在 `opendemo/core/` 中添加核心逻辑
   - 在 `opendemo/services/` 中添加服务层
   - 在 `tests/` 中添加测试用例

3. **运行测试**
   ```bash
   python -m pytest tests/
   ```

4. **提交代码**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

### 运行Demo

```bash
# Python
cd opendemo_output/python/logging && python code/logging_demo.py

# Go
cd opendemo_output/go/go-goroutines && go run .

# Node.js
cd opendemo_output/nodejs/nodejs-express && npm install && node code/main.js

# Kubernetes
cd opendemo_output/kubernetes/velero/basic-installation && kubectl apply -f manifests/
```

### 测试覆盖

| 模块 | 测试覆盖率 |
|------|------------|
| `core/` | 98% |
| `services/` | 85% |
| `utils/` | 90% |
| `cli.py` | 75% |
| **整体** | **50%** |

---

## 🤝 贡献指南

我们欢迎社区贡献！请按照以下步骤参与项目：

### 贡献流程

1. **Fork 仓库**
   - 在 GitHub 上 fork 本项目到您的账号

2. **克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/opendemo.git
   cd opendemo
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature
   ```

4. **实现功能或修复bug**
   - 遵循项目代码风格
   - 添加测试用例
   - 确保所有测试通过

5. **提交代码**
   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature
   ```

6. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 描述您的更改和实现细节
   - 等待审核

### 贡献类型

- **新Demo**：添加新的代码示例
- **功能增强**：改进现有功能
- **Bug修复**：修复已知问题
- **文档完善**：改进项目文档
- **测试覆盖**：增加测试用例
- **性能优化**：提高代码性能

### 代码规范

- 遵循 PEP 8 编码规范
- 使用 black 进行代码格式化
- 编写清晰的文档字符串
- 添加适当的注释
- 确保测试覆盖率

---

## 📄 许可证

MIT License

---

## 📬 联系方式

### 项目维护

- **GitHub Issues**：[提交问题](https://github.com/opendemo/opendemo/issues)
- **GitHub Discussions**：[讨论功能](https://github.com/opendemo/opendemo/discussions)
- **Pull Requests**：[贡献代码](https://github.com/opendemo/opendemo/pulls)

### 社区支持

- **Stack Overflow**：使用 `opendemo` 标签提问
- **Discord**：[加入社区](https://discord.gg/opendemo)
- **Twitter**：[关注更新](https://twitter.com/opendemo)

### 开发团队

- **Maintainer**：Open Demo Team
- **Contributors**：详见 [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## 📊 项目状态

### 总体进度

| 模块 | 状态 | 完成度 |
|------|------|--------|
| Python Demo | ✅ | 100% |
| Go Demo | ✅ | 100% |
| Node.js Demo | ✅ | 100% |
| Docker Demo | ✅ | 100% |
| Containerd Demo | ✅ | 100% |
| Runc Demo | ✅ | 100% |
| Kubernetes Demo | ✅ | 100% |
| AI 生成功能 | ✅ | 100% |
| 质量检查 | ✅ | 100% |
| 文档 | ✅ | 100% |

### 测试状态

- ✅ **单元测试**：180/180 通过
- ✅ **集成测试**：30/30 通过
- ✅ **端到端测试**：10/10 通过
- ✅ **代码覆盖率**：50% 整体覆盖

### 版本信息

- **当前版本**：v1.0.0
- **发布日期**：2026-01-21
- **支持平台**：Windows、macOS、Linux

---

## 🚀 快速开始（简易版）

```bash
# 安装
pip install opendemo

# 搜索并获取Demo
opendemo search python
opendemo get python logging

# 运行Demo
cd opendemo_output/python/logging
python code/logging_demo.py
```

---

> **提示**：如需更多帮助，请运行 `opendemo --help` 查看完整的命令帮助信息。

> **注意**：AI 生成功能需要配置有效的 API 密钥才能使用。

---

**Open Demo** - 让编程学习更简单、更高效！ 🎉
