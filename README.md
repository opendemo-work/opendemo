# 🛠️ Open Demo CLI

> 智能化编程学习CLI工具 - 快速获取高质量、可执行的Demo代码

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Demos](https://img.shields.io/badge/Demos-247-orange.svg)](#demo-statistics)

---

## 📑 目录

- [快速开始](#-快速开始)
- [命令参考](#-命令参考)
- [Demo统计](#-demo统计)
- [Demo完整清单](#-demo完整清单)
- [配置说明](#️-配置说明)
- [项目架构](#-项目架构)
- [开发指南](#-开发指南)

---

## 🚀 快速开始

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

| 命令 | 功能 | 示例 |
|------|------|------|
| `search` | 搜索Demo | `opendemo search python async` |
| `get` | 获取Demo | `opendemo get go goroutines` |
| `new` | AI生成Demo | `opendemo new python pandas` |
| `config` | 配置管理 | `opendemo config list` |

### new命令特性

- **第三方库自动识别**：`numpy`, `pandas`, `gin` 等自动归类到 `libraries/` 目录
- **中文主题支持**：`opendemo new python 网络爬虫`
- **验证选项**：`--verify` 自动验证代码可执行性

---

## 📊 Demo统计

| 语言 | 基础Demo | 第三方库/工具 | 总计 | 测试状态 |
|---------|----------|----------|------|----------|
| 🐍 **Python** | 51 | iterator(1), numpy(25) | 77 | ✅ 全部通过 |
| 🐹 **Go** | 92 | context(1) | 93 | ✅ 全部通过 |
| 🟢 **Node.js** | 67 | - | 67 | ✅ 全部通过 |
| ⎈ **Kubernetes** | 0 | kubeskoop(10) | 10 | ✅ 全部通过 |
| **总计** | **210** | **37** | **247** | ✅ |

---

## 📚 Demo完整清单

### 🐍 Python (76个)

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

### ⎈ Kubernetes (10个)

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

---

## 🏗️ 项目架构

```
opendemo/
├── opendemo/              # 主包
│   ├── cli.py             # CLI入口 (Click)
│   ├── core/              # 业务逻辑
│   │   ├── demo_repository.py
│   │   ├── demo_search.py
│   │   ├── demo_generator.py
│   │   └── demo_verifier.py
│   └── services/          # 服务层
│       ├── ai_service.py
│       └── storage_service.py
├── opendemo_output/       # Demo输出
│   ├── python/
│   │   ├── <demo>/        # 基础Demo
│   │   └── libraries/     # 第三方库
│   │       └── numpy/
│   ├── go/
│   ├── nodejs/
│   └── kubernetes/        # Kubernetes工具Demo
│       └── kubeskoop/     # KubeSkoop网络诊断
└── tests/                 # 测试文件
```

### 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.8+ | 核心语言 |
| Click | CLI框架 |
| Rich | 终端美化 |
| OpenAI API | AI生成 |

---

## 👨‍💻 开发指南

### 环境搭建

```bash
git clone https://github.com/opendemo/opendemo.git
cd opendemo
pip install -e ".[dev]"
```

### 运行测试

```bash
python -m pytest tests/
```

### 运行Demo

```bash
# Python
cd opendemo_output/python/logging && python code/logging_demo.py

# Go
cd opendemo_output/go/go-goroutines && go run .

# Node.js
cd opendemo_output/nodejs/nodejs-express && npm install && node code/main.js
```

---

## 📄 许可证

MIT License

---

## 📬 联系方式

- **Issues**: [GitHub Issues](https://github.com/opendemo/opendemo/issues)
- **Repository**: https://github.com/opendemo/opendemo
