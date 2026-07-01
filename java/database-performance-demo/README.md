<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 数据库性能优化演示

## 🎯 学习目标

通过本案例你将掌握数据库性能优化的核心技术：

- 识别并解决N+1查询问题
- 掌握JPA批量插入和更新技术
- 理解数据库索引对查询性能的影响
- 掌握HikariCP连接池配置和优化
- 学会使用JPA投影查询和查询优化技巧
- 掌握聚合查询和分页查询优化

## 🛠️ 环境准备

### 系统要求
- Java 11+ 运行环境
- Maven 3.6+
- 无需额外安装数据库（使用内嵌H2）

### 构建项目
```bash
cd java/database-performance-demo
mvn clean compile
```

### 运行测试
```bash
mvn test
```

### 启动应用
```bash
mvn spring-boot:run
```

### H2控制台
启动后访问 http://localhost:8080/h2-console
- JDBC URL: `jdbc:h2:mem:testdb`
- 用户名: `sa`
- 密码: (空)

## 📁 项目结构

```
database-performance-demo/
├── pom.xml                                      # Maven配置文件
├── README.md                                    # 本文档
├── metadata.json                                # 元数据信息
└── src/
    ├── main/
    │   ├── java/com/example/demo/
    │   │   ├── DatabasePerformanceApplication.java  # Spring Boot主类
    │   │   ├── entity/Product.java                  # 产品实体（含索引定义）
    │   │   ├── repository/ProductRepository.java    # 数据访问层
    │   │   ├── service/ProductService.java          # 性能测试服务
    │   │   ├── config/BatchConfig.java              # JPA批量配置
    │   │   └── controller/PerformanceController.java # 性能测试API
    │   └── resources/
    │       └── application.yml                      # 应用配置
    └── test/
        └── java/com/example/demo/
            └── DatabasePerformanceApplicationTest.java # 单元测试
```

## 📚 核心知识点

### 1. N+1查询问题

**问题描述：**
查询N条记录时，执行1次主查询 + N次关联查询，共N+1次SQL。

```java
// N+1问题示例
List<Order> orders = orderRepository.findAll();  // 1次查询
for (Order order : orders) {
    order.getItems().size();  // 每次触发1次查询 → N次查询
}
// 总计: 1 + N 次SQL
```

**解决方案：**

```java
// 方案1: JOIN FETCH
@Query("SELECT o FROM Order o JOIN FETCH o.items")
List<Order> findAllWithItems();

// 方案2: EntityGraph
@EntityGraph(attributePaths = {"items"})
List<Order> findAll();

// 方案3: 投影查询（只查需要的字段）
@Query("SELECT o.id, o.total FROM Order o")
List<Object[]> findProjected();

// 方案4: 批量获取
@BatchSize(size = 100)
@OneToMany(fetch = FetchType.LAZY)
List<OrderItem> items;
```

### 2. 批量操作优化

#### 逐条插入 vs 批量插入
```java
// ❌ 逐条插入（性能差）
for (Product p : products) {
    repository.save(p);  // 每次执行1条INSERT
}

// ✅ 批量插入
repository.saveAll(products);  // 合并为批量INSERT
repository.flush();
```

#### Hibernate批量配置
```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc.batch_size: 50          # 批量大小
        order_inserts: true          # 相同INSERT排序
        order_updates: true          # 相同UPDATE排序
        batch_versioned_data: true   # 版本数据批量
```

**批量插入原理：**
```
逐条插入:
INSERT INTO products (...) VALUES (1, ...);  -- 1次网络往返
INSERT INTO products (...) VALUES (2, ...);  -- 1次网络往返
INSERT INTO products (...) VALUES (3, ...);  -- 1次网络往返
→ 3次网络往返，3次SQL解析

批量插入:
INSERT INTO products (...) VALUES (1, ...), (2, ...), (3, ...);
→ 1次网络往返，1次SQL解析
```

### 3. 索引优化

#### 本项目创建的索引
```java
@Table(name = "products", indexes = {
    @Index(name = "idx_product_name", columnList = "name"),           // 单列索引
    @Index(name = "idx_product_category", columnList = "category"),   // 单列索引
    @Index(name = "idx_product_price", columnList = "price"),         // 单列索引
    @Index(name = "idx_product_name_category", columnList = "name, category")  // 复合索引
})
```

#### 索引使用原则
```
1. WHERE条件常用列 → 建立索引
2. JOIN关联列 → 建立索引
3. ORDER BY排序列 → 考虑索引
4. 高选择性列 → 适合索引（如email, sku）
5. 低选择性列 → 不适合单独索引（如性别）
6. 复合索引遵循最左前缀原则

避免过度索引：
  - 索引占用额外存储空间
  - 降低INSERT/UPDATE/DELETE性能
  - 建议: 单表索引不超过5-6个
```

#### 索引效果对比
```sql
-- 无索引: 全表扫描 (ALL)
SELECT * FROM products WHERE category = '电子产品';
-- 扫描所有行 → O(n)

-- 有索引: 索引查找 (ref)
-- 使用idx_product_category
-- 直接定位 → O(log n)
```

### 4. 连接池配置

#### HikariCP配置参数
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10        # 最大连接数
      minimum-idle: 5              # 最小空闲连接
      idle-timeout: 30000          # 空闲超时 30s
      connection-timeout: 20000    # 获取连接超时 20s
      max-lifetime: 1800000        # 连接最大生命周期 30min
      pool-name: PerfHikariCP      # 连接池名称
```

#### 连接池大小计算公式
```
连接数 = CPU核心数 * (1 + 等待时间/计算时间)

示例:
  CPU核心数: 4
  等待时间(磁盘IO): 10ms
  计算时间: 2ms
  连接数 = 4 * (1 + 10/2) = 24

经验值:
  - Web应用: 10-20
  - 批处理应用: 5-10
  - 微服务: 5-10
```

### 5. 查询优化技巧

#### 使用投影减少数据传输
```java
// ❌ 查询所有字段
List<Product> products = repository.findByCategory("电子产品");

// ✅ 只查询需要的字段
@Query("SELECT p.id, p.name, p.price FROM Product p WHERE p.category = :category")
List<Object[]> findProjectedByCategory(@Param("category") String category);

// ✅ 使用DTO投影
public interface ProductSummary {
    Long getId();
    String getName();
    BigDecimal getPrice();
}
```

#### 使用readOnly优化读操作
```java
@Transactional(readOnly = true)
public List<Product> findProducts() {
    return repository.findAll();
}
```

#### 设置合理的fetchSize
```java
@QueryHints(@QueryHint(name = org.hibernate.jpa.QueryHints.HINT_FETCH_SIZE, value = "100"))
List<Product> findAllLargeDataset();
```

#### 使用原生SQL优化复杂查询
```java
@Query(value = "SELECT * FROM products WHERE price > :minPrice ORDER BY price DESC LIMIT :limit",
       nativeQuery = true)
List<Product> findTopByPriceNative(@Param("minPrice") BigDecimal minPrice,
                                    @Param("limit") int limit);
```

### 6. 聚合查询优化

```java
// 在数据库层聚合（推荐）
@Query("SELECT p.category, COUNT(p), AVG(p.price) FROM Product p GROUP BY p.category")
List<Object[]> getCategoryStats();

// 而不是在应用层聚合（不推荐）
List<Product> all = repository.findAll();
Map<String, Long> counts = all.stream()
    .collect(Collectors.groupingBy(Product::getCategory, Collectors.counting()));
```

## 🚀 运行指南

### 启动应用
```bash
mvn spring-boot:run
```

### API测试

#### 对比插入性能
```bash
curl "http://localhost:8080/api/perf/insert-compare?count=1000"
```

#### N+1问题演示
```bash
curl "http://localhost:8080/api/perf/n-plus-1?count=1000"
```

#### 索引 vs 全表扫描
```bash
curl "http://localhost:8080/api/perf/index-vs-scan?count=5000"
```

#### 批量更新演示
```bash
curl "http://localhost:8080/api/perf/batch-update?count=1000"
```

#### 聚合查询演示
```bash
curl "http://localhost:8080/api/perf/aggregate"
```

#### 性能优化总结
```bash
curl "http://localhost:8080/api/perf/summary"
```

## 📊 性能优化检查清单

- [ ] 识别并解决N+1查询问题
- [ ] 使用批量操作替代逐条操作
- [ ] 为常用查询条件创建索引
- [ ] 使用投影查询减少数据传输
- [ ] 配置合理的连接池参数
- [ ] 使用@Transactional(readOnly=true)
- [ ] 设置合理的fetchSize
- [ ] 在数据库层进行聚合计算
- [ ] 使用分页避免一次加载大量数据
- [ ] 开启SQL日志监控慢查询

## ⚙️ 性能优化参数参考

### JPA/Hibernate配置
| 参数 | 推荐值 | 说明 |
|------|--------|------|
| hibernate.jdbc.batch_size | 50 | 批量操作大小 |
| hibernate.jdbc.fetch_size | 100 | 查询获取大小 |
| hibernate.order_inserts | true | INSERT排序以提升批量 |
| hibernate.order_updates | true | UPDATE排序以提升批量 |
| hibernate.generate_statistics | true | 生成统计信息（开发环境） |

### HikariCP配置
| 参数 | 推荐值 | 说明 |
|------|--------|------|
| maximumPoolSize | 10-20 | 最大连接数 |
| minimumIdle | 5 | 最小空闲连接 |
| connectionTimeout | 20000ms | 获取连接超时 |
| idleTimeout | 30000ms | 空闲连接超时 |
| maxLifetime | 1800000ms | 连接最大生命周期 |

## 🔗 相关资源

- [Spring Data JPA官方文档](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [HikariCP配置指南](https://github.com/brettwooldridge/HikariCP)
- [Hibernate性能优化](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html)
- [相关Demo: spring-data-jpa-demo](../spring-data-jpa-demo/)
- [相关Demo: spring-transaction-demo](../spring-transaction-demo/)

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

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
