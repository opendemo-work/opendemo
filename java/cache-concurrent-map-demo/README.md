<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# ConcurrentMap 缓存演示

> 使用 ConcurrentHashMap 实现本地缓存，支持 TTL 过期、缓存淘汰和缓存统计

## 🎯 学习目标

- ✅ 理解基于 ConcurrentMap 的本地缓存实现原理
- ✅ 掌握 TTL（Time To Live）缓存过期策略
- ✅ 学会缓存命中/未命中的判断和处理
- ✅ 了解 Spring Cache 抽象与手动缓存的区别

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **ConcurrentHashMap** | 线程安全的 HashMap，适合做缓存容器 |
| **TTL** | Time To Live，缓存存活时间 |
| **Eviction** | 缓存淘汰策略，如 LRU、LFU、定时淘汰 |
| **Cache Hit** | 缓存命中，数据在缓存中找到 |
| **Cache Miss** | 缓存未命中，需要从数据源加载 |

---

## 🛠️ 缓存架构

```
┌────────────────────────────────────────────────────┐
│                   请求流程                          │
├────────────────────────────────────────────────────┤
│                                                    │
│  请求 ──→ 查询缓存 ──→ 命中？ ──→ 是 ──→ 返回缓存  │
│                │                                   │
│                └──→ 否 ──→ 查询数据库               │
│                          │                         │
│                          ├──→ 写入缓存              │
│                          └──→ 返回结果              │
│                                                    │
│  定时任务 ──→ 扫描过期缓存 ──→ 淘汰                  │
└────────────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. 缓存管理器 SimpleCacheManager

```java
@Component
public class SimpleCacheManager {

    private final Map<String, CacheEntry> cache = new ConcurrentHashMap<>();

    public void put(String key, Object value, long ttlMillis) {
        CacheEntry entry = new CacheEntry(value, System.currentTimeMillis() + ttlMillis);
        cache.put(key, entry);
    }

    public <T> T get(String key) {
        CacheEntry entry = cache.get(key);
        if (entry == null || entry.isExpired()) {
            cache.remove(key);
            return null;
        }
        return (T) entry.getValue();
    }
}
```

### 2. 缓存服务 CacheService

```java
@Service
public class CacheService {

    public String getProduct(String productId) {
        String cached = cacheManager.get(productId);
        if (cached != null) {
            return "[缓存] " + cached;
        }
        String product = loadFromDb(productId);
        cacheManager.put(productId, product, 60000);
        return "[数据库] " + product;
    }
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/cache-concurrent-map-demo
mvn spring-boot:run
```

### 2. 测试缓存

```bash
# 第一次查询 - 缓存未命中
curl http://localhost:8080/api/cache/product/P001

# 第二次查询 - 缓存命中
curl http://localhost:8080/api/cache/product/P001

# 查看缓存统计
curl http://localhost:8080/api/cache/stats

# 刷新单个缓存
curl -X DELETE http://localhost:8080/api/cache/product/P001

# 清空所有缓存
curl -X DELETE http://localhost:8080/api/cache/clear
```

---

## 📁 项目结构

```
cache-concurrent-map-demo/
├── src/main/java/com/example/demo/
│   ├── CacheApplication.java              # 应用入口
│   ├── cache/
│   │   └── SimpleCacheManager.java        # 缓存管理器（TTL、淘汰）
│   ├── service/
│   │   └── CacheService.java              # 缓存服务
│   └── controller/
│       └── CacheController.java           # REST 接口
├── src/test/java/com/example/demo/
│   └── CacheConcurrentMapDemoTest.java    # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | /api/cache/product/{id} | 查询商品（自动缓存） |
| DELETE | /api/cache/product/{id} | 刷新指定商品缓存 |
| GET | /api/cache/stats | 获取缓存统计 |
| DELETE | /api/cache/clear | 清空所有缓存 |

---

## 🔧 ConcurrentMap 缓存 vs Spring Cache

| 特性 | ConcurrentMap 手动缓存 | Spring @Cacheable |
|------|----------------------|-------------------|
| 实现复杂度 | 较高，需手动管理 | 低，注解驱动 |
| TTL 支持 | 需自行实现 | 需配置缓存提供者 |
| 灵活性 | 高 | 中等 |
| 适用场景 | 简单本地缓存 | 企业级缓存方案 |
| 分布式 | 不支持 | 需 Redis 等中间件 |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Redis Cache Integration](../redis-cache-integration-demo/) - Redis 分布式缓存
- [Spring Cache @Cacheable](https://docs.spring.io/spring-framework/docs/current/reference/html/integration.html#cache)

---

*最后更新：2026年4月*

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
