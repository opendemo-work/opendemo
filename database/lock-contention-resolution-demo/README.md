# 🔒 数据库锁等待处理指南

> 企业级数据库锁机制分析和死锁处理方案，涵盖锁类型识别、等待链分析、死锁预防等完整的锁问题诊断和解决体系

## 📋 案例概述

本案例深入讲解数据库锁机制的工作原理和常见问题处理方法，通过系统性的锁分析工具和预防策略，帮助DBA有效解决锁等待和死锁问题，保障数据库系统的稳定运行。

### 🎯 学习目标

- 理解各种数据库锁机制的工作原理
- 掌握锁等待和死锁的诊断方法
- 学会使用专业工具分析锁问题
- 实施有效的锁优化和预防策略
- 建立锁监控和告警机制

### ⏱️ 学习时长

- **理论学习**: 3小时
- **实践操作**: 4小时
- **总计**: 7小时

---

## 🔧 锁机制基础理论

### 数据库锁类型分类

```
数据库锁类型
├── 按锁定对象分类
│   ├── 表级锁(Table Lock)
│   ├── 行级锁(Row Lock)
│   ├── 页级锁(Page Lock)
│   └── 数据库级锁(Database Lock)
├── 按锁定模式分类
│   ├── 共享锁(Shared Lock, S)
│   ├── 排他锁(Exclusive Lock, X)
│   ├── 意向共享锁(Intent Shared Lock, IS)
│   ├── 意向排他锁(Intent Exclusive Lock, IX)
│   └── 自增锁(Auto-Increment Lock)
├── 按锁定粒度分类
│   ├── 悲观锁(Pessimistic Lock)
│   └── 乐观锁(Optimistic Lock)
└── 按锁定时间分类
    ├── 短期锁(Short-term Lock)
    ├── 长期锁(Long-term Lock)
    └── 持久锁(Persistent Lock)
```

### 锁兼容性矩阵

```
锁兼容性表 (MySQL InnoDB)
┌─────────┬───┬───┬────┬────┬────┐
│         │ S │ X │ IS │ IX │ AI │
├─────────┼───┼───┼────┼────┼────┤
│    S    │ ✓ │ ✗ │ ✓  │ ✗  │ ✓  │
│    X    │ ✗ │ ✗ │ ✗  │ ✗  │ ✗  │
│   IS    │ ✓ │ ✗ │ ✓  │ ✓  │ ✓  │
│   IX    │ ✗ │ ✗ │ ✓  │ ✓  │ ✓  │
│   AI    │ ✓ │ ✗ │ ✓  │ ✓  │ ✗  │
└─────────┴───┴───┴────┴────┴────┘

✓ = 兼容  ✗ = 冲突
```

### 死锁形成条件

```
死锁四要素
├── 互斥条件: 资源不能被多个进程同时使用
├── 请求和保持条件: 进程已获得资源但又请求新资源
├── 不剥夺条件: 已获得的资源不能被强制释放
└── 环路等待条件: 存在进程资源循环等待链

死锁预防策略
├── 破坏互斥条件 (通常不可行)
├── 破坏请求和保持条件 (预先分配)
├── 破坏不剥夺条件 (超时抢占)
└── 破坏环路等待条件 (资源有序分配)
```

---

## 🐬 MySQL锁等待分析实践

### 1. 锁状态监控

#### 基础锁信息查询
```sql
-- 查看当前锁等待情况
SELECT 
    r.trx_id waiting_trx_id,
    r.trx_mysql_thread_id waiting_thread,
    r.trx_query waiting_query,
    b.trx_id blocking_trx_id,
    b.trx_mysql_thread_id blocking_thread,
    b.trx_query blocking_query
FROM information_schema.innodb_lock_waits w
INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;

-- 查看事务和锁详细信息
SELECT 
    trx_id,
    trx_state,
    trx_started,
    trx_requested_lock_id,
    trx_wait_started,
    TIME_TO_SEC(TIMEDIFF(NOW(), trx_wait_started)) as wait_time_seconds,
    trx_mysql_thread_id,
    trx_query
FROM information_schema.innodb_trx 
WHERE trx_state = 'LOCK WAIT';

-- 查看锁信息
SELECT 
    lock_id,
    lock_trx_id,
    lock_mode,
    lock_type,
    lock_table,
    lock_index,
    lock_space,
    lock_page,
    lock_rec,
    lock_data
FROM information_schema.innodb_locks;
```

#### 实时锁监控脚本
```bash
#!/bin/bash
# mysql_lock_monitor.sh

ALERT_EMAIL="dba@company.com"
LOG_FILE="/var/log/mysql/lock_monitor.log"
ALERT_THRESHOLD_SECONDS=30

# 监控锁等待
monitor_lock_waits() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 查询长时间等待的事务
    local long_waits=$(mysql -e "
        SELECT 
            trx_id,
            trx_mysql_thread_id,
            trx_query,
            TIME_TO_SEC(TIMEDIFF(NOW(), trx_wait_started)) as wait_time
        FROM information_schema.innodb_trx 
        WHERE trx_state = 'LOCK WAIT' 
        AND trx_wait_started < DATE_SUB(NOW(), INTERVAL $ALERT_THRESHOLD_SECONDS SECOND);
    " --silent --raw)
    
    if [ -n "$long_waits" ]; then
        echo "[$timestamp] Long lock waits detected:" >> $LOG_FILE
        echo "$long_waits" >> $LOG_FILE
        
        # 发送告警邮件
        echo "Long MySQL lock waits detected:
$long_waits" | mail -s "MySQL Lock Wait Alert" $ALERT_EMAIL
    fi
    
    # 记录当前锁状态
    local current_locks=$(mysql -e "
        SELECT COUNT(*) as lock_count 
        FROM information_schema.innodb_locks;
    " --silent --raw | tail -1)
    
    echo "[$timestamp] Current active locks: $current_locks" >> $LOG_FILE
}

# 分析锁等待链
analyze_lock_chain() {
    local lock_chain_info=$(mysql -e "
        SELECT 
            CONCAT('Blocked: Thread ', r.trx_mysql_thread_id, 
                   ' waiting for ', r.trx_query) as blocked_info,
            CONCAT('Blocking: Thread ', b.trx_mysql_thread_id, 
                   ' running ', b.trx_query) as blocking_info,
            TIME_TO_SEC(TIMEDIFF(NOW(), r.trx_wait_started)) as wait_duration
        FROM information_schema.innodb_lock_waits w
        INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
        INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id
        ORDER BY wait_duration DESC;
    " --silent --raw)
    
    if [ -n "$lock_chain_info" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Lock chain analysis:" >> $LOG_FILE
        echo "$lock_chain_info" >> $LOG_FILE
    fi
}

# 执行监控
monitor_lock_waits
analyze_lock_chain
```

### 2. 死锁诊断和处理

#### 死锁日志分析
```sql
-- 启用死锁日志记录
SET GLOBAL innodb_print_all_deadlocks = ON;

-- 查看最近的死锁信息
SHOW ENGINE INNODB STATUS;

-- 从错误日志中提取死锁信息
-- tail -f /var/log/mysql/error.log | grep -i deadlock

-- 死锁历史记录表
CREATE TABLE deadlock_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trx_id VARCHAR(20),
    trx_query TEXT,
    deadlock_info LONGTEXT,
    resolved BOOLEAN DEFAULT FALSE
);

-- 自动记录死锁的触发器
DELIMITER //
CREATE PROCEDURE log_deadlock_info()
BEGIN
    DECLARE deadlock_info LONGTEXT;
    
    -- 获取最新的死锁信息
    SELECT ENGINE_TRANSACTION_INFO INTO deadlock_info
    FROM information_schema.ENGINES 
    WHERE ENGINE = 'InnoDB';
    
    -- 记录到日志表
    INSERT INTO deadlock_log (deadlock_info) VALUES (deadlock_info);
END //
DELIMITER ;
```

#### 死锁分析工具
```python
#!/usr/bin/env python3
# mysql_deadlock_analyzer.py

import mysql.connector
import re
from datetime import datetime
from collections import defaultdict

class MySQLDeadlockAnalyzer:
    def __init__(self, connection_config):
        self.config = connection_config
        self.deadlocks = []
        
    def get_deadlock_info(self):
        """获取死锁信息"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            cursor.execute("SHOW ENGINE INNODB STATUS")
            result = cursor.fetchone()
            
            if result and result[2]:
                deadlock_info = result[2]
                self.parse_deadlock_info(deadlock_info)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
    
    def parse_deadlock_info(self, status_output):
        """解析死锁信息"""
        # 查找死锁部分
        deadlock_pattern = r"------------------------\nLATEST DETECTED DEADLOCK\n------------------------\n(.*?)------------\nTRANSACTIONS"
        deadlock_match = re.search(deadlock_pattern, status_output, re.DOTALL)
        
        if deadlock_match:
            deadlock_text = deadlock_match.group(1)
            deadlock_data = self.extract_deadlock_details(deadlock_text)
            self.deadlocks.append(deadlock_data)
    
    def extract_deadlock_details(self, deadlock_text):
        """提取死锁详细信息"""
        deadlock_info = {
            'timestamp': None,
            'transactions': [],
            'resource_conflicts': [],
            'resolution': None
        }
        
        # 提取时间戳
        timestamp_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        timestamp_match = re.search(timestamp_pattern, deadlock_text)
        if timestamp_match:
            deadlock_info['timestamp'] = timestamp_match.group(1)
        
        # 提取事务信息
        transaction_pattern = r"TRANSACTION (\w+), ACTIVE.*?\n(.*?)(?=TRANSACTION|\*\*\* \(1\) WAITING FOR)"
        transactions = re.findall(transaction_pattern, deadlock_text, re.DOTALL)
        
        for trx_id, trx_info in transactions:
            transaction_data = {
                'id': trx_id,
                'query': None,
                'holding_locks': [],
                'waiting_for': None
            }
            
            # 提取查询语句
            query_pattern = r"mysql tables in use.*?\n(.*?)\n"
            query_match = re.search(query_pattern, trx_info, re.DOTALL)
            if query_match:
                transaction_data['query'] = query_match.group(1).strip()
            
            # 提取持有的锁
            holding_pattern = r"(\w+) locks rec but not gap on .*?index (.+?) of table (.+?) trx id (\w+)"
            holding_matches = re.findall(holding_pattern, trx_info)
            transaction_data['holding_locks'] = holding_matches
            
            deadlock_info['transactions'].append(transaction_data)
        
        return deadlock_info
    
    def analyze_deadlock_patterns(self):
        """分析死锁模式"""
        pattern_stats = defaultdict(int)
        
        for deadlock in self.deadlocks:
            # 分析涉及的表
            tables_involved = set()
            for transaction in deadlock['transactions']:
                for lock_info in transaction['holding_locks']:
                    if len(lock_info) > 2:
                        tables_involved.add(lock_info[2])
            
            pattern_key = f"tables:{len(tables_involved)}_txns:{len(deadlock['transactions'])}"
            pattern_stats[pattern_key] += 1
        
        return dict(pattern_stats)
    
    def generate_prevention_recommendations(self):
        """生成预防建议"""
        recommendations = []
        
        pattern_stats = self.analyze_deadlock_patterns()
        
        # 基于模式的建议
        for pattern, count in pattern_stats.items():
            if count > 3:  # 同一模式出现多次
                recommendations.append({
                    'type': 'PATTERN_BASED',
                    'pattern': pattern,
                    'occurrences': count,
                    'recommendation': '分析该模式的查询顺序，统一访问顺序'
                })
        
        # 通用预防建议
        recommendations.extend([
            {
                'type': 'GENERAL',
                'pattern': 'all_patterns',
                'recommendation': '实施一致的资源访问顺序'
            },
            {
                'type': 'GENERAL',
                'pattern': 'all_patterns',
                'recommendation': '减少事务持有锁的时间'
            },
            {
                'type': 'GENERAL',
                'pattern': 'all_patterns',
                'recommendation': '使用较低的事务隔离级别'
            }
        ])
        
        return recommendations
    
    def export_analysis_report(self, filename):
        """导出分析报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_deadlocks_analyzed': len(self.deadlocks),
            'deadlock_patterns': self.analyze_deadlock_patterns(),
            'prevention_recommendations': self.generate_prevention_recommendations(),
            'recent_deadlocks': self.deadlocks[-10:] if self.deadlocks else []
        }
        
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

# 使用示例
if __name__ == "__main__":
    analyzer = MySQLDeadlockAnalyzer({
        'host': 'localhost',
        'user': 'root',
        'password: "${DB_PASSWORD}",
        'database': 'information_schema'
    })
    
    analyzer.get_deadlock_info()
    analyzer.export_analysis_report('/var/reports/mysql_deadlock_analysis.json')
```

### 3. 锁优化策略

#### 事务优化
```sql
-- 优化事务隔离级别
-- 查看当前隔离级别
SELECT @@transaction_isolation;

-- 设置合适的隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- 或者在应用层设置
-- SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- 事务超时设置
SET SESSION innodb_lock_wait_timeout = 50; -- 50秒超时
SET SESSION deadlock_detection = ON;

-- 批量操作优化
-- 避免大事务
START TRANSACTION;
    -- 分批处理，每批提交
    INSERT INTO large_table SELECT * FROM temp_table LIMIT 1000;
    COMMIT;
    
    START TRANSACTION;
    INSERT INTO large_table SELECT * FROM temp_table LIMIT 1000 OFFSET 1000;
    COMMIT;
-- 继续分批...

-- 索引优化减少锁竞争
-- 添加覆盖索引减少回表
CREATE INDEX idx_orders_covering ON orders(user_id, status, created_at, total_amount);

-- 优化查询减少锁范围
-- 避免全表扫描
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- 确保使用索引
```

#### 应用层锁优化
```python
# 应用层锁优化示例
import threading
import time
from contextlib import contextmanager

class DatabaseLockManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.lock_timeout = 30  # 30秒超时
        
    @contextmanager
    def acquire_lock(self, lock_name, timeout=None):
        """获取应用层锁"""
        timeout = timeout or self.lock_timeout
        lock_acquired = False
        
        try:
            # 尝试获取锁
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT GET_LOCK(%s, %s)", 
                (lock_name, timeout)
            )
            result = cursor.fetchone()[0]
            
            if result == 1:
                lock_acquired = True
                yield True
            else:
                yield False
                
        finally:
            # 释放锁
            if lock_acquired:
                cursor.execute("SELECT RELEASE_LOCK(%s)", (lock_name,))
            cursor.close()
    
    def optimize_transaction_order(self, operations):
        """优化事务操作顺序"""
        # 按资源ID排序，避免死锁
        sorted_operations = sorted(operations, key=lambda x: x['resource_id'])
        return sorted_operations

# 使用示例
def transfer_money(from_account, to_account, amount):
    lock_manager = DatabaseLockManager(get_db_connection())
    
    # 按账户ID排序获取锁
    accounts = sorted([from_account, to_account])
    
    with lock_manager.acquire_lock(f"account_{accounts[0]}"):
        with lock_manager.acquire_lock(f"account_{accounts[1]}"):
            # 执行转账操作
            execute_transfer(from_account, to_account, amount)

def batch_update_products(product_ids, updates):
    """批量更新产品，避免大事务"""
    lock_manager = DatabaseLockManager(get_db_connection())
    
    # 按ID排序
    sorted_ids = sorted(product_ids)
    
    # 分批处理
    batch_size = 100
    for i in range(0, len(sorted_ids), batch_size):
        batch_ids = sorted_ids[i:i + batch_size]
        
        with lock_manager.acquire_lock("batch_update_lock", timeout=60):
            # 执行批量更新
            update_products_batch(batch_ids, updates)
            time.sleep(0.1)  # 短暂延迟避免锁竞争
```

---

## 🐘 PostgreSQL锁等待分析实践

### 1. 锁监控和诊断

#### 锁状态查询
```sql
-- 查看当前锁信息
SELECT 
    l.locktype,
    l.database,
    l.relation::regclass as relation_name,
    l.page,
    l.tuple,
    l.virtualxid,
    l.transactionid,
    l.classid::regclass as class_name,
    l.objid,
    l.objsubid,
    l.virtualtransaction,
    l.pid,
    l.mode,
    l.granted,
    a.usename,
    a.application_name,
    a.client_addr,
    a.backend_start,
    a.state,
    a.query
FROM pg_locks l
LEFT JOIN pg_stat_activity a ON l.pid = a.pid
ORDER BY l.granted DESC, l.pid;

-- 查看阻塞和等待关系
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity 
    ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity 
    ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- 查看长时间运行的事务
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    backend_start,
    state_change,
    state,
    query
FROM pg_stat_activity 
WHERE state = 'active' 
AND backend_start < NOW() - INTERVAL '5 minutes'
ORDER BY backend_start;
```

#### 锁监控脚本
```bash
#!/bin/bash
# postgres_lock_monitor.sh

PG_CONN="dbname=myapp user=postgres"
ALERT_EMAIL="dba@company.com"
LOG_FILE="/var/log/postgresql/lock_monitor.log"
ALERT_THRESHOLD_MINUTES=5

# 监控长时间运行的事务
monitor_long_transactions() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    local long_transactions=$(psql $PG_CONN -t -c "
        SELECT 
            pid,
            usename,
            application_name,
            client_addr,
            EXTRACT(EPOCH FROM (NOW() - backend_start))/60 as duration_minutes,
            state,
            query
        FROM pg_stat_activity 
        WHERE state = 'active' 
        AND backend_start < NOW() - INTERVAL '${ALERT_THRESHOLD_MINUTES} minutes'
        ORDER BY backend_start;
    " 2>/dev/null)
    
    if [ -n "$long_transactions" ]; then
        echo "[$timestamp] Long running transactions detected:" >> $LOG_FILE
        echo "$long_transactions" >> $LOG_FILE
        
        echo "Long PostgreSQL transactions detected:
$long_transactions" | mail -s "PostgreSQL Long Transaction Alert" $ALERT_EMAIL
    fi
}

# 监控锁等待
monitor_lock_waits() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    local lock_waits=$(psql $PG_CONN -t -c "
        SELECT 
            blocked_locks.pid AS blocked_pid,
            blocked_activity.usename AS blocked_user,
            blocking_locks.pid AS blocking_pid,
            blocking_activity.usename AS blocking_user,
            EXTRACT(EPOCH FROM (NOW() - blocked_activity.state_change))/60 as wait_minutes,
            blocked_activity.query AS blocked_statement,
            blocking_activity.query AS blocking_statement
        FROM pg_catalog.pg_locks blocked_locks
        JOIN pg_catalog.pg_stat_activity blocked_activity 
            ON blocked_activity.pid = blocked_locks.pid
        JOIN pg_catalog.pg_locks blocking_locks 
            ON blocking_locks.locktype = blocked_locks.locktype
            AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
            AND blocking_locks.pid != blocked_locks.pid
        JOIN pg_catalog.pg_stat_activity blocking_activity 
            ON blocking_activity.pid = blocking_locks.pid
        WHERE NOT blocked_locks.granted
        AND blocked_activity.state_change < NOW() - INTERVAL '2 minutes'
        ORDER BY wait_minutes DESC;
    " 2>/dev/null)
    
    if [ -n "$lock_waits" ]; then
        echo "[$timestamp] Lock waits detected:" >> $LOG_FILE
        echo "$lock_waits" >> $LOG_FILE
        
        echo "PostgreSQL lock waits detected:
$lock_waits" | mail -s "PostgreSQL Lock Wait Alert" $ALERT_EMAIL
    fi
}

# 执行监控
monitor_long_transactions
monitor_lock_waits
```

### 2. 死锁处理机制

#### 死锁检测和处理
```sql
-- 启用死锁检测
ALTER SYSTEM SET deadlock_timeout = '1s';
SELECT pg_reload_conf();

-- 查看死锁相关信息
SELECT 
    datname,
    usename,
    application_name,
    client_addr,
    state,
    wait_event_type,
    wait_event,
    state_change,
    query
FROM pg_stat_activity 
WHERE wait_event_type = 'Lock';

-- 死锁日志分析
-- 在postgresql.conf中配置
-- log_lock_waits = on
-- log_statement = 'all'
-- log_min_duration_statement = 1000

-- 创建死锁监控视图
CREATE VIEW deadlock_analysis AS
SELECT 
    blocked.pid AS blocked_pid,
    blocked.usename AS blocked_user,
    blocked.application_name AS blocked_app,
    blocked.client_addr AS blocked_client,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.usename AS blocking_user,
    blocking.application_name AS blocking_app,
    blocking.client_addr AS blocking_client,
    blocking.query AS blocking_query,
    EXTRACT(EPOCH FROM (NOW() - blocked.state_change)) AS wait_seconds
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked 
    ON blocked.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking 
    ON blocking.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted
AND blocked.state = 'active';
```

#### 死锁预防策略
```sql
-- 应用层死锁预防
-- 1. 一致的访问顺序
CREATE OR REPLACE FUNCTION transfer_funds_consistent(
    from_account_id INTEGER,
    to_account_id INTEGER,
    amount NUMERIC
) RETURNS VOID AS $$
BEGIN
    -- 始终按ID顺序获取锁
    IF from_account_id < to_account_id THEN
        PERFORM pg_advisory_lock(from_account_id);
        PERFORM pg_advisory_lock(to_account_id);
    ELSE
        PERFORM pg_advisory_lock(to_account_id);
        PERFORM pg_advisory_lock(from_account_id);
    END IF;
    
    -- 执行转账
    UPDATE accounts SET balance = balance - amount WHERE id = from_account_id;
    UPDATE accounts SET balance = balance + amount WHERE id = to_account_id;
    
    -- 释放锁
    IF from_account_id < to_account_id THEN
        PERFORM pg_advisory_unlock(from_account_id);
        PERFORM pg_advisory_unlock(to_account_id);
    ELSE
        PERFORM pg_advisory_unlock(to_account_id);
        PERFORM pg_advisory_unlock(from_account_id);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 2. 使用较低的隔离级别
BEGIN ISOLATION LEVEL READ COMMITTED;
    -- 执行操作
    UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 123;
    UPDATE orders SET status = 'processed' WHERE id = 456;
COMMIT;

-- 3. 减少事务持有时间
-- 避免在事务中执行长时间操作
BEGIN;
    -- 快速执行数据库操作
    UPDATE user_sessions SET last_activity = NOW() WHERE user_id = 789;
    -- 外部API调用应该在事务外进行
COMMIT;

-- 4. 批量操作优化
CREATE OR REPLACE FUNCTION batch_update_products(
    product_updates JSONB
) RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER := 0;
    product_record JSONB;
BEGIN
    -- 按ID排序处理
    FOR product_record IN 
        SELECT jsonb_array_elements(product_updates) 
        ORDER BY (jsonb_array_elements->>'id')::INTEGER
    LOOP
        UPDATE products 
        SET price = (product_record->>'price')::NUMERIC,
            stock = (product_record->>'stock')::INTEGER
        WHERE id = (product_record->>'id')::INTEGER;
        
        updated_count := updated_count + 1;
        
        -- 小批量提交避免大事务
        IF updated_count % 100 = 0 THEN
            COMMIT;
            BEGIN;
        END IF;
    END LOOP;
    
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;
```

### 3. 锁性能优化

#### 索引优化减少锁竞争
```sql
-- 分析锁等待的查询
EXPLAIN (ANALYZE, BUFFERS)
SELECT p.name, p.price, c.name as category
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.price > 100
ORDER BY p.name;

-- 优化索引减少锁范围
-- 创建覆盖索引
CREATE INDEX idx_products_price_covering 
ON products(price) INCLUDE (name, category_id);

-- 创建复合索引优化JOIN
CREATE INDEX idx_products_category_price 
ON products(category_id, price);

-- 分析索引使用情况
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    100.0 * idx_tup_fetch / nullif(idx_tup_read, 0) as fetch_ratio
FROM pg_stat_user_indexes 
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

#### 配置优化
```sql
-- 锁相关配置优化
ALTER SYSTEM SET deadlock_timeout = '1s';           -- 死锁检测超时
ALTER SYSTEM SET lock_timeout = '30s';              -- 锁等待超时
ALTER SYSTEM SET max_locks_per_transaction = 128;   -- 每事务最大锁数
ALTER SYSTEM SET max_pred_locks_per_transaction = 128; -- 每事务预测锁数

-- 内存配置优化
ALTER SYSTEM SET shared_buffers = '2GB';            -- 共享缓冲区
ALTER SYSTEM SET effective_cache_size = '6GB';      -- 有效缓存大小
ALTER SYSTEM SET work_mem = '64MB';                 -- 工作内存
ALTER SYSTEM SET maintenance_work_mem = '512MB';    -- 维护工作内存

-- 重新加载配置
SELECT pg_reload_conf();

-- 监控锁性能
SELECT 
    datname,
    usename,
    wait_event_type,
    wait_event,
    state,
    query
FROM pg_stat_activity 
WHERE wait_event_type IS NOT NULL;
```

---

## 🍃 MongoDB锁等待分析实践

### 1. MongoDB锁机制监控

#### 锁状态查询
```javascript
// MongoDB锁监控
use admin

// 查看当前操作和锁状态
db.currentOp({
    "$or": [
        { "lockType": { "$exists": true } },
        { "waitingForLock": true }
    ]
})

// 查看数据库级别的锁信息
db.serverStatus().locks

// 查看全局锁统计
db.serverStatus().globalLock

// 分析特定集合的锁情况
function analyzeCollectionLocks(databaseName, collectionName) {
    const db = db.getSiblingDB(databaseName);
    const collection = db[collectionName];
    
    // 获取集合统计信息
    const stats = collection.stats();
    
    print(`=== ${databaseName}.${collectionName} Lock Analysis ===`);
    print(`Document Count: ${stats.count}`);
    print(`Average Object Size: ${stats.avgObjSize} bytes`);
    print(`Storage Size: ${stats.storageSize} bytes`);
    
    // 查看正在进行的操作
    const currentOps = db.currentOp({
        "ns": `${databaseName}.${collectionName}`,
        "waitingForLock": true
    });
    
    if (currentOps.inprog.length > 0) {
        print("\nOperations waiting for locks:");
        currentOps.inprog.forEach(op => {
            print(`- PID: ${op.connectionId}`);
            print(`  Operation: ${op.op}`);
            print(`  Query: ${JSON.stringify(op.query)}`);
            print(`  Waiting Time: ${op.waitingForLock ? 'Yes' : 'No'}`);
            print(`  Lock Type: ${op.lockType || 'None'}`);
        });
    }
    
    return stats;
}

// 使用示例
analyzeCollectionLocks("myapp", "users");
```

#### 实时锁监控脚本
```python
#!/usr/bin/env python3
# mongodb_lock_monitor.py

from pymongo import MongoClient
from datetime import datetime, timedelta
import json

class MongoDBLockMonitor:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client.admin
        
    def get_current_operations(self):
        """获取当前操作"""
        try:
            current_ops = self.db.current_op({
                "$or": [
                    {"lockType": {"$exists": True}},
                    {"waitingForLock": True},
                    {"secs_running": {"$gt": 30}}  # 运行超过30秒的操作
                ]
            })
            return current_ops.get('inprog', [])
        except Exception as e:
            print(f"Error getting current operations: {e}")
            return []
    
    def analyze_lock_contention(self):
        """分析锁争用情况"""
        current_ops = self.get_current_operations()
        
        lock_analysis = {
            'timestamp': datetime.utcnow(),
            'total_operations': len(current_ops),
            'waiting_for_lock': 0,
            'long_running_ops': 0,
            'lock_types': {},
            'problematic_operations': []
        }
        
        for op in current_ops:
            # 统计等待锁的操作
            if op.get('waitingForLock'):
                lock_analysis['waiting_for_lock'] += 1
                lock_analysis['problematic_operations'].append({
                    'op': op.get('op'),
                    'ns': op.get('ns'),
                    'secs_running': op.get('secs_running', 0),
                    'desc': op.get('desc', ''),
                    'client': op.get('client', '')
                })
            
            # 统计长时间运行的操作
            if op.get('secs_running', 0) > 60:
                lock_analysis['long_running_ops'] += 1
            
            # 统计锁类型
            lock_type = op.get('lockType', 'unknown')
            lock_analysis['lock_types'][lock_type] = lock_analysis['lock_types'].get(lock_type, 0) + 1
        
        return lock_analysis
    
    def get_database_lock_info(self):
        """获取数据库锁信息"""
        try:
            server_status = self.db.command("serverStatus")
            return {
                'globalLock': server_status.get('globalLock', {}),
                'locks': server_status.get('locks', {}),
                'wiredTiger': server_status.get('wiredTiger', {}).get('concurrentTransactions', {})
            }
        except Exception as e:
            print(f"Error getting lock info: {e}")
            return {}
    
    def identify_lock_problems(self, lock_analysis):
        """识别锁问题"""
        problems = []
        
        # 高等待锁比例
        if lock_analysis['total_operations'] > 0:
            wait_ratio = lock_analysis['waiting_for_lock'] / lock_analysis['total_operations']
            if wait_ratio > 0.3:
                problems.append({
                    'type': 'HIGH_LOCK_WAIT_RATIO',
                    'severity': 'HIGH',
                    'description': f'锁等待比例过高: {wait_ratio:.2%}',
                    'current_value': lock_analysis['waiting_for_lock'],
                    'total_operations': lock_analysis['total_operations']
                })
        
        # 大量长时间运行操作
        if lock_analysis['long_running_ops'] > 10:
            problems.append({
                'type': 'MANY_LONG_RUNNING_OPS',
                'severity': 'HIGH',
                'description': f'存在{lock_analysis["long_running_ops"]}个长时间运行的操作',
                'threshold': 10
            })
        
        return problems
    
    def generate_recommendations(self, lock_analysis, lock_info):
        """生成优化建议"""
        recommendations = []
        
        problems = self.identify_lock_problems(lock_analysis)
        
        for problem in problems:
            if problem['type'] == 'HIGH_LOCK_WAIT_RATIO':
                recommendations.append({
                    'category': 'IMMEDIATE_ACTION',
                    'issue': problem['description'],
                    'recommendation': '检查并优化引起锁等待的查询，考虑添加索引或调整查询顺序'
                })
            elif problem['type'] == 'MANY_LONG_RUNNING_OPS':
                recommendations.append({
                    'category': 'IMMEDIATE_ACTION',
                    'issue': problem['description'],
                    'recommendation': '终止长时间运行的操作，分析其查询计划并优化'
                })
        
        # 基于锁信息的建议
        wired_tiger = lock_info.get('wiredTiger', {})
        if wired_tiger:
            read_out = wired_tiger.get('read', {}).get('out', 0)
            write_out = wired_tiger.get('write', {}).get('out', 0)
            
            if read_out > 50 or write_out > 50:
                recommendations.append({
                    'category': 'CONFIGURATION',
                    'issue': f'并发事务数较高 - 读:{read_out}, 写:{write_out}',
                    'recommendation': '考虑调整WiredTiger并发设置或优化应用程序'
                })
        
        return recommendations
    
    def export_monitoring_report(self, filename):
        """导出监控报告"""
        lock_analysis = self.analyze_lock_contention()
        lock_info = self.get_database_lock_info()
        recommendations = self.generate_recommendations(lock_analysis, lock_info)
        
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'lock_analysis': lock_analysis,
            'lock_info': lock_info,
            'identified_problems': self.identify_lock_problems(lock_analysis),
            'optimization_recommendations': recommendations
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        return report

# 使用示例
if __name__ == "__main__":
    monitor = MongoDBLockMonitor()
    report = monitor.export_monitoring_report('/var/reports/mongodb_lock_report.json')
    print(f"锁监控报告已生成，发现问题: {len(report['identified_problems'])}个")
```

### 2. 锁优化和预防

#### 查询优化减少锁竞争
```javascript
// MongoDB查询优化示例

// 1. 添加适当索引减少锁范围
db.products.createIndex({ "category": 1, "price": 1 })
db.orders.createIndex({ "userId": 1, "createdAt": -1 })

// 2. 使用投影减少数据传输
// 优化前
db.users.find({ "status": "active" })

// 优化后
db.users.find(
    { "status": "active" }, 
    { "name": 1, "email": 1, "lastLogin": 1, "_id": 0 }
)

// 3. 分批处理大数据集
function batchProcessUsers(batchSize = 1000) {
    let skip = 0;
    let processed = 0;
    
    while (true) {
        const users = db.users.find({ "status": "pending" })
                              .skip(skip)
                              .limit(batchSize)
                              .toArray();
        
        if (users.length === 0) break;
        
        // 批量处理
        users.forEach(user => {
            // 处理单个用户
            db.users.updateOne(
                { "_id": user._id },
                { "$set": { "status": "processed" } }
            );
        });
        
        processed += users.length;
        skip += batchSize;
        
        // 短暂延迟避免锁竞争
        sleep(100);
    }
    
    return processed;
}

// 4. 使用findAndModify原子操作
function atomicInventoryUpdate(productId, quantityChange) {
    return db.inventory.findAndModify({
        query: { 
            "_id": productId, 
            "quantity": { "$gte": quantityChange > 0 ? 0 : Math.abs(quantityChange) }
        },
        update: { "$inc": { "quantity": quantityChange } },
        new: true
    });
}

// 5. 优化聚合管道减少中间结果
db.orders.aggregate([
    { $match: { "status": "completed", "createdAt": { "$gte": new Date("2024-01-01") } } },
    { $project: { 
        "userId": 1, 
        "totalAmount": 1, 
        "month": { "$month": "$createdAt" } 
    }},
    { $group: { 
        "_id": { "userId": "$userId", "month": "$month" },
        "totalSpent": { "$sum": "$totalAmount" },
        "orderCount": { "$sum": 1 }
    }},
    { $sort: { "totalSpent": -1 } },
    { $limit: 100 }
]);
```

#### 应用层锁管理
```python
# MongoDB应用层锁管理
from pymongo import MongoClient, ReadPreference
import threading
import time
from contextlib import contextmanager

class MongoLockManager:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.myapp
        self.lock_collection = self.db.locks
        self.default_timeout = 30  # 30秒超时
        
    @contextmanager
    def distributed_lock(self, lock_name, timeout=None):
        """分布式锁实现"""
        timeout = timeout or self.default_timeout
        lock_doc = {
            "_id": lock_name,
            "locked_at": time.time(),
            "expires_at": time.time() + timeout,
            "owner": f"{threading.current_thread().ident}"
        }
        
        try:
            # 尝试获取锁
            result = self.lock_collection.replace_one(
                {"_id": lock_name, "expires_at": {"$lt": time.time()}},
                lock_doc,
                upsert=True
            )
            
            if result.modified_count > 0 or result.upserted_id:
                yield True
            else:
                yield False
                
        finally:
            # 释放锁
            self.lock_collection.delete_one({
                "_id": lock_name,
                "owner": f"{threading.current_thread().ident}"
            })
    
    def optimistic_lock_update(self, collection_name, doc_id, updates, version_field="version"):
        """乐观锁更新"""
        collection = self.db[collection_name]
        
        # 获取当前文档
        current_doc = collection.find_one({"_id": doc_id})
        if not current_doc:
            raise ValueError("Document not found")
        
        current_version = current_doc.get(version_field, 0)
        
        # 添加版本号到更新条件
        updates["$inc"] = {version_field: 1}
        
        result = collection.update_one(
            {"_id": doc_id, version_field: current_version},
            updates
        )
        
        if result.modified_count == 0:
            raise Exception("Concurrent modification detected")
        
        return result
    
    def batch_operation_with_retry(self, operation_func, max_retries=3):
        """带重试的批量操作"""
        for attempt in range(max_retries):
            try:
                return operation_func()
            except Exception as e:
                if "E11000 duplicate key" in str(e) or "WriteConflict" in str(e):
                    if attempt < max_retries - 1:
                        time.sleep(0.1 * (2 ** attempt))  # 指数退避
                        continue
                raise e

# 使用示例
def update_user_profile(user_id, profile_updates):
    lock_manager = MongoLockManager("mongodb://localhost:27017/")
    
    def update_operation():
        with lock_manager.distributed_lock(f"user_profile_{user_id}"):
            # 使用乐观锁更新
            return lock_manager.optimistic_lock_update(
                "users",
                user_id,
                {"$set": profile_updates}
            )
    
    return lock_manager.batch_operation_with_retry(update_operation)

# 批量处理示例
def process_batch_orders(order_ids, status_update):
    lock_manager = MongoLockManager("mongodb://localhost:27017/")
    
    # 按ID排序避免死锁
    sorted_ids = sorted(order_ids)
    
    def batch_operation():
        # 分批处理
        batch_size = 100
        for i in range(0, len(sorted_ids), batch_size):
            batch_ids = sorted_ids[i:i + batch_size]
            
            with lock_manager.distributed_lock("batch_order_processing"):
                # 批量更新
                result = lock_manager.db.orders.update_many(
                    {"_id": {"$in": batch_ids}},
                    {"$set": {"status": status_update}}
                )
                time.sleep(0.01)  # 短暂延迟
                
        return len(sorted_ids)
    
    return lock_manager.batch_operation_with_retry(batch_operation)
```

---

## 🔧 锁问题处理最佳实践

### 应急处理流程

#### 1. 快速诊断步骤
```sql
-- MySQL紧急诊断
-- 1. 查看当前锁等待
SELECT * FROM information_schema.innodb_lock_waits;

-- 2. 查看阻塞的事务
SELECT 
    blocking_trx.trx_mysql_thread_id as blocking_thread,
    blocking_trx.trx_query as blocking_query,
    waiting_trx.trx_mysql_thread_id as waiting_thread,
    waiting_trx.trx_query as waiting_query
FROM information_schema.innodb_lock_waits w
JOIN information_schema.innodb_trx blocking_trx 
    ON blocking_trx.trx_id = w.blocking_trx_id
JOIN information_schema.innodb_trx waiting_trx 
    ON waiting_trx.trx_id = w.requesting_trx_id;

-- 3. 终止问题事务（谨慎使用）
KILL 12345; -- 替换为实际的线程ID

-- PostgreSQL紧急诊断
-- 1. 查看阻塞关系
SELECT 
    blocked.pid as blocked_pid,
    blocked.query as blocked_query,
    blocking.pid as blocking_pid,
    blocking.query as blocking_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked ON blocked.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking ON blocking.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- 2. 终止阻塞的进程
SELECT pg_terminate_backend(blocking_pid) FROM (
    SELECT blocking.pid as blocking_pid
    FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_stat_activity blocked ON blocked.pid = blocked_locks.pid
    JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.pid != blocked_locks.pid
    JOIN pg_catalog.pg_stat_activity blocking ON blocking.pid = blocking_locks.pid
    WHERE NOT blocked_locks.granted
) blockers;
```

#### 2. 预防措施实施
```markdown
# 锁问题预防检查清单

## 应用层预防
- [ ] 实施一致的资源访问顺序
- [ ] 使用合适的事务隔离级别
- [ ] 减少事务持有锁的时间
- [ ] 避免在事务中执行长时间操作
- [ ] 实施合理的重试机制

## 数据库层优化
- [ ] 添加必要的索引减少锁范围
- [ ] 优化查询执行计划
- [ ] 配置合适的锁超时时间
- [ ] 启用死锁检测和日志记录
- [ ] 定期分析锁等待模式

## 监控告警
- [ ] 建立锁等待监控机制
- [ ] 设置合理的告警阈值
- [ ] 实施自动化的锁问题检测
- [ ] 建立定期的锁性能评估
- [ ] 完善锁问题处理流程
```

---

## 📊 锁性能评估报告模板

```markdown
# 数据库锁性能评估报告

## 评估周期
2024年1月锁性能评估

## 锁性能指标

### MySQL锁指标
| 指标 | 当前值 | 目标值 | 状态 |
|------|--------|--------|------|
| 平均锁等待时间 | 2.3秒 | < 1秒 | ⚠️ 需改进 |
| 死锁发生频率 | 3次/天 | < 1次/周 | ⚠️ 需改进 |
| 最大并发锁数 | 156个 | < 100个 | ⚠️ 需优化 |
| 锁超时次数 | 12次/小时 | < 5次/小时 | ⚠️ 需改进 |

### PostgreSQL锁指标
| 指标 | 当前值 | 目标值 | 状态 |
|------|--------|--------|------|
| 平均事务等待时间 | 1.8秒 | < 1秒 | ⚠️ 需改进 |
| 阻塞事务数量 | 8个 | < 3个 | ⚠️ 需改进 |
| 死锁检测次数 | 2次/天 | < 1次/周 | ✓ 正常 |
| 锁升级频率 | 15次/小时 | < 10次/小时 | ⚠️ 需优化 |

## 主要问题分析

### 1. 锁等待热点表
- **users表**: 平均等待时间3.2秒，主要由于用户状态更新冲突
- **orders表**: 平均等待时间2.8秒，主要由于订单状态变更
- **inventory表**: 平均等待时间4.1秒，主要由于库存扣减操作

### 2. 死锁模式分析
- **模式1**: 用户资料更新 ↔ 订单创建 (占40%)
- **模式2**: 库存扣减 ↔ 订单取消 (占35%)
- **模式3**: 批量导入 ↔ 实时查询 (占25%)

## 优化建议

### 立即执行
1. 为users表添加status字段索引
2. 优化订单状态变更的事务顺序
3. 实施库存操作的队列机制

### 短期计划
1. 重构高并发业务逻辑
2. 实施应用层分布式锁
3. 优化批量操作的执行时机

### 长期规划
1. 考虑读写分离架构
2. 实施微服务拆分减少数据竞争
3. 建立智能锁管理平台

## ROI分析
- **优化投入**: 20人天开发和测试工作
- **性能提升**: 预期锁等待时间降低60%
- **业务收益**: 系统吞吐量提升40%
- **投资回报率**: 约300%
```

---