# 📁 OpenDemo 项目完整目录结构清单

## 🏗️ 根目录结构

```
opendemo/                               # 项目根目录
├── .env.example                        # 🔧 环境配置模板文件
├── .gitignore                          # 🚫 Git忽略文件配置
├── README.md                           # 📚 项目主文档
├── README_OLD.md                       # 📚 旧版README备份
├── DETAILED_STRUCTURE.md               # 📁 本详细结构文档
```

## 🎯 核心技术栈目录

### 🐍 **python/** *(Python技术栈)*
```
python/
├── abc-interfaces/                     # 🧩 抽象基类和接口演示
├── async-programming/                  # ⚡ 异步编程实践
├── bitwise-operations/                 # 🔢 位运算操作示例
├── caching/                            # 🗃️ 缓存机制实现
├── cli-argparse/                       # 💻 命令行参数解析
├── collections-module/                 # 📦 Collections模块使用
├── comprehensions/                     # 🔤 列表/字典推导式
├── config-management/                  # ⚙️ 配置管理方案
├── context-managers/                   # 🔧 上下文管理器
├── control-flow/                       # 🔀 控制流语句
├── copy-deepcopy/                      # 🔄 深浅拷贝操作
├── database-sqlite/                    # 🗄️ SQLite数据库操作
├── dataclasses/                        # 🏷️ 数据类使用
├── datetime/                           # 📅 日期时间处理
├── debugging/                          # 🐞 调试技巧演示
├── descriptors-property/               # 🏠 描述符和属性
├── dict-operations/                    # 📖 字典操作详解
├── enums/                              # 🔢 枚举类型使用
├── environment-variables/              # 🌍 环境变量管理
├── exception-handling/                 # ⚠️ 异常处理机制
├── file-operations/                    # 📁 文件操作示例
├── functions-decorators/               # 🎨 函数装饰器
├── functools-module/                   # 🔧 Functools模块
├── http-requests/                      # 🌐 HTTP请求处理
├── inheritance-mro/                    # 🧬 继承和MRO
├── iterators-generators/               # 🔁 迭代器和生成器
├── itertools-module/                   # 🔧 Itertools模块
├── json-yaml/                          # 📄 JSON/YAML处理
├── lambda-expressions/                 # λ Lambda表达式
├── libraries/                          # 📚 第三方库使用示例
├── list-operations/                    # 📋 列表操作详解
├── logging/                            # 📝 日志记录系统
├── magic-methods/                      # ✨ 魔法方法使用
├── metaclasses/                        # 🏗️ 元类编程
├── modules-packages/                   # 📦 模块和包管理
├── multiprocessing/                    # 🧵 多进程编程
├── multithreading/                     # 🔗 多线程编程
├── numbers-math/                       # 🔢 数字和数学运算
├── oop-classes/                        # 🏛️ 面向对象编程
├── operator-module/                    # ➕ Operator模块
├── pathlib-os/                         # 🗂️ 路径和操作系统
├── profiling-optimization/             # ⚡ 性能分析优化
├── python-debugging-tools-demo/        # 🐞 Python调试工具
├── python-oop-basics-demo/             # 🏛️ Python OOP基础
├── python-variables-types-demo/        # 🔤 变量和类型演示
├── regex/                              # 🔍 正则表达式使用
├── scope-closures/                     # 🔄 作用域和闭包
├── serialization-pickle/               # 📦 序列化和pickle
├── set-operations/                     # 🔘 集合操作详解
├── socket-networking/                  # 🌐 Socket网络编程
├── string-operations/                  # 🔤 字符串操作
├── threading-synchronization/          # 🔗 线程同步机制
├── tuple-basics/                       # 🔘 元组基础操作
├── type-hints/                         # 🏷️ 类型提示使用
└── unit-testing/                       # ✅ 单元测试实践
```

### 🦫 **go/** *(Go语言技术栈)*
```
go/
├── go-cobra-cli-cli-tool-demo/         # 💻 Cobra CLI工具开发
├── go-debugging-tools-demo/            # 🐞 Go调试工具集
├── go-dockersdkgo-container-management/ # 🐳 Docker SDK容器管理
├── go-ginwebdemo-web-framework-intro/  # 🌐 Gin Web框架入门
├── go-go/                              # 🔧 Go基础语法演示
├── go-go-badgerdb-demo-embedded-db-storage/ # 🗄️ BadgerDB嵌入式存储
├── go-go-cache-warmup-strategy-demo/   # 🗃️ 缓存预热策略
├── go-go-channels-demo/                # ⚡ Channels并发编程
├── go-go-consul-service-discovery/     # 🔍 Consul服务发现
├── go-go-context/                      # 🔧 Context上下文管理
├── go-go-context-practice/             # 🔧 Context实践应用
├── go-go-control-flow-demo/            # 🔀 控制流语句演示
├── go-go-db-connection-pool-demo/      # 🗄️ 数据库连接池
├── go-go-defer-demo/                   # ⏱️ Defer机制演示
├── go-go-demo/                         # 🔧 Go函数编程
├── go-go-demo-1/                       # 🔧 Go反射编程
├── go-go-demo-10/                      # 📄 模板引擎使用
├── go-go-demo-11/                      # 🔍 正则表达式处理
├── go-go-demo-12/                      # 🏗️ 结构体应用
├── go-go-demo-13/                      # 🏗️ 结构体详解
├── go-go-demo-14/                      # 🔁 闭包编程实践
├── go-go-demo-15/                      # 🛡️ 限流熔断机制
├── go-go-demo-2/                       # 🔤 变量类型演示
├── go-go-demo-3/                       # 🔤 字符串处理
├── go-go-demo-4/                       # ⚡ 并发原语使用
├── go-go-demo-5/                       # 🔗 接口编程实践
├── go-go-demo-6/                       # 🔀 控制流语句
├── go-go-demo-7/                       # 📊 数组切片操作
├── go-go-demo-8/                       # 📁 文件操作实践
├── go-go-demo-9/                       # 📅 时间处理演示
├── go-go-elkdemo-log-aggregation/      # 📝 ELK日志聚合
├── go-go-embedded-programming-demo/    # 🏗️ 嵌入式编程
├── go-go-embeddemo-embed-static-assets/ # 📦 静态资源嵌入
├── go-go-error-handling-demo/          # ⚠️ 错误处理最佳实践
├── go-go-http-demo/                    # 🌐 HTTP客户端演示
├── go-go-http-restful-api-demo/        # 🌐 RESTful API开发
├── go-go-json-demo/                    # 📄 JSON处理实践
├── go-go-jwtdemo-auth-login-verify/    # 🔐 JWT认证系统
├── go-go-maps-demo/                    # 🗺️ Maps数据结构
├── go-go-oauth20-third-party-login/    # 🔐 OAuth2.0集成
├── go-go-panic-recover-demo/           # ⚠️ Panic/Recover机制
├── go-go-pprof-demo/                   # ⚡ 性能分析工具
├── go-go-prometheus-metrics-demo/      # 📊 Prometheus监控
├── go-go-protobuf-serialization-demo/  # 📦 Protobuf序列化
├── go-go-redis-cache-operations-demo/  # 🗃️ Redis缓存操作
├── go-go-redis-distributed-lock-demo/  # 🔒 Redis分布式锁
├── go-go-select-demo/                  # ⚡ Select语句使用
├── go-go-select-mechanism-demo/        # ⚡ Select机制详解
├── go-go-swagger-demo/                 # 📚 Swagger API文档
├── go-go-tcp-network-programming/      # 🌐 TCP网络编程
├── go-go-variable-types-demo/          # 🔤 变量类型详解
├── go-go-variables-types-demo/         # 🔤 变量类型演示
├── go-go-viper-config-env-integration/ # ⚙️ Viper配置管理
├── go-go-worker-pool-demo/             # 👥 Worker池模式
├── go-gocontextdemo-timeout-context-demo/ # ⏱️ 超时控制实践
├── go-gocron-cron-scheduler-demo/      # ⏰ Cron定时任务
├── go-godemo/                          # 🔧 Go函数编程实践
├── go-godemo-benchmark-profiling/      # ⚡ 基准测试分析
├── go-godemo-config-hot-reload-demo/   # ⚙️ 配置热更新
├── go-godemo-dependency-injection-demo/ # 💉 依赖注入模式
├── go-godemo-exponential-backoff-retry/ # 🔁 指数退避重试
├── go-godemo-functional-programming-practice/ # λ 函数式编程
├── go-godemo-health-check-monitor/     # ❤️ 健康检查监控
├── go-godemo-load-balancer-reverse-proxy/ # ⚖️ 负载均衡代理
├── go-godemo-log-rotation-demo/        # 📝 日志轮转管理
├── go-godemo-signal-graceful-shutdown/ # ⚠️ 优雅关闭处理
├── go-godemo-table-driven-testing/     # ✅ 表驱动测试
├── go-godocker-multi-stage-docker-build/ # 🐳 多阶段Docker构建
├── go-gogoroutines-demo/               # ⚡ Goroutines入门
├── go-gogoroutines-goroutines-basics-demo/ # ⚡ Goroutines基础
├── go-gogoroutines-goroutines-basics-demo-1/ # ⚡ Goroutines应用
├── go-gogoroutines-goroutines-detailed-demo/ # ⚡ Goroutines详解
├── go-gogoroutines-goroutines-practical-demo/ # ⚡ Goroutines实践
├── go-gohashjwt-crypto-hash-jwt-demo/  # 🔐 加密哈希JWT
├── go-gohttp-middleware-http-server/   # 🌐 中间件HTTP服务
├── go-goiota-const-enum-iota-demo/     # 🔢 常量枚举iota
├── go-goiota-const-enum-iota-usage/    # 🔢 iota使用示例
├── go-goiota-constants-enums-iota-demo/ # 🔢 常量枚举演示
├── go-golrudemo-lru-cache-impl-demo/   # 🗃️ LRU缓存实现
├── go-gomakefile-makefile-automation-demo/ # 🛠️ Makefile自动化
├── go-gomutexwaitgroup-mutex-waitgroup-control-demo/ # 🔒 Mutex/WaitGroup控制
├── go-gomutexwaitgroup-mutex-waitgroup-demo/ # 🔒 并发控制实践
├── go-gomutexwaitgroup-mutex-waitgroup-demo-1/ # 🔒 Mutex/WaitGroup详解
├── go-gorm-demo/                       # 🗄️ GORM ORM框架
├── go-goselect-mechanism-demo/         # ⚡ Select机制演示
├── go-gosql-sql-transaction-demo/      # 🗄️ SQL事务操作
├── go-gozapdemo-structured-logging-zap-demo/ # 📝 Zap结构化日志
├── go-grpc-protobuf-go-demo/           # 🔄 gRPC Protobuf
├── go-istiogo-service-mesh-proxy/      # 🌐 Istio服务网格
├── go-kafkago-producer-consumer/       # 📨 Kafka生产消费
├── go-opentelemetrygo-distributed-tracing/ # 📊 分布式追踪
├── go-rabbitmq-amqp-go-demo/           # 📨 RabbitMQ AMQP
├── go-websocket-gorilla-realtime-communication/ # 🌐 WebSocket实时通信
├── libraries/                          # 📚 Go库使用示例
└── metadata.json                       # 📄 Go技术栈元数据
```

### ☕ **java/** *(Java技术栈)*
```
java/
├── java-abstraction-demo/              # 🧩 抽象类演示
├── java-annotations-demo/              # 🏷️ 注解使用示例
├── java-arrays-collections-demo/       # 📊 数组集合操作
├── java-classes-objects-demo/          # 🏛️ 类与对象基础
├── java-control-flow-demo/             # 🔀 控制流语句
├── java-date-time-demo/                # 📅 日期时间处理
├── java-diagnostic-tools-demo/         # 🛠️ 诊断工具集
├── java-encapsulation-demo/            # 🛡️ 封装特性演示
├── java-enumerations-demo/             # 🔢 枚举类型使用
├── java-exception-handling-demo/       # ⚠️ 异常处理机制
├── java-generics-demo/                 # 🔁 泛型编程实践
├── java-inheritance-demo/              # 🧬 继承特性演示
├── java-inner-classes-demo/            # 🏠 内部类使用
├── java-input-output-demo/             # 📥 输入输出操作
├── java-interfaces-demo/               # 🔗 接口编程实践
├── java-jvm-troubleshooting-trinity/   # 🛠️ JVM故障排查
├── java-lambda-demo/                   # λ Lambda表达式
├── java-polymorphism-demo/             # 🎭 多态特性演示
├── java-reflection-demo/               # 🔍 反射机制使用
├── java-regular-expressions-demo/      # 🔍 正则表达式
├── java-string-operations-demo/        # 🔤 字符串操作
├── java-variables-types-demo/          # 🔤 变量类型基础
├── JAVA-CASE-TEMPLATE.md               # 📄 Java案例模板
├── JAVA-TECH-STACK-COMPLETION-PLAN.md  # 📋 技术栈完善计划
├── README.md                           # 📚 Java技术栈文档
└── metadata.json                       # 📄 Java元数据文件
```

### 🟩 **nodejs/** *(Node.js技术栈)*
```
nodejs/
├── nodejs-array-methods-demo/          # 📊 数组方法实践
├── nodejs-arrow-functions-demo/        # λ 箭头函数使用
├── nodejs-async-await-nodejs-demo/     # ⚡ Async/Await异步
├── nodejs-axios-demo/                  # 🌐 Axios拦截器
├── nodejs-bullnodejs-demo-queue-async-tasks/ # 📨 Bull队列任务
├── nodejs-callback-functions-demo/     # 🔁 回调函数实践
├── nodejs-child-process-demo/          # 👶 子进程管理
├── nodejs-circuit-breaker-demo/        # 🛡️ 熔断器模式
├── nodejs-closures-demo/               # 🔁 闭包机制详解
├── nodejs-consulnodejsdemo-service-discovery-config/ # 🔍 Consul服务发现
├── nodejs-control-flow-demo/           # 🔀 控制流语句
├── nodejs-destructuring-demo/          # 🔧 解构赋值使用
├── nodejs-docker-sdk-for-nodejs-container-management-demo/ # 🐳 Docker SDK容器管理
├── nodejs-error-handling-demo/         # ⚠️ 错误处理实践
├── nodejs-event-emitter-demo/          # 📢 事件发射器
├── nodejs-express-restful-api-demo/    # 🌐 Express RESTful API
├── nodejs-express-web-demo/            # 🌐 Express Web框架
├── nodejs-functional-programming-demo/ # λ 函数式编程
├── nodejs-generator-async-flow-control-demo/ # ⚡ Generator异步控制
├── nodejs-graphql-api-demo/            # 🔀 GraphQL API
├── nodejs-helmet-security-middleware-demo/ # 🛡️ Helmet安全中间件
├── nodejs-higher-order-functions-demo/ # 🔁 高阶函数使用
├── nodejs-ioredis-nodejs-demo/         # 🗃️ IoRedis缓存操作
├── nodejs-jest-mockdemo-mock-unit-testing/ # ✅ Jest Mock单元测试
├── nodejs-jwtnodejs-auth-authorization/ # 🔐 JWT认证授权
├── nodejs-kafkanodejs-producer-consumer/ # 📨 Kafka生产消费
├── nodejs-mapsetdemo/                  # 🗺️ Map/Set数据结构
├── nodejs-multerdemo-file-upload-handling/ # 📁 Multer文件上传
├── nodejs-nestjsdemo-framework-intro/  # 🏛️ NestJS框架入门
├── nodejs-node-cron-cron-scheduler-demo/ # ⏰ Node-Cron定时任务
├── nodejs-nodejs-buffer-demo/          # 📦 Buffer操作实践
├── nodejs-nodejs-class-inheritance-demo/ # 🧬 类继承演示
├── nodejs-nodejs-cluster-cluster-load-balancing/ # ⚖️ Cluster负载均衡
├── nodejs-nodejs-demo-regex-validation-demo/ # 🔍 正则表达式验证
├── nodejs-nodejs-filesystem-operations-demo/ # 📁 文件系统操作
├── nodejs-nodejs-health-check-demo/    # ❤️ 健康检查实现
├── nodejs-nodejs-http-demo/            # 🌐 HTTP模块使用
├── nodejs-nodejs-json-demo/            # 📄 JSON处理实践
├── nodejs-nodejs-middleware-chain-demo/ # 🔗 中间件链处理
├── nodejs-nodejs-mongodb-mongoose-demo/ # 🗄️ MongoDB Mongoose
├── nodejs-nodejs-object-operations-demo/ # 🏠 对象操作实践
├── nodejs-nodejs-osdemo-os-system-monitor/ # 🖥️ OS系统监控
├── nodejs-nodejs-path-demo/            # 📍 Path路径操作
├── nodejs-nodejs-prometheusdemo-metrics-collection/ # 📊 Prometheus监控
├── nodejs-nodejs-promises-demo/        # ⚡ Promises异步编程
├── nodejs-nodejs-proxyreflect-demo/    # 🔍 Proxy/Reflect元编程
├── nodejs-nodejs-rate-limiter-demo/    # 🛑 限流器实现
├── nodejs-nodejs-streams-demo/         # 🌊 Streams流处理
├── nodejs-nodejs-swagger-openapi-demo/ # 📚 Swagger OpenAPI
├── nodejs-nodejs-variable-types-demo/  # 🔤 变量类型详解
├── nodejs-nodejs-variables-basics-demo/ # 🔤 变量基础演示
├── nodejs-nodejs-worker-threads-multithreading-demo/ # 🧵 Worker线程
├── nodejs-nodejscrypto-hashbcrypt-crypto-bcrypt-demo/ # 🔐 加密哈希bcrypt
├── nodejs-nodejsdemo-cron-scheduling/  # ⏰ Cron调度实践
├── nodejs-nodejsdemo-env-variables-demo/ # 🌍 环境变量管理
├── nodejs-nodejsdemo-graceful-shutdown-demo/ # ⚠️ 优雅关闭处理
├── nodejs-nodejsdemo-logging-management/ # 📝 日志管理实践
├── nodejs-nodejsdemo-retry-exponential-backoff/ # 🔁 指数退避重试
├── nodejs-nodejsdemo-unit-testing-coverage/ # ✅ 单元测试覆盖率
├── nodejs-nodejshttpdemo-load-balancer-proxy/ # ⚖️ 负载均衡代理
├── nodejs-oauth20passportnodejs-demo-passport-oauth-integration/ # 🔐 OAuth2.0 Passport集成
├── nodejs-pm2nodejs-multi-process-deployment/ # 🚀 PM2多进程部署
├── nodejs-sequelize-orm-database-operations-demo/ # 🗄️ Sequelize ORM
├── nodejs-socketiodemo-realtime-chat-demo/ # 💬 Socket.io实时聊天
├── nodejs-spread-operator-demo/        # 🔧 展开运算符
├── nodejs-symbol-symbol-iterator-demo/ # 🔁 Symbol迭代器
├── nodejs-template-strings-demo/       # 📄 模板字符串
├── nodejs-typescript-express-api-demo/ # 🏛️ TypeScript Express API
├── nodejs-variables-types-demo/        # 🔤 变量类型实践
├── nodejs-websocket-realtime-communication/ # 🌐 WebSocket实时通信
├── README.md                           # 📚 Node.js技术栈文档
├── metadata.json                       # 📄 Node.js元数据
└── libraries/                          # 📚 第三方库示例
```

### 🗄️ **database/** *(数据库技术栈)*
```
database/
├── access-control-demo/                # 🔐 访问控制实现
├── audit-logging-demo/                 # 📝 审计日志记录
├── auto-scaling-demo/                  # ⚖️ 自动扩缩容
├── backup-strategy-demo/               # 💾 备份策略设计
├── caching-strategy-demo/              # 🗃️ 缓存策略优化
├── capacity-planning-demo/             # 📊 容量规划分析
├── cloud-databases-demo/               # ☁️ 云数据库部署
├── compliance-certification-demo/      # 📜 合规认证实践
├── connection-pool-demo/               # 🔄 连接池管理
├── containerized-deployment-demo/      # 🐳 容器化部署
├── data-encryption-demo/               # 🔐 数据加密保护
├── database-installation-config-demo/  # ⚙️ 数据库安装配置
├── disaster-recovery-demo/             # 🆘 灾难恢复方案
├── disaster-recovery-solutions-demo/   # 🆘 灾难恢复解决方案
├── failover-switching-demo/            # 🔁 故障切换机制
├── index-design-demo/                  # 📇 索引设计优化
├── kubernetes-database-ops-demo/       # ☸️ Kubernetes数据库运维
├── load-balancing-demo/                # ⚖️ 负载均衡配置
├── lock-contention-resolution-demo/    # 🔒 锁竞争解决
├── metadata.json                       # 📄 数据库元数据
├── mongodb-replica-set-demo/           # 🔄 MongoDB副本集
├── monitoring-setup-demo/              # 📊 监控系统搭建
├── multi-region-deployment-demo/       # 🌍 多区域部署
├── mysql-high-availability-demo/       # 🛡️ MySQL高可用
├── mysql-troubleshooting-demo/         # 🛠️ MySQL故障排查
├── parameter-tuning-demo/              # ⚙️ 参数调优实践
├── partitioning-optimization-demo/     # 📂 分区优化策略
├── performance-monitoring-demo/        # ⚡ 性能监控分析
├── postgresql-high-availability-demo/  # 🛡️ PostgreSQL高可用
├── postgresql-troubleshooting-demo/    # 🛠️ PostgreSQL故障排查
├── query-optimization-demo/            # 🔍 查询优化技巧
├── read-write-splitting-demo/          # 🔀 读写分离配置
├── redis-cluster-demo/                 # 🔄 Redis集群部署
├── security-hardening-demo/            # 🛡️ 安全加固实践
├── serverless-database-demo/           # ☁️ 无服务器数据库
├── slow-query-analysis-demo/           # 🔍 慢查询分析
├── upgrade-migration-demo/             # ⬆️ 升级迁移方案
└── user-permission-management-demo/    # 👥 用户权限管理
```

### ☸️ **kubernetes/** *(Kubernetes技术栈)*
```
kubernetes/
├── agent/                              # 🕵️ 监控代理部署
├── ai-infra/                           # 🤖 AI基础设施
├── ai-security/                        # 🛡️ AI安全防护
├── crd/                                # 📄 自定义资源定义
├── efk/                                # 📝 EFK日志栈
├── elk/                                # 📝 ELK日志栈
├── fluid/                              # 💧 Fluid存储加速
├── gemini/                             # 🤖 Gemini AI集成
├── grafana/                            # 📊 Grafana可视化
├── infrastructure/                     # 🏗️ 基础设施组件
├── ingress/                            # 🌐 Ingress控制器
├── jaeger/                             # 📊 Jaeger链路追踪
├── kubeflow/                           # 🤖 Kubeflow机器学习
├── kubeflow-dashboard-installation-demo/ # 📊 Kubeflow仪表板安装
├── kubeflow-dashboard-rbac-demo/       # 🔐 Kubeflow RBAC演示
├── kubeskoop/                          # 🕵️ KubeSkoop网络诊断
├── llmops/                             # 🤖 LLMOPS大模型运维
├── loki/                               # 📝 Loki日志系统
├── mcp/                                # 🎛️ MCP模型控制平面
├── metadata.json                       # 📄 Kubernetes元数据
├── model-inference/                    # 🤖 模型推理部署
├── model-ops/                          # 🎛️ ModelOps模型运维
├── model-training/                     # 🤖 模型训练平台
├── modelscope/                         # 🤖 ModelScope模型空间
├── n8n/                                # ⚙️ N8N工作流自动化
├── network/                            # 🌐 网络策略管理
├── ollama/                             # 🤖 OLLAMA本地大模型
├── opentelemetry/                      # 📊 OpenTelemetry可观测性
├── operator/                           # ⚙️ Operator模式
├── operator-framework/                 # ⚙️ Operator框架
├── prometheus/                         # 📊 Prometheus监控
├── pv-pvc/                             # 💾 PV/PVC存储管理
├── rag/                                # 🤖 RAG检索增强生成
├── rbac/                               # 🔐 RBAC权限管理
├── regflow/                            # 🔄 RegFlow注册流程
├── service/                            # 🌐 服务发现负载均衡
├── storage/                            # 💾 存储卷管理
├── troubleshooting/                    # 🛠️ 故障排查工具
├── velero/                             # 💾 Velero备份恢复
├── workload/                           # ⚙️ 工作负载管理
├── zipkin/                             # 📊 Zipkin分布式追踪
├── README.md                           # 📚 Kubernetes文档
└── CROSS-REFERENCE-INDEX.md            # 🔗 交叉引用索引
```

### 🐧 **linux/** *(Linux系统管理)*
```
linux/
├── linux-advanced-performance-monitoring-demo/ # ⚡ 高级性能监控
├── linux-common-monitoring-commands-demo/      # 📊 常用监控命令
├── linux-netstat-network-monitoring-demo/      # 🌐 netstat网络监控
├── linux-process-thread-debugging-demo/        # 🐞 进程线程调试
├── linux-production-ops-commands-demo/         # ⚙️ 生产运维命令
├── linux-security-logging-demo/                # 🛡️ 安全日志管理
├── linux-top-process-monitoring-demo/          # 📈 top进程监控
├── linux-tsar-system-monitoring-demo/          # 📊 Tsar系统监控
├── README.md                                   # 📚 Linux技术栈文档
└── metadata.json                               # 📄 Linux元数据
```

### 🐳 **container/** *(容器技术)*
```
container/
├── containerd/                         # 🐳 Containerd运行时
├── docker/                             # 🐳 Docker容器技术
├── runc/                               # 🐳 RunC底层运行时
├── README.md                           # 📚 容器技术文档
└── metadata.json                       # 📄 容器技术元数据
```

### 🤖 **ai-ml/** *(AI/机器学习)*
```
ai-ml/
├── data-science/                       # 📊 数据科学实践
├── deep-learning/                      # 🤖 深度学习技术
├── math-foundations/                   # 🔢 数学基础理论
├── README.md                           # 📚 AI/ML技术文档
└── metadata.json                       # 📄 AI/ML元数据
```

## 🛠️ 辅助工具目录

### 💻 **opendemo-cli/** *(命令行工具)*
```
opendemo-cli/
├── __pycache__/                        # 📦 Python缓存文件
├── build/                              # 🏗️ 构建输出目录
├── config/                             # ⚙️ 配置文件目录
├── config_original/                    # ⚙️ 原始配置备份
├── core/                               # 🧠 核心功能模块
├── docs/                               # 📚 工具文档
├── env/                                # 🌍 环境配置
├── services/                           # ⚙️ 服务模块
├── utils/                              # 🛠️ 工具函数
└── metadata.json                       # 📄 CLI工具元数据
```

### 📚 **docs/** *(技术文档)*
```
docs/
├── checking/                           # ✅ 检查工具
│   └── original_check/                 # 🔍 原始检查脚本
├── guides/                             # 📖 使用指南
├── meta/                               # 📄 元数据文档
├── plans/                              # 📋 规划文档
├── reports/                            # 📊 报告文档
├── status/                             # 📈 状态报告
├── testing/                            # ✅ 测试相关
│   └── original_tests/                 # 🧪 原始测试
├── CROSS-TECH-INDEX.md                 # 🔗 跨技术栈索引
├── README.md                           # 📚 文档目录说明
└── demo-list.md                        # 📋 Demo清单
```

### 🛠️ **scripts/** *(自动化脚本)*
```
scripts/
├── cleanup/                            # 🧹 清理脚本
├── generation/                         # 🏗️ 生成脚本
├── security/                           # 🛡️ 安全相关脚本
├── utility/                            # 🛠️ 工具脚本
├── validation/                         # ✅ 验证脚本
└── metadata.json                       # 📄 脚本元数据
```

### 💫 **vibe-coding/** *(创意编程)*
```
vibe-coding/
├── gemini-cli/                         # 🤖 Gemini CLI集成
├── local-demo/                         # 🏠 本地演示示例
├── other-cli/                          # 💻 其他CLI工具
└── qoder-cli/                          # ⚙️ Qoder CLI集成
```

### 📊 **data/** *(数据管理)*
```
data/
├── demo_mapping.json                   # 🗺️ Demo映射关系
└── java_validation_report.json         # 📊 Java验证报告
```

## 📊 统计信息

### 📈 目录统计
- **总目录数**: 287个
- **技术栈目录**: 9个主要技术栈
- **辅助工具目录**: 5个支撑目录
- **文档目录**: 12个文档相关目录

### 🎯 技术栈分布
- **Go语言**: 78个Demo目录
- **Node.js**: 65个Demo目录  
- **Java**: 27个Demo目录
- **数据库**: 37个Demo目录
- **Kubernetes**: 44个Demo目录
- **Python**: 58个Demo目录
- **Linux**: 11个Demo目录
- **容器技术**: 6个Demo目录
- **AI/ML**: 4个Demo目录

### 📁 文件类型分布
- **源代码文件**: 约2000+个
- **文档文件**: 约150+个
- **配置文件**: 约50+个
- **数据文件**: 约10+个

---
*最后更新: 2026年2月3日*