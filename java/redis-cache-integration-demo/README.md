# Redis Cache Integration Demo

Redis缓存集成示例项目，演示Spring Boot与Redis的集成以及Spring Cache注解的使用。

## 技术栈

- Spring Boot 2.7
- Spring Data Redis
- Spring Cache
- Lettuce连接池

## 项目结构

```
redis-cache-integration-demo/
├── src/main/java/com/example/demo/
│   ├── CacheDemoApplication.java          # 应用入口
│   ├── config/
│   │   └── RedisConfig.java               # Redis配置类
│   ├── controller/
│   │   └── ProductController.java         # 商品控制器
│   ├── entity/
│   │   └── Product.java                   # 商品实体
│   └── service/
│       └── ProductService.java            # 商品服务（带缓存）
├── src/main/resources/
│   └── application.yml                    # 应用配置
├── pom.xml
└── README.md
```

## 核心注解说明

### @EnableCaching
在配置类上启用缓存功能。

```java
@Configuration
@EnableCaching
public class RedisConfig { ... }
```

### @Cacheable
在方法上标注，表示该方法的返回值应该被缓存。

```java
@Cacheable(value = "products", key = "#id")
public Product getProduct(Long id) { ... }
```

- 先查询缓存，缓存存在则直接返回
- 缓存不存在则执行方法，并将结果存入缓存

### @CachePut
在方法上标注，表示执行方法并更新缓存。

```java
@CachePut(value = "products", key = "#product.id")
public Product updateProduct(Product product) { ... }
```

- 始终执行方法
- 将方法返回值更新到缓存

### @CacheEvict
在方法上标注，表示清除缓存。

```java
@CacheEvict(value = "products", key = "#id")
public void deleteProduct(Long id) { ... }

@CacheEvict(value = "products", allEntries = true)
public void clearCache() { ... }
```

- 按key清除单个缓存
- `allEntries = true`清除整个缓存空间

## 配置说明

### application.yml

```yaml
spring:
  cache:
    type: redis          # 指定缓存类型为Redis
  redis:
    host: localhost      # Redis服务器地址
    port: 6379          # Redis端口
```

### RedisCacheManager配置

```java
@Bean
public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
    RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))  // 默认TTL 10分钟
            .serializeValuesWith(
                RedisSerializationContext.SerializationPair
                    .fromSerializer(new GenericJackson2JsonRedisSerializer()));
    
    return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
}
```

## 快速开始

### 1. 启动Redis

```bash
# 使用Docker启动Redis
docker run -d --name redis -p 6379:6379 redis:latest

# 或使用本地Redis
redis-server
```

### 2. 运行应用

```bash
# 编译运行
mvn spring-boot:run
```

### 3. 测试接口

```bash
# 首次查询（会查询数据库）
curl http://localhost:8080/products/1

# 再次查询（从缓存返回，无数据库查询）
curl http://localhost:8080/products/1

# 更新商品（更新缓存）
curl -X PUT "http://localhost:8080/products/1?name=iPhone15&price=6999"

# 删除商品（清除缓存）
curl -X DELETE http://localhost:8080/products/1
```

## 缓存效果验证

查看控制台输出验证缓存效果：

```
# 首次查询
[查询数据库] 查询商品ID: 1

# 第二次查询（无输出，直接返回缓存）

# 更新后查询
[更新数据库] 更新商品: 1
[查询数据库] 查询商品ID: 1  # 缓存已更新，再次查询走缓存
```

使用Redis CLI查看缓存：

```bash
redis-cli
KEYS products::*              # 查看所有商品缓存
GET "products::1"             # 查看具体缓存值
TTL "products::1"             # 查看缓存剩余时间
```

## 生产环境建议

1. **配置连接池**
```yaml
spring:
  redis:
    lettuce:
      pool:
        max-active: 8
        max-idle: 8
        min-idle: 0
```

2. **设置合理的TTL**
- 根据业务数据变化频率设置
- 热点数据设置较长TTL
- 实时性要求高的数据设置较短TTL

3. **使用Cache Namespaces**
```java
@Cacheable(value = "app:products", key = "#id")
```

4. **监控缓存命中率**
```java
@Autowired
private CacheManager cacheManager;

public void printCacheStats() {
    Cache cache = cacheManager.getCache("products");
    // 查看缓存统计
}
```

## 学习要点

1. Spring Cache抽象设计原理
2. Redis序列化方式选择
3. 缓存穿透、雪崩、击穿的防护
4. 缓存与数据库一致性问题
5. 分布式环境下的缓存策略
