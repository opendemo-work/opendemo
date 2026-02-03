# 📚 数据库索引设计原则指南

> 企业级数据库索引优化策略，涵盖索引类型选择、设计原则、性能分析等完整索引优化体系，显著提升查询性能，降低系统资源消耗

## 📋 案例概述

本案例深入讲解数据库索引的设计原理和优化策略，通过科学的索引设计方法和性能分析工具，帮助开发者和DBA构建高效的索引体系，最大化数据库查询性能。

### 🎯 学习目标

- 掌握各种索引类型的特性和适用场景
- 理解索引设计的核心原则和最佳实践
- 学会使用执行计划分析索引效果
- 实施索引监控和维护策略
- 避免常见的索引设计陷阱

### ⏱️ 学习时长

- **理论学习**: 3小时
- **实践操作**: 4小时
- **总计**: 7小时

---

## 📚 索引基础知识

### 索引类型概览

```
┌─────────────────────────────────────────────────┐
│              主要索引类型                       │
├─────────────────────────────────────────────────┤
│ B-Tree索引     │ 最常用，支持范围查询           │
│ 哈希索引       │ 等值查询快，不支持范围         │
│ 全文索引       │ 文本搜索优化                   │
│ 空间索引       │ 地理位置数据查询               │
│ 位图索引       │ 低基数列优化                   │
│ 聚簇索引       │ 数据物理存储顺序               │
│ 覆盖索引       │ 包含查询所需全部列             │
└─────────────────────────────────────────────────┘
```

### 索引选择决策树

```
开始索引设计
      ↓
是否是主键？
  ├── 是 → 创建聚簇索引(PRIMARY KEY)
  └── 否 → 是否频繁等值查询？
        ├── 是 → 考虑哈希索引或B-Tree
        └── 否 → 是否范围查询？
              ├── 是 → B-Tree索引
              └── 否 → 是否文本搜索？
                    ├── 是 → 全文索引
                    └── 否 → 是否地理位置？
                          ├── 是 → 空间索引
                          └── 否 → 位图索引(低基数)
```

---

## 🐬 MySQL索引设计实践

### 1. B-Tree索引优化

#### 索引创建策略
```sql
-- 单列索引
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_order_date ON orders(created_at);

-- 复合索引（最左前缀原则）
CREATE INDEX idx_user_status_date ON users(status, created_at);
CREATE INDEX idx_product_category_price ON products(category_id, price);

-- 前缀索引（适用于长文本）
CREATE INDEX idx_product_name_prefix ON products(name(20));

-- 唯一索引
CREATE UNIQUE INDEX idx_user_username ON users(username);
CREATE UNIQUE INDEX idx_email_token ON password_resets(token);

-- 降序索引（MySQL 8.0+）
CREATE INDEX idx_order_desc ON orders(created_at DESC);
```

#### 索引效果分析
```sql
-- 查看索引使用情况
SHOW INDEX FROM users;
ANALYZE TABLE users;

-- 执行计划分析
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
EXPLAIN SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-01-31';

-- 索引统计信息
SELECT 
    table_name,
    index_name,
    seq_in_index,
    column_name,
    cardinality
FROM information_schema.statistics 
WHERE table_schema = 'myapp' 
AND table_name = 'users';
```

#### 索引优化示例
```sql
-- 优化前：无索引查询
EXPLAIN SELECT u.username, o.total_amount 
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE u.status = 'active' 
AND o.created_at >= '2024-01-01';

-- 优化后：合理索引设计
CREATE INDEX idx_users_status_id ON users(status, id);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);

-- 验证优化效果
EXPLAIN SELECT u.username, o.total_amount 
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE u.status = 'active' 
AND o.created_at >= '2024-01-01';
```

### 2. 全文索引应用

#### 全文索引创建和使用
```sql
-- 创建全文索引
CREATE FULLTEXT INDEX idx_articles_content ON articles(title, content);

-- 自然语言模式搜索
SELECT *, MATCH(title, content) AGAINST('数据库优化') AS relevance_score
FROM articles 
WHERE MATCH(title, content) AGAINST('数据库优化' IN NATURAL LANGUAGE MODE)
ORDER BY relevance_score DESC;

-- 布尔模式搜索
SELECT * FROM articles 
WHERE MATCH(title, content) AGAINST('+MySQL -Oracle' IN BOOLEAN MODE);

-- 查询扩展模式
SELECT * FROM articles 
WHERE MATCH(title, content) AGAINST('性能优化' WITH QUERY EXPANSION);
```

#### 全文索引配置优化
```sql
-- 系统变量调整
SET GLOBAL innodb_ft_min_token_size = 2;  -- 最小词长度
SET GLOBAL innodb_ft_max_token_size = 84;  -- 最大词长度
SET GLOBAL innodb_ft_enable_stopword = ON; -- 启用停用词

-- 自定义停用词
CREATE TABLE custom_stopwords (value VARCHAR(30)) ENGINE=INNODB;
INSERT INTO custom_stopwords VALUES ('的'), ('是'), ('在');

-- 重建全文索引
ALTER TABLE articles DROP INDEX idx_articles_content;
ALTER TABLE articles ADD FULLTEXT INDEX idx_articles_content (title, content);
```

### 3. 索引维护和监控

#### 索引碎片整理
```sql
-- 检查索引碎片
SELECT 
    table_name,
    index_name,
    ROUND(stat_value * @@innodb_page_size / 1024 / 1024, 2) AS size_mb
FROM mysql.innodb_index_stats 
WHERE stat_name = 'size' 
AND database_name = 'myapp';

-- 优化表和索引
OPTIMIZE TABLE users;
ANALYZE TABLE orders;

-- 在线重建索引（MySQL 8.0+）
ALTER TABLE users ALGORITHM=INPLACE, LOCK=NONE 
ADD INDEX idx_new_index (email);
```

#### 索引使用监控
```sql
-- 启用性能模式监控
UPDATE performance_schema.setup_instruments 
SET ENABLED = 'YES' 
WHERE NAME LIKE 'statement/sql/select';

UPDATE performance_schema.setup_consumers 
SET ENABLED = 'YES' 
WHERE NAME LIKE '%statements%';

-- 查询索引使用统计
SELECT 
    object_schema,
    object_name,
    index_name,
    count_read,
    count_write,
    sum_timer_wait
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE object_schema = 'myapp'
ORDER BY sum_timer_wait DESC;
```

---

## 🐘 PostgreSQL索引设计实践

### 1. 高级索引类型

#### 部分索引
```sql
-- 只对活跃用户创建索引
CREATE INDEX idx_active_users_email 
ON users(email) 
WHERE status = 'active';

-- 只对近期订单创建索引
CREATE INDEX idx_recent_orders_user 
ON orders(user_id) 
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';

-- 表达式索引
CREATE INDEX idx_users_lower_email 
ON users(LOWER(email));

CREATE INDEX idx_orders_year_month 
ON orders(EXTRACT(YEAR FROM created_at), EXTRACT(MONTH FROM created_at));
```

#### 多列索引和排序
```sql
-- 复合索引（注意列顺序）
CREATE INDEX idx_orders_user_date_amount 
ON orders(user_id, created_at DESC, total_amount DESC);

-- 包含列索引（覆盖索引）
CREATE INDEX idx_orders_covering 
ON orders(user_id) 
INCLUDE (created_at, total_amount, status);

-- 唯一约束索引
CREATE UNIQUE INDEX idx_unique_username 
ON users(LOWER(username));
```

### 2. 特殊索引类型

#### GiST索引（地理空间）
```sql
-- 创建地理空间索引
CREATE INDEX idx_locations_geom 
ON locations 
USING GIST(geom);

-- 空间查询
SELECT name, ST_Distance(geom, ST_Point(116.4074, 39.9042)) as distance
FROM locations 
WHERE ST_DWithin(geom, ST_Point(116.4074, 39.9042), 10000)  -- 10公里内
ORDER BY distance;
```

#### GIN索引（数组和JSON）
```sql
-- 数组索引
CREATE INDEX idx_user_tags_gin 
ON users 
USING GIN(tags);

-- JSONB索引
CREATE INDEX idx_product_specs_gin 
ON products 
USING GIN(specifications jsonb_path_ops);

-- 查询示例
SELECT * FROM users WHERE tags @> ARRAY['premium'];
SELECT * FROM products WHERE specifications @> '{"color": "red"}';
```

### 3. 索引性能分析

#### 执行计划详解
```sql
-- 详细执行计划
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT u.username, COUNT(o.id) as order_count
FROM users u 
LEFT JOIN orders o ON u.id = o.user_id 
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.username
ORDER BY order_count DESC
LIMIT 10;

-- 索引扫描统计
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes 
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

#### 索引建议工具
```sql
-- 使用pg_stat_statements分析查询
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT 
    query,
    calls,
    mean_time,
    stddev_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements 
WHERE userid = (SELECT usesysid FROM pg_user WHERE usename = current_user)
ORDER BY mean_time DESC
LIMIT 10;

-- 索引缺失检测
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE schemaname = 'public' 
AND tablename = 'users'
ORDER BY correlation ASC;
```

---

## 🍃 MongoDB索引设计实践

### 1. 索引创建和管理

#### 基本索引操作
```javascript
// 单字段索引
db.users.createIndex({ email: 1 })
db.orders.createIndex({ createdAt: -1 })

// 复合索引
db.users.createIndex({ status: 1, createdAt: -1 })
db.products.createIndex({ category: 1, price: 1 })

// 唯一索引
db.users.createIndex({ username: 1 }, { unique: true })
db.emailTokens.createIndex({ token: 1 }, { unique: true })

// 部分索引
db.users.createIndex(
    { email: 1 }, 
    { partialFilterExpression: { status: "active" } }
)

// TTL索引（自动过期）
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 })
db.logs.createIndex({ timestamp: 1 }, { expireAfterSeconds: 2592000 }) // 30天
```

#### 高级索引类型
```javascript
// 文本索引
db.articles.createIndex({ 
    title: "text", 
    content: "text" 
}, {
    weights: { title: 3, content: 1 },
    default_language: "zh"
})

// 地理空间索引
db.locations.createIndex({ location: "2dsphere" })
db.stores.createIndex({ coordinates: "2d" })

// 哈希索引
db.users.createIndex({ email: "hashed" })

// 通配符索引
db.products.createIndex({ "$**": 1 })
```

### 2. 索引效果分析

#### 执行计划分析
```javascript
// 基本执行计划
db.users.find({ email: "user@example.com" }).explain("executionStats")

// 复杂查询分析
db.orders.aggregate([
    { $match: { userId: ObjectId("...") } },
    { $group: { _id: "$status", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
]).explain("executionStats")

// 索引使用详情
db.users.find({ status: "active", createdAt: { $gte: ISODate("2024-01-01") } })
  .hint({ status: 1, createdAt: -1 })
  .explain()
```

#### 索引统计监控
```javascript
// 查看索引信息
db.users.getIndexes()

// 索引大小统计
db.users.stats({ indexDetails: true })

// 查询性能分析
db.system.profile.find().sort({ ts: -1 }).limit(10)

// 索引命中率监控
db.serverStatus().metrics.queryExecutor
```

### 3. 索引优化策略

#### 索引重建和优化
```javascript
// 重建索引
db.users.reIndex()

// 删除无效索引
db.users.dropIndex("email_1")

// 索引碎片整理
db.runCommand({ compact: "users" })

// 并发索引创建
db.users.createIndex(
    { newField: 1 }, 
    { background: true }
)
```

#### 性能监控脚本
```javascript
// 索引使用监控
function monitorIndexUsage() {
    const collections = db.getCollectionNames();
    
    collections.forEach(collectionName => {
        const stats = db[collectionName].stats({ indexDetails: true });
        
        print(`\n=== ${collectionName} Index Stats ===`);
        if (stats.indexSizes) {
            Object.keys(stats.indexSizes).forEach(indexName => {
                print(`${indexName}: ${stats.indexSizes[indexName]} bytes`);
            });
        }
    });
}

// 慢查询分析
function analyzeSlowQueries() {
    const slowQueries = db.system.profile.find({
        millis: { $gt: 1000 }
    }).sort({ ts: -1 }).limit(20);
    
    slowQueries.forEach(query => {
        print(`Query: ${query.ns} - ${query.millis}ms`);
        print(`Plan: ${JSON.stringify(query.planSummary)}`);
    });
}

monitorIndexUsage();
analyzeSlowQueries();
```

---

## 🔍 索引设计最佳实践

### 核心设计原则

#### 1. 选择性原则
```sql
-- 高选择性列适合做索引
SELECT COUNT(DISTINCT email) / COUNT(*) as selectivity FROM users;
-- 理想选择性 > 0.1 (10%)

-- 低选择性列不适合单独索引
SELECT COUNT(DISTINCT status) / COUNT(*) as selectivity FROM users;
-- 状态字段选择性通常很低(< 0.01)
```

#### 2. 最左前缀原则
```sql
-- 正确：能利用复合索引
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
SELECT * FROM orders WHERE user_id = 123;                    -- ✓
SELECT * FROM orders WHERE user_id = 123 AND created_at > '2024-01-01'; -- ✓

-- 错误：无法利用索引
SELECT * FROM orders WHERE created_at > '2024-01-01';        -- ✗
```

#### 3. 覆盖索引原则
```sql
-- 创建覆盖索引
CREATE INDEX idx_users_covering ON users(status, email, username);

-- 查询只需要索引中的列（覆盖查询）
SELECT status, email FROM users WHERE status = 'active';
-- 不需要回表查询，性能更好
```

### 常见设计误区

#### 1. 过度索引问题
```sql
-- 反面教材：过度索引
CREATE INDEX idx_user_1 ON users(email);
CREATE INDEX idx_user_2 ON users(username);
CREATE INDEX idx_user_3 ON users(phone);
CREATE INDEX idx_user_4 ON users(email, username);
CREATE INDEX idx_user_5 ON users(username, phone);
-- 问题：维护成本高，写入性能下降

-- 正确做法：精简索引
CREATE INDEX idx_user_main ON users(email);  -- 主要用作登录
CREATE INDEX idx_user_contact ON users(username, phone); -- 联系信息查询
```

#### 2. 索引列顺序问题
```sql
-- 错误的列顺序
CREATE INDEX idx_bad_order ON orders(amount, user_id);
-- 查询条件通常是 user_id = ? AND amount > ?

-- 正确的列顺序
CREATE INDEX idx_good_order ON orders(user_id, amount);
-- 先等值匹配，后范围查询
```

#### 3. 忽视查询模式
```sql
-- 分析实际查询模式
SELECT DIGEST_TEXT, COUNT_STAR, AVG_TIMER_WAIT
FROM performance_schema.events_statements_summary_by_digest
WHERE SCHEMA_NAME = 'myapp'
AND DIGEST_TEXT LIKE '%SELECT%'
ORDER BY COUNT_STAR DESC
LIMIT 10;

-- 根据查询频率创建索引，而非凭感觉
```

---

## 📊 索引性能评估报告

### 索引效果评估模板

```markdown
# 数据库索引性能评估报告

## 评估时间
2024年1月索引优化评估

## 当前索引状况
- **总索引数**: 45个
- **表平均索引数**: 3.2个
- **索引总大小**: 2.3GB
- **索引维护成本**: 中等

## 性能改善情况

### 查询性能提升
| 查询类型 | 优化前(ms) | 优化后(ms) | 改善幅度 |
|---------|-----------|-----------|----------|
| 用户查询 | 1200 | 45 | -96.25% |
| 订单统计 | 2800 | 120 | -95.71% |
| 商品搜索 | 3500 | 85 | -97.57% |

### 系统资源节省
- **CPU使用率**: 降低15%
- **内存占用**: 减少8%
- **磁盘I/O**: 减少25%
- **平均响应时间**: 降低85%

## 索引优化建议

### 新增索引
1. **idx_user_login_history**: 优化登录历史查询
2. **idx_order_payment_status**: 优化支付状态统计
3. **idx_product_inventory**: 优化库存查询

### 索引调整
1. **合并重复索引**: idx_user_email 和 idx_user_email_status
2. **删除低效索引**: idx_user_old_status (使用率<1%)
3. **调整列顺序**: idx_order_date_amount → idx_order_amount_date

## ROI分析
- **投入成本**: 8人天索引优化工作
- **收益估算**: 每月节省服务器成本约￥15,000
- **投资回报率**: 约250%
- **回收周期**: 2个月

## 后续优化计划
- [ ] 实施新增索引方案
- [ ] 建立索引使用监控机制
- [ ] 制定定期索引审查流程
- [ ] 优化索引维护自动化脚本
```

---