# PostgreSQL数据库性能分析与故障排查实战演示

## 🎯 学习目标

通过本案例你将掌握PostgreSQL数据库的专业排查和优化技能：

- 数据库性能监控和瓶颈分析
- 慢查询诊断和执行计划优化
- 连接池管理和服务进程分析
- 锁等待和死锁检测
- WAL日志和复制延迟分析
- 内存和IO性能调优
- 数据库备份恢复和灾难恢复

## 🛠️ 环境准备

### 系统要求
- PostgreSQL 10+ 服务
- Linux/Unix系统环境
- 数据库超级用户权限
- 至少2GB内存用于分析工具

### 依赖安装
```bash
# 安装PostgreSQL客户端工具
sudo yum install -y postgresql postgresql-contrib pgbadger
sudo apt-get install -y postgresql-client postgresql-contrib pgbadger

# 安装性能分析工具
sudo yum install -y sysstat iotop
sudo apt-get install -y sysstat iotop

# 安装监控工具
pip install pgcli  # 增强版PostgreSQL客户端
pip install psycopg2-binary

# 验证安装
psql --version
pgbadger --version
```

## 📁 项目结构

```
postgresql-troubleshooting-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 排查脚本
│   ├── postgres_performance_analyzer.sh # 性能分析脚本
│   ├── slow_query_analyzer.sh          # 慢查询分析脚本
│   ├── connection_monitor.sh           # 连接监控脚本
│   ├── replication_lag_checker.sh      # 复制延迟检查脚本
│   ├── deadlock_detector.sh            # 死锁检测脚本
│   └── backup_restore_validator.sh     # 备份恢复验证脚本
├── configs/                           # 配置文件
│   ├── postgres_performance.conf       # 性能优化配置
│   ├── logging.conf                    # 日志配置
│   ├── monitoring_roles.sql            # 监控角色配置
│   └── alert_rules.conf                # 告警规则配置
├── examples/                          # 实际案例
│   ├── slow_query_logs/                # 慢查询日志样本
│   ├── explain_plans/                  # 执行计划样本
│   ├── replication_issues/             # 复制问题案例
│   └── troubleshooting_playbooks/      # 故障排查手册
└── docs/                              # 详细文档
    ├── postgresql_performance_tuning.md # PostgreSQL性能调优指南
    ├── query_optimization_guide.md     # 查询优化手册
    ├── replication_troubleshooting.md  # 复制故障排除
    └── backup_recovery_best_practices.md # 备份恢复最佳实践
```

## 🔧 核心排查技术详解

### 1. 性能监控和分析

```sql
-- 基础性能监控查询
-- 查看当前活动会话
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    backend_start,
    state,
    state_change,
    query
FROM pg_stat_activity 
WHERE state != 'idle' 
ORDER BY state_change;

-- 查看数据库统计信息
SELECT 
    datname,
    numbackends as connections,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted
FROM pg_stat_database 
WHERE datname NOT IN ('template0', 'template1');

-- 查看表级统计
SELECT 
    schemaname,
    relname,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_tup_hot_upd,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables 
ORDER BY (n_tup_ins + n_tup_upd + n_tup_del) DESC 
LIMIT 10;

-- 查看索引使用统计
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan > 0 
ORDER BY idx_scan DESC 
LIMIT 10;

-- 查看缓存命中率
SELECT 
    datname,
    round(blks_hit::float/(blks_hit+blks_read)*100, 2) as cache_hit_ratio
FROM pg_stat_database 
WHERE blks_read > 0;
```

```bash
#!/bin/bash
# PostgreSQL性能分析脚本

PG_HOST=${1:-"localhost"}
PG_PORT=${2:-"5432"}
PG_USER=${3:-"postgres"}
PG_DB=${4:-"postgres"}

echo "=== PostgreSQL性能分析报告 ==="
echo "主机: $PG_HOST:$PG_PORT"
echo "数据库: $PG_DB"
echo "用户: $PG_USER"
echo "时间: $(date)"
echo ""

# 1. 连接和会话状态
echo "1. 连接和会话状态:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    count(*) as total_connections,
    count(*) FILTER (WHERE state = 'active') as active_sessions,
    count(*) FILTER (WHERE state = 'idle') as idle_sessions,
    count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction
FROM pg_stat_activity;
" 2>/dev/null

# 2. 数据库性能统计
echo -e "\n2. 数据库性能统计:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    datname,
    numbackends as connections,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    round(blks_hit::float/(blks_hit+blks_read)*100, 2) as cache_hit_ratio
FROM pg_stat_database 
WHERE datname NOT IN ('template0', 'template1');
" 2>/dev/null

# 3. 慢查询统计
echo -e "\n3. 慢查询统计:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent,
    regexp_replace(query, '[\s]+', ' ', 'g') as query_sample
FROM pg_stat_statements 
WHERE mean_time > 1000  -- 平均执行时间超过1秒
ORDER BY mean_time DESC 
LIMIT 10;
" 2>/dev/null

# 4. 表膨胀检查
echo -e "\n4. 表和索引膨胀检查:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    n_tup_ins + n_tup_upd + n_tup_del as total_ops,
    n_dead_tup as dead_tuples,
    round(n_dead_tup::float / (n_live_tup + 1) * 100, 2) as dead_tuple_ratio
FROM pg_stat_user_tables 
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC 
LIMIT 10;
" 2>/dev/null

# 5. 锁等待检查
echo -e "\n5. 锁等待情况:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
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
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
" 2>/dev/null

# 6. 生成性能报告
REPORT_FILE="/tmp/postgres_performance_$(date +%Y%m%d_%H%M%S).txt"
cat > $REPORT_FILE << EOF
PostgreSQL性能分析报告
======================
主机: $PG_HOST:$PG_PORT
数据库: $PG_DB
时间: $(date)

主要性能指标:
$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    datname,
    numbackends as connections,
    xact_commit,
    xact_rollback,
    round(blks_hit::float/(blks_hit+blks_read)*100, 2) as cache_hit_ratio
FROM pg_stat_database 
WHERE datname NOT IN ('template0', 'template1');
" 2>/dev/null)

建议优化方向:
1. 根据连接数调整max_connections参数
2. 优化高成本的SQL查询
3. 定期清理表膨胀(VACUUM)
4. 检查索引使用效率
5. 调整共享缓冲区大小
EOF

echo -e "\n详细报告已保存: $REPORT_FILE"
```

### 2. 慢查询分析和优化

```sql
-- 启用扩展和慢查询日志
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- 配置慢查询日志
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- 1秒
ALTER SYSTEM SET log_statement = 'none';
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';
SELECT pg_reload_conf();

-- 分析慢查询
SELECT 
    userid,
    dbid,
    queryid,
    calls,
    total_time,
    min_time,
    max_time,
    mean_time,
    stddev_time,
    rows,
    shared_blks_hit,
    shared_blks_read,
    shared_blks_dirtied,
    shared_blks_written,
    local_blks_hit,
    local_blks_read,
    local_blks_dirtied,
    local_blks_written,
    temp_blks_read,
    temp_blks_written,
    blk_read_time,
    blk_write_time,
    regexp_replace(query, '[\s]+', ' ', 'g') as normalized_query
FROM pg_stat_statements 
WHERE mean_time > 1000
ORDER BY mean_time DESC 
LIMIT 20;

-- 查看执行计划
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT * FROM users WHERE email = 'user@example.com';

-- 查看未使用索引的查询
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    CASE 
        WHEN seq_scan > 0 THEN seq_tup_read::float / seq_scan 
        ELSE 0 
    END as avg_seq_tup_read
FROM pg_stat_user_tables 
WHERE seq_scan > 0 AND idx_scan = 0
ORDER BY seq_tup_read DESC;
```

### 3. 连接池和服务进程分析

```sql
-- 查看所有后台进程
SELECT 
    pid,
    backend_type,
    application_name,
    client_addr,
    client_hostname,
    backend_start,
    state,
    wait_event_type,
    wait_event,
    query
FROM pg_stat_activity 
ORDER BY backend_start;

-- 查看WAL发送和接收进程
SELECT 
    pid,
    state,
    sender_sent_location,
    receiver_received_location,
    receiver_last_transaction,
    flush_location,
    replay_location,
    sync_priority,
    sync_state
FROM pg_stat_replication;

-- 查看后台写进程状态
SELECT 
    pg_backend_pid() as current_pid,
    pg_is_in_recovery() as is_standby,
    pg_current_wal_lsn() as current_lsn,
    pg_last_wal_receive_lsn() as received_lsn,
    pg_last_wal_replay_lsn() as replayed_lsn;

-- 连接池配置检查
SHOW max_connections;
SHOW superuser_reserved_connections;
SHOW shared_buffers;
SHOW work_mem;
SHOW maintenance_work_mem;
```

```bash
#!/bin/bash
# PostgreSQL连接监控脚本

PG_HOST=${1:-"localhost"}
PG_PORT=${2:-"5432"}
PG_USER=${3:-"postgres"}
PG_DB=${4:-"postgres"}

echo "=== PostgreSQL连接监控 ==="
echo "主机: $PG_HOST:$PG_PORT"
echo "数据库: $PG_DB"
echo "时间: $(date)"
echo ""

# 1. 连接池状态
echo "1. 连接池当前状态:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    count(*) as total_connections,
    count(*) FILTER (WHERE state = 'active') as active_sessions,
    count(*) FILTER (WHERE state = 'idle') as idle_sessions,
    count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction,
    max_connections,
    round(count(*)::float / max_connections * 100, 2) as usage_percentage
FROM pg_stat_activity,
     (SELECT setting::int as max_connections FROM pg_settings WHERE name = 'max_connections') max_conn;
" 2>/dev/null

# 2. 活跃会话详情
echo -e "\n2. 活跃会话详情:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    backend_start,
    state,
    state_change,
    wait_event_type,
    wait_event,
    substring(query, 1, 100) as query_preview
FROM pg_stat_activity 
WHERE state = 'active' 
    AND backend_type = 'client backend'
ORDER BY state_change;
" 2>/dev/null

# 3. 连接来源分析
echo -e "\n3. 连接来源统计:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    client_addr,
    count(*) as connection_count,
    count(*) FILTER (WHERE state = 'active') as active_count,
    max(extract(epoch from (now() - backend_start))) as max_connection_age
FROM pg_stat_activity 
WHERE backend_type = 'client backend'
GROUP BY client_addr 
ORDER BY connection_count DESC;
" 2>/dev/null

# 4. 长时间运行的查询
echo -e "\n4. 长时间运行的查询:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    pid,
    usename,
    client_addr,
    extract(epoch from (now() - query_start)) as duration_seconds,
    state,
    wait_event_type,
    wait_event,
    substring(query, 1, 200) as query_text
FROM pg_stat_activity 
WHERE state = 'active' 
    AND extract(epoch from (now() - query_start)) > 30  -- 超过30秒
ORDER BY duration_seconds DESC;
" 2>/dev/null

# 5. 连接池压力评估
echo -e "\n5. 连接池压力评估:"
CONNECTION_STATS=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    count(*) as current_connections,
    (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max_connections
FROM pg_stat_activity;
" -t 2>/dev/null | xargs)

CURRENT_CONN=$(echo $CONNECTION_STATS | awk '{print $1}')
MAX_CONN=$(echo $CONNECTION_STATS | awk '{print $2}')
USAGE_PCT=$(awk "BEGIN {printf \"%.2f\", $CURRENT_CONN*100/$MAX_CONN}")

echo "连接池使用率: ${USAGE_PCT}% (${CURRENT_CONN}/${MAX_CONN})"

if (( $(echo "$USAGE_PCT > 80" | bc -l) )); then
    echo "⚠️  高风险: 连接池使用率超过80%"
    echo "建议措施:"
    echo "- 增加max_connections参数"
    echo "- 优化应用连接池配置"
    echo "- 检查是否有连接泄漏"
    echo "- 考虑读写分离"
elif (( $(echo "$USAGE_PCT > 60" | bc -l) )); then
    echo "⚠️  中等风险: 连接池使用率超过60%"
    echo "建议监控连接使用趋势"
else
    echo "✅ 连接池使用正常"
fi
```

### 4. 锁等待和死锁分析

```sql
-- 查看当前锁信息
SELECT 
    locktype,
    database,
    relation::regclass,
    page,
    tuple,
    virtualxid,
    transactionid,
    classid,
    objid,
    objsubid,
    virtualtransaction,
    pid,
    mode,
    granted,
    fastpath
FROM pg_locks 
WHERE NOT granted;

-- 查看阻塞和等待关系
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS current_blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
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
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- 查看死锁检测信息
SELECT 
    pg_backend_pid() as current_pid,
    pg_is_in_recovery() as is_standby,
    pg_current_wal_lsn() as current_lsn;

-- 启用死锁检测日志
ALTER SYSTEM SET log_lock_waits = on;
ALTER SYSTEM SET deadlock_timeout = '1s';
SELECT pg_reload_conf();
```

### 5. 复制和WAL分析

```sql
-- 主库复制状态
SELECT 
    client_addr,
    state,
    sync_state,
    write_lag,
    flush_lag,
    replay_lag,
    pg_size_pretty(pg_current_wal_lsn() - sent_lsn) as pending_wal
FROM pg_stat_replication;

-- 从库复制状态
SELECT 
    pg_is_in_recovery() as is_standby,
    pg_last_wal_receive_lsn() as received_lsn,
    pg_last_wal_replay_lsn() as replayed_lsn,
    pg_last_xact_replay_timestamp() as last_replay_time,
    extract(epoch from (now() - pg_last_xact_replay_timestamp())) as lag_seconds;

-- WAL日志统计
SELECT 
    pg_current_wal_lsn() as current_lsn,
    pg_walfile_name(pg_current_wal_lsn()) as current_wal_file,
    pg_size_pretty(pg_current_wal_lsn()) as current_wal_size;

-- 复制槽信息
SELECT 
    slot_name,
    plugin,
    slot_type,
    active,
    active_pid,
    pg_size_pretty(restart_lsn) as restart_lsn,
    pg_size_pretty(confirmed_flush_lsn) as confirmed_flush_lsn
FROM pg_replication_slots;
```

## 🔍 综合诊断实战

### 场景1：数据库性能下降

```bash
#!/bin/bash
# PostgreSQL性能下降诊断脚本

PG_HOST=${1:-"localhost"}
PG_PORT=${2:-"5432"}
PG_USER=${3:-"postgres"}
PG_DB=${4:-"postgres"}

echo "=== PostgreSQL性能下降诊断 ==="
echo "主机: $PG_HOST:$PG_PORT"
echo "数据库: $PG_DB"
echo "时间: $(date)"
echo ""

# 1. 基础性能指标
echo "1. 基础性能指标:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    datname,
    numbackends as connections,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted,
    round(blks_hit::float/(blks_hit+blks_read)*100, 2) as cache_hit_ratio
FROM pg_stat_database 
WHERE datname NOT IN ('template0', 'template1');
" 2>/dev/null

# 2. 慢查询分析
echo -e "\n2. 慢查询TOP 10:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent,
    regexp_replace(substring(query, 1, 150), '[\s]+', ' ', 'g') as query_sample
FROM pg_stat_statements 
WHERE mean_time > 500  -- 平均超过0.5秒
ORDER BY mean_time DESC 
LIMIT 10;
" 2>/dev/null

# 3. 表膨胀检查
echo -e "\n3. 表膨胀检查:"
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    n_tup_ins + n_tup_upd + n_tup_del as total_ops,
    n_dead_tup as dead_tuples,
    round(n_dead_tup::float / (n_live_tup + 1) * 100, 2) as dead_tuple_ratio
FROM pg_stat_user_tables 
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC 
LIMIT 10;
" 2>/dev/null

# 4. 锁等待检查
echo -e "\n4. 锁等待情况:"
LOCK_WAIT_COUNT=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT count(*) 
FROM pg_catalog.pg_locks 
WHERE NOT granted;
" -t 2>/dev/null | xargs)

echo "当前锁等待数: $LOCK_WAIT_COUNT"

if [ "$LOCK_WAIT_COUNT" -gt 0 ]; then
    echo "⚠️  发现锁等待，详情:"
    psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
    SELECT 
        blocked_locks.pid AS blocked_pid,
        blocked_activity.usename AS blocked_user,
        blocking_locks.pid AS blocking_pid,
        blocking_activity.usename AS blocking_user,
        substring(blocked_activity.query, 1, 100) AS blocked_statement,
        substring(blocking_activity.query, 1, 100) AS blocking_statement
    FROM pg_catalog.pg_locks blocked_locks
    JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
    JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
        AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
        AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
        AND blocking_locks.pid != blocked_locks.pid
    JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
    WHERE NOT blocked_locks.granted;
    " 2>/dev/null
fi

# 5. 系统资源检查
echo -e "\n5. 系统资源使用:"
echo "CPU使用率:"
top -b -n 1 | grep "Cpu(s)" | head -1

echo "内存使用情况:"
free -h | head -2

echo "磁盘IO:"
iostat -x 1 1 | grep -A 1 "Device"

# 6. 生成诊断结论
echo -e "\n=== 诊断结论 ==="
CACHE_HIT_RATIO=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT round(avg(blks_hit::float/(blks_hit+blks_read)*100), 2)
FROM pg_stat_database 
WHERE blks_read > 0 AND datname NOT IN ('template0', 'template1');
" -t 2>/dev/null | xargs)

echo "缓存命中率: ${CACHE_HIT_RATIO}%"

if (( $(echo "$CACHE_HIT_RATIO < 90" | bc -l) )); then
    echo "⚠️  缓存命中率较低，考虑增加shared_buffers"
fi

if [ "$LOCK_WAIT_COUNT" -gt 0 ]; then
    echo "⚠️  存在锁等待问题"
fi

SLOW_QUERIES=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT count(*) 
FROM pg_stat_statements 
WHERE mean_time > 1000;
" -t 2>/dev/null | xargs)

if [ "$SLOW_QUERIES" -gt 10 ]; then
    echo "⚠️  慢查询较多，需要优化"
fi

echo "✅ 诊断完成"
```

### 场景2：复制延迟问题

```bash
#!/bin/bash
# PostgreSQL复制延迟诊断脚本

PG_STANDBY_HOST=${1:-"localhost"}
PG_STANDBY_PORT=${2:-"5432"}
PG_USER=${3:-"postgres"}

echo "=== PostgreSQL复制延迟诊断 ==="
echo "从库主机: $PG_STANDBY_HOST:$PG_STANDBY_PORT"
echo "时间: $(date)"
echo ""

# 1. 从库状态检查
echo "1. 从库状态:"
psql -h $PG_STANDBY_HOST -p $PG_STANDBY_PORT -U $PG_USER -c "
SELECT 
    pg_is_in_recovery() as is_standby,
    pg_last_wal_receive_lsn() as received_lsn,
    pg_last_wal_replay_lsn() as replayed_lsn,
    pg_last_xact_replay_timestamp() as last_replay_time,
    extract(epoch from (now() - pg_last_xact_replay_timestamp())) as lag_seconds;
" 2>/dev/null

# 2. 复制槽状态
echo -e "\n2. 复制槽状态:"
psql -h $PG_STANDBY_HOST -p $PG_STANDBY_PORT -U $PG_USER -c "
SELECT 
    slot_name,
    plugin,
    slot_type,
    active,
    pg_size_pretty(restart_lsn) as restart_lsn,
    pg_size_pretty(confirmed_flush_lsn) as confirmed_flush_lsn
FROM pg_replication_slots;
" 2>/dev/null

# 3. 获取主库信息
echo -e "\n3. 主库状态:"
PRIMARY_HOST=$(psql -h $PG_STANDBY_HOST -p $PG_STANDBY_PORT -U $PG_USER -c "
SHOW primary_conninfo;
" 2>/dev/null | grep "host=" | sed 's/.*host=\([^ ]*\).*/\1/')

if [ -n "$PRIMARY_HOST" ]; then
    echo "主库地址: $PRIMARY_HOST"
    
    # 检查主库连接
    PRIMARY_STATUS=$(psql -h $PRIMARY_HOST -U $PG_USER -c "SELECT pg_current_wal_lsn();" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "主库连接正常"
        echo "主库当前LSN: $PRIMARY_STATUS"
    else
        echo "❌ 无法连接到主库"
    fi
else
    echo "❌ 未配置主库信息"
fi

# 4. 延迟详细分析
echo -e "\n4. 延迟详细分析:"
LAG_SECONDS=$(psql -h $PG_STANDBY_HOST -p $PG_STANDBY_PORT -U $PG_USER -c "
SELECT extract(epoch from (now() - pg_last_xact_replay_timestamp()));
" -t 2>/dev/null | xargs)

echo "延迟秒数: $LAG_SECONDS"

if [ "$LAG_SECONDS" = "" ] || [ "$LAG_SECONDS" = "0" ]; then
    echo "✅ 无延迟或延迟很小"
elif [ "$LAG_SECONDS" -lt 60 ]; then
    echo "⚠️  轻微延迟，建议监控"
elif [ "$LAG_SECONDS" -lt 300 ]; then
    echo "⚠️  中等延迟，需要关注"
else
    echo "⚠️  严重延迟，需要立即处理"
fi

# 5. 性能建议
echo -e "\n5. 优化建议:"
if [ "$LAG_SECONDS" -gt 300 ]; then
    echo "严重延迟处理建议:"
    echo "- 检查网络连接质量"
    echo "- 增加WAL发送缓冲区"
    echo "- 考虑异步复制"
    echo "- 检查从库硬件性能"
elif [ "$LAG_SECONDS" -gt 60 ]; then
    echo "延迟优化建议:"
    echo "- 监控WAL生成速度"
    echo "- 检查从库负载"
    echo "- 考虑并行应用"
    echo "- 优化查询性能"
else
    echo "✅ 复制状态良好"
fi
```

## 📊 监控和告警配置

### 自动化监控脚本
```bash
#!/bin/bash
# PostgreSQL健康检查守护脚本

CONFIG_FILE="/etc/postgres_monitor.conf"
LOG_FILE="/var/log/postgres_monitor.log"

# 默认配置
PG_HOST="localhost"
PG_PORT="5432"
PG_USER="monitor"
PG_DB="postgres"
ALERT_EMAIL="admin@example.com"

# 加载配置
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
fi

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

check_connection() {
    psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "SELECT 1;" >/dev/null 2>&1
    return $?
}

check_slow_queries() {
    SLOW_COUNT=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
        SELECT count(*) 
        FROM pg_stat_statements 
        WHERE mean_time > 1000;
    " -t 2>/dev/null | xargs)
    
    if [ "$SLOW_COUNT" -gt 20 ]; then
        log "WARN: 慢查询过多 ($SLOW_COUNT)"
        return 1
    fi
    return 0
}

check_connections() {
    USAGE_RATIO=$(psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
        SELECT round(count(*)::float / (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') * 100, 2)
        FROM pg_stat_activity;
    " -t 2>/dev/null | xargs)
    
    if (( $(echo "$USAGE_RATIO > 80" | bc -l) )); then
        log "WARN: 连接池使用率过高 (${USAGE_RATIO}%)"
        return 1
    fi
    return 0
}

# 主监控循环
while true; do
    if ! check_connection; then
        log "ERROR: 数据库连接失败"
        echo "Database connection failed" | mail -s "PostgreSQL Alert" $ALERT_EMAIL
    else
        check_slow_queries || echo "High slow query count" | mail -s "PostgreSQL Slow Query Alert" $ALERT_EMAIL
        check_connections || echo "High connection usage" | mail -s "PostgreSQL Connection Alert" $ALERT_EMAIL
    fi
    
    sleep 60
done
```

## 🧪 验证测试

### 工具可用性验证
```bash
#!/bin/bash
# PostgreSQL排查工具验证脚本

echo "=== PostgreSQL排查工具验证 ==="

# 检查PostgreSQL客户端
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL客户端可用"
    psql --version
else
    echo "❌ PostgreSQL客户端未安装"
fi

# 检查pgBadger
if command -v pgbadger &> /dev/null; then
    echo "✅ pgBadger可用"
    pgbadger --version
else
    echo "⚠️  pgBadger未安装"
fi

# 检查PgCLI
if command -v pgcli &> /dev/null; then
    echo "✅ PgCLI可用"
    pgcli --version
else
    echo "⚠️  PgCLI未安装"
fi

# 测试数据库连接
echo "测试数据库连接..."
psql -h localhost -c "SELECT version();" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 数据库连接正常"
else
    echo "⚠️  数据库连接异常"
fi

echo "验证完成"
```

## ❓ 常见问题处理

### Q1: 如何优化慢查询？
**优化步骤**：
```sql
-- 1. 启用pg_stat_statements扩展
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- 2. 分析执行计划
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'user@example.com';

-- 3. 添加合适索引
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- 4. 更新表统计信息
ANALYZE users;

-- 5. 考虑查询重写
-- 避免SELECT *
-- 使用具体条件
-- 考虑分页查询
```

### Q2: 连接数过多怎么办？
**解决方案**：
```sql
-- 1. 调整最大连接数
ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();

-- 2. 优化应用连接池配置
-- 减少最大连接数
-- 设置合理的超时时间
-- 启用连接复用

-- 3. 监控连接使用情况
SELECT count(*) FROM pg_stat_activity;
```

### Q3: 如何处理复制延迟？
**处理方法**：
```sql
-- 1. 检查复制状态
SELECT * FROM pg_stat_replication;

-- 2. 检查WAL日志
SELECT pg_current_wal_lsn(), pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn();

-- 3. 重启复制(严重延迟时)
-- 在从库执行
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE backend_type = 'walsender';
-- 重新配置复制
```

## 📚 扩展学习

### 专业工具推荐
- **pgAdmin**: 官方管理工具
- **Barman**: 备份和恢复工具
- **Patroni**: 高可用集群管理
- **pgBackRest**: 企业级备份工具

### 学习进阶路径
1. 深入理解PostgreSQL存储引擎架构
2. 掌握查询优化器工作原理
3. 学习流复制和逻辑复制
4. 掌握分区表和并行查询
5. 学习云原生PostgreSQL运维

---
> **💡 提示**: PostgreSQL性能优化需要结合具体业务场景，建议建立完整的监控体系，定期进行性能评估和优化。