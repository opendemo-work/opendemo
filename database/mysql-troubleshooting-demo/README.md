# MySQL数据库性能分析与故障排查实战演示

## 🎯 学习目标

通过本案例你将掌握MySQL数据库的专业排查和优化技能：

- 数据库性能监控和瓶颈分析
- 慢查询诊断和SQL优化
- 连接池问题排查和优化
- 锁等待和死锁分析
- 主从复制延迟诊断
- 内存和磁盘IO性能分析
- 数据库备份恢复最佳实践

## 🛠️ 环境准备

### 系统要求
- MySQL 5.7+ 或 MySQL 8.0+ 服务
- Linux/Unix系统环境
- 数据库管理员权限
- 至少2GB内存用于分析工具

### 依赖安装
```bash
# 安装MySQL客户端工具
sudo yum install -y mysql-community-client mysql-community-devel
sudo apt-get install -y mysql-client libmysqlclient-dev

# 安装性能分析工具
sudo yum install -y percona-toolkit sysbench
sudo apt-get install -y percona-toolkit sysbench

# 安装监控工具
pip install mycli  # 增强版MySQL客户端
pip install mysql-connector-python

# 验证安装
mysql --version
pt-query-digest --version
```

## 📁 项目结构

```
mysql-troubleshooting-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 排查脚本
│   ├── mysql_performance_analyzer.sh   # 性能分析脚本
│   ├── slow_query_analyzer.sh          # 慢查询分析脚本
│   ├── connection_pool_monitor.sh      # 连接池监控脚本
│   ├── replication_lag_checker.sh      # 主从延迟检查脚本
│   ├── deadlock_detector.sh            # 死锁检测脚本
│   └── backup_restore_validator.sh     # 备份恢复验证脚本
├── configs/                           # 配置文件
│   ├── mysql_performance.cnf           # 性能优化配置
│   ├── slow_query_log.cnf              # 慢查询日志配置
│   ├── monitoring_users.sql            # 监控用户权限配置
│   └── alert_rules.conf                # 告警规则配置
├── examples/                          # 实际案例
│   ├── slow_query_logs/                # 慢查询日志样本
│   ├── performance_schema_samples/     # 性能模式样本
│   ├── replication_issues/             # 主从复制问题案例
│   └── troubleshooting_playbooks/      # 故障排查手册
└── docs/                              # 详细文档
    ├── mysql_performance_tuning.md     # MySQL性能调优指南
    ├── query_optimization_guide.md     # 查询优化手册
    ├── replication_troubleshooting.md  # 主从复制故障排除
    └── backup_recovery_best_practices.md # 备份恢复最佳实践
```

## 🔧 核心排查技术详解

### 1. 性能监控和分析

```sql
-- 基础性能监控查询
-- 查看当前连接状态
SHOW PROCESSLIST;
SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE COMMAND != 'Sleep';

-- 查看数据库状态
SHOW STATUS LIKE 'Threads_%';
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Slow_queries';

-- 查看InnoDB状态
SHOW ENGINE INNODB STATUS\G

-- 性能模式查询
SELECT * FROM performance_schema.events_statements_summary_by_digest 
WHERE DIGEST_TEXT LIKE '%SELECT%' 
ORDER BY AVG_TIMER_WAIT DESC 
LIMIT 10;

-- 查看缓冲池使用情况
SELECT 
    pool_id,
    block_id,
    state,
    chunk_size,
    page_size
FROM performance_schema.buffer_page
LIMIT 10;
```

```bash
#!/bin/bash
# MySQL性能分析脚本

MYSQL_HOST=${1:-"localhost"}
MYSQL_PORT=${2:-"3306"}
MYSQL_USER=${3:-"root"}
MYSQL_PASS=${4:-""}

echo "=== MySQL性能分析报告 ==="
echo "主机: $MYSQL_HOST:$MYSQL_PORT"
echo "用户: $MYSQL_USER"
echo "时间: $(date)"
echo ""

# 1. 连接和线程状态
echo "1. 连接和线程状态:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW STATUS LIKE 'Threads_%';
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Aborted_connects';
" 2>/dev/null

# 2. 查询性能统计
echo -e "\n2. 查询性能统计:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW GLOBAL STATUS LIKE 'Questions';
SHOW GLOBAL STATUS LIKE 'Queries';
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SELECT 
    VARIABLE_VALUE as 'QPS' 
FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
WHERE VARIABLE_NAME = 'Questions';
" 2>/dev/null

# 3. InnoDB缓冲池状态
echo -e "\n3. InnoDB缓冲池状态:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW ENGINE INNODB STATUS\G
" 2>/dev/null | grep -E "(BUFFER POOL AND MEMORY|SEMAPHORES|TRANSACTIONS)" | head -20

# 4. 表锁等待情况
echo -e "\n4. 表锁等待情况:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW ENGINE INNODB STATUS\G
" 2>/dev/null | grep -A 10 "TRANSACTIONS"

# 5. 慢查询统计
echo -e "\n5. 慢查询统计:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW VARIABLES LIKE 'slow_query_log%';
SELECT COUNT(*) as '慢查询总数' FROM mysql.slow_log;
" 2>/dev/null

# 6. 生成性能报告
REPORT_FILE="/tmp/mysql_performance_$(date +%Y%m%d_%H%M%S).txt"
cat > $REPORT_FILE << EOF
MySQL性能分析报告
=================
主机: $MYSQL_HOST:$MYSQL_PORT
时间: $(date)

主要性能指标:
$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Threads_running';
SHOW STATUS LIKE 'Questions';
SHOW STATUS LIKE 'Slow_queries';
" 2>/dev/null)

建议优化方向:
1. 根据连接数调整max_connections参数
2. 优化慢查询SQL语句
3. 调整InnoDB缓冲池大小
4. 检查表结构和索引设计
EOF

echo -e "\n详细报告已保存: $REPORT_FILE"
```

### 2. 慢查询分析和优化

```sql
-- 慢查询日志配置
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';
SET GLOBAL log_queries_not_using_indexes = 'ON';

-- 分析慢查询日志
SELECT 
    DIGEST_TEXT,
    COUNT_STAR,
    AVG_TIMER_WAIT/1000000000 as avg_exec_time_sec,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest 
WHERE AVG_TIMER_WAIT > 1000000000  -- 平均执行时间超过1秒
ORDER BY AVG_TIMER_WAIT DESC 
LIMIT 10;

-- 查看没有使用索引的查询
SELECT 
    DIGEST_TEXT,
    COUNT_STAR,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT,
    ROUND(SUM_ROWS_EXAMINED/SUM_ROWS_SENT, 2) as examined_per_sent
FROM performance_schema.events_statements_summary_by_digest 
WHERE DIGEST_TEXT LIKE '%SELECT%' 
    AND SUM_ROWS_EXAMINED > SUM_ROWS_SENT * 10  -- 扫描行数远大于返回行数
ORDER BY examined_per_sent DESC 
LIMIT 10;
```

```bash
#!/bin/bash
# 慢查询分析脚本

MYSQL_HOST=${1:-"localhost"}
MYSQL_PORT=${2:-"3306"}
MYSQL_USER=${3:-"root"}
MYSQL_PASS=${4:-""}

echo "=== MySQL慢查询分析 ==="
echo "主机: $MYSQL_HOST:$MYSQL_PORT"
echo "时间: $(date)"
echo ""

# 1. 检查慢查询日志配置
echo "1. 慢查询日志配置:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW VARIABLES LIKE 'slow_query_log%';
SHOW VARIABLES LIKE 'long_query_time';
SHOW VARIABLES LIKE 'log_queries_not_using_indexes';
" 2>/dev/null

# 2. 分析性能模式中的慢查询
echo -e "\n2. 性能模式慢查询分析:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    LEFT(DIGEST_TEXT, 100) as query_sample,
    COUNT_STAR as execution_count,
    ROUND(AVG_TIMER_WAIT/1000000000, 4) as avg_time_sec,
    ROUND(MAX_TIMER_WAIT/1000000000, 4) as max_time_sec,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest 
WHERE AVG_TIMER_WAIT > 1000000000  -- 平均超过1秒
    AND DIGEST_TEXT IS NOT NULL
ORDER BY AVG_TIMER_WAIT DESC 
LIMIT 10;
" 2>/dev/null

# 3. 检查没有使用索引的查询
echo -e "\n3. 未使用索引的查询分析:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    LEFT(DIGEST_TEXT, 100) as query_sample,
    COUNT_STAR as execution_count,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT,
    ROUND(SUM_ROWS_EXAMINED/SUM_ROWS_SENT, 2) as rows_examined_per_sent
FROM performance_schema.events_statements_summary_by_digest 
WHERE DIGEST_TEXT LIKE 'SELECT%'
    AND SUM_ROWS_EXAMINED > 0
    AND SUM_ROWS_SENT > 0
    AND SUM_ROWS_EXAMINED > SUM_ROWS_SENT * 10
ORDER BY rows_examined_per_sent DESC 
LIMIT 10;
" 2>/dev/null

# 4. 使用pt-query-digest分析慢查询日志
if command -v pt-query-digest &> /dev/null; then
    echo -e "\n4. pt-query-digest分析结果:"
    SLOW_LOG_FILE=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
        SHOW VARIABLES LIKE 'slow_query_log_file';
    " 2>/dev/null | awk 'NR==2 {print $2}')
    
    if [ -n "$SLOW_LOG_FILE" ] && [ -f "$SLOW_LOG_FILE" ]; then
        echo "分析慢查询日志文件: $SLOW_LOG_FILE"
        pt-query-digest $SLOW_LOG_FILE --limit 10 2>/dev/null | head -30
    else
        echo "未找到慢查询日志文件"
    fi
else
    echo -e "\n4. pt-query-digest工具未安装"
fi

# 5. 生成优化建议
echo -e "\n5. 优化建议:"
echo "常见优化措施:"
echo "- 为高频查询字段添加合适的索引"
echo "- 优化JOIN条件和WHERE子句"
echo "- 考虑查询缓存策略"
echo "- 分析表结构是否需要重构"
echo "- 检查数据库配置参数"
```

### 3. 连接池和并发问题

```sql
-- 连接状态监控
SELECT 
    ID,
    USER,
    HOST,
    DB,
    COMMAND,
    TIME,
    STATE,
    INFO
FROM INFORMATION_SCHEMA.PROCESSLIST 
WHERE COMMAND != 'Sleep' 
ORDER BY TIME DESC;

-- 查看连接统计
SHOW STATUS LIKE 'Threads_%';
SHOW STATUS LIKE 'Connections%';

-- 查看最大连接数配置
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'max_connect_errors';

-- 查看连接使用率
SELECT 
    VARIABLE_VALUE as current_connections
FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
WHERE VARIABLE_NAME = 'Threads_connected';

SELECT 
    VARIABLE_VALUE as max_connections
FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES 
WHERE VARIABLE_NAME = 'max_connections';
```

```bash
#!/bin/bash
# 连接池监控脚本

MYSQL_HOST=${1:-"localhost"}
MYSQL_PORT=${2:-"3306"}
MYSQL_USER=${3:-"root"}
MYSQL_PASS=${4:-""}

echo "=== MySQL连接池监控 ==="
echo "主机: $MYSQL_HOST:$MYSQL_PORT"
echo "时间: $(date)"
echo ""

# 1. 连接池状态
echo "1. 连接池当前状态:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    VARIABLE_VALUE as current_connections
FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
WHERE VARIABLE_NAME = 'Threads_connected';

SELECT 
    VARIABLE_VALUE as max_connections
FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES 
WHERE VARIABLE_NAME = 'max_connections';

SHOW STATUS LIKE 'Threads_%';
SHOW STATUS LIKE 'Connections%';
" 2>/dev/null

# 2. 活跃连接分析
echo -e "\n2. 活跃连接详情:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    ID,
    USER,
    HOST,
    DB,
    COMMAND,
    TIME as duration_seconds,
    STATE,
    LEFT(INFO, 100) as query_preview
FROM INFORMATION_SCHEMA.PROCESSLIST 
WHERE COMMAND != 'Sleep' 
    AND TIME > 5  -- 超过5秒的连接
ORDER BY TIME DESC 
LIMIT 10;
" 2>/dev/null

# 3. 连接来源分析
echo -e "\n3. 连接来源统计:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    SUBSTRING_INDEX(HOST, ':', 1) as client_ip,
    COUNT(*) as connection_count,
    MAX(TIME) as max_duration
FROM INFORMATION_SCHEMA.PROCESSLIST 
GROUP BY SUBSTRING_INDEX(HOST, ':', 1)
ORDER BY connection_count DESC;
" 2>/dev/null

# 4. 连接池压力评估
echo -e "\n4. 连接池压力评估:"
CONNECTION_RATIO=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    ROUND(
        (SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME = 'Threads_connected') * 100.0 /
        (SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME = 'max_connections'),
        2
    ) as connection_ratio;
" 2>/dev/null | tail -1)

echo "连接池使用率: ${CONNECTION_RATIO}%"

if (( $(echo "$CONNECTION_RATIO > 80" | bc -l) )); then
    echo "⚠️  高风险: 连接池使用率超过80%"
    echo "建议措施:"
    echo "- 增加max_connections参数"
    echo "- 优化应用连接池配置"
    echo "- 检查是否有连接泄漏"
    echo "- 考虑读写分离"
elif (( $(echo "$CONNECTION_RATIO > 60" | bc -l) )); then
    echo "⚠️  中等风险: 连接池使用率超过60%"
    echo "建议监控连接使用趋势"
else
    echo "✅ 连接池使用正常"
fi

# 5. 长时间连接检查
echo -e "\n5. 长时间连接检查:"
LONG_CONNECTIONS=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT COUNT(*) as long_connections
FROM INFORMATION_SCHEMA.PROCESSLIST 
WHERE COMMAND != 'Sleep' AND TIME > 300;
" 2>/dev/null | tail -1)

echo "超过5分钟的活跃连接数: $LONG_CONNECTIONS"

if [ "$LONG_CONNECTIONS" -gt 0 ]; then
    echo "⚠️  发现长时间运行的连接，可能存在性能问题"
fi
```

### 4. 锁等待和死锁分析

```sql
-- 查看当前锁等待
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

-- 查看事务锁信息
SELECT 
    trx_id,
    trx_state,
    trx_started,
    trx_requested_lock_id,
    trx_wait_started,
    trx_weight,
    trx_mysql_thread_id,
    trx_query
FROM information_schema.innodb_trx
WHERE trx_state = 'LOCK WAIT';

-- 查看最近的死锁信息
SHOW ENGINE INNODB STATUS;
-- 在输出中查找 "LATEST DETECTED DEADLOCK" 部分
```

### 5. 主从复制监控

```sql
-- 主库状态检查
SHOW MASTER STATUS;

-- 从库状态检查
SHOW SLAVE STATUS\G

-- 从库延迟检查
SELECT 
    Seconds_Behind_Master,
    Slave_IO_Running,
    Slave_SQL_Running,
    Last_Error
FROM information_schema.slave_status;

-- 从库复制性能统计
SELECT 
    CHANNEL_NAME,
    SERVICE_STATE,
    LAST_ERROR_NUMBER,
    LAST_ERROR_MESSAGE,
    LAST_ERROR_TIMESTAMP
FROM performance_schema.replication_applier_status;
```

## 🔍 综合诊断实战

### 场景1：数据库响应缓慢

```bash
#!/bin/bash
# 数据库响应缓慢诊断脚本

MYSQL_HOST=${1:-"localhost"}
MYSQL_PORT=${2:-"3306"}
MYSQL_USER=${3:-"root"}
MYSQL_PASS=${4:-""}

echo "=== 数据库响应缓慢诊断 ==="
echo "主机: $MYSQL_HOST:$MYSQL_PORT"
echo "时间: $(date)"
echo ""

# 1. 基础性能指标
echo "1. 基础性能指标:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW STATUS LIKE 'Questions';
SHOW STATUS LIKE 'Queries';
SHOW STATUS LIKE 'Slow_queries';
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Threads_running';
" 2>/dev/null

# 2. 慢查询分析
echo -e "\n2. 慢查询TOP 10:"
mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    LEFT(DIGEST_TEXT, 150) as query_sample,
    COUNT_STAR as executions,
    ROUND(AVG_TIMER_WAIT/1000000000, 4) as avg_time_sec,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest 
WHERE AVG_TIMER_WAIT > 500000000  -- 平均超过0.5秒
ORDER BY AVG_TIMER_WAIT DESC 
LIMIT 10;
" 2>/dev/null

# 3. 连接池压力检查
echo -e "\n3. 连接池状态:"
CONNECTION_INFO=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    (SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME = 'Threads_connected') as connected,
    (SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME = 'max_connections') as max_conn;
" 2>/dev/null | tail -1)

CONNECTED=$(echo $CONNECTION_INFO | awk '{print $1}')
MAX_CONN=$(echo $CONNECTION_INFO | awk '{print $2}')
USAGE_PCT=$((CONNECTED * 100 / MAX_CONN))

echo "当前连接数: $CONNECTED/$MAX_CONN (${USAGE_PCT}%)"

# 4. 锁等待检查
echo -e "\n4. 锁等待情况:"
LOCK_WAITS=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT COUNT(*) as lock_waits
FROM information_schema.innodb_lock_waits;
" 2>/dev/null | tail -1)

echo "当前锁等待数: $LOCK_WAITS"

if [ "$LOCK_WAITS" -gt 0 ]; then
    echo "⚠️  发现锁等待，详情:"
    mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
    SELECT 
        r.trx_id as waiting_trx,
        r.trx_mysql_thread_id as waiting_thread,
        LEFT(r.trx_query, 100) as waiting_query,
        b.trx_id as blocking_trx,
        b.trx_mysql_thread_id as blocking_thread,
        LEFT(b.trx_query, 100) as blocking_query
    FROM information_schema.innodb_lock_waits w
    INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
    INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;
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
if [ "$USAGE_PCT" -gt 80 ]; then
    echo "⚠️  连接池压力过大"
fi

if [ "$LOCK_WAITS" -gt 0 ]; then
    echo "⚠️  存在锁等待问题"
fi

SLOW_QUERIES=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME = 'Slow_queries';
" 2>/dev/null | tail -1)

if [ "$SLOW_QUERIES" -gt 100 ]; then
    echo "⚠️  慢查询较多，需要优化"
fi

echo "✅ 诊断完成"
```

### 场景2：主从复制延迟

```bash
#!/bin/bash
# 主从复制延迟诊断脚本

MYSQL_SLAVE_HOST=${1:-"localhost"}
MYSQL_SLAVE_PORT=${2:-"3306"}
MYSQL_USER=${3:-"root"}
MYSQL_PASS=${4:-""}

echo "=== 主从复制延迟诊断 ==="
echo "从库主机: $MYSQL_SLAVE_HOST:$MYSQL_SLAVE_PORT"
echo "时间: $(date)"
echo ""

# 1. 复制状态检查
echo "1. 复制状态:"
mysql -h$MYSQL_SLAVE_HOST -P$MYSQL_SLAVE_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW SLAVE STATUS\G
" 2>/dev/null | grep -E "(Slave_IO_Running|Slave_SQL_Running|Seconds_Behind_Master|Last_Error)"

# 2. 延迟详细分析
echo -e "\n2. 延迟详细信息:"
mysql -h$MYSQL_SLAVE_HOST -P$MYSQL_SLAVE_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SELECT 
    CHANNEL_NAME,
    SERVICE_STATE,
    REMAINING_DELAY,
    COUNT_TRANSACTIONS_RETRIES
FROM performance_schema.replication_applier_status_by_worker;
" 2>/dev/null

# 3. 主库信息获取
echo -e "\n3. 主库状态:"
MASTER_HOST=$(mysql -h$MYSQL_SLAVE_HOST -P$MYSQL_SLAVE_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW SLAVE STATUS\G
" 2>/dev/null | grep "Master_Host" | awk '{print $2}')

if [ -n "$MASTER_HOST" ]; then
    echo "主库地址: $MASTER_HOST"
    
    # 检查主库连接
    MASTER_STATUS=$(mysql -h$MASTER_HOST -u$MYSQL_USER -p$MYSQL_PASS -e "SHOW MASTER STATUS\G" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "主库连接正常"
        echo "$MASTER_STATUS" | head -10
    else
        echo "❌ 无法连接到主库"
    fi
else
    echo "❌ 未配置主库信息"
fi

# 4. 延迟原因分析
echo -e "\n4. 延迟可能原因:"
SLAVE_STATUS=$(mysql -h$MYSQL_SLAVE_HOST -P$MYSQL_SLAVE_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
SHOW SLAVE STATUS\G
" 2>/dev/null)

# 检查IO线程状态
IO_RUNNING=$(echo "$SLAVE_STATUS" | grep "Slave_IO_Running" | awk '{print $2}')
SQL_RUNNING=$(echo "$SLAVE_STATUS" | grep "Slave_SQL_Running" | awk '{print $2}')
SECONDS_BEHIND=$(echo "$SLAVE_STATUS" | grep "Seconds_Behind_Master" | awk '{print $2}')

echo "IO线程运行状态: $IO_RUNNING"
echo "SQL线程运行状态: $SQL_RUNNING"
echo "延迟秒数: $SECONDS_BEHIND"

if [ "$IO_RUNNING" != "Yes" ]; then
    echo "⚠️  IO线程异常，检查网络连接和主库状态"
fi

if [ "$SQL_RUNNING" != "Yes" ]; then
    echo "⚠️  SQL线程异常，检查错误日志"
    echo "$SLAVE_STATUS" | grep "Last_Error"
fi

# 5. 性能建议
echo -e "\n5. 优化建议:"
if [ "$SECONDS_BEHIND" = "NULL" ] || [ "$SECONDS_BEHIND" -gt 300 ]; then
    echo "⚠️  延迟严重，建议措施:"
    echo "- 检查从库硬件性能"
    echo "- 优化慢查询"
    echo "- 考虑并行复制"
    echo "- 检查网络延迟"
elif [ "$SECONDS_BEHIND" -gt 60 ]; then
    echo "⚠️  延迟中等，建议监控"
else
    echo "✅ 延迟在可接受范围内"
fi
```

## 📊 监控和告警配置

### 自动化监控脚本
```bash
#!/bin/bash
# MySQL健康检查守护脚本

CONFIG_FILE="/etc/mysql_monitor.conf"
LOG_FILE="/var/log/mysql_monitor.log"

# 默认配置
MYSQL_HOST="localhost"
MYSQL_PORT="3306"
MYSQL_USER="monitor"
MYSQL_PASS=""
ALERT_EMAIL="admin@example.com"

# 加载配置
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
fi

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

check_connection() {
    mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT 1;" >/dev/null 2>&1
    return $?
}

check_slow_queries() {
    SLOW_COUNT=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
        SELECT VARIABLE_VALUE 
        FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
        WHERE VARIABLE_NAME = 'Slow_queries';
    " 2>/dev/null | tail -1)
    
    if [ "$SLOW_COUNT" -gt 100 ]; then
        log "WARN: 慢查询过多 ($SLOW_COUNT)"
        return 1
    fi
    return 0
}

check_connections() {
    CONNECTION_RATIO=$(mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PASS -e "
        SELECT 
            ROUND(
                (SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS WHERE VARIABLE_NAME = 'Threads_connected') * 100.0 /
                (SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES WHERE VARIABLE_NAME = 'max_connections'),
                2
            );
    " 2>/dev/null | tail -1)
    
    if (( $(echo "$CONNECTION_RATIO > 80" | bc -l) )); then
        log "WARN: 连接池使用率过高 (${CONNECTION_RATIO}%)"
        return 1
    fi
    return 0
}

# 主监控循环
while true; do
    if ! check_connection; then
        log "ERROR: 数据库连接失败"
        echo "Database connection failed" | mail -s "MySQL Alert" $ALERT_EMAIL
    else
        check_slow_queries || echo "High slow query count" | mail -s "MySQL Slow Query Alert" $ALERT_EMAIL
        check_connections || echo "High connection usage" | mail -s "MySQL Connection Alert" $ALERT_EMAIL
    fi
    
    sleep 60
done
```

## 🧪 验证测试

### 工具可用性验证
```bash
#!/bin/bash
# MySQL排查工具验证脚本

echo "=== MySQL排查工具验证 ==="

# 检查MySQL客户端
if command -v mysql &> /dev/null; then
    echo "✅ MySQL客户端可用"
    mysql --version
else
    echo "❌ MySQL客户端未安装"
fi

# 检查Percona工具
if command -v pt-query-digest &> /dev/null; then
    echo "✅ Percona Toolkit可用"
    pt-query-digest --version
else
    echo "⚠️  Percona Toolkit未安装"
fi

# 检查MyCLI
if command -v mycli &> /dev/null; then
    echo "✅ MyCLI可用"
    mycli --version
else
    echo "⚠️  MyCLI未安装"
fi

# 测试数据库连接
echo "测试数据库连接..."
mysql -hlocalhost -e "SELECT VERSION();" 2>/dev/null
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
-- 1. 启用慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- 2. 分析执行计划
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- 3. 添加合适索引
CREATE INDEX idx_users_email ON users(email);

-- 4. 优化查询语句
-- 避免SELECT *
-- 使用具体的WHERE条件
-- 考虑分页查询
```

### Q2: 连接数过多怎么办？
**解决方案**：
```sql
-- 1. 调整最大连接数
SET GLOBAL max_connections = 200;

-- 2. 优化应用连接池配置
-- 减少最大连接数
-- 设置合理的超时时间
-- 启用连接复用

-- 3. 监控连接使用情况
SELECT 
    VARIABLE_VALUE as current_connections
FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
WHERE VARIABLE_NAME = 'Threads_connected';
```

### Q3: 如何处理主从复制延迟？
**处理方法**：
```sql
-- 1. 检查复制状态
SHOW SLAVE STATUS\G

-- 2. 跳过错误事务（谨慎使用）
STOP SLAVE;
SET GLOBAL sql_slave_skip_counter = 1;
START SLAVE;

-- 3. 重建复制（严重延迟时）
-- 在主库备份
mysqldump --master-data=2 --single-transaction db_name > backup.sql
-- 在从库恢复并重新配置复制
```

## 📚 扩展学习

### 专业工具推荐
- **Percona Monitoring and Management**: 完整的MySQL监控解决方案
- **MySQL Enterprise Monitor**: Oracle官方监控工具
- **Zabbix + MySQL模板**: 开源监控方案
- **Prometheus + Grafana**: 现代化监控栈

### 学习进阶路径
1. 深入理解MySQL存储引擎架构
2. 掌握查询优化器工作原理
3. 学习高可用架构设计
4. 掌握分库分表策略
5. 学习云原生数据库运维

---
> **💡 提示**: 数据库性能优化是一个持续的过程，建议建立完整的监控体系，定期进行性能评估和优化。