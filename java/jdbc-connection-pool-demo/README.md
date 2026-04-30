# JDBC连接池演示项目

## 项目简介

本项目是一个基于 Spring Boot 2.7.12 的 JDBC 连接池演示应用，使用 HikariCP 作为默认连接池，H2 作为内存数据库。项目展示了 JDBC 连接池的核心概念、配置方法和使用最佳实践。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 11 | JDK 版本 |
| Spring Boot | 2.7.12 | 应用框架 |
| HikariCP | 默认内置 | JDBC 连接池 |
| H2 | Runtime | 内存数据库 |
| Maven | - | 构建工具 |

## 什么是连接池

### 基本概念

数据库连接池（Connection Pool）是一种缓存数据库连接的技术。应用程序在启动时预先创建一定数量的数据库连接，并将这些连接保存在一个"池"中。当应用程序需要访问数据库时，不需要每次都创建新的连接，而是从池中获取一个已有的连接；使用完毕后，连接不会被销毁，而是归还到池中供后续使用。

### 为什么需要连接池

在没有连接池的情况下，每次数据库操作都需要经历以下步骤：

1. **建立 TCP 连接** - 客户端与数据库服务器之间建立网络连接
2. **TCP 三次握手** - 网络层建立可靠连接
3. **数据库认证** - 用户名密码验证
4. **会话建立** - 数据库创建会话上下文
5. **执行 SQL** - 实际的数据库操作
6. **关闭连接** - 销毁连接和会话

其中只有第5步是真正有价值的操作，其余步骤都是开销。连接池通过复用连接，消除了重复的建立和关闭连接的开销。

### 连接池的性能优势

#### 无连接池的情况

```
请求1: [创建连接(200ms)] [执行SQL(10ms)] [关闭连接(50ms)] = 260ms
请求2: [创建连接(200ms)] [执行SQL(10ms)] [关闭连接(50ms)] = 260ms
请求3: [创建连接(200ms)] [执行SQL(10ms)] [关闭连接(50ms)] = 260ms
总耗时: 780ms
```

#### 有连接池的情况

```
初始化: [创建连接1][创建连接2][创建连接3]  (启动时完成)
请求1: [获取连接(<1ms)] [执行SQL(10ms)] [归还连接(<1ms)] = ~11ms
请求2: [获取连接(<1ms)] [执行SQL(10ms)] [归还连接(<1ms)] = ~11ms
请求3: [获取连接(<1ms)] [执行SQL(10ms)] [归还连接(<1ms)] = ~11ms
总耗时: ~33ms
```

在高并发场景下，连接池的性能优势更加明显。

## HikariCP 详解

### HikariCP 简介

HikariCP（ひかり - 日语中"光"的意思）是由 Brett Wooldridge 开发的高性能 JDBC 连接池。从 Spring Boot 2.x 开始，HikariCP 成为 Spring Boot 的默认连接池实现，取代了之前的 Tomcat JDBC Pool。

### 为什么 HikariCP 最快

HikariCP 之所以性能出色，主要归功于以下优化：

1. **字节码级优化** - 使用 javassist 生成代理类的字节码，减少方法调用开销
2. **ConcurrentBag 设计** - 自定义的无锁数据结构，专为连接池设计
3. **FastList** - 替代 ArrayList 的优化列表实现，减少内存分配
4. **Proxy 优化** - 代理对象非常轻量，方法调用开销极小
5. **精简设计** - 代码量少，减少了不必要的同步和检查

### HikariCP 核心配置参数

#### maximumPoolSize（最大连接数）

最大连接数是连接池中允许存在的最大连接数量。设置过大会浪费数据库资源，设置过小会导致请求排队等待。

推荐计算公式：

```
连接数 = ((核心数 * 2) + 有效磁盘数)
```

例如一台 4 核的服务器：` connections = (4 * 2) + 1 = 9`，可以设为 10。

#### minimumIdle（最小空闲连接数）

连接池中维持的最小空闲连接数。当空闲连接数低于此值时，HikariCP 会尝试添加新连接。建议与 maximumPoolSize 相同。

#### idleTimeout（空闲超时时间）

空闲连接在池中的最大存活时间（毫秒）。超过此时间的空闲连接将被移除。仅在 minimumIdle < maximumPoolSize 时生效。

默认值：600000（10分钟）

#### connectionTimeout（连接超时时间）

客户端等待连接的最大毫秒数。超过此时间将抛出 SQLException。

默认值：30000（30秒）

#### maxLifetime（连接最大生命周期）

连接在池中的最大存活时间（毫秒）。到期的连接将被优雅关闭。建议设置为比数据库的 wait_timeout 小30秒到1分钟。

默认值：1800000（30分钟）

#### connectionTestQuery（连接测试查询）

在向调用者返回连接之前执行的简单 SQL，用于验证连接是否仍然有效。如果数据库支持 Connection.isValid()，则不需要设置此参数。

#### leakDetectionThreshold（泄漏检测阈值）

连接被借出后超过此时间（毫秒）仍未归还，将记录一条警告日志，表示可能存在连接泄漏。

默认值：0（不检测）

## 项目结构

```
jdbc-connection-pool-demo/
├── pom.xml                                    # Maven 项目配置
├── README.md                                  # 项目说明文档
├── metadata.json                              # 项目元数据
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── JdbcPoolDemoApplication.java   # 应用启动类
    │   │   ├── config/
    │   │   │   └── DataSourceConfig.java      # 数据源配置（HikariCP）
    │   │   ├── entity/
    │   │   │   └── Product.java               # 商品实体类
    │   │   ├── repository/
    │   │   │   └── ProductRepository.java     # 数据访问层（JdbcTemplate）
    │   │   ├── service/
    │   │   │   └── ProductService.java        # 业务逻辑层
    │   │   └── controller/
    │   │       └── ProductController.java     # REST API 控制器
    │   └── resources/
    │       ├── application.yml                # 应用配置
    │       ├── schema.sql                     # 数据库表结构
    │       └── data.sql                       # 初始数据
    └── test/
        └── java/com/example/demo/
            ├── JdbcPoolDemoApplicationTest.java  # 启动测试
            └── repository/
                └── ProductRepositoryTest.java    # Repository 测试
```

## JdbcTemplate CRUD 操作详解

### 什么是 JdbcTemplate

JdbcTemplate 是 Spring JDBC 模块的核心类，它简化了 JDBC 的使用。它处理了资源的创建和释放，避免了常见错误，并提供了简洁的 API 来执行 SQL 操作。

### JdbcTemplate 的优势

1. **自动资源管理** - 自动关闭 Connection、Statement、ResultSet
2. **异常转换** - 将 checked SQLException 转换为 Spring 的 DataAccessException 层次结构
3. **事务管理** - 与 Spring 事务管理器无缝集成
4. **简洁 API** - 提供了 query、update、batchUpdate 等简洁方法

### 本项目中的 CRUD 示例

#### Create（创建）

```java
KeyHolder keyHolder = new GeneratedKeyHolder();
jdbcTemplate.update(connection -> {
    PreparedStatement ps = connection.prepareStatement(
        "INSERT INTO product (name, price, stock, category) VALUES (?, ?, ?, ?)",
        Statement.RETURN_GENERATED_KEYS
    );
    ps.setString(1, product.getName());
    ps.setDouble(2, product.getPrice());
    ps.setInt(3, product.getStock());
    ps.setString(4, product.getCategory());
    return ps;
}, keyHolder);
```

使用 KeyHolder 获取自增主键值。

#### Read（读取）

```java
// 查询列表
List<Product> products = jdbcTemplate.query("SELECT * FROM product", rowMapper);

// 查询单条
Product product = jdbcTemplate.queryForObject("SELECT * FROM product WHERE id = ?", rowMapper, id);

// 查询计数
Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM product", Integer.class);
```

#### Update（更新）

```java
int rows = jdbcTemplate.update(
    "UPDATE product SET name = ?, price = ?, stock = ?, category = ? WHERE id = ?",
    product.getName(), product.getPrice(), product.getStock(), product.getCategory(), product.getId()
);
```

#### Delete（删除）

```java
int rows = jdbcTemplate.update("DELETE FROM product WHERE id = ?", id);
```

## 连接池监控

### HikariCP 内置监控指标

HikariCP 提供了 JMX 和 Micrometer 两种监控方式：

#### 通过 JMX 监控

在 application.yml 中启用 JMX：

```yaml
spring:
  datasource:
    hikari:
      register-mbeans: true
```

可以使用 JConsole 或 VisualVM 连接到 JVM，查看 HikariCP 的 MBean 信息：

- **TotalConnections** - 总连接数
- **ActiveConnections** - 活跃连接数
- **IdleConnections** - 空闲连接数
- **ThreadsAwaitingConnection** - 等待连接的线程数

#### 通过 Actuator 监控

添加 Spring Boot Actuator 依赖后，可以通过 `/actuator` 端点查看数据源健康状态：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

#### 通过日志监控

设置 HikariCP 日志级别为 DEBUG 可以查看连接池的详细操作：

```yaml
logging:
  level:
    com.zaxxer.hikari: DEBUG
```

### 连接泄漏检测

当设置了 `leakDetectionThreshold` 后，如果连接被借出超过指定时间未归还，HikariCP 会记录包含完整堆栈跟踪的警告日志，帮助定位连接泄漏问题。

## 连接池性能对比

### 主流连接池对比

| 特性 | HikariCP | Druid | Tomcat JDBC | DBCP2 |
|------|----------|-------|-------------|-------|
| 性能 | ★★★★★ | ★★★★ | ★★★ | ★★★ |
| 监控 | 一般 | 优秀 | 一般 | 一般 |
| 稳定性 | 优秀 | 优秀 | 良好 | 良好 |
| 配置复杂度 | 简单 | 中等 | 简单 | 简单 |
| Spring Boot 默认 | 是 | 否 | 否 | 否 |

### HikariCP vs Druid

- **HikariCP**：性能最优，代码精简，Spring Boot 默认选项
- **Druid**：阿里巴巴开源，监控功能强大，SQL 解析和防火墙功能

在高性能场景推荐 HikariCP，需要强大监控功能时推荐 Druid。

## 最佳实践

### 连接数配置建议

1. **不要设置过大的连接池** - 数据库连接是昂贵资源，通常 10-20 个连接就能满足大多数应用
2. **考虑数据库服务器配置** - 数据库最大连接数（max_connections）应大于所有应用连接池的最大连接数之和
3. **不同环境使用不同配置** - 开发环境可以用较小的连接池，生产环境需要根据负载调整

### 连接泄漏预防

1. **设置 leakDetectionThreshold** - 推荐设置为 30000-60000（30-60秒）
2. **确保连接正确关闭** - 使用 try-with-resources 或 Spring 事务管理
3. **避免在循环中获取连接** - 批量操作应该复用连接

### 超时配置

1. **connectionTimeout** - 设置合理的等待超时，避免请求无限等待
2. **idleTimeout** - 定期清理长时间空闲的连接
3. **maxLifetime** - 设置比数据库 wait_timeout 小的值，避免数据库主动断开连接

## 快速开始

### 环境要求

- JDK 11+
- Maven 3.6+

### 运行步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd jdbc-connection-pool-demo
```

2. **编译项目**

```bash
mvn clean compile
```

3. **运行测试**

```bash
mvn test
```

4. **启动应用**

```bash
mvn spring-boot:run
```

5. **访问 H2 控制台**

打开浏览器访问 `http://localhost:8080/h2-console`，使用以下信息连接：
- JDBC URL: `jdbc:h2:mem:demo_db`
- 用户名: `sa`
- 密码: （空）

### API 测试示例

```bash
# 获取所有商品
curl http://localhost:8080/api/products

# 创建商品
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"测试商品","price":99.99,"stock":100,"category":"测试"}'

# 获取指定商品
curl http://localhost:8080/api/products/1

# 按分类查询
curl http://localhost:8080/api/products/category/电子产品

# 更新商品
curl -X PUT http://localhost:8080/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"更新商品","price":199.99,"stock":50,"category":"更新分类"}'

# 删除商品
curl -X DELETE http://localhost:8080/api/products/1
```

## 常见问题

### 1. 连接池耗尽

**现象**：应用抛出 `SQLTransientConnectionException: DemoHikariPool - Connection is not available, request timed out after 20000ms`

**原因**：连接被借出后未归还，或者并发量过大超过连接池容量。

**解决方案**：
- 检查是否有连接泄漏（开启 leakDetectionThreshold）
- 适当增大 maximumPoolSize
- 优化慢查询减少连接占用时间

### 2. 连接超时

**现象**：连接创建失败，提示连接超时。

**原因**：数据库服务器不可达或者数据库连接数已满。

**解决方案**：
- 检查数据库服务器状态
- 检查网络连接
- 确认数据库最大连接数配置

### 3. 性能不佳

**现象**：数据库操作延迟高。

**原因**：连接池配置不合理或存在慢查询。

**解决方案**：
- 调整连接池参数
- 检查 SQL 执行计划
- 添加适当的数据库索引

## 学习资源

- [HikariCP 官方文档](https://github.com/brettwooldridge/HikariCP)
- [Spring JDBC 文档](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#jdbc)
- [Spring Boot 数据源配置](https://docs.spring.io/spring-boot/docs/current/reference/html/data.html#data.sql.datasource)
