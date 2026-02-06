# OpenDemo 技术演示平台 🚀

## 🎯 项目简介

OpenDemo 是一个综合性技术学习和演示平台，涵盖多种主流编程语言和技术栈的实战案例。本项目致力于提供高质量的技术示例和最佳实践指南，帮助开发者快速掌握各种技术栈的核心概念和实际应用。

> **项目规模**: 300+ 个技术演示案例 | **覆盖技术栈**: 10大类别 | **持续更新中**

---

## 📊 项目概览

### 🏗️ 技术栈分布

| 技术栈 | Demo数量 | 完备度 | 学习难度 | 主要用途 |
|--------|----------|--------|----------|----------|
| **Go语言** | 95个 | ✅ 完备 | 🟡 中等 | 系统编程、微服务 |
| **Node.js** | 71个 | ✅ 完备 | 🟢 简单 | Web开发、全栈应用 |
| **Java** | 23个 | 🚧 基础 | 🟡 中等 | 企业级应用开发 |
| **数据库** | 38个 | ✅ 完备 | 🟢 简单 | 数据存储与管理 |
| **基础设施** | 8个 | ✅ 完备 | 🟡 中等 | 负载均衡、API网关 |
| **监控系统** | 7个 | ✅ 完备 | 🟡 中等 | 系统监控、可视化 |
| **消息队列** | 4个 | ✅ 完备 | 🔴 困难 | 异步处理、应用解耦 |
| **Python** | 56个 | ✅ 完备 | 🟢 简单 | 数据科学、脚本开发 |
| **Kubernetes** | 43个 | ✅ 完备 | 🔴 困难 | 容器编排、云原生 |
| **Linux** | 19个 | ✅ 完备 | 🟡 中等 | 系统管理、运维 |
| **容器技术** | 0个 | ⏳ 规划中 | - | 容器化部署 |
| **AI/ML** | 15个 | ✅ 完备 | 🔴 困难 | 人工智能、机器学习、LLM训练推理运维 |

### 📈 学习路径推荐

#### 🎓 初学者路径
```
Python基础(4) → Node.js入门(15) → 数据库操作(10) → Linux基础(5)
     ↓              ↓                ↓              ↓
   快速上手      Web开发能力      数据处理能力      系统运维基础
```

#### 💼 全栈开发者路径
```
Node.js全套(65) → Go后端(20) → Kubernetes部署(10) → 数据库优化(15)
      ↓             ↓              ↓                  ↓
   前后端开发      高性能服务      云原生部署          数据架构
```

#### 🏢 企业级开发者路径
```
Java全套(45) → 微服务架构(15) → 数据库高可用(12) → 监控运维(8)
     ↓              ↓                ↓              ↓
  企业应用      分布式系统        数据可靠性      生产运维
```

---

## 🔍 多维度检索系统

### 📱 按技术栈检索

<details>
<summary><strong>🏗️ 基础设施技术栈</strong></summary>

#### 负载均衡与代理
- [`haproxy-traffic-management`](traffic/haproxy-traffic-management/) - HAProxy高级流量管理与路由
- [`haproxy-load-balancing`](traffic/haproxy-load-balancing/) - HAProxy负载均衡配置
- [`haproxy-ssl-termination`](traffic/haproxy-ssl-termination/) - HAProxy SSL终止配置
- [`nginx-web-server`](traffic/nginx-web-server/) - Nginx高性能Web服务器
- [`nginx-reverse-proxy`](traffic/nginx-reverse-proxy/) - Nginx反向代理配置
- [`nginx-load-balancing`](traffic/nginx-load-balancing/) - Nginx负载均衡设置

#### API网关与服务网格
- [`higress-api-gateway`](traffic/higress-api-gateway/) - Higress API网关演示
- [`higress-service-mesh`](traffic/higress-service-mesh/) - Higress服务网格配置

</details>

<details>
<summary><strong>📊 监控技术栈</strong></summary>

#### Prometheus监控
- [`prometheus-metrics-collection`](monitoring/prometheus-metrics-collection/) - Prometheus指标收集与告警
- [`prometheus-alerting`](monitoring/prometheus-alerting/) - Prometheus告警规则配置
- [`prometheus-federation`](monitoring/prometheus-federation/) - Prometheus联邦集群配置

#### 可视化与日志
- [`grafana-dashboard-custom`](monitoring/grafana-dashboard-custom/) - Grafana自定义仪表板
- [`grafana-alerting`](monitoring/grafana-alerting/) - Grafana告警配置
- [`kibana-log-analysis`](monitoring/kibana-log-analysis/) - Kibana日志分析
- [`kibana-visualization`](monitoring/kibana-visualization/) - Kibana数据可视化

</details>

<details>
<summary><strong>📬 消息队列技术栈</strong></summary>

#### RocketMQ消息队列
- [`rocketmq-producer-consumer`](messaging/rocketmq-producer-consumer/) - RocketMQ生产者消费者模式
- [`rocketmq-message-filtering`](messaging/rocketmq-message-filtering/) - RocketMQ消息过滤
- [`rocketmq-transaction-messages`](messaging/rocketmq-transaction-messages/) - RocketMQ事务消息
- [`rocketmq-delay-messages`](messaging/rocketmq-delay-messages/) - RocketMQ延迟消息

</details>



<details>
<summary><strong>🐍 Python 技术栈 (4个Demo)</strong></summary>

#### 基础语法系列
- [`python-variables-types-demo`](python/python-variables-types-demo/) - Python变量与数据类型基础
- [`python-oop-basics-demo`](python/python-oop-basics-demo/) - Python面向对象编程入门
- [`tuple-basics`](python/tuple-basics/) - Python元组操作详解

#### 调试工具系列
- [`python-debugging-tools-demo`](python/python-debugging-tools-demo/) - Python调试工具实战

</details>

<details>
<summary><strong>🦫 Go语言技术栈 (92个Demo)</strong></summary>

#### 基础语法系列
- [`go-go-basic-variables-demo`](go/go-go-basic-variables-demo/) - Go变量类型实战演示
- [`go-go-variable-types-demo`](go/go-go-variable-types-demo/) - Go变量类型演示
- [`go-go-control-flow-demo`](go/go-go-control-flow-demo/) - Go控制流演示
- [`go-go-control-statements-demo`](go/go-go-control-statements-demo/) - Go控制流语句实战演示
- [`go-go-functions-demo`](go/go-go-functions-demo/) - Go函数编程实战演示
- [`go-go-strings-processing-demo`](go/go-go-strings-processing-demo/) - Go字符串处理实战演示
- [`go-go-arrays-slices-demo`](go/go-go-arrays-slices-demo/) - Go数组与切片实战演示
- [`go-go-interfaces-demo`](go/go-go-interfaces-demo/) - Go接口实战演示
- [`go-go-structs-fundamentals-demo`](go/go-go-structs-fundamentals-demo/) - Go结构体基础演示
- [`go-go-structs-advanced-demo`](go/go-structs-advanced-demo/) - Go结构体高级应用演示

#### 并发编程系列
- [`go-gogoroutines-demo`](go/go-gogoroutines-demo/) - Go并发编程入门：Goroutines实战演示
- [`go-gogoroutines-goroutines-basics-demo`](go/go-gogoroutines-goroutines-basics-demo/) - Go并发编程实战：Goroutines入门
- [`go-gogoroutines-goroutines-detailed-demo`](go/go-gogoroutines-goroutines-detailed-demo/) - Go并发编程实战：Goroutines详解
- [`go-go-channels-demo`](go/go-go-channels-demo/) - Go Channels 实战演示
- [`go-go-select-demo`](go/go-go-select-demo/) - Go Select 机制实战演示
- [`go-gomutexwaitgroup-mutex-waitgroup-demo`](go/go-gomutexwaitgroup-mutex-waitgroup-demo/) - Go并发编程实战：Mutex与WaitGroup
- [`go-go-concurrency-primitives-demo`](go/go-go-concurrency-primitives-demo/) - Go并发原语实战演示
- [`go-go-closures-demo`](go/go-go-closures-demo/) - Go闭包编程实战演示

#### Web开发系列
- [`go-ginwebdemo-web-framework-intro`](go/go-ginwebdemo-web-framework-intro/) - Gin框架Web开发入门Demo
- [`go-go-http-restful-api-demo`](go/go-go-http-restful-api-demo/) - Go_HTTP_RESTful_API_Demo
- [`go-go-http-demo`](go/go-go-http-demo/) - Go HTTP客户端实战演示
- [`go-go-jwtdemo-auth-login-verify`](go/go-go-jwtdemo-auth-login-verify/) - Go-JWT认证用户登录验证Demo
- [`go-go-oauth20-third-party-login`](go/go-go-oauth20-third-party-login/) - Go OAuth2.0 第三方登录示例

#### 数据库系列
- [`go-gorm-demo`](go/go-gorm-demo/) - GORM增删改查实战演示
- [`go-gosql-sql-transaction-demo`](go/go-gosql-sql-transaction-demo/) - Go数据库SQL事务操作演示
- [`go-go-db-connection-pool-demo`](go/go-go-db-connection-pool-demo/) - Go数据库连接池管理演示

#### 中间件与工具系列
- [`go-go-redis-cache-operations-demo`](go/go-go-redis-cache-operations-demo/) - Go Redis缓存操作演示
- [`go-go-redis-distributed-lock-demo`](go/go-go-redis-distributed-lock-demo/) - Go-Redis分布式锁演示
- [`go-go-prometheus-metrics-demo`](go/go-go-prometheus-metrics-demo/) - Go_Prometheus_Metrics_Demo
- [`go-go-elkdemo-log-aggregation`](go/go-go-elkdemo-log-aggregation/) - Go-ELK日志聚合集成Demo
- [`go-gozapdemo-structured-logging-zap-demo`](go/go-gozapdemo-structured-logging-zap-demo/) - Go结构化日志管理Zap实战Demo

#### 微服务与云原生系列
- [`go-go-consul-service-discovery`](go/go-go-consul-service-discovery/) - Go Consul 服务注册与发现演示
- [`go-grpc-protobuf-go-demo`](go/go-grpc-protobuf-go-demo/) - gRPC-Protobuf-Go-Demo
- [`go-kafkago-producer-consumer`](go/go-kafkago-producer-consumer/) - Kafka生产者消费者Go示例
- [`go-rabbitmq-amqp-go-demo`](go/go-rabbitmq-amqp-go-demo/) - RabbitMQ_AMQP_Go_Demo
- [`go-opentelemetrygo-distributed-tracing`](go/go-opentelemetrygo-distributed-tracing/) - OpenTelemetry分布式追踪Go示例

#### 系统工具系列
- [`go-cobra-cli-cli-tool-demo`](go/go-cobra-cli-cli-tool-demo/) - Cobra CLI 工具开发演示
- [`go-go-viper-config-env-integration`](go/go-go-viper-config-env-integration/) - Go Viper配置管理与环境变量集成示例
- [`go-gocron-cron-scheduler-demo`](go/go-gocron-cron-scheduler-demo/) - Go定时任务调度Cron示例
- [`go-gocontextdemo-timeout-context-demo`](go/go-gocontextdemo-timeout-context-demo/) - Go超时控制与Context实践Demo
- [`go-go-reflection-meta-programming-demo`](go/go-go-reflection-meta-programming-demo/) - Go反射与元编程实战演示
- [`go-go-file-io-demo`](go/go-go-file-io-demo/) - Go文件操作实战演示
- [`go-go-time-processing-demo`](go/go-go-time-processing-demo/) - Go时间处理实战演示
- [`go-go-templates-demo`](go/go-go-templates-demo/) - Go模板引擎实战演示
- [`go-go-regex-text-matching-demo`](go/go-go-regex-text-matching-demo/) - Go正则表达式文本匹配实战演示
- [`go-go-rate-limiting-circuit-breaker-demo`](go/go-go-rate-limiting-circuit-breaker-demo/) - Go限流与熔断机制实战演示

#### 性能优化系列
- [`go-go-pprof-demo`](go/go-go-pprof-demo/) - Go pprof性能分析实战演示
- [`go-godemo-benchmark-profiling`](go/go-godemo-benchmark-profiling/) - Go基准测试性能分析Demo
- [`go-godemo-exponential-backoff-retry`](go/go-godemo-exponential-backoff-retry/) - Go指数退避重试机制Demo

</details>

<details>
<summary><strong>☕ Java技术栈 (45个Demo)</strong></summary>

#### 面向对象基础系列
- [`java-classes-objects-demo`](java/java-classes-objects-demo/) - Java类与对象演示
- [`java-variables-types-demo`](java/java-variables-types-demo/) - Java变量与类型演示
- [`java-encapsulation-demo`](java/java-encapsulation-demo/) - Java封装演示
- [`java-inheritance-demo`](java/java-inheritance-demo/) - Java继承演示
- [`java-polymorphism-demo`](java/java-polymorphism-demo/) - Java多态演示
- [`java-abstraction-demo`](java/java-abstraction-demo/) - Java抽象演示

#### 核心特性系列
- [`java-interfaces-demo`](java/java-interfaces-demo/) - Java接口演示
- [`java-enumerations-demo`](java/java-enumerations-demo/) - Java枚举演示
- [`java-inner-classes-demo`](java/java-inner-classes-demo/) - Java内部类演示
- [`java-annotations-demo`](java/java-annotations-demo/) - Java注解演示
- [`java-generics-demo`](java/java-generics-demo/) - Java泛型演示
- [`java-lambda-demo`](java/java-lambda-demo/) - Java Lambda表达式演示

#### 数据处理系列
- [`java-arrays-collections-demo`](java/java-arrays-collections-demo/) - Java数组与集合演示
- [`java-string-operations-demo`](java/java-string-operations-demo/) - Java字符串操作演示
- [`java-date-time-demo`](java/java-date-time-demo/) - Java日期时间处理演示
- [`java-regular-expressions-demo`](java/java-regular-expressions-demo/) - Java正则表达式演示

#### 异常处理系列
- [`java-exception-handling-demo`](java/java-exception-handling-demo/) - Java异常处理演示

#### JVM工具系列
- [`java-diagnostic-tools-demo`](java/java-diagnostic-tools-demo/) - Java诊断工具演示
- [`java-jvm-troubleshooting-trinity`](java/java-jvm-troubleshooting-trinity/) - Java JVM故障排查三剑客

#### 控制流系列
- [`java-control-flow-demo`](java/java-control-flow-demo/) - Java控制流演示

#### 输入输出系列
- [`java-input-output-demo`](java/java-input-output-demo/) - Java输入输出演示

#### 反射系列
- [`java-reflection-demo`](java/java-reflection-demo/) - Java反射演示

</details>

<details>
<summary><strong>🟩 Node.js技术栈 (65个Demo)</strong></summary>

#### 基础语法系列
- [`nodejs-nodejs-variables-basics-demo`](nodejs/nodejs-nodejs-variables-basics-demo/) - NodeJS变量基础演示
- [`nodejs-nodejs-variable-types-demo`](nodejs/nodejs-nodejs-variable-types-demo/) - NodeJS变量类型演示
- [`nodejs-control-flow-demo`](nodejs/nodejs-control-flow-demo/) - NodeJS控制流演示

#### 函数编程系列
- [`nodejs-arrow-functions-demo`](nodejs/nodejs-arrow-functions-demo/) - Arrow Functions Demo
- [`nodejs-callback-functions-demo`](nodejs/nodejs-callback-functions-demo/) - NodeJS回调函数实战演示
- [`nodejs-higher-order-functions-demo`](nodejs/nodejs-higher-order-functions-demo/) - Node.js高阶函数实战演示
- [`nodejs-closures-demo`](nodejs/nodejs-closures-demo/) - NodeJS闭包实战演示
- [`nodejs-functional-programming-demo`](nodejs/nodejs-functional-programming-demo/) - NodeJS函数编程实战演示

#### 异步编程系列
- [`nodejs-async-await-nodejs-demo`](nodejs/nodejs-async-await-nodejs-demo/) - async-await-nodejs-demo
- [`nodejs-nodejs-promises-demo`](nodejs/nodejs-nodejs-promises-demo/) - Node.js Promises 实战演示
- [`nodejs-generator-async-flow-control-demo`](nodejs/nodejs-generator-async-flow-control-demo/) - Generator异步流控制演示

#### Web开发系列
- [`nodejs-express-web-demo`](nodejs/nodejs-express-web-demo/) - Express Web框架入门
- [`nodejs-express-restful-api-demo`](nodejs/nodejs-express-restful-api-demo/) - Express_RESTful_API_Demo
- [`nodejs-nodejs-http-demo`](nodejs/nodejs-http-demo/) - Node.js HTTP模块实战演示
- [`nodejs-nodejs-middleware-chain-demo`](nodejs/nodejs-nodejs-middleware-chain-demo/) - Node.js中间件处理链演示
- [`nodejs-helmet-security-middleware-demo`](nodejs/nodejs-helmet-security-middleware-demo/) - Helmet安全中间件防护示例

#### 数据库系列
- [`nodejs-nodejs-mongodb-mongoose-demo`](nodejs/nodejs-nodejs-mongodb-mongoose-demo/) - NodeJS_MongoDB_Mongoose_Demo
- [`nodejs-sequelize-orm-database-operations-demo`](nodejs/nodejs-sequelize-orm-database-operations-demo/) - Sequelize ORM 数据库操作实战示例

#### 缓存与队列系列
- [`nodejs-ioredis-nodejs-demo`](nodejs/nodejs-ioredis-nodejs-demo/) - ioredis-nodejs-demo
- [`nodejs-bullnodejs-demo-queue-async-tasks`](nodejs/nodejs-bullnodejs-demo-queue-async-tasks/) - Bull队列异步任务处理Node.js Demo

#### 认证授权系列
- [`nodejs-jwtnodejs-auth-authorization`](nodejs/nodejs-jwtnodejs-auth-authorization/) - JWT认证与授权Node.js演示
- [`nodejs-oauth20passportnodejs-demo-passport-oauth-integration`](nodejs/nodejs-oauth20passportnodejs-demo-passport-oauth-integration/) - OAuth2.0授权Passport集成Node.js Demo

#### 消息队列系列
- [`nodejs-kafkanodejs-producer-consumer`](nodejs/nodejs-kafkanodejs-producer-consumer/) - Kafka生产者消费者Node.js演示

#### 实时通信系列
- [`nodejs-websocket-realtime-communication`](nodejs/nodejs-websocket-realtime-communication/) - WebSocket实时通信演示
- [`nodejs-socketiodemo-realtime-chat-demo`](nodejs/nodejs-socketiodemo-realtime-chat-demo/) - Socket.io实时聊天室Demo

#### 微服务系列
- [`nodejs-nodejs-cluster-cluster-load-balancing`](nodejs/nodejs-nodejs-cluster-cluster-load-balancing/) - Node.js_Cluster_多进程负载均衡示例
- [`nodejs-nodejshttpdemo-load-balancer-proxy`](nodejs/nodejs-nodejshttpdemo-load-balancer-proxy/) - Node.js负载均衡HTTP代理Demo
- [`nodejs-consulnodejsdemo-service-discovery-config`](nodejs/nodejs-consulnodejsdemo-service-discovery-config/) - Consul服务发现与配置中心Node.js集成Demo

#### 定时任务系列
- [`nodejs-node-cron-cron-scheduler-demo`](nodejs/nodejs-node-cron-cron-scheduler-demo/) - Node-Cron定时任务调度演示
- [`nodejs-nodejsdemo-cron-scheduling`](nodejs/nodejs-nodejsdemo-cron-scheduling/) - NodeJS定时任务调度Demo

#### 系统工具系列
- [`nodejs-nodejs-filesystem-operations-demo`](nodejs/nodejs-nodejs-filesystem-operations-demo/) - Node.js文件系统操作演示
- [`nodejs-nodejs-path-demo`](nodejs/nodejs-nodejs-path-demo/) - Node.js Path模块实战演示
- [`nodejs-nodejs-buffer-demo`](nodejs/nodejs-nodejs-buffer-demo/) - Node.js Buffer 操作实战演示
- [`nodejs-nodejs-osdemo-os-system-monitor`](nodejs/nodejs-nodejs-osdemo-os-system-monitor/) - Node.js OS模块系统信息监控Demo
- [`nodejs-child-process-demo`](nodejs/nodejs-child-process-demo/) - Node.js子进程管理实战演示
- [`nodejs-nodejs-worker-threads-multithreading-demo`](nodejs/nodejs-nodejs-worker-threads-multithreading-demo/) - Node.js Worker Threads 多线程编程实战示例

#### 数据处理系列
- [`nodejs-nodejs-json-demo`](nodejs/nodejs-nodejs-json-demo/) - Node.js JSON处理实战演示
- [`nodejs-nodejs-object-operations-demo`](nodejs/nodejs-nodejs-object-operations-demo/) - NodeJS对象操作实战：深拷贝、冻结与遍历
- [`nodejs-nodejs-demo-regex-validation-demo`](nodejs/nodejs-nodejs-demo-regex-validation-demo/) - NodeJS_正则表达式文本匹配验证_Demo
- [`nodejs-mapsetdemo`](nodejs/nodejs-mapsetdemo/) - MapSetDemo

#### 框架系列
- [`nodejs-nestjsdemo-framework-intro`](nodejs/nodejs-nestjsdemo-framework-intro/) - NestJS框架入门Demo
- [`nodejs-typescript-express-api-demo`](nodejs/nodejs-typescript-express-api-demo/) - TypeScript_Express_API_Demo

#### 安全系列
- [`nodejs-nodejscrypto-hashbcrypt-crypto-bcrypt-demo`](nodejs/nodejs-nodejscrypto-hashbcrypt-crypto-bcrypt-demo/) - NodeJS加密安全示例：Crypto Hash与Bcrypt实战

#### 部署运维系列
- [`nodejs-pm2nodejs-multi-process-deployment`](nodejs/nodejs-pm2nodejs-multi-process-deployment/) - PM2多进程部署Node.js示例
- [`nodejs-nodejsdemo-graceful-shutdown-demo`](nodejs/nodejs-nodejsdemo-graceful-shutdown-demo/) - Node.js优雅关闭实践Demo
- [`nodejs-nodejsdemo-health-check-demo`](nodejs/nodejs-nodejsdemo-health-check-demo/) - Node.js健康检查示例

#### 测试系列
- [`nodejs-nodejsdemo-unit-testing-coverage`](nodejs/nodejs-nodejsdemo-unit-testing-coverage/) - NodeJS单元测试与覆盖率实战Demo
- [`nodejs-jest-mockdemo-mock-unit-testing`](nodejs/nodejs-jest-mockdemo-mock-unit-testing/) - Jest Mock模拟单元测试Demo

#### 监控系列
- [`nodejs-nodejs-prometheusdemo-metrics-collection`](nodejs/nodejs-nodejs-prometheusdemo-metrics-collection/) - Node.js Prometheus监控指标采集Demo

#### 文件处理系列
- [`nodejs-multerdemo-file-upload-handling`](nodejs/nodejs-multerdemo-file-upload-handling/) - Multer文件上传处理Demo

#### 网络编程系列
- [`nodejs-axios-demo`](nodejs/nodejs-axios-demo/) - Axios拦截器实战演示
- [`nodejs-docker-sdk-for-nodejs-container-management-demo`](nodejs/nodejs-docker-sdk-for-nodejs-container-management-demo/) - Docker SDK for Node.js 容器管理演示

#### 限流熔断系列
- [`nodejs-nodejs-rate-limiter-demo`](nodejs/nodejs-nodejs-rate-limiter-demo/) - NodeJS限流器演示
- [`nodejs-circuit-breaker-demo`](nodejs/nodejs-circuit-breaker-demo/) - NodeJS熔断器模式实战演示

#### 重试机制系列
- [`nodejs-nodejsdemo-retry-exponential-backoff`](nodejs/nodejs-nodejsdemo-retry-exponential-backoff/) - NodeJS请求重试与指数退避机制实战Demo

#### 日志管理系列
- [`nodejs-nodejsdemo-logging-management`](nodejs/nodejs-nodejsdemo-logging-management/) - NodeJS日志管理Demo

#### 环境变量系列
- [`nodejs-nodejsdemo-env-variables-demo`](nodejs/nodejs-nodejsdemo-env-variables-demo/) - NodeJS环境变量管理Demo

#### 元编程系列
- [`nodejs-nodejs-proxyreflect-demo`](nodejs/nodejs-nodejs-proxyreflect-demo/) - Node.js Proxy与Reflect元编程实战演示

#### 类继承系列
- [`nodejs-nodejs-class-inheritance-demo`](nodejs/nodejs-nodejs-class-inheritance-demo/) - NodeJS类继承演示

#### 数据结构系列
- [`nodejs-array-methods-demo`](nodejs/nodejs-array-methods-demo/) - NodeJS数组方法实战演示
- [`nodejs-destructuring-demo`](nodejs/nodejs-destructuring-demo/) - Node.js解构赋值实战演示
- [`nodejs-spread-operator-demo`](nodejs/nodejs-spread-operator-demo/) - NodeJS展开运算符实战演示
- [`nodejs-symbol-symbol-iterator-demo`](nodejs/nodejs-symbol-symbol-iterator-demo/) - Symbol符号与迭代器应用示例
- [`nodejs-template-strings-demo`](nodejs/nodejs-template-strings-demo/) - template-strings-demo

#### 错误处理系列
- [`nodejs-error-handling-demo`](nodejs/nodejs-error-handling-demo/) - NodeJS错误处理实战演示

#### 事件处理系列
- [`nodejs-event-emitter-demo`](nodejs/nodejs-event-emitter-demo/) - Node.js事件发射器实战演示

#### 流处理系列
- [`nodejs-nodejs-streams-demo`](nodejs/nodejs-nodejs-streams-demo/) - Node.js Streams 实战演示

#### API文档系列
- [`nodejs-nodejs-swagger-openapi-demo`](nodejs/nodejs-nodejs-swagger-openapi-demo/) - NodeJS_Swagger_OpenAPI_Demo

#### GraphQL系列
- [`nodejs-graphql-api-demo`](nodejs/nodejs-graphql-api-demo/) - GraphQL API 查询语言实战演示

</details>

<details>
<summary><strong>🗄️ 数据库技术栈 (37个Demo)</strong></summary>

#### 基础管理系列
- [`database-installation-config-demo`](database/database-installation-config-demo/) - 数据库安装配置演示
- [`connection-pool-demo`](database/connection-pool-demo/) - 连接池配置演示
- [`user-permission-management-demo`](database/user-permission-management-demo/) - 用户权限管理演示
- [`access-control-demo`](database/access-control-demo/) - 访问控制演示
- [`security-hardening-demo`](database/security-hardening-demo/) - 安全加固演示

#### 高可用系列
- [`mysql-high-availability-demo`](database/mysql-high-availability-demo/) - MySQL高可用演示
- [`postgresql-high-availability-demo`](database/postgresql-high-availability-demo/) - PostgreSQL高可用演示
- [`mongodb-replica-set-demo`](database/mongodb-replica-set-demo/) - MongoDB副本集演示
- [`failover-switching-demo`](database/failover-switching-demo/) - 故障切换演示
- [`auto-scaling-demo`](database/auto-scaling-demo/) - 自动扩缩容演示

#### 性能优化系列
- [`query-optimization-demo`](database/query-optimization-demo/) - 查询优化演示
- [`index-design-demo`](database/index-design-demo/) - 索引设计演示
- [`partitioning-optimization-demo`](database/partitioning-optimization-demo/) - 分区优化演示
- [`slow-query-analysis-demo`](database/slow-query-analysis-demo/) - 慢查询分析演示
- [`performance-monitoring-demo`](database/performance-monitoring-demo/) - 性能监控演示
- [`lock-contention-resolution-demo`](database/lock-contention-resolution-demo/) - 锁竞争解决演示

#### 备份恢复系列
- [`backup-strategy-demo`](database/backup-strategy-demo/) - 备份策略演示
- [`disaster-recovery-demo`](database/disaster-recovery-demo/) - 灾难恢复演示
- [`disaster-recovery-solutions-demo`](database/disaster-recovery-solutions-demo/) - 灾难恢复解决方案演示
- [`upgrade-migration-demo`](database/upgrade-migration-demo/) - 升级迁移演示

#### 缓存系列
- [`caching-strategy-demo`](database/caching-strategy-demo/) - 缓存策略演示
- [`redis-cluster-demo`](database/redis-cluster-demo/) - Redis集群演示

#### 读写分离系列
- [`read-write-splitting-demo`](database/read-write-splitting-demo/) - 读写分离演示

#### 参数调优系列
- [`parameter-tuning-demo`](database/parameter-tuning-demo/) - 参数调优演示

#### 容器化部署系列
- [`containerized-deployment-demo`](database/containerized-deployment-demo/) - 容器化部署演示
- [`kubernetes-database-ops-demo`](database/kubernetes-database-ops-demo/) - Kubernetes数据库运维演示

#### 监控审计系列
- [`monitoring-setup-demo`](database/monitoring-setup-demo/) - 监控设置演示
- [`audit-logging-demo`](database/audit-logging-demo/) - 审计日志演示

#### 云数据库系列
- [`cloud-databases-demo`](database/cloud-databases-demo/) - 云数据库演示
- [`serverless-database-demo`](database/serverless-database-demo/) - 无服务器数据库演示

#### 多区域部署系列
- [`multi-region-deployment-demo`](database/multi-region-deployment-demo/) - 多区域部署演示

#### 合规认证系列
- [`compliance-certification-demo`](database/compliance-certification-demo/) - 合规认证演示

#### 容量规划系列
- [`capacity-planning-demo`](database/capacity-planning-demo/) - 容量规划演示

#### 负载均衡系列
- [`load-balancing-demo`](database/load-balancing-demo/) - 负载均衡演示

</details>

<details>
<summary><strong>☸️ Kubernetes技术栈 (16个Demo)</strong></summary>

#### 基础概念系列
- [`workload`](kubernetes/workload/) - 工作负载管理
- [`service`](kubernetes/service/) - 服务发现与负载均衡
- [`network`](kubernetes/network/) - 网络策略与通信
- [`storage`](kubernetes/storage/) - 存储卷管理
- [`pv-pvc`](kubernetes/pv-pvc/) - 持久卷声明管理

#### 运维工具系列
- [`agent`](kubernetes/agent/) - 监控代理部署
- [`troubleshooting`](kubernetes/troubleshooting/) - 故障排查工具

#### 基础设施系列
- [`infrastructure`](kubernetes/traffic/) - 基础设施组件
- [`ingress`](kubernetes/ingress/) - Ingress控制器配置

#### 安全系列
- [`rbac`](kubernetes/rbac/) - RBAC权限管理

#### 监控系列
- [`prometheus`](kubernetes/prometheus/) - Prometheus监控部署
- [`grafana`](kubernetes/grafana/) - Grafana可视化
- [`jaeger`](kubernetes/jaeger/) - Jaeger链路追踪
- [`zipkin`](kubernetes/zipkin/) - Zipkin分布式追踪

#### 日志系列
- [`efk`](kubernetes/efk/) - EFK日志栈
- [`elk`](kubernetes/elk/) - ELK日志栈
- [`loki`](kubernetes/loki/) - Loki日志系统

#### 备份恢复系列
- [`velero`](kubernetes/velero/) - Velero备份恢复

#### AI/ML系列
- [`kubeflow`](kubernetes/kubeflow/) - Kubeflow机器学习平台
- [`model-training`](kubernetes/model-training/) - 模型训练
- [`model-inference`](kubernetes/model-inference/) - 模型推理

#### 自定义资源系列
- [`crd`](kubernetes/crd/) - 自定义资源定义
- [`operator`](kubernetes/operator/) - Operator模式
- [`operator-framework`](kubernetes/operator-framework/) - Operator框架

#### 服务网格系列
- [`opentelemetry`](kubernetes/opentelemetry/) - OpenTelemetry可观测性

#### AI基础设施系列
- [`ai-infra`](kubernetes/ai-infra/) - AI基础设施
- [`ai-security`](kubernetes/ai-security/) - AI安全

#### 模型运维系列
- [`model-ops`](kubernetes/model-ops/) - ModelOps模型运维

#### RAG系列
- [`rag`](kubernetes/rag/) - RAG检索增强生成

#### MCP系列
- [`mcp`](kubernetes/mcp/) - MCP模型控制平面

#### LLMOPS系列
- [`llmops`](kubernetes/llmops/) - LLMOPS大语言模型运维

#### 模型注册系列
- [`modelscope`](kubernetes/modelscope/) - ModelScope模型空间

#### OLLAMA系列
- [`ollama`](kubernetes/ollama/) - OLLAMA本地大模型

#### REGFLOW系列
- [`regflow`](kubernetes/regflow/) - RegFlow注册流程

#### N8N系列
- [`n8n`](kubernetes/n8n/) - N8N工作流自动化

#### KUBEFLOW系列
- [`kubeflow-dashboard-installation-demo`](kubernetes/kubeflow-dashboard-installation-demo/) - Kubeflow仪表板安装演示
- [`kubeflow-dashboard-rbac-demo`](kubernetes/kubeflow-dashboard-rbac-demo/) - Kubeflow仪表板RBAC演示

#### 网络诊断系列
- [`kubeskoop`](kubernetes/kubeskoop/) - KubeSkoop网络诊断

#### 存储系列
- [`fluid`](kubernetes/fluid/) - Fluid加速存储

</details>

<details>
<summary><strong>🐧 Linux技术栈 (16个Demo)</strong></summary>

#### 系统监控系列
- [`linux-common-monitoring-commands-demo`](linux/linux-common-monitoring-commands-demo/) - Linux常用监控命令演示
- [`linux-top-process-monitoring-demo`](linux/linux-top-process-monitoring-demo/) - Linux top进程监控演示
- [`linux-advanced-performance-monitoring-demo`](linux/linux-advanced-performance-monitoring-demo/) - Linux高级性能监控演示
- [`linux-tsar-system-monitoring-demo`](linux/linux-tsar-system-monitoring-demo/) - Linux Tsar系统监控演示

#### 网络监控系列
- [`linux-netstat-network-monitoring-demo`](linux/linux-netstat-network-monitoring-demo/) - Linux netstat网络监控演示
- [`linux-nc-network-connections-demo`](linux/linux-nc-network-connections-demo/) - Linux nc网络连接工具演示
- [`linux-nslookup-dns-lookup-demo`](linux/linux-nslookup-dns-lookup-demo/) - Linux nslookup DNS查询工具演示
- [`linux-dig-dns-utility-demo`](linux/linux-dig-dns-utility-demo/) - Linux dig DNS查询工具演示
- [`linux-traceroute-network-path-demo`](linux/linux-traceroute-network-path-demo/) - Linux traceroute网络路径跟踪演示

#### 进程调试系列
- [`linux-process-thread-debugging-demo`](linux/linux-process-thread-debugging-demo/) - Linux进程线程调试演示

#### 生产运维系列
- [`linux-production-ops-commands-demo`](linux/linux-production-ops-commands-demo/) - Linux生产运维命令演示

#### 安全日志系列
- [`linux-security-logging-demo`](linux/linux-security-logging-demo/) - Linux安全日志演示

#### 数据同步系列
- [`linux-rsync-file-sync-demo`](linux/linux-rsync-file-sync-demo/) - Linux rsync文件同步工具演示

#### 文件监控系列
- [`linux-lsof-file-list-demo`](linux/linux-lsof-file-list-demo/) - Linux lsof文件列表工具演示

#### 系统监控系列 (新增)
- [`linux-htop-system-monitor-demo`](linux/linux-htop-system-monitor-demo/) - Linux htop系统监控工具演示

#### 磁盘IO监控系列
- [`linux-iotop-disk-monitor-demo`](linux/linux-iotop-disk-monitor-demo/) - Linux iotop磁盘IO监控工具演示

#### 网络配置系列
- [`linux-ifconfig-network-config-demo`](linux/linux-ifconfig-network-config-demo/) - Linux ifconfig网络配置工具演示

#### 现代网络管理系列
- [`linux-iproute2-network-tool-demo`](linux/linux-iproute2-network-tool-demo/) - Linux iproute2网络工具演示

</details>

<details>
<summary><strong>🐳 容器技术栈</strong></summary>

#### 容器运行时系列
- [`docker`](container/docker/) - Docker容器技术
- [`containerd`](container/containerd/) - Containerd容器运行时
- [`runc`](container/runc/) - RunC底层容器运行时

</details>

<details>
<summary><strong>🤖 AI/ML技术栈</strong></summary>

#### 基础数学系列
- [`math-foundations`](ai-ml/math-foundations/) - 机器学习数学基础

#### 深度学习系列
- [`deep-learning`](ai-ml/deep-learning/) - 深度学习核心技术

#### 数据科学系列
- [`data-science`](ai-ml/data-science/) - 数据科学实践

#### 大语言模型训练系列
- [`llm-training-demo`](ai-ml/llm-training-demo/) - 大语言模型训练实战演示

#### 大语言模型微调系列
- [`llm-fine-tuning-demo`](ai-ml/llm-fine-tuning-demo/) - 大语言模型微调实战演示

#### 大语言模型推理系列
- [`llm-inference-demo`](ai-ml/llm-inference-demo/) - 大语言模型推理实战演示

#### 大语言模型运维系列
- [`llm-ops-demo`](ai-ml/llm-ops-demo/) - 大语言模型运维实战演示

#### 大语言模型分布式训练系列
- [`llm-distributed-training-demo`](ai-ml/llm-distributed-training-demo/) - 大语言模型分布式训练实战演示

#### 大语言模型评估系列
- [`llm-evaluation-demo`](ai-ml/llm-evaluation-demo/) - 大语言模型评估实战演示

#### 大语言模型压缩系列
- [`llm-compression-demo`](ai-ml/llm-compression-demo/) - 大语言模型压缩实战演示

#### MLOps流水线系列
- [`mlops-pipeline-demo`](ai-ml/mlops-pipeline-demo/) - MLOps流水线实战演示

#### RAG系统系列
- [`rag-pipeline-demo`](ai-ml/rag-pipeline-demo/) - RAG(检索增强生成)管道实战演示

#### AI模型监控系列
- [`model-monitoring-demo`](ai-ml/model-monitoring-demo/) - AI模型监控与可观测性实战演示

#### 联邦学习系列
- [`federated-learning-demo`](ai-ml/federated-learning-demo/) - 联邦学习实战演示

#### AutoML系列
- [`automl-demo`](ai-ml/automl-demo/) - AutoML(自动化机器学习)实战演示

#### 模型服务系列
- [`model-serving-demo`](ai-ml/model-serving-demo/) - AI模型部署与推理服务实战演示

#### 计算机视觉系列
- [`computer-vision-demo`](ai-ml/computer-vision-demo/) - 计算机视觉实战演示

#### 自然语言处理系列
- [`nlp-foundation-demo`](ai-ml/nlp-foundation-demo/) - 自然语言处理基础实战演示

</details>

### 🔍 按功能主题检索

#### 🌐 Web开发相关
- **框架**: Gin(Go)、Express(Node.js)、NestJS(Node.js)
- **API**: RESTful API、GraphQL、gRPC
- **认证**: JWT、OAuth2.0、Passport
- **安全**: Helmet中间件、加密哈希

#### ⚡ 并发编程相关
- **Go**: Goroutines、Channels、Select、Mutex
- **Java**: 多线程、线程池
- **Node.js**: Worker Threads、Cluster

#### 🗄️ 数据库相关
- **ORM**: GORM(Go)、Sequelize(Node.js)、Mongoose(Node.js)
- **连接池**: 数据库连接池管理
- **缓存**: Redis操作、分布式锁
- **高可用**: 主从复制、故障切换

#### 🚀 微服务相关
- **服务发现**: Consul集成
- **消息队列**: Kafka、RabbitMQ
- **负载均衡**: 反向代理、多进程负载
- **监控**: Prometheus、健康检查

#### 📊 数据处理相关
- **JSON**: 解析与生成
- **文件操作**: 读写、上传、流处理
- **正则表达式**: 文本匹配与验证
- **数据结构**: Map、Set、数组操作

#### 🔧 系统工具相关
- **CLI**: Cobra(Go)、命令行参数解析
- **配置管理**: Viper(Go)、环境变量
- **定时任务**: Cron调度、定时器
- **日志管理**: Zap(Go)、结构化日志

#### 🛡️ 安全相关
- **认证授权**: JWT、OAuth2.0
- **加密**: 哈希算法、bcrypt
- **安全中间件**: Helmet、安全头设置
- **权限控制**: RBAC、访问控制

#### 📈 性能优化相关
- **基准测试**: 性能分析、pprof
- **缓存策略**: LRU缓存、预热策略
- **限流熔断**: 限流器、熔断器模式
- **重试机制**: 指数退避重试

#### 🐳 容器化相关
- **Docker**: 镜像构建、容器管理
- **Kubernetes**: 部署、服务发现、监控
- **编排**: Helm Charts、Operator模式

#### 🔍 调试监控相关
- **调试工具**: pprof、诊断工具
- **日志聚合**: ELK、EFK栈
- **链路追踪**: OpenTelemetry、Jaeger
- **健康检查**: 存活探针、就绪探针

### 🎯 按难度等级检索

#### 🟢 初级入门 (适合新手)
- Python基础语法
- Node.js变量类型
- Java类与对象
- 数据库基础操作
- Linux常用命令

#### 🟡 中级进阶 (有一定基础)
- Go并发编程
- Java面向对象特性
- Node.js异步编程
- 数据库性能优化
- Kubernetes基础概念

#### 🔴 高级专家 (深入学习)
- 微服务架构
- 分布式系统
- AI/ML工程实践
- 云原生运维
- 系统架构设计

---

## 📁 项目结构

> 💡 **提示**: 以下为基础目录结构，[查看完整详细结构清单](DETAILED_STRUCTURE.md)

```
opendemo/
├── ai-ml/              # 🤖 AI/机器学习技术栈
├── container/          # 🐳 容器化技术示例
├── data/               # 📊 数据管理和映射文件
├── database/           # 🗄️ 数据库相关演示
├── docs/               # 📚 技术文档资料
├── go/                 # 🦫 Go 语言技术栈
├── traffic/     # 🏗️ 基础设施技术栈
├── java/               # ☕ Java 企业级应用
├── kubernetes/         # ☸️ Kubernetes 容器编排
├── linux/              # 🐧 Linux 系统管理
├── messaging/          # 📬 消息队列技术栈
├── monitoring/         # 📊 监控技术栈
├── nodejs/             # 🟩 Node.js 全栈开发
├── opendemo-cli/       # 💻 CLI 命令行工具
├── python/             # 🐍 Python 数据科学
├── scripts/            # 🛠️ 自动化脚本工具
├── vibe-coding/        # 💫 创意编程和AI助手集成
└── .env.example        # ⚙️ 环境配置模板
```

## 🛠️ 快速开始指南

### 📥 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd opendemo

# 复制环境配置
cp .env.example .env

# 编辑配置文件（根据实际需求填写）
nano .env
```

### 🔒 安全检查
```bash
# 运行自动化安全扫描
./scripts/security/check_security.sh

# 生成项目所需密钥
./scripts/security/generate_keys.sh
```

### 🚀 运行第一个Demo

```bash
# 选择一个简单的demo开始
cd python/python-variables-types-demo/

# 查看README了解运行方式
cat README.md

# 运行示例
python main.py
```

### 📚 学习路径建议

#### 🎓 新手入门路径
1. 从Python基础开始（简单易懂）
2. 学习Node.js Web开发（实用性强）
3. 掌握数据库操作（必需技能）
4. 了解Linux基础（运维必备）

#### 💼 职业发展路径
- **Web全栈开发者**: Node.js → Go → Kubernetes
- **后端工程师**: Java → 微服务 → 云原生
- **数据工程师**: Python → 数据库 → 大数据
- **DevOps工程师**: Linux → 容器 → Kubernetes

### 🛠️ 开发工具

#### 安全工具
- `./scripts/security/check_security.sh` - 安全检查
- `./scripts/security/scan_secrets.py` - 敏感信息扫描
- `./scripts/security/generate_keys.sh` - 密钥生成

#### 开发辅助
- `make help` - 查看可用命令
- `make test` - 运行测试
- `make lint` - 代码检查

### 📚 文档资源
- [安全配置指南](SECURITY_CONFIG.md)
- [跨技术栈索引](docs/CROSS-TECH-INDEX.md)
- [技术栈规划](java/JAVA-TECH-STACK-COMPLETION-PLAN.md)
- [项目元数据映射](data/demo_mapping.json)
- [Java验证报告](data/java_validation_report.json)
- [详细目录结构](DETAILED_STRUCTURE.md)

---

## 🤝 参与贡献

### 📝 贡献方式
- 🐛 修复bug和完善现有demo
- ✨ 添加新的技术示例
- 📚 补充文档和注释
- 🔧 优化项目结构和工具
- 🎨 改进用户体验

### 🎯 贡献重点领域
- **Java技术栈完善**: 当前只有45个demo，需要扩充至100+
- **AI/ML技术栈建设**: 从0开始构建机器学习示例
- **容器技术深化**: Docker和Kubernetes实践案例
- **跨技术栈整合**: 不同技术栈间的协同示例

### 📋 贡献流程
1. Fork项目到个人仓库
2. 创建功能分支 `git checkout -b feature/NewDemo`
3. 提交更改 `git commit -m 'Add new demo example'`
4. 推送到分支 `git push origin feature/NewDemo`
5. 发起Pull Request

---

## 📊 项目统计

### 📈 当前状态
- **总Demo数量**: 285个
- **技术栈覆盖**: 12大类别
- **文档完备度**: 100%
- **代码质量**: ⭐⭐⭐⭐⭐

### 🎯 发展规划
- **短期目标**: 完善Java技术栈至100+案例
- **中期目标**: 启动AI/ML技术栈建设
- **长期愿景**: 构建完整的技术人才培养体系

---

## 🔐 安全保障

### 🛡️ 安全措施
- 环境变量管理，杜绝硬编码敏感信息
- 定期安全扫描和漏洞检测
- 密钥轮换和权限最小化原则
- CI/CD集成安全检查

### ⚠️ 使用提醒
- 本项目仅供学习和演示用途
- 生产环境使用请进行充分测试
- 遵循各技术栈的最佳实践
- 及时关注安全更新和补丁

### 🔒 安全规范
- ❌ 禁止在代码中硬编码敏感信息
- 🔁 定期更新密钥和密码
- 🛡️ 提交前务必运行安全检查
- 🔐 严格遵循最小权限原则

### 📊 Kubernetes CLI文档统计
- **基础命令文档**: 56个核心kubectl命令 ([k8s-cli.md](kubernetes/k8s-cli.md))
- **详细命令文档**: 110个kubectl及相关生态工具命令 ([k8s-cli-detail.md](kubernetes/k8s-cli-detail.md))
- **文档总行数**: 13,418行 (基础文档4,559行 + 详细文档8,859行)
- **涵盖领域**: 基础操作、集群管理、网络存储、安全监控、AI/ML平台、服务网格、GitOps等

---

<p align="center">
  <strong>🌟 喜欢这个项目？给个Star支持我们！</strong><br>
  <strong>👨‍💻 欢迎贡献代码，一起打造更好的技术学习平台！</strong>
</p>

---
*最后更新：2026年2月3日*