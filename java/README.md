<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# ☕ Java技术栈完整指南

> Java编程语言从基础到企业级开发的完整学习体系，包含100+个案例：Spring生态、设计模式、DDD、TDD、JVM调优、微服务、DevOps全链路

## 🚀 快速入门

想要快速上手Java开发？查看我们的 [Java CLI 命令行速查表](./cli/java-cli.md) 获取JDK工具、构建工具和调试命令！

## 📋 技术栈概述

Java是一种面向对象的编程语言，以其"一次编写，到处运行"的特性而著称。本技术栈提供从基础语法到企业级架构的完整学习路径。

### 🔧 核心技能覆盖

- **基础语法**: 变量、数据类型、控制流、面向对象编程、泛型、异常处理、反射、注解、Lambda
- **企业级开发**: Spring框架、微服务架构、数据持久化、消息队列、分布式事务
- **DevOps工具**: Maven/Gradle构建、单元测试、CI/CD、容器化部署、K8s编排
- **高级架构**: 设计模式(GoF)、性能优化、安全防护、JVM调优、分布式系统

### 🎯 适用人群

- Java初学者
- 企业级应用开发者
- 微服务架构师
- 后端开发工程师
- 系统架构师
- DevOps工程师

---

## 📚 学习路径

### 基础语法系列 (20个案例)
从最基本的变量类型到高级的Lambda表达式，循序渐进掌握Java核心概念。

### 企业级开发系列 (30个案例)
深入学习Spring生态系统，掌握企业级应用开发的核心技术。

### DevOps工具系列 (10个案例)
掌握现代化Java项目的构建、测试和部署工具链。

### 高级架构系列 (17个案例)
学习设计模式、性能优化和安全防护等高级主题。

### Spring Boot补充特性 (17个案例)
Spring Boot常用开发特性与实践技巧。

---

## 🚀 快速开始

```bash
# 查看所有Java案例
opendemo search java

# 获取基础语法案例
opendemo get java variables-types

# 获取Spring Boot案例
opendemo get java spring-boot-basics

# 验证Java环境
java -version
javac -version
```

---

## 📊 案例统计

| 分类 | 案例数量 | 状态 |
|------|----------|------|
| 基础语法 | 20 | ✅ 完成 |
| 企业级开发 | 30 | ✅ 完成 |
| DevOps工具 | 10 | ✅ 完成 |
| 高级架构 | 17 | ✅ 完成 |
| Spring Boot补充 | 17 | ✅ 完成 |
| **总计** | **94** | ✅ 完成 |

---

## 📚 详细目录

### 基础语法 (20个)
<details>
<summary>点击查看完整列表</summary>

1. ✅ `java-variables-types-demo` - 变量与数据类型
2. ✅ `java-control-flow-demo` - 控制流程语句
3. ✅ `java-arrays-collections-demo` - 数组与集合
4. ✅ `java-string-operations-demo` - 字符串操作
5. ✅ `java-exception-handling-demo` - 异常处理机制
6. ✅ `java-input-output-demo` - 输入输出操作
7. ✅ `java-date-time-demo` - 日期时间处理
8. ✅ `java-regular-expressions-demo` - 正则表达式应用
9. ✅ `java-classes-objects-demo` - 类与对象基础
10. ✅ `java-inheritance-demo` - 继承机制
11. ✅ `java-polymorphism-demo` - 多态特性
12. ✅ `java-encapsulation-demo` - 封装原则
13. ✅ `java-abstraction-demo` - 抽象概念
14. ✅ `java-interfaces-demo` - 接口设计
15. ✅ `java-inner-classes-demo` - 内部类应用
16. ✅ `java-generics-demo` - 泛型编程
17. ✅ `java-annotations-demo` - 注解机制
18. ✅ `java-reflection-demo` - 反射API
19. ✅ `java-enumerations-demo` - 枚举类型
20. ✅ `java-lambda-demo` - Lambda表达式

</details>

### 企业级开发 (30个)
<details>
<summary>点击查看完整列表</summary>

**Spring Core / Boot 框架 (10个)**
1. ✅ `spring-core-ioc-demo` - IoC容器基础
2. ✅ `spring-bean-lifecycle-demo` - Bean生命周期
3. ✅ `spring-aop-demo` - 面向切面编程
4. ✅ `spring-data-jpa-demo` - JPA数据访问
5. ✅ `spring-transaction-demo` - 事务管理
6. ✅ `spring-security-basics-demo` - 安全框架基础
7. ✅ `spring-security-jwt-demo` - JWT令牌安全
8. ✅ `spring-mvc-web-demo` - MVC Web开发
9. ✅ `spring-boot-autoconfig-demo` - 自动配置原理
10. ✅ `actuator-demo` - 应用监控

**数据持久化 (4个)**
11. ✅ `jdbc-connection-pool-demo` - JDBC连接池
12. ✅ `mybatis-crud-demo` - MyBatis CRUD
13. ✅ `hibernate-entity-mapping-demo` - Hibernate实体映射
14. ✅ `database-migration-flyway-demo` - 数据库迁移Flyway

**中间件集成 (5个)**
15. ✅ `mongodb-integration-demo` - MongoDB集成
16. ✅ `redis-cache-integration-demo` - Redis缓存应用
17. ✅ `elasticsearch-integration-demo` - Elasticsearch搜索
18. ✅ `rabbitmq-producer-consumer-demo` - RabbitMQ消息
19. ✅ `apache-kafka-demo` - Kafka消息处理

**Spring Cloud / 微服务 (8个)**
20. ✅ `spring-cloud-eureka-demo` - 服务注册发现
21. ✅ `spring-cloud-gateway-demo` - API网关路由
22. ✅ `spring-cloud-gateway-advanced-demo` - API网关高级特性
23. ✅ `spring-cloud-feign-demo` - 声明式客户端
24. ✅ `spring-cloud-hystrix-demo` - 熔断降级
25. ✅ `spring-cloud-config-demo` - 分布式配置中心
26. ✅ `spring-cloud-sleuth-demo` - 分布式链路追踪
27. ✅ `spring-cloud-alibaba-nacos-demo` - Nacos配置中心
28. ✅ `spring-cloud-alibaba-sentinel-demo` - Sentinel限流
29. ✅ `distributed-transaction-seata-demo` - Seata分布式事务
30. ✅ `activemq-jms-demo` - JMS消息服务

</details>

### DevOps工具 (10个)
<details>
<summary>点击查看完整列表</summary>

1. ✅ `maven-project-structure-demo` - Maven项目结构
2. ✅ `gradle-build-script-demo` - Gradle构建脚本
3. ✅ `multi-module-project-demo` - 多模块项目
4. ✅ `junit5-testing-demo` - JUnit 5单元测试
5. ✅ `mockito-mocking-demo` - Mockito模拟测试
6. ✅ `docker-integration-demo` - Docker容器化
7. ✅ `jenkins-pipeline-demo` - Jenkins流水线
8. ✅ `kubernetes-java-deployment-demo` - K8s部署实践

</details>

### 高级架构 (17个)
<details>
<summary>点击查看完整列表</summary>

**GoF设计模式 (6个)**
1. ✅ `singleton-pattern-demo` - 单例模式
2. ✅ `factory-pattern-demo` - 工厂模式
3. ✅ `observer-pattern-demo` - 观察者模式
4. ✅ `strategy-pattern-demo` - 策略模式
5. ✅ `decorator-pattern-demo` - 装饰器模式
6. ✅ `template-method-pattern-demo` - 模板方法模式

**性能优化 (5个)**
7. ✅ `jvm-memory-management-demo` - JVM内存管理
8. ✅ `garbage-collection-tuning-demo` - 垃圾回收调优
9. ✅ `database-performance-demo` - 数据库性能优化
10. ✅ `concurrent-programming-demo` - 并发编程实践
11. ✅ `application-profiling-demo` - 应用性能分析

**安全防护 (3个)**
12. ✅ `spring-security-oauth2-demo` - OAuth2认证授权
13. ✅ `csrf-protection-demo` - CSRF防护机制
14. ✅ `sql-injection-prevention-demo` - SQL注入防范

**诊断与调优 (3个)**
15. ✅ `java-diagnostic-tools-demo` - Java诊断工具与Arthas实战
16. ✅ `java-jvm-troubleshooting-trinity` - JVM性能分析三剑客实战
17. ✅ `java-jvm-internals` - JVM内部原理

</details>

### Spring Boot 补充特性 (17个)
<details>
<summary>点击查看完整列表</summary>

1. ✅ `async-demo` - 异步编程
2. ✅ `swagger-openapi-demo` - Swagger API文档
3. ✅ `validation-demo` - 数据验证
4. ✅ `bean-validation-demo` - Bean Validation
5. ✅ `websocket-realtime-demo` - WebSocket实时通信
6. ✅ `exception-handling-demo` - 全局异常处理
7. ✅ `filter-interceptor-demo` - 过滤器与拦截器
8. ✅ `schedule-task-demo` - 定时任务
9. ✅ `profiles-demo` - 多环境配置
10. ✅ `logback-demo` - 日志框架
11. ✅ `file-upload-demo` - 文件上传
12. ✅ `rest-template-demo` - REST调用
13. ✅ `cors-demo` - 跨域配置
14. ✅ `cache-concurrent-map-demo` - 本地缓存
15. ✅ `conditional-demo` - 条件装配
16. ✅ `event-listener-demo` - 事件机制
17. ✅ `environment-demo` - Environment抽象
18. ✅ `value-annotation-demo` - @Value注解
19. ✅ `spel-demo` - SpEL表达式
20. ✅ `aop-logging-demo` - AOP日志
21. ✅ `application-runner-demo` - ApplicationRunner
22. ✅ `command-line-runner-demo` - CommandLineRunner

</details>

---

## 🛠️ 开发环境配置

```bash
# 安装JDK
# 推荐版本: OpenJDK 11+ 或 Oracle JDK 11+

# 验证安装
java -version
javac -version

# 安装构建工具
# Maven
mvn -version

# Gradle  
gradle -version

# 安装常用IDE
# IntelliJ IDEA Community Edition (推荐)
# Eclipse IDE for Java Developers
# VS Code with Java extensions
```

---

## 📖 学习建议

1. **循序渐进**: 按照基础语法 → 企业级开发 → 高级架构的顺序学习
2. **动手实践**: 每个案例都要亲自运行和修改代码
3. **项目驱动**: 结合实际项目应用所学知识
4. **持续练习**: 定期回顾和练习重点概念

---

## 🤝 贡献指南

欢迎提交新的Java案例或改进现有案例：
- 遵循统一的目录结构和文档格式（参见 [JAVA-CASE-TEMPLATE.md](./JAVA-CASE-TEMPLATE.md)）
- 遵循命名规范（参见 [NAMING_CONVENTIONS.md](./NAMING_CONVENTIONS.md)）
- 提供完整的代码示例和详细说明
- 确保案例的可运行性和实用性
- 遵循Java编码规范和最佳实践

---

> **💡 提示**: Java是企业级应用开发的主流语言，掌握好Spring生态系统和微服务架构对职业发展非常重要。

## 🔗 相关技术栈交叉引用

### 与Python的关联
- [Python基础语法案例](../python/README.md) - 对应的基础编程概念
- [Python面向对象](../python/oop-classes/) - 类似概念的Python实现

### 与Go的关联
- [Go基础语法](../go/README.md) - 简洁语法对比
- [Go并发编程](../go/go-goroutines-demo/) - 不同的并发模型

### 与Node.js的关联
- [Node.js异步编程](../nodejs/nodejs-promises-demo/) - JavaScript异步处理
- [Node.js类与继承](../nodejs/nodejs-class-inheritance-demo/) - 原型继承vs类继承

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
