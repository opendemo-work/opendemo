# 数据库查询优化技术实战演示

## 🎯 学习目标

通过本案例你将掌握企业级数据库查询优化的核心技能：

- 深入理解查询执行计划和优化器工作原理
- 掌握SQL语句性能分析和优化技巧
- 学会索引优化策略和最佳实践
- 实施查询重写和重构技术
- 建立系统性的性能优化方法论
- 满足生产环境的高性能要求

## 🛠️ 环境准备

### 系统要求
- 已完成数据库安装配置环境
- 具备基础SQL查询能力
- 理解数据库索引基本概念
- 准备测试数据集用于性能验证

### 前置条件验证
```bash
# 验证数据库服务状态
systemctl is-active mysqld postgresql-14 mongod redis

# 创建测试数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS query_optimization_test;"
psql -U postgres -c "CREATE DATABASE query_optimization_test;"

# 准备测试数据
mysql -u root -p query_optimization_test < /opt/test_data/sample_data.sql
```

## 📁 项目结构

```
query-optimization-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 优化脚本
│   ├── mysql_query_optimizer.sh       # MySQL查询优化脚本
│   ├── postgresql_query_optimizer.sh  # PostgreSQL查询优化脚本
│   ├── mongodb_query_optimizer.js     # MongoDB查询优化脚本
│   ├── query_analysis_tool.py         # 查询分析工具
│   └── performance_benchmark.sh       # 性能基准测试脚本
├── configs/                           # 配置文件
│   ├── optimization_rules/            # 优化规则配置
│   ├── index_strategies/              # 索引策略配置
│   ├── cost_models/                   # 成本模型配置
│   └── workload_profiles/             # 工作负载配置
├── examples/                          # 优化案例
│   ├── slow_query_examples/           # 慢查询优化案例
│   ├── join_optimization/             # 连接优化案例
│   ├── subquery_rewrite/              # 子查询重写案例
│   └── index_design_patterns/         # 索引设计模式
├── benchmarks/                        # 基准测试
│   ├── tpcc_benchmark/                # TPC-C基准测试
│   ├── sysbench_tests/                # Sysbench测试
│   ├── custom_workloads/              # 自定义工作负载
│   └── performance_reports/           # 性能报告
└── docs/                              # 详细文档
    ├── optimization_methodology.md    # 优化方法论
    ├── execution_plan_analysis.md     # 执行计划分析
    ├── index_design_guide.md          # 索引设计指南
    └── best_practices.md              # 最佳实践指南
```

## 📊 查询优化方法论

### 优化金字塔模型
```yaml
# 查询优化金字塔
optimization_pyramid:
  foundation_layer:          # 基础层
    - schema_design          # 模式设计优化
    - data_modeling          # 数据建模优化
    - normalization          # 规范化设计
  
  structural_layer:          # 结构层
    - indexing_strategy      # 索引策略
    - partitioning_design    # 分区设计
    - clustering_keys        # 聚簇键设计
  
  operational_layer:         # 操作层
    - query_rewrite          # 查询重写
    - execution_planning     # 执行计划优化
    - resource_allocation    # 资源分配优化
  
  tactical_layer:            # 战术层
    - caching_strategies     # 缓存策略
    - connection_pooling     # 连接池优化
    - batch_processing       # 批处理优化
  
  strategic_layer:           # 战略层
    - workload_analysis      # 工作负载分析
    - capacity_planning      # 容量规划
    - performance_monitoring # 性能监控
```

## 🔧 核心优化技术实现

### 1. MySQL查询优化技术

```sql
-- MySQL查询优化完整示例

-- 1. 执行计划分析
-- 基础执行计划查看
EXPLAIN SELECT u.name, o.order_date, p.product_name 
FROM users u 
JOIN orders o ON u.id = o.user_id 
JOIN order_items oi ON o.id = oi.order_id 
JOIN products p ON oi.product_id = p.id 
WHERE u.created_at > '2024-01-01' 
AND o.status = 'completed';

-- 详细执行计划分析
EXPLAIN FORMAT=JSON SELECT u.name, o.order_date, p.product_name 
FROM users u 
JOIN orders o ON u.id = o.user_id 
JOIN order_items oi ON o.id = oi.order_id 
JOIN products p ON oi.product_id = p.id 
WHERE u.created_at > '2024-01-01' 
AND o.status = 'completed';

-- 2. 索引优化策略
-- 创建复合索引优化连接查询
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);
CREATE INDEX idx_products_id_name ON products(id, product_name);

-- 3. 查询重写优化
-- 原始慢查询
SELECT u.name, COUNT(o.id) as order_count, SUM(oi.quantity * p.price) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 1 YEAR)
GROUP BY u.id, u.name
HAVING order_count > 10
ORDER BY total_amount DESC
LIMIT 100;

-- 优化后的查询
SELECT u.name, 
       user_stats.order_count,
       user_stats.total_amount
FROM users u
JOIN (
    SELECT o.user_id,
           COUNT(*) as order_count,
           SUM(oi.quantity * p.price) as total_amount
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    AND o.order_date > DATE_SUB(NOW(), INTERVAL 1 YEAR)
    GROUP BY o.user_id
    HAVING COUNT(*) > 10
) user_stats ON u.id = user_stats.user_id
WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 1 YEAR)
ORDER BY user_stats.total_amount DESC
LIMIT 100;

-- 4. 子查询优化
-- 相关子查询优化为连接查询
-- 原始查询（相关子查询）
SELECT u.name, u.email
FROM users u
WHERE u.id IN (
    SELECT o.user_id 
    FROM orders o 
    WHERE o.order_date > DATE_SUB(NOW(), INTERVAL 30 DAY)
    AND o.total_amount > 1000
);

-- 优化后（使用EXISTS）
SELECT u.name, u.email
FROM users u
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.user_id = u.id
    AND o.order_date > DATE_SUB(NOW(), INTERVAL 30 DAY)
    AND o.total_amount > 1000
);

-- 5. 分页查询优化
-- 大数据量分页优化
-- 原始慢分页查询
SELECT * FROM orders 
WHERE status = 'completed' 
ORDER BY created_at DESC 
LIMIT 100000, 20;

-- 优化后的分页查询（使用游标）
SELECT o.* FROM orders o
INNER JOIN (
    SELECT id FROM orders 
    WHERE status = 'completed' 
    ORDER BY created_at DESC 
    LIMIT 100000, 20
) AS pagination_cursor ON o.id = pagination_cursor.id;

-- 6. 聚合查询优化
-- 复杂聚合查询优化
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') as month,
    p.category,
    COUNT(DISTINCT o.id) as order_count,
    COUNT(oi.id) as item_count,
    SUM(oi.quantity) as total_quantity,
    AVG(oi.quantity * p.price) as avg_order_value
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m'), p.category
ORDER BY month DESC, order_count DESC;

-- 优化索引支持
CREATE INDEX idx_orders_date_status ON orders(order_date, status);
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);
CREATE INDEX idx_products_category_price ON products(category, price);

-- 7. 统计信息更新
-- 更新表统计信息以优化查询计划
ANALYZE TABLE users, orders, order_items, products;

-- 8. 配置参数优化
-- 调整MySQL优化器参数
SET SESSION optimizer_search_depth = 0;  -- 自动选择搜索深度
SET SESSION join_buffer_size = 2097152;  -- 2MB连接缓冲区
SET SESSION sort_buffer_size = 2097152;  -- 2MB排序缓冲区
SET SESSION read_rnd_buffer_size = 524288; -- 512KB随机读缓冲区

-- 9. 查询缓存优化
-- 启用查询缓存（适用于读多写少场景）
SET GLOBAL query_cache_type = ON;
SET GLOBAL query_cache_size = 268435456;  -- 256MB缓存大小

-- 10. 性能基准测试
-- 使用sysbench进行查询性能测试
sysbench /usr/share/sysbench/oltp_read_only.lua \
  --mysql-host=localhost \
  --mysql-port=3306 \
  --mysql-user=sbtest \
  --mysql-password=sbtest \
  --mysql-db=sbtest \
  --table-size=1000000 \
  --tables=10 \
  --threads=16 \
  --time=300 \
  run
```

### 2. PostgreSQL查询优化技术

```sql
-- PostgreSQL查询优化完整示例

-- 1. 执行计划详细分析
-- 基础执行计划
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON)
SELECT u.name, o.order_date, p.product_name 
FROM users u 
JOIN orders o ON u.id = o.user_id 
JOIN order_items oi ON o.id = oi.order_id 
JOIN products p ON oi.product_id = p.id 
WHERE u.created_at > '2024-01-01' 
AND o.status = 'completed';

-- 2. 索引优化策略
-- 创建支持连接查询的复合索引
CREATE INDEX CONCURRENTLY idx_users_created_at ON users(created_at);
CREATE INDEX CONCURRENTLY idx_orders_user_status_date ON orders(user_id, status, order_date);
CREATE INDEX CONCURRENTLY idx_order_items_order_product ON order_items(order_id, product_id);
CREATE INDEX CONCURRENTLY idx_products_category_name ON products(category, product_name);

-- 3. 查询重写优化
-- 使用CTE优化复杂查询
WITH user_order_stats AS (
    SELECT 
        o.user_id,
        COUNT(*) as order_count,
        SUM(oi.quantity * p.price) as total_amount,
        AVG(oi.quantity * p.price) as avg_order_value
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'completed'
    AND o.order_date > CURRENT_DATE - INTERVAL '1 year'
    GROUP BY o.user_id
    HAVING COUNT(*) > 10
)
SELECT 
    u.name,
    uos.order_count,
    uos.total_amount,
    uos.avg_order_value
FROM users u
JOIN user_order_stats uos ON u.id = uos.user_id
WHERE u.created_at > CURRENT_DATE - INTERVAL '1 year'
ORDER BY uos.total_amount DESC
LIMIT 100;

-- 4. 窗口函数优化
-- 使用窗口函数替代子查询
SELECT 
    u.name,
    o.order_date,
    o.total_amount,
    ROW_NUMBER() OVER (PARTITION BY u.id ORDER BY o.order_date DESC) as order_rank,
    SUM(o.total_amount) OVER (PARTITION BY u.id) as user_total_spent,
    AVG(o.total_amount) OVER (PARTITION BY u.id) as user_avg_order
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
AND o.order_date > CURRENT_DATE - INTERVAL '1 year';

-- 5. 分区表优化
-- 创建分区表提高查询性能
CREATE TABLE orders_partitioned (
    id SERIAL,
    user_id INTEGER,
    order_date DATE,
    status VARCHAR(20),
    total_amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- 创建月度分区
CREATE TABLE orders_2024_01 PARTITION OF orders_partitioned
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders_partitioned
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- 6. 物化视图优化
-- 创建物化视图预计算复杂聚合
CREATE MATERIALIZED VIEW mv_user_statistics AS
SELECT 
    u.id as user_id,
    u.name,
    COUNT(o.id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- 刷新物化视图
REFRESH MATERIALIZED VIEW mv_user_statistics;

-- 7. 统计信息更新
-- 更新表和索引统计信息
ANALYZE users;
ANALYZE orders;
ANALYZE order_items;
ANALYZE products;

-- 8. 配置参数优化
-- 调整PostgreSQL优化器参数
ALTER SYSTEM SET shared_buffers = '2GB';
ALTER SYSTEM SET effective_cache_size = '6GB';
ALTER SYSTEM SET work_mem = '64MB';
ALTER SYSTEM SET maintenance_work_mem = '512MB';
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET seq_page_cost = 1.0;
SELECT pg_reload_conf();

-- 9. 并行查询优化
-- 启用并行查询
SET max_parallel_workers_per_gather = 4;
SET parallel_setup_cost = 1000;
SET parallel_tuple_cost = 0.1;

-- 10. 性能基准测试
-- 使用pgbench进行基准测试
pgbench -i -s 100 query_optimization_test  # 初始化测试数据
pgbench -c 50 -j 10 -T 300 query_optimization_test  # 运行测试
```

### 3. MongoDB查询优化技术

```javascript
// MongoDB查询优化完整示例

// 1. 查询计划分析
// 分析查询执行计划
db.orders.find({
  status: "completed",
  orderDate: {$gte: new Date("2024-01-01")}
}).explain("executionStats");

// 2. 索引优化策略
// 创建复合索引支持查询
db.orders.createIndex({status: 1, orderDate: -1});
db.orders.createIndex({"userId": 1, "status": 1});
db.orderItems.createIndex({"orderId": 1, "productId": 1});

// 创建文本索引支持全文搜索
db.products.createIndex({productName: "text", description: "text"});

// 3. 查询重写优化
// 原始慢查询
db.orders.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "userId",
      foreignField: "_id",
      as: "user"
    }
  },
  {
    $match: {
      "user.createdAt": {$gte: new Date("2024-01-01")},
      status: "completed"
    }
  },
  {
    $lookup: {
      from: "orderItems",
      localField: "_id",
      foreignField: "orderId",
      as: "items"
    }
  },
  {
    $project: {
      userName: {$arrayElemAt: ["$user.name", 0]},
      orderDate: 1,
      totalAmount: {$sum: "$items.amount"}
    }
  }
]);

// 优化后的查询
db.orders.aggregate([
  // 预过滤减少连接数据量
  {$match: {status: "completed", orderDate: {$gte: new Date("2024-01-01")}}},
  
  // 使用pipeline进行连接优化
  {
    $lookup: {
      from: "users",
      let: {userId: "$userId"},
      pipeline: [
        {$match: {$expr: {$and: [
          {$eq: ["$_id", "$$userId"]},
          {$gte: ["$createdAt", new Date("2024-01-01")]}
        ]}}},
        {$project: {name: 1}}
      ],
      as: "user"
    }
  },
  
  // 只获取需要的字段
  {$project: {
    userId: 1,
    orderDate: 1,
    user: 1
  }}
]);

// 4. 聚合管道优化
// 优化复杂的聚合查询
db.orders.aggregate([
  {$match: {
    status: "completed",
    orderDate: {$gte: new Date(new Date().setFullYear(new Date().getFullYear() - 1))}
  }},
  
  // 使用$facet进行并行处理
  {$facet: {
    orderStats: [
      {$group: {
        _id: null,
        totalOrders: {$sum: 1},
        avgOrderValue: {$avg: "$totalAmount"},
        maxOrderValue: {$max: "$totalAmount"}
      }}
    ],
    
    userStats: [
      {$group: {
        _id: "$userId",
        orderCount: {$sum: 1},
        totalSpent: {$sum: "$totalAmount"}
      }},
      {$sort: {totalSpent: -1}},
      {$limit: 100}
    ],
    
    monthlyStats: [
      {$group: {
        _id: {
          year: {$year: "$orderDate"},
          month: {$month: "$orderDate"}
        },
        orderCount: {$sum: 1},
        totalRevenue: {$sum: "$totalAmount"}
      }},
      {$sort: {"_id.year": -1, "_id.month": -1}}
    ]
  }}
]);

// 5. 分片键优化
// 为分片集合选择合适的分片键
sh.shardCollection("ecommerce.orders", {"userId": 1, "orderDate": 1});

// 6. 查询缓存优化
// 使用MapReduce预计算结果
db.orders.mapReduce(
  function() {
    emit(this.userId, {
      orderCount: 1,
      totalAmount: this.totalAmount,
      lastOrderDate: this.orderDate
    });
  },
  function(key, values) {
    var result = {orderCount: 0, totalAmount: 0, lastOrderDate: new Date(0)};
    values.forEach(function(value) {
      result.orderCount += value.orderCount;
      result.totalAmount += value.totalAmount;
      if (value.lastOrderDate > result.lastOrderDate) {
        result.lastOrderDate = value.lastOrderDate;
      }
    });
    return result;
  },
  {
    out: "user_order_summary",
    query: {status: "completed"}
  }
);

// 7. 性能监控和分析
// 启用慢查询日志
db.setProfilingLevel(1, {slowms: 100});  // 记录超过100ms的查询

// 分析慢查询日志
db.system.profile.find().sort({$natural: -1}).limit(10);

// 8. 内存使用优化
// 调整WiredTiger缓存大小
db.adminCommand({
  "setParameter": 1,
  "wiredTigerEngineConfigString": "cache_size=2G"
});

// 9. 连接池优化
// 配置应用程序连接池
const mongoOptions = {
  maxPoolSize: 50,
  minPoolSize: 10,
  maxIdleTimeMS: 30000,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000
};

// 10. 基准测试
// 使用mongostat监控实时性能
// mongostat --host localhost:27017 --discover 10

// 使用mongoperf测试磁盘性能
// echo '{"nThreads":8,"fileSizeMB":1000,"sleepMicros":1000}' | mongoperf
```

### 4. Redis查询优化技术

```bash
#!/bin/bash
# Redis查询优化技术脚本

# 1. 键空间优化
optimize_key_structure() {
  echo "优化Redis键结构..."
  
  # 使用哈希结构减少键数量
  # 原始方式（多个键）
  redis-cli SET "user:1001:name" "John Doe"
  redis-cli SET "user:1001:email" "john@example.com"
  redis-cli SET "user:1001:age" "30"
  
  # 优化方式（哈希结构）
  redis-cli HSET "user:1001" name "John Doe" email "john@example.com" age "30"
  
  # 使用命名空间前缀
  redis-cli SET "session:user:1001:last_active" "$(date +%s)"
  redis-cli SET "cache:product:2001:price" "29.99"
}

# 2. 内存优化
optimize_memory_usage() {
  echo "优化Redis内存使用..."
  
  # 使用较小的数据类型
  # 原始方式
  redis-cli SET "user:1001:active" "true"
  
  # 优化方式
  redis-cli SETBIT "user:active_flags" 1001 1
  
  # 使用整数编码
  redis-cli INCR "counter:page_views"
  
  # 配置内存淘汰策略
  redis-cli CONFIG SET maxmemory 2gb
  redis-cli CONFIG SET maxmemory-policy allkeys-lru
}

# 3. 管道优化
optimize_with_pipelining() {
  echo "使用管道优化批量操作..."
  
  # 原始方式（多次网络往返）
  for i in {1..1000}; do
    redis-cli SET "item:$i" "value_$i"
  done
  
  # 优化方式（管道批量操作）
  redis-cli --pipe << EOF
$(for i in {1..1000}; do echo "SET item:$i value_$i"; done)
EOF
}

# 4. Lua脚本优化
optimize_with_lua_scripts() {
  echo "使用Lua脚本优化原子操作..."
  
  # 复杂的原子操作
  local lua_script=$(cat << 'EOF'
local user_id = KEYS[1]
local product_id = ARGV[1]
local quantity = tonumber(ARGV[2])

-- 检查库存
local stock = redis.call('HGET', 'product:' .. product_id, 'stock')
if not stock or tonumber(stock) < quantity then
  return {err = 'Insufficient stock'}
end

-- 扣减库存
redis.call('HINCRBY', 'product:' .. product_id, 'stock', -quantity)

-- 记录订单
local order_key = 'order:' .. user_id .. ':' .. redis.call('TIME')[1]
redis.call('HMSET', order_key, 'product_id', product_id, 'quantity', quantity, 'timestamp', redis.call('TIME')[1])

return 'Order placed successfully'
EOF
)
  
  # 执行Lua脚本
  redis-cli EVAL "$lua_script" 1 "user:1001" "product:2001" "2"
}

# 5. 过期时间优化
optimize_expiration_strategy() {
  echo "优化键过期策略..."
  
  # 合理设置过期时间
  redis-cli SETEX "session:user:1001" 3600 "session_data"
  redis-cli SETEX "cache:api_response" 300 "cached_response"
  
  # 使用随机过期避免雪崩效应
  local ttl=$((3600 + RANDOM % 3600))
  redis-cli SETEX "cache:expensive_query" $ttl "cached_result"
}

# 6. 集群优化
optimize_cluster_performance() {
  echo "优化Redis集群性能..."
  
  # 使用hash tags确保相关键在同一slot
  redis-cli SET "{user:1001}:profile" "profile_data"
  redis-cli SET "{user:1001}:preferences" "preference_data"
  
  # 批量操作优化
  redis-cli MGET "{user:1001}:profile" "{user:1001}:preferences"
}

# 7. 监控和分析
setup_performance_monitoring() {
  echo "设置性能监控..."
  
  # 启用慢查询日志
  redis-cli CONFIG SET slowlog-log-slower-than 10000  # 10ms
  redis-cli CONFIG SET slowlog-max-len 128
  
  # 监控关键指标
  redis-cli INFO stats
  redis-cli INFO memory
  redis-cli INFO cpu
  redis-cli INFO commandstats
  
  # 分析慢查询
  redis-cli SLOWLOG GET 10
}

# 8. 基准测试
run_performance_benchmark() {
  echo "运行性能基准测试..."
  
  # 使用redis-benchmark进行测试
  redis-benchmark -h localhost -p 6379 -n 100000 -c 50 -t get,set,lpush,lpop
  
  # 测试不同数据类型的性能
  echo "测试字符串操作性能:"
  redis-benchmark -t set,get -n 100000 -d 256
  
  echo "测试哈希操作性能:"
  redis-benchmark -t hset,hget -n 100000
  
  echo "测试列表操作性能:"
  redis-benchmark -t lpush,lpop -n 100000
}

# 9. 配置优化
optimize_redis_configuration() {
  echo "优化Redis配置参数..."
  
  # 内存相关配置
  redis-cli CONFIG SET tcp-keepalive 300
  redis-cli CONFIG SET timeout 0
  redis-cli CONFIG SET tcp-backlog 511
  
  # 持久化配置优化
  redis-cli CONFIG SET save "900 1 300 10 60 10000"
  redis-cli CONFIG SET appendfsync everysec
  
  # 网络配置优化
  redis-cli CONFIG SET tcp-nodelay yes
}

# 主执行函数
main() {
  case "$1" in
    optimize-all)
      optimize_key_structure
      optimize_memory_usage
      optimize_with_pipelining
      optimize_with_lua_scripts
      optimize_expiration_strategy
      optimize_cluster_performance
      setup_performance_monitoring
      run_performance_benchmark
      optimize_redis_configuration
      echo "Redis查询优化完成"
      ;;
    benchmark)
      run_performance_benchmark
      ;;
    monitor)
      setup_performance_monitoring
      ;;
    *)
      echo "Usage: $0 {optimize-all|benchmark|monitor}"
      exit 1
      ;;
  esac
}

main "$@"
```

## 🎯 统一查询优化平台

### Python查询优化分析器
```python
#!/usr/bin/env python3
"""
企业级统一查询优化分析平台
支持多数据库查询优化的智能分析和建议
"""

import re
import json
import sqlite3
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class DatabaseType(Enum):
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    REDIS = "redis"

@dataclass
class QueryAnalysis:
    """查询分析结果"""
    query_text: str
    database_type: DatabaseType
    complexity_score: float
    optimization_suggestions: List[str]
    estimated_performance_gain: float
    execution_plan_issues: List[str]

class QueryOptimizer:
    """统一查询优化器"""
    
    def __init__(self):
        self.optimization_rules = self._load_optimization_rules()
        self.performance_baselines = self._load_baselines()
    
    def _load_optimization_rules(self) -> Dict:
        """加载优化规则"""
        return {
            'anti_patterns': [
                'SELECT *',
                'COUNT(*) with WHERE clause',
                'LIKE with leading wildcard',
                'Functions in WHERE clause',
                'Multiple subqueries'
            ],
            'best_practices': [
                'Use specific column names instead of *',
                'Add appropriate indexes',
                'Limit result sets',
                'Use EXPLAIN to analyze queries',
                'Consider query rewriting'
            ]
        }
    
    def _load_baselines(self) -> Dict:
        """加载性能基线"""
        return {
            'mysql': {'avg_query_time': 0.1, 'max_result_set': 1000},
            'postgresql': {'avg_query_time': 0.08, 'max_result_set': 1500},
            'mongodb': {'avg_query_time': 0.05, 'max_result_set': 2000},
            'redis': {'avg_operation_time': 0.001, 'max_batch_size': 10000}
        }
    
    def analyze_query(self, query: str, db_type: DatabaseType) -> QueryAnalysis:
        """分析查询并提供优化建议"""
        analysis = QueryAnalysis(
            query_text=query,
            database_type=db_type,
            complexity_score=0.0,
            optimization_suggestions=[],
            estimated_performance_gain=0.0,
            execution_plan_issues=[]
        )
        
        # 计算复杂度分数
        analysis.complexity_score = self._calculate_complexity(query, db_type)
        
        # 识别反模式
        anti_patterns_found = self._detect_anti_patterns(query)
        if anti_patterns_found:
            analysis.optimization_suggestions.extend(anti_patterns_found)
        
        # 生成优化建议
        suggestions = self._generate_optimization_suggestions(query, db_type)
        analysis.optimization_suggestions.extend(suggestions)
        
        # 估算性能提升
        analysis.estimated_performance_gain = self._estimate_performance_gain(
            analysis.complexity_score, len(analysis.optimization_suggestions)
        )
        
        return analysis
    
    def _calculate_complexity(self, query: str, db_type: DatabaseType) -> float:
        """计算查询复杂度"""
        score = 0.0
        
        # 基础复杂度计算
        if 'JOIN' in query.upper():
            score += 0.3
        if 'UNION' in query.upper():
            score += 0.2
        if 'SUBQUERY' in query.upper() or query.count('(') > 3:
            score += 0.25
        if 'GROUP BY' in query.upper():
            score += 0.15
        if 'ORDER BY' in query.upper():
            score += 0.1
        
        # 数据库特定调整
        if db_type == DatabaseType.MYSQL:
            if 'DISTINCT' in query.upper():
                score += 0.1
        elif db_type == DatabaseType.POSTGRESQL:
            if 'WINDOW' in query.upper() or 'OVER' in query.upper():
                score += 0.2
        
        return min(score, 1.0)
    
    def _detect_anti_patterns(self, query: str) -> List[str]:
        """检测查询反模式"""
        suggestions = []
        
        query_upper = query.upper()
        
        if 'SELECT *' in query_upper:
            suggestions.append("避免使用SELECT *，明确指定需要的列")
        
        if 'COUNT(*)' in query_upper and 'WHERE' in query_upper:
            suggestions.append("对带有WHERE条件的COUNT(*)考虑使用索引优化")
        
        if 'LIKE \'%\' in query_upper:
            suggestions.append("避免前导通配符的LIKE查询，这会导致全表扫描")
        
        # 检测函数在WHERE子句中
        functions = ['UPPER(', 'LOWER(', 'DATE(', 'YEAR(', 'MONTH(']
        for func in functions:
            if func in query_upper:
                suggestions.append(f"避免在WHERE子句中使用{func.rstrip('(')}函数")
        
        return suggestions
    
    def _generate_optimization_suggestions(self, query: str, db_type: DatabaseType) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 通用建议
        suggestions.append("使用EXPLAIN分析查询执行计划")
        suggestions.append("为经常查询的列添加适当的索引")
        
        # 数据库特定建议
        if db_type == DatabaseType.MYSQL:
            suggestions.append("考虑使用查询缓存（适用于读多写少场景）")
            suggestions.append("优化JOIN顺序，将选择性高的表放在前面")
        elif db_type == DatabaseType.POSTGRESQL:
            suggestions.append("考虑使用物化视图预计算复杂查询")
            suggestions.append("使用CTE改善复杂查询的可读性和性能")
        elif db_type == DatabaseType.MONGODB:
            suggestions.append("使用投影减少返回的字段数量")
            suggestions.append("考虑使用聚合管道替代多个查询")
        elif db_type == DatabaseType.REDIS:
            suggestions.append("使用哈希结构合并相关键值")
            suggestions.append("合理使用管道批量操作")
        
        return suggestions
    
    def _estimate_performance_gain(self, complexity: float, suggestion_count: int) -> float:
        """估算性能提升百分比"""
        base_gain = complexity * 30  # 基础提升
        suggestion_bonus = suggestion_count * 5  # 建议奖励
        return min(base_gain + suggestion_bonus, 90)  # 最大90%提升

# 使用示例
def main():
    optimizer = QueryOptimizer()
    
    # 测试查询
    test_queries = [
        ("SELECT * FROM users WHERE created_at > '2024-01-01'", DatabaseType.MYSQL),
        ("SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id", DatabaseType.POSTGRESQL),
        ("db.users.find({createdAt: {$gt: new Date('2024-01-01')}})", DatabaseType.MONGODB),
        ("GET user:1001:profile", DatabaseType.REDIS)
    ]
    
    for query, db_type in test_queries:
        analysis = optimizer.analyze_query(query, db_type)
        print(f"\n{db_type.value.upper()} 查询分析:")
        print(f"复杂度分数: {analysis.complexity_score:.2f}")
        print(f"预计性能提升: {analysis.estimated_performance_gain:.1f}%")
        print("优化建议:")
        for suggestion in analysis.optimization_suggestions:
            print(f"  - {suggestion}")

if __name__ == "__main__":
    main()
```

## 🧪 性能优化验证测试

### 自动化优化效果测试
```bash
#!/bin/bash
# 查询优化效果验证测试套件

TEST_RESULTS=()

# MySQL查询优化测试
test_mysql_query_optimization() {
  echo "=== MySQL查询优化测试 ==="
  
  # 创建测试表和数据
  mysql -u root -p << EOF
DROP DATABASE IF EXISTS optimization_test;
CREATE DATABASE optimization_test;
USE optimization_test;

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  order_date DATE,
  status VARCHAR(20),
  total_amount DECIMAL(10,2),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 插入测试数据
INSERT INTO users (name, email, created_at) 
SELECT CONCAT('User', seq), CONCAT('user', seq, '@example.com'), DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY)
FROM seq_1_to_10000;

INSERT INTO orders (user_id, order_date, status, total_amount)
SELECT FLOOR(RAND() * 10000) + 1, DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY), 
       ELT(FLOOR(RAND() * 3) + 1, 'pending', 'completed', 'cancelled'), RAND() * 1000
FROM seq_1_to_50000;
EOF
  
  # 测试原始查询性能
  echo "测试原始查询性能..."
  local start_time=$(date +%s%N)
  mysql -u root -p optimization_test << EOF > /dev/null
SELECT u.name, COUNT(o.id) as order_count, SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 1 YEAR)
GROUP BY u.id, u.name
HAVING order_count > 5
ORDER BY total_spent DESC
LIMIT 100;
EOF
  local end_time=$(date +%s%N)
  local original_time=$((($end_time - $start_time) / 1000000))
  
  # 创建索引
  mysql -u root -p optimization_test << EOF
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);
EOF
  
  # 测试优化后查询性能
  echo "测试优化后查询性能..."
  start_time=$(date +%s%N)
  mysql -u root -p optimization_test << EOF > /dev/null
SELECT u.name, user_stats.order_count, user_stats.total_spent
FROM users u
JOIN (
  SELECT user_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
  FROM orders 
  WHERE order_date > DATE_SUB(NOW(), INTERVAL 1 YEAR)
  GROUP BY user_id
  HAVING COUNT(*) > 5
) user_stats ON u.id = user_stats.user_id
WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 1 YEAR)
ORDER BY user_stats.total_spent DESC
LIMIT 100;
EOF
  end_time=$(date +%s%N)
  local optimized_time=$((($end_time - $start_time) / 1000000))
  
  local improvement_pct=$((($original_time - $optimized_time) * 100 / $original_time))
  
  if [ $improvement_pct -gt 30 ]; then
    TEST_RESULTS+=("MySQL查询优化测试: 通过 (性能提升${improvement_pct}%)")
    echo "✅ MySQL查询优化成功，性能提升${improvement_pct}%"
  else
    TEST_RESULTS+=("MySQL查询优化测试: 失败 (性能提升${improvement_pct}%)")
    echo "❌ MySQL查询优化效果不佳，仅提升${improvement_pct}%"
  fi
}

# PostgreSQL查询优化测试
test_postgresql_query_optimization() {
  echo "=== PostgreSQL查询优化测试 ==="
  
  # 创建测试环境
  psql -U postgres << EOF
DROP DATABASE IF EXISTS optimization_test;
CREATE DATABASE optimization_test;
\c optimization_test

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  order_date DATE,
  status VARCHAR(20),
  total_amount DECIMAL(10,2)
);

-- 插入测试数据
INSERT INTO users (name, email, created_at)
SELECT 'User' || seq, 'user' || seq || '@example.com', CURRENT_DATE - (RANDOM() * 365)::INTEGER
FROM generate_series(1, 10000) seq;

INSERT INTO orders (user_id, order_date, status, total_amount)
SELECT (RANDOM() * 10000)::INTEGER + 1, CURRENT_DATE - (RANDOM() * 365)::INTEGER,
       CASE (RANDOM() * 3)::INTEGER 
         WHEN 0 THEN 'pending'
         WHEN 1 THEN 'completed'
         ELSE 'cancelled'
       END,
       RANDOM() * 1000
FROM generate_series(1, 50000);
EOF
  
  # 测试原始查询性能
  echo "测试原始查询性能..."
  local original_time=$(psql -U postgres -d optimization_test -t -A -c "
    EXPLAIN (ANALYZE, TIMING)
    SELECT u.name, COUNT(o.id) as order_count, SUM(o.total_amount) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.created_at > CURRENT_DATE - INTERVAL '1 year'
    GROUP BY u.id, u.name
    HAVING COUNT(o.id) > 5
    ORDER BY total_spent DESC
    LIMIT 100;
  " | grep 'Execution Time' | awk '{print $3}')
  
  # 创建索引
  psql -U postgres -d optimization_test << EOF
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_orders_user_date_status ON orders(user_id, order_date, status);
EOF
  
  # 测试优化后查询性能
  echo "测试优化后查询性能..."
  local optimized_time=$(psql -U postgres -d optimization_test -t -A -c "
    EXPLAIN (ANALYZE, TIMING)
    WITH user_order_stats AS (
      SELECT user_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
      FROM orders
      WHERE order_date > CURRENT_DATE - INTERVAL '1 year'
      GROUP BY user_id
      HAVING COUNT(*) > 5
    )
    SELECT u.name, uos.order_count, uos.total_spent
    FROM users u
    JOIN user_order_stats uos ON u.id = uos.user_id
    WHERE u.created_at > CURRENT_DATE - INTERVAL '1 year'
    ORDER BY uos.total_spent DESC
    LIMIT 100;
  " | grep 'Execution Time' | awk '{print $3}')
  
  local improvement_pct=$(echo "scale=2; (($original_time - $optimized_time) / $original_time) * 100" | bc)
  
  if (( $(echo "$improvement_pct > 30" | bc -l) )); then
    TEST_RESULTS+=("PostgreSQL查询优化测试: 通过 (性能提升${improvement_pct}%)")
    echo "✅ PostgreSQL查询优化成功，性能提升${improvement_pct}%"
  else
    TEST_RESULTS+=("PostgreSQL查询优化测试: 失败 (性能提升${improvement_pct}%)")
    echo "❌ PostgreSQL查询优化效果不佳，仅提升${improvement_pct}%"
  fi
}

# 生成优化测试报告
generate_optimization_test_report() {
  echo "=== 查询优化测试综合报告 ==="
  
  local total_tests=${#TEST_RESULTS[@]}
  local passed_tests=0
  
  for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
    if [[ $result == *"通过"* ]]; then
      ((passed_tests++))
    fi
  done
  
  echo ""
  echo "测试总结:"
  echo "总测试项: $total_tests"
  echo "通过项: $passed_tests"
  echo "通过率: $((passed_tests * 100 / total_tests))%"
  
  # 保存报告
  local report_file="/tmp/query_optimization_report_$(date +%Y%m%d_%H%M%S).txt"
  printf "%s\n" "${TEST_RESULTS[@]}" > "$report_file"
  echo "详细报告已保存: $report_file"
}

# 执行所有测试
test_mysql_query_optimization
test_postgresql_query_optimization
generate_optimization_test_report
```

## 📚 最佳实践总结

### 查询优化核心原则
1. **预防优于治疗**: 在设计阶段就考虑性能因素
2. **测量驱动优化**: 基于实际性能数据进行优化决策
3. **渐进式优化**: 从最影响性能的地方开始优化
4. **成本效益平衡**: 考虑优化投入与收益的比例
5. **持续监控**: 优化是一个持续的过程，需要不断监控和调整

### 常见优化策略优先级
1. **索引优化** (最高优先级) - 解决大部分性能问题
2. **查询重写** (高优先级) - 改变查询结构提升效率
3. **统计信息更新** (中等优先级) - 确保优化器做出正确决策
4. **配置参数调整** (中等优先级) - 优化系统资源配置
5. **架构重构** (低优先级) - 重大结构调整

### 性能监控要点
- **响应时间**: 关注95th和99th百分位响应时间
- **吞吐量**: 每秒处理的查询数量
- **资源利用率**: CPU、内存、磁盘I/O使用情况
- **缓存命中率**: 各级缓存的效率指标
- **错误率**: 查询失败和超时的比例

---
> **💡 提示**: 查询优化需要理论知识和实践经验相结合，建议在测试环境中充分验证后再应用到生产环境。