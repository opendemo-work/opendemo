# 🔍 数据库慢查询分析指南

> 企业级数据库性能诊断体系，涵盖慢查询识别、分析工具使用、优化建议生成等完整的性能问题诊断和解决方案

## 📋 案例概述

本案例详细介绍数据库慢查询的诊断方法和优化技术，通过系统性的分析工具和优化策略，帮助DBA快速定位和解决数据库性能瓶颈问题。

### 🎯 学习目标

- 掌握慢查询识别和监控方法
- 熟练使用各种性能分析工具
- 理解执行计划的解读和优化
- 实施系统性的性能优化策略
- 建立持续性能监控机制

### ⏱️ 学习时长

- **理论学习**: 3小时
- **实践操作**: 4小时
- **总计**: 7小时

---

## 📊 慢查询诊断框架

### 性能问题分类

```
数据库性能问题
├── 查询性能问题
│   ├── 慢查询
│   ├── 全表扫描
│   ├── 索引失效
│   └── JOIN效率低下
├── 系统资源问题
│   ├── CPU使用率高
│   ├── 内存不足
│   ├── 磁盘I/O瓶颈
│   └── 网络延迟
├── 架构设计问题
│   ├── 表结构不合理
│   ├── 索引设计缺陷
│   ├── 分区策略不当
│   └── 缓存配置错误
└── 并发控制问题
    ├── 锁等待
    ├── 死锁
    ├── 连接池耗尽
    └── 事务隔离级别过高
```

### 诊断流程

```
问题发现
    ↓
数据收集
    ↓
根本原因分析
    ↓
解决方案制定
    ↓
实施优化
    ↓
效果验证
    ↓
持续监控
```

---

## 🐬 MySQL慢查询分析实践

### 1. 慢查询监控配置

#### 启用慢查询日志
```sql
-- 查看当前慢查询配置
SHOW VARIABLES LIKE 'slow_query_log%';
SHOW VARIABLES LIKE 'long_query_time';
SHOW VARIABLES LIKE 'log_queries_not_using_indexes';

-- 启用慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';
SET GLOBAL long_query_time = 1.0; -- 超过1秒的查询记录
SET GLOBAL log_queries_not_using_indexes = 'ON'; -- 记录未使用索引的查询
SET GLOBAL log_throttle_queries_not_using_indexes = 10; -- 限制未使用索引查询的日志频率

-- 验证配置
SELECT @@slow_query_log, @@long_query_time, @@log_queries_not_using_indexes;
```

#### 慢查询日志配置文件
```ini
# /etc/my.cnf 慢查询配置
[mysqld]
# 慢查询日志基础配置
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1.0
log_queries_not_using_indexes = 1
log_throttle_queries_not_using_indexes = 10

# 日志格式优化
log_slow_admin_statements = 1
log_slow_slave_statements = 1
log_output = FILE,TABLE  # 同时输出到文件和表

# 性能模式配置
performance_schema = ON
```

### 2. 慢查询分析工具

#### 使用mysqldumpslow分析
```bash
#!/bin/bash
# mysql_slow_query_analyzer.sh

LOG_FILE="/var/log/mysql/slow.log"
ANALYSIS_DIR="/var/reports/slow_queries"

# 创建分析目录
mkdir -p $ANALYSIS_DIR

# 基本统计分析
echo "=== 慢查询基本统计 ===" > $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt
mysqldumpslow -s t -t 10 $LOG_FILE >> $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt

# 按平均执行时间排序
echo -e "\n=== 按平均执行时间排序 ===" >> $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt
mysqldumpslow -s at -t 10 $LOG_FILE >> $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt

# 按执行次数排序
echo -e "\n=== 按执行次数排序 ===" >> $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt
mysqldumpslow -s c -t 10 $LOG_FILE >> $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt

# 分析特定模式的查询
echo -e "\n=== SELECT查询分析 ===" >> $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt
mysqldumpslow -g "SELECT" $LOG_FILE >> $ANALYSIS_DIR/analysis_$(date +%Y%m%d).txt

# 生成HTML报告
cat > $ANALYSIS_DIR/report_$(date +%Y%m%d).html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>MySQL慢查询分析报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .section { margin: 20px 0; }
        .query { background: #f5f5f5; padding: 10px; margin: 5px 0; border-left: 4px solid #007cba; }
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .stat-card { background: #e9f7fe; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>MySQL慢查询分析报告</h1>
    <div class="stats">
        <div class="stat-card">
            <h3>总慢查询数</h3>
            <p id="total_queries">-</p>
        </div>
        <div class="stat-card">
            <h3>平均执行时间</h3>
            <p id="avg_time">-</p>
        </div>
        <div class="stat-card">
            <h3>最慢查询</h3>
            <p id="slowest_query">-</p>
        </div>
    </div>
    <div class="section">
        <h2>Top 10 慢查询</h2>
        <div id="top_queries"></div>
    </div>
</body>
<script>
// JavaScript代码用于动态填充数据
</script>
</html>
EOF
```

#### Percona Toolkit使用
```bash
#!/bin/bash
# percona_toolkit_analyzer.sh

# 安装Percona Toolkit
# yum install percona-toolkit 或 apt-get install percona-toolkit

# 使用pt-query-digest分析慢查询日志
pt-query-digest \
    --limit 10 \
    --order-by Query_time:sum \
    --filter '($event->{Bytes} || 0) > 1024' \
    /var/log/mysql/slow.log > /var/reports/pt-query-digest-report.txt

# 详细分析特定查询
pt-query-digest \
    --filter '$event->{arg} =~ m/SELECT.*users/i' \
    /var/log/mysql/slow.log > /var/reports/users-query-analysis.txt

# 实时监控模式
pt-query-digest \
    --processlist h=localhost,u=root,p=password \
    --run-time 60 \
    --interval 5 \
    --review D=test,t=query_review \
    --history D=test,t=query_history
```

### 3. 执行计划深度分析

#### EXPLAIN详细解读
```sql
-- 基础执行计划分析
EXPLAIN FORMAT=JSON 
SELECT u.username, o.order_date, o.total_amount
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE u.status = 'active' 
AND o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC 
LIMIT 10;

-- 扩展执行计划
EXPLAIN FORMAT=TREE
SELECT u.username, COUNT(o.id) as order_count
FROM users u 
LEFT JOIN orders o ON u.id = o.user_id 
GROUP BY u.id, u.username
HAVING order_count > 5;

-- 分析表统计信息
ANALYZE TABLE users, orders;
SHOW TABLE STATUS LIKE 'users';
SHOW INDEX FROM users;

-- 优化器跟踪
SET optimizer_trace="enabled=on";
SELECT u.username, o.order_date
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE u.email = 'user@example.com';
SELECT * FROM information_schema.OPTIMIZER_TRACE;
SET optimizer_trace="enabled=off";
```

#### 性能模式分析
```sql
-- 启用性能模式监控
UPDATE performance_schema.setup_instruments 
SET ENABLED = 'YES', TIMED = 'YES' 
WHERE NAME LIKE '%statement%';

UPDATE performance_schema.setup_consumers 
SET ENABLED = 'YES' 
WHERE NAME LIKE '%statements%';

-- 查询执行统计
SELECT 
    DIGEST_TEXT,
    COUNT_STAR as execution_count,
    AVG_TIMER_WAIT/1000000000 as avg_time_sec,
    MAX_TIMER_WAIT/1000000000 as max_time_sec,
    SUM_ROWS_EXAMINED as total_rows_examined,
    SUM_CREATED_TMP_TABLES as tmp_tables_created,
    SUM_SELECT_FULL_JOIN as full_joins
FROM performance_schema.events_statements_summary_by_digest
WHERE SCHEMA_NAME = 'myapp'
AND AVG_TIMER_WAIT > 1000000000  -- 超过1秒的查询
ORDER BY AVG_TIMER_WAIT DESC
LIMIT 10;

-- 等待事件分析
SELECT 
    EVENT_NAME,
    COUNT_STAR,
    SUM_TIMER_WAIT/1000000000 as total_wait_time_sec,
    AVG_TIMER_WAIT/1000000000 as avg_wait_time_sec
FROM performance_schema.events_waits_summary_global_by_event_name
WHERE COUNT_STAR > 0
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;
```

---

## 🐘 PostgreSQL慢查询分析实践

### 1. 慢查询日志配置

#### 基础配置
```sql
-- 查看当前配置
SHOW log_min_duration_statement;
SHOW log_statement;
SHOW log_line_prefix;

-- 配置慢查询日志
ALTER SYSTEM SET log_min_duration_statement = 1000; -- 1秒
ALTER SYSTEM SET log_statement = 'none'; -- 不记录所有语句
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';
ALTER SYSTEM SET log_duration = on;
ALTER SYSTEM SET log_lock_waits = on;

-- 重新加载配置
SELECT pg_reload_conf();
```

#### 日志格式优化
```conf
# postgresql.conf 详细配置
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_file_mode = 0600
log_truncate_on_rotation = off
log_rotation_age = 1d
log_rotation_size = 100MB

# 慢查询相关配置
log_min_duration_statement = 1000
log_statement = 'none'
log_duration = on
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_lock_waits = on
log_temp_files = 0
log_checkpoints = on
log_connections = on
log_disconnections = on
```

### 2. 查询性能分析工具

#### pgBadger日志分析
```bash
#!/bin/bash
# pgbadger_analyzer.sh

# 安装pgBadger
# cpan install pgBadger 或 yum install pgbadger

# 生成HTML报告
pgbadger \
    -I \
    -O /var/reports/pgbadger \
    -o report_$(date +%Y%m%d).html \
    /var/lib/pgsql/data/pg_log/postgresql-*.log

# 详细分析特定时间段
pgbadger \
    --begin 2024-01-01 00:00:00 \
    --end 2024-01-01 23:59:59 \
    -O /var/reports/pgbadger_daily \
    -o daily_report_20240101.html \
    /var/lib/pgsql/data/pg_log/postgresql-2024-01-01*.log

# 按查询类型分类分析
pgbadger \
    --exclude-query "autovacuum.*" \
    --include-query-time 5 \
    -O /var/reports/pgbadger_filtered \
    -o filtered_report.html \
    /var/lib/pgsql/data/pg_log/postgresql-*.log
```

#### 自定义分析脚本
```python
#!/usr/bin/env python3
# postgres_slow_query_analyzer.py

import psycopg2
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json

class PostgresSlowQueryAnalyzer:
    def __init__(self, connection_params):
        self.conn_params = connection_params
        self.queries = []
        
    def connect_and_extract(self):
        """连接数据库并提取慢查询信息"""
        try:
            conn = psycopg2.connect(**self.conn_params)
            cur = conn.cursor()
            
            # 从pg_stat_statements获取慢查询
            cur.execute("""
                SELECT 
                    query,
                    calls,
                    total_time,
                    mean_time,
                    rows,
                    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) as hit_percent,
                    temp_blks_written,
                    blk_read_time,
                    blk_write_time
                FROM pg_stat_statements 
                WHERE userid = (SELECT usesysid FROM pg_user WHERE usename = current_user)
                AND mean_time > 1000  -- 超过1秒的查询
                ORDER BY mean_time DESC
                LIMIT 50
            """)
            
            columns = [desc[0] for desc in cur.description]
            for row in cur.fetchall():
                query_info = dict(zip(columns, row))
                self.queries.append(query_info)
            
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"数据库连接错误: {e}")
            return False
        return True
    
    def analyze_query_patterns(self):
        """分析查询模式"""
        pattern_stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'queries': []})
        
        for query_info in self.queries:
            query = query_info['query'].strip()
            
            # 识别查询类型
            if query.upper().startswith('SELECT'):
                pattern = 'SELECT'
            elif query.upper().startswith('INSERT'):
                pattern = 'INSERT'
            elif query.upper().startswith('UPDATE'):
                pattern = 'UPDATE'
            elif query.upper().startswith('DELETE'):
                pattern = 'DELETE'
            else:
                pattern = 'OTHER'
            
            pattern_stats[pattern]['count'] += 1
            pattern_stats[pattern]['total_time'] += query_info['total_time']
            pattern_stats[pattern]['queries'].append({
                'query': query[:100] + '...' if len(query) > 100 else query,
                'mean_time': query_info['mean_time'],
                'calls': query_info['calls']
            })
        
        return dict(pattern_stats)
    
    def identify_performance_issues(self):
        """识别性能问题"""
        issues = []
        
        for query_info in self.queries:
            query = query_info['query']
            mean_time = query_info['mean_time']
            hit_percent = query_info['hit_percent'] or 0
            
            # 缓冲区命中率低
            if hit_percent < 80:
                issues.append({
                    'type': 'LOW_BUFFER_HIT_RATE',
                    'query': query[:200],
                    'hit_percent': hit_percent,
                    'severity': 'HIGH' if hit_percent < 50 else 'MEDIUM'
                })
            
            # 产生大量临时文件
            if query_info['temp_blks_written'] > 1000:
                issues.append({
                    'type': 'HIGH_TEMP_BLOCKS',
                    'query': query[:200],
                    'temp_blocks': query_info['temp_blks_written'],
                    'severity': 'HIGH'
                })
            
            # I/O等待时间长
            io_time = query_info['blk_read_time'] + query_info['blk_write_time']
            if io_time > 1000:
                issues.append({
                    'type': 'HIGH_IO_WAIT',
                    'query': query[:200],
                    'io_time': io_time,
                    'severity': 'HIGH' if io_time > 5000 else 'MEDIUM'
                })
        
        return issues
    
    def generate_recommendations(self):
        """生成优化建议"""
        recommendations = []
        
        pattern_stats = self.analyze_query_patterns()
        
        # 基于查询模式的建议
        if pattern_stats.get('SELECT', {}).get('count', 0) > len(self.queries) * 0.7:
            recommendations.append({
                'category': 'QUERY_PATTERN',
                'issue': '大量SELECT查询',
                'recommendation': '考虑添加适当的索引或优化查询条件'
            })
        
        # 基于性能问题的建议
        issues = self.identify_performance_issues()
        high_severity_issues = [issue for issue in issues if issue['severity'] == 'HIGH']
        
        if high_severity_issues:
            recommendations.append({
                'category': 'PERFORMANCE',
                'issue': f'发现{len(high_severity_issues)}个高严重性性能问题',
                'recommendation': '立即优化相关查询，重点关注缓冲区命中率和I/O性能'
            })
        
        return recommendations
    
    def export_report(self, filename):
        """导出分析报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_slow_queries': len(self.queries),
            'pattern_analysis': self.analyze_query_patterns(),
            'performance_issues': self.identify_performance_issues(),
            'recommendations': self.generate_recommendations(),
            'top_queries': self.queries[:10]  # Top 10慢查询
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

# 使用示例
if __name__ == "__main__":
    analyzer = PostgresSlowQueryAnalyzer({
        'host': 'localhost',
        'database': 'myapp',
        'user': 'postgres',
        'password: "${DB_PASSWORD}"
    })
    
    if analyzer.connect_and_extract():
        analyzer.export_report('/var/reports/postgres_slow_query_report.json')
        print("分析报告已生成")
```

### 3. 执行计划详解

#### EXPLAIN ANALYZE深度分析
```sql
-- 详细执行计划分析
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON)
SELECT 
    u.username,
    COUNT(o.id) as order_count,
    AVG(o.total_amount) as avg_order_value
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE u.created_at >= '2024-01-01'
AND u.status = 'active'
GROUP BY u.id, u.username
HAVING COUNT(o.id) > 5
ORDER BY avg_order_value DESC
LIMIT 20;

-- 并行查询分析
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT 
    p.category,
    COUNT(*) as product_count,
    AVG(p.price) as avg_price
FROM products p 
WHERE p.price > 100
GROUP BY p.category
ORDER BY avg_price DESC;

-- 索引使用情况分析
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan,
    100.0 * idx_tup_fetch / nullif(idx_tup_read, 0) as fetch_ratio
FROM pg_stat_user_indexes 
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

---

## 🍃 MongoDB慢查询分析实践

### 1. 慢查询配置和监控

#### 启用慢查询日志
```javascript
// MongoDB慢查询配置
use admin

// 设置慢查询阈值
db.setProfilingLevel(1, { slowms: 1000 })  // 记录超过1秒的查询

// 或者设置为记录所有操作
// db.setProfilingLevel(2)

// 查看当前配置
db.getProfilingStatus()

// 查看慢查询日志
db.system.profile.find().sort({ ts: -1 }).limit(10)

// 分析特定时间范围的慢查询
db.system.profile.find({
    ts: {
        $gte: new Date(Date.now() - 24*60*60*1000),  // 最近24小时
        $lte: new Date()
    },
    millis: { $gte: 1000 }  // 超过1秒的操作
}).sort({ millis: -1 })
```

#### 慢查询聚合分析
```javascript
// 慢查询统计分析
use admin

// 按操作类型统计
db.system.profile.aggregate([
    { $match: { millis: { $gte: 1000 } } },
    { $group: {
        _id: "$op",
        count: { $sum: 1 },
        avgDuration: { $avg: "$millis" },
        maxDuration: { $max: "$millis" },
        minDuration: { $min: "$millis" }
    }},
    { $sort: { avgDuration: -1 } }
])

// 按命名空间统计
db.system.profile.aggregate([
    { $match: { millis: { $gte: 1000 } } },
    { $group: {
        _id: "$ns",
        count: { $sum: 1 },
        totalDuration: { $sum: "$millis" },
        avgDuration: { $avg: "$millis" },
        operations: { $addToSet: { op: "$op", query: "$query" } }
    }},
    { $sort: { totalDuration: -1 } },
    { $limit: 10 }
])

// 识别最耗时的查询模式
db.system.profile.aggregate([
    { $match: { 
        millis: { $gte: 1000 },
        op: "query"
    }},
    { $project: {
        queryPattern: { $substr: ["$query", 0, 200] },
        duration: "$millis",
        timestamp: "$ts"
    }},
    { $group: {
        _id: "$queryPattern",
        count: { $sum: 1 },
        avgDuration: { $avg: "$duration" },
        maxDuration: { $max: "$duration" },
        firstSeen: { $min: "$timestamp" },
        lastSeen: { $max: "$timestamp" }
    }},
    { $sort: { avgDuration: -1 } },
    { $limit: 20 }
])
```

### 2. 性能分析工具

#### MongoDB Compass性能分析器
```javascript
// 使用MongoDB Compass的性能分析功能
// 1. 连接到数据库
// 2. 打开Performance Tab
// 3. 查看实时性能指标
// 4. 分析慢查询和索引使用情况

// 通过shell模拟分析
function analyzeMongoDBPerformance() {
    const analysis = {
        timestamp: new Date(),
        slowQueries: [],
        indexUsage: {},
        connectionStats: {}
    };
    
    // 分析慢查询
    const slowQueries = db.system.profile.find({
        millis: { $gte: 1000 }
    }).sort({ millis: -1 }).limit(50);
    
    slowQueries.forEach(query => {
        analysis.slowQueries.push({
            operation: query.op,
            namespace: query.ns,
            duration: query.millis,
            query: JSON.stringify(query.query),
            timestamp: query.ts
        });
    });
    
    // 分析索引使用情况
    db.getSiblingDB("myapp").getCollectionInfos().forEach(collection => {
        if (collection.name !== "system.profile") {
            const stats = db[collection.name].stats();
            analysis.indexUsage[collection.name] = {
                size: stats.size,
                count: stats.count,
                avgObjSize: stats.avgObjSize,
                indexes: stats.nindexes
            };
        }
    });
    
    return analysis;
}

// 执行分析
const perfAnalysis = analyzeMongoDBPerformance();
printjson(perfAnalysis);
```

#### 自定义监控脚本
```python
#!/usr/bin/env python3
# mongodb_performance_analyzer.py

from pymongo import MongoClient
from datetime import datetime, timedelta
import json
from collections import defaultdict, Counter

class MongoDBPerformanceAnalyzer:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client.admin
        
    def get_slow_queries(self, hours_back=24, min_duration_ms=1000):
        """获取慢查询"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        slow_queries = self.db.system.profile.find({
            "ts": {"$gte": cutoff_time},
            "millis": {"$gte": min_duration_ms}
        }).sort("millis", -1)
        
        return list(slow_queries)
    
    def analyze_query_patterns(self, slow_queries):
        """分析查询模式"""
        patterns = defaultdict(lambda: {
            'count': 0,
            'total_duration': 0,
            'avg_duration': 0,
            'max_duration': 0,
            'sample_queries': []
        })
        
        for query in slow_queries:
            # 提取查询特征
            op_type = query.get('op', 'unknown')
            namespace = query.get('ns', 'unknown')
            duration = query.get('millis', 0)
            
            pattern_key = f"{op_type}:{namespace}"
            
            patterns[pattern_key]['count'] += 1
            patterns[pattern_key]['total_duration'] += duration
            patterns[pattern_key]['max_duration'] = max(
                patterns[pattern_key]['max_duration'], 
                duration
            )
            
            # 保存样本查询（最多3个）
            if len(patterns[pattern_key]['sample_queries']) < 3:
                patterns[pattern_key]['sample_queries'].append({
                    'query': str(query.get('query', ''))[:200],
                    'duration': duration,
                    'timestamp': query.get('ts')
                })
        
        # 计算平均持续时间
        for pattern in patterns.values():
            if pattern['count'] > 0:
                pattern['avg_duration'] = pattern['total_duration'] / pattern['count']
        
        return dict(patterns)
    
    def analyze_index_usage(self):
        """分析索引使用情况"""
        index_analysis = {}
        
        # 获取所有数据库
        databases = self.client.list_database_names()
        
        for db_name in databases:
            if db_name in ['admin', 'config', 'local']:
                continue
                
            db = self.client[db_name]
            index_analysis[db_name] = {}
            
            # 获取集合信息
            collections = db.list_collection_names()
            
            for collection_name in collections:
                try:
                    # 获取集合统计
                    stats = db.command("collStats", collection_name)
                    
                    # 获取索引信息
                    indexes = list(db[collection_name].list_indexes())
                    
                    index_analysis[db_name][collection_name] = {
                        'document_count': stats.get('count', 0),
                        'size_bytes': stats.get('size', 0),
                        'avg_obj_size': stats.get('avgObjSize', 0),
                        'index_count': len(indexes),
                        'indexes': [idx.get('name') for idx in indexes]
                    }
                except Exception as e:
                    print(f"Error analyzing {db_name}.{collection_name}: {e}")
        
        return index_analysis
    
    def identify_performance_bottlenecks(self, slow_queries):
        """识别性能瓶颈"""
        bottlenecks = []
        
        # 按操作类型分类
        op_counts = Counter(query.get('op', 'unknown') for query in slow_queries)
        
        for op_type, count in op_counts.most_common():
            if count > len(slow_queries) * 0.3:  # 超过30%的慢查询
                bottlenecks.append({
                    'type': 'OPERATION_TYPE_BOTTLENECK',
                    'operation': op_type,
                    'count': count,
                    'percentage': round(count / len(slow_queries) * 100, 2),
                    'severity': 'HIGH' if count > len(slow_queries) * 0.5 else 'MEDIUM'
                })
        
        # 识别长时间运行的查询
        long_running = [q for q in slow_queries if q.get('millis', 0) > 10000]  # 超过10秒
        if long_running:
            bottlenecks.append({
                'type': 'LONG_RUNNING_QUERIES',
                'count': len(long_running),
                'max_duration': max(q.get('millis', 0) for q in long_running),
                'severity': 'HIGH'
            })
        
        return bottlenecks
    
    def generate_optimization_recommendations(self, slow_queries, index_analysis):
        """生成优化建议"""
        recommendations = []
        
        # 基于查询分析的建议
        patterns = self.analyze_query_patterns(slow_queries)
        
        for pattern, stats in patterns.items():
            if stats['avg_duration'] > 5000:  # 平均超过5秒
                recommendations.append({
                    'category': 'QUERY_OPTIMIZATION',
                    'issue': f'慢查询模式: {pattern}',
                    'impact': f'平均执行时间 {stats["avg_duration"]:.0f}ms',
                    'recommendation': '分析查询条件，考虑添加适当索引'
                })
        
        # 基于索引分析的建议
        for db_name, collections in index_analysis.items():
            for collection_name, stats in collections.items():
                if stats['document_count'] > 100000 and stats['index_count'] < 3:
                    recommendations.append({
                        'category': 'INDEX_DESIGN',
                        'issue': f'{db_name}.{collection_name} 索引不足',
                        'impact': f'{stats["document_count"]} 文档仅有 {stats["index_count"]} 个索引',
                        'recommendation': '分析查询模式，添加必要的复合索引'
                    })
        
        return recommendations
    
    def export_comprehensive_report(self, output_file, hours_back=24):
        """导出综合性能报告"""
        slow_queries = self.get_slow_queries(hours_back)
        index_analysis = self.analyze_index_usage()
        bottlenecks = self.identify_performance_bottlenecks(slow_queries)
        recommendations = self.generate_optimization_recommendations(slow_queries, index_analysis)
        
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'analysis_period_hours': hours_back,
            'total_slow_queries': len(slow_queries),
            'query_patterns': self.analyze_query_patterns(slow_queries),
            'index_analysis': index_analysis,
            'performance_bottlenecks': bottlenecks,
            'optimization_recommendations': recommendations,
            'top_slow_queries': [
                {
                    'operation': q.get('op'),
                    'namespace': q.get('ns'),
                    'duration_ms': q.get('millis'),
                    'timestamp': q.get('ts').isoformat() if q.get('ts') else None,
                    'query_sample': str(q.get('query', ''))[:300]
                }
                for q in slow_queries[:20]  # Top 20慢查询
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        return report

# 使用示例
if __name__ == "__main__":
    analyzer = MongoDBPerformanceAnalyzer()
    report = analyzer.export_comprehensive_report(
        '/var/reports/mongodb_performance_report.json',
        hours_back=48
    )
    print(f"性能报告已生成，包含 {report['total_slow_queries']} 个慢查询")
```

---

## 🔍 性能优化策略

### 通用优化原则

#### 1. 索引优化策略
```sql
-- 索引使用分析
SELECT 
    table_name,
    index_name,
    seq_in_index,
    column_name,
    cardinality,
    100.0 * cardinality / table_rows as selectivity
FROM information_schema.statistics s
JOIN information_schema.tables t ON s.table_schema = t.table_schema AND s.table_name = t.table_name
WHERE s.table_schema = 'myapp'
AND t.table_type = 'BASE TABLE'
ORDER BY table_name, index_name, seq_in_index;

-- 索引效果评估
EXPLAIN FORMAT=JSON
SELECT u.username, o.order_date
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE u.status = 'active' 
AND o.total_amount > 1000;

-- 索引建议生成
SELECT 
    t.table_schema,
    t.table_name,
    ROUND((t.data_length + t.index_length) / 1024 / 1024, 2) AS total_size_mb,
    t.table_rows,
    COUNT(k.column_name) AS indexed_columns,
    GROUP_CONCAT(k.column_name ORDER BY k.seq_in_index) AS indexed_columns_list
FROM information_schema.tables t
LEFT JOIN information_schema.key_column_usage k 
    ON t.table_schema = k.table_schema 
    AND t.table_name = k.table_name
    AND k.constraint_name = 'PRIMARY'
WHERE t.table_schema = 'myapp'
GROUP BY t.table_schema, t.table_name
HAVING indexed_columns = 0  -- 无主键的表
ORDER BY total_size_mb DESC;
```

#### 2. 查询重构优化
```sql
-- 子查询优化为JOIN
-- 优化前
SELECT u.username 
FROM users u 
WHERE u.id IN (
    SELECT user_id FROM orders WHERE total_amount > 1000
);

-- 优化后
SELECT DISTINCT u.username
FROM users u 
JOIN orders o ON u.id = o.user_id 
WHERE o.total_amount > 1000;

-- EXISTS优化
-- 优化前
SELECT u.username 
FROM users u 
WHERE (
    SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id
) > 5;

-- 优化后
SELECT u.username
FROM users u 
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.user_id = u.id 
    LIMIT 5
);

-- LIMIT优化
-- 优化前
SELECT * FROM users ORDER BY created_at DESC;

-- 优化后
SELECT id, username, email, created_at 
FROM users 
ORDER BY created_at DESC 
LIMIT 100;
```

#### 3. 配置参数优化
```sql
-- MySQL配置优化
SET GLOBAL innodb_buffer_pool_size = 2147483648;  -- 2GB
SET GLOBAL query_cache_size = 134217728;          -- 128MB
SET GLOBAL tmp_table_size = 67108864;             -- 64MB
SET GLOBAL max_heap_table_size = 67108864;        -- 64MB
SET GLOBAL sort_buffer_size = 2097152;            -- 2MB
SET GLOBAL read_buffer_size = 1048576;            -- 1MB
SET GLOBAL join_buffer_size = 1048576;            -- 1MB

-- PostgreSQL配置优化
ALTER SYSTEM SET shared_buffers = '2GB';
ALTER SYSTEM SET effective_cache_size = '6GB';
ALTER SYSTEM SET work_mem = '64MB';
ALTER SYSTEM SET maintenance_work_mem = '512MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- 重新加载配置
SELECT pg_reload_conf();
```

---

## 📊 性能监控和告警

### 实时监控脚本

#### 综合性能监控
```bash
#!/bin/bash
# database_performance_monitor.sh

ALERT_EMAIL="dba@company.com"
LOG_DIR="/var/log/performance"
REPORT_DIR="/var/reports/performance"

# 创建目录
mkdir -p $LOG_DIR $REPORT_DIR

# MySQL性能监控
monitor_mysql_performance() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 慢查询数量
    local slow_queries=$(mysql -e "SHOW GLOBAL STATUS LIKE 'Slow_queries';" | awk 'NR==2 {print $2}')
    
    # 连接数
    local connections=$(mysql -e "SHOW STATUS LIKE 'Threads_connected';" | awk 'NR==2 {print $2}')
    local max_connections=$(mysql -e "SHOW VARIABLES LIKE 'max_connections';" | awk 'NR==2 {print $2}')
    
    # QPS和TPS
    local questions=$(mysql -e "SHOW GLOBAL STATUS LIKE 'Questions';" | awk 'NR==2 {print $2}')
    local commits=$(mysql -e "SHOW GLOBAL STATUS LIKE 'Com_commit';" | awk 'NR==2 {print $2}')
    
    echo "[$timestamp] MySQL - Slow Queries: $slow_queries, Connections: $connections/$max_connections, QPS: $questions, TPS: $commits" >> $LOG_DIR/mysql_performance.log
    
    # 告警检查
    if [ $slow_queries -gt 100 ] || [ $connections -gt $((max_connections * 80 / 100)) ]; then
        echo "MySQL Performance Alert - Slow Queries: $slow_queries, Connections: $connections/$max_connections" | \
        mail -s "MySQL Performance Alert" $ALERT_EMAIL
    fi
}

# PostgreSQL性能监控
monitor_postgresql_performance() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 活跃连接数
    local active_connections=$(psql -t -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';" 2>/dev/null || echo "0")
    
    # 慢查询统计
    local slow_queries=$(psql -t -c "
        SELECT count(*) FROM pg_stat_statements 
        WHERE mean_time > 1000;
    " 2>/dev/null || echo "0")
    
    # 缓冲区命中率
    local buffer_hit_ratio=$(psql -t -c "
        SELECT round(blks_hit::numeric / (blks_hit + blks_read + 1) * 100, 2) 
        FROM pg_stat_database 
        WHERE datname = current_database();
    " 2>/dev/null || echo "0")
    
    echo "[$timestamp] PostgreSQL - Active Connections: $active_connections, Slow Queries: $slow_queries, Buffer Hit Ratio: ${buffer_hit_ratio}%" >> $LOG_DIR/postgresql_performance.log
    
    # 告警检查
    if [ $active_connections -gt 50 ] || [ $(echo "$buffer_hit_ratio < 85" | bc) -eq 1 ]; then
        echo "PostgreSQL Performance Alert - Active Connections: $active_connections, Buffer Hit Ratio: ${buffer_hit_ratio}%" | \
        mail -s "PostgreSQL Performance Alert" $ALERT_EMAIL
    fi
}

# MongoDB性能监控
monitor_mongodb_performance() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 连接数
    local connections=$(mongo --quiet --eval "db.serverStatus().connections" 2>/dev/null | grep "current" | awk '{print $2}' | tr -d ',')
    
    # 操作计数
    local opcounters=$(mongo --quiet --eval "db.serverStatus().opcounters" 2>/dev/null)
    
    echo "[$timestamp] MongoDB - Connections: $connections" >> $LOG_DIR/mongodb_performance.log
    echo "$opcounters" >> $LOG_DIR/mongodb_performance.log
    
    # 告警检查
    if [ $connections -gt 1000 ]; then
        echo "MongoDB Connection Alert - Current Connections: $connections" | \
        mail -s "MongoDB Connection Alert" $ALERT_EMAIL
    fi
}

# 执行监控
while true; do
    monitor_mysql_performance
    monitor_postgresql_performance
    monitor_mongodb_performance
    
    # 每5分钟执行一次
    sleep 300
done
```

### 性能趋势分析
```sql
-- 创建性能监控表
CREATE TABLE performance_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    database_type ENUM('MYSQL', 'POSTGRESQL', 'MONGODB') NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    threshold_value DECIMAL(15,4),
    alert_triggered BOOLEAN DEFAULT FALSE
);

-- 性能趋势分析视图
CREATE VIEW performance_trends AS
SELECT 
    database_type,
    metric_name,
    DATE(timestamp) as metric_date,
    AVG(metric_value) as avg_value,
    MAX(metric_value) as max_value,
    MIN(metric_value) as min_value,
    COUNT(*) as sample_count
FROM performance_metrics
WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY database_type, metric_name, DATE(timestamp)
ORDER BY database_type, metric_name, metric_date;

-- 异常检测查询
SELECT 
    database_type,
    metric_name,
    timestamp,
    metric_value,
    threshold_value,
    ((metric_value - threshold_value) / threshold_value * 100) as deviation_percent
FROM performance_metrics
WHERE alert_triggered = TRUE
AND timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY timestamp DESC;
```

---

## 📋 性能优化检查清单

### 系统性优化流程

```markdown
# 数据库性能优化检查清单

## 1. 问题识别阶段
- [ ] 确认性能问题的具体表现
- [ ] 收集相关性能指标数据
- [ ] 确定问题的影响范围和严重程度
- [ ] 建立性能基线用于对比

## 2. 根因分析阶段
- [ ] 使用EXPLAIN分析执行计划
- [ ] 检查索引使用情况
- [ ] 分析查询模式和频率
- [ ] 评估系统资源配置
- [ ] 识别锁等待和阻塞情况

## 3. 优化方案制定
- [ ] 确定优化优先级
- [ ] 制定具体的优化措施
- [ ] 评估优化方案的风险
- [ ] 制定回滚计划
- [ ] 准备测试环境验证

## 4. 实施优化阶段
- [ ] 在测试环境验证优化效果
- [ ] 制定生产环境实施计划
- [ ] 选择合适的时间窗口
- [ ] 分步骤实施优化措施
- [ ] 实时监控实施过程

## 5. 效果验证阶段
- [ ] 对比优化前后的性能指标
- [ ] 验证业务功能正常性
- [ ] 监控系统稳定性和资源使用
- [ ] 收集用户反馈
- [ ] 评估ROI和优化收益

## 6. 持续改进阶段
- [ ] 建立常态化监控机制
- [ ] 定期性能评估和优化
- [ ] 完善性能优化文档
- [ ] 培训团队成员
- [ ] 建立性能优化知识库
```

---