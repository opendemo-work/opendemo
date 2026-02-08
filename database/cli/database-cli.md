# 🗄️ Database 命令行速查表 (database-cli.md)

> 生产环境必备的数据库命令行参考手册，涵盖主流数据库系统的管理、监控、优化命令，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [MySQL管理](#mysql管理)
- [PostgreSQL管理](#postgresql管理)
- [MongoDB管理](#mongodb管理)
- [Redis管理](#redis管理)
- [性能监控](#性能监控)
- [查询优化](#查询优化)
- [备份恢复](#备份恢复)
- [复制同步](#复制同步)
- [安全管理](#安全管理)
- [连接池管理](#连接池管理)
- [索引管理](#索引管理)
- [故障排查](#故障排查)
- [自动化运维](#自动化运维)
- [最佳实践](#最佳实践)

---

## MySQL管理

### 基础连接和状态
```bash
# 连接MySQL数据库
mysql -u username -p -h hostname -P port database_name

# 无密码连接（生产环境不推荐）
mysql -u username -p$password -h hostname database_name

# 执行单条SQL命令
mysql -u username -p -e "SELECT VERSION();"

# 查看MySQL版本和状态
mysql -u root -p -e "SHOW VARIABLES LIKE '%version%';"
mysql -u root -p -e "SHOW STATUS LIKE 'Uptime';"

# 查看当前连接
mysql -u root -p -e "SHOW PROCESSLIST;"
```

### 数据库和表管理
```sql
-- 创建数据库
CREATE DATABASE database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 删除数据库
DROP DATABASE database_name;

-- 查看所有数据库
SHOW DATABASES;

-- 使用数据库
USE database_name;

-- 查看当前数据库
SELECT DATABASE();

-- 创建表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 查看表结构
DESCRIBE table_name;
SHOW CREATE TABLE table_name;

-- 修改表结构
ALTER TABLE table_name ADD COLUMN new_column VARCHAR(100);
ALTER TABLE table_name DROP COLUMN column_name;
```

### 用户权限管理
```sql
-- 创建用户
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';

-- 授权用户
GRANT SELECT, INSERT, UPDATE ON database_name.* TO 'username'@'localhost';

-- 授权所有权限
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 查看用户权限
SHOW GRANTS FOR 'username'@'localhost';

-- 撤销权限
REVOKE DELETE ON database_name.* FROM 'username'@'localhost';

-- 删除用户
DROP USER 'username'@'localhost';
```

### 性能监控查询
```sql
-- 查看当前连接状态
SHOW PROCESSLIST;
SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE COMMAND != 'Sleep';

-- 查看数据库状态变量
SHOW STATUS LIKE 'Threads_%';
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Slow_queries';

-- 查看InnoDB状态
SHOW ENGINE INNODB STATUS\G

-- 查看缓冲池使用情况
SELECT 
    pool_id,
    block_id,
    state,
    chunk_size,
    pages_free,
    pages_used
FROM INFORMATION_SCHEMA.INNODB_BUFFER_POOL_STATS;

-- 查看表空间使用
SELECT 
    table_schema,
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size(MB)'
FROM information_schema.tables 
WHERE table_schema = 'database_name'
ORDER BY (data_length + index_length) DESC;
```

---

## PostgreSQL管理

### 基础连接和状态
```bash
# 连接PostgreSQL数据库
psql -U username -d database_name -h hostname -p port

# 指定密码连接
PGPASSWORD=password psql -U username -d database_name

# 执行单条SQL命令
psql -U postgres -c "SELECT version();"

# 查看PostgreSQL版本
psql -U postgres -c "SELECT version();"

# 查看当前连接
psql -U postgres -c "SELECT * FROM pg_stat_activity WHERE state != 'idle';"
```

### 数据库和表管理
```sql
-- 创建数据库
CREATE DATABASE database_name WITH ENCODING='UTF8' OWNER=username;

-- 删除数据库
DROP DATABASE database_name;

-- 查看所有数据库
\l

-- 切换数据库
\c database_name

-- 创建表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 查看表结构
\d table_name

-- 查看表详细信息
\d+ table_name

-- 修改表结构
ALTER TABLE table_name ADD COLUMN new_column VARCHAR(100);
ALTER TABLE table_name DROP COLUMN column_name;
```

### 用户权限管理
```sql
-- 创建用户
CREATE USER username WITH PASSWORD 'password';

-- 创建角色
CREATE ROLE role_name;

-- 授权数据库权限
GRANT CONNECT ON DATABASE database_name TO username;

-- 授权表权限
GRANT SELECT, INSERT, UPDATE ON TABLE table_name TO username;

-- 授权所有权限
GRANT ALL PRIVILEGES ON DATABASE database_name TO username;

-- 查看用户权限
\du

-- 撤销权限
REVOKE DELETE ON TABLE table_name FROM username;

-- 删除用户
DROP USER username;
```

### 性能监控查询
```sql
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
WHERE datname = 'database_name';

-- 查看表大小
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 查看索引使用情况
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_tup_read DESC;
```

---

## MongoDB管理

### 基础连接和状态
```bash
# 连接MongoDB
mongo hostname:port/database_name -u username -p password

# 使用认证连接
mongo --host hostname --port port -u username -p password --authenticationDatabase admin

# 查看MongoDB版本
mongo --eval "db.version()"

# 查看数据库状态
mongo --eval "db.serverStatus()"
```

### 数据库和集合管理
```javascript
// 查看所有数据库
show dbs

// 切换数据库
use database_name

// 查看当前数据库
db.getName()

// 创建集合
db.createCollection("collection_name")

// 查看所有集合
show collections

// 删除集合
db.collection_name.drop()

// 删除数据库
use database_name
db.dropDatabase()
```

### 文档操作
```javascript
// 插入文档
db.users.insert({
    username: "john_doe",
    email: "john@example.com",
    created_at: new Date()
})

// 查询文档
db.users.find({username: "john_doe"})
db.users.findOne({email: "john@example.com"})

// 更新文档
db.users.update(
    {username: "john_doe"},
    {$set: {email: "newemail@example.com"}}
)

// 删除文档
db.users.remove({username: "john_doe"})

// 查看集合统计
db.users.stats()
```

### 性能监控
```javascript
// 查看数据库状态
db.serverStatus()

// 查看连接数
db.serverStatus().connections

// 查看操作计数器
db.serverStatus().opcounters

// 查看内存使用
db.serverStatus().mem

// 查看集合统计
db.collection_name.stats()

// 查看慢查询日志
db.system.profile.find().sort({$natural: -1}).limit(10)

// 启用慢查询日志
db.setProfilingLevel(1, 100)  // 记录超过100ms的查询
```

---

## Redis管理

### 基础连接和状态
```bash
# 连接Redis
redis-cli -h hostname -p port -a password

# 执行单条命令
redis-cli -h hostname -p port GET key_name

# 查看Redis信息
redis-cli INFO

# 查看特定部分信息
redis-cli INFO server
redis-cli INFO memory
redis-cli INFO clients
redis-cli INFO stats
```

### 键值操作
```bash
# 设置键值
SET key_name "value"

# 获取键值
GET key_name

# 删除键
DEL key_name

# 检查键是否存在
EXISTS key_name

# 设置过期时间
EXPIRE key_name 3600
TTL key_name

# 查看所有键
KEYS *

# 批量删除键
redis-cli KEYS "pattern*" | xargs redis-cli DEL
```

### 数据库管理
```bash
# 选择数据库
SELECT 0

# 查看当前数据库键数量
DBSIZE

# 清空当前数据库
FLUSHDB

# 清空所有数据库
FLUSHALL

# 查看慢查询日志
SLOWLOG GET 10

# 配置慢查询阈值
CONFIG SET slowlog-log-slower-than 10000
```

### 性能监控
```bash
# 查看内存使用
INFO memory

# 查看客户端连接
INFO clients

# 查看命中率
INFO stats | grep -E "(keyspace_hits|keyspace_misses)"

# 查看持久化状态
INFO persistence

# 查看复制状态
INFO replication

# 实时监控
redis-cli --stat

# 监控特定命令
redis-cli monitor
```

---

## 性能监控

### 数据库性能指标收集
```bash
# MySQL性能模式查询
mysql -u root -p -e "
SELECT 
    DIGEST_TEXT,
    COUNT_STAR,
    AVG_TIMER_WAIT/1000000000 AS avg_latency_ms,
    SUM_ROWS_EXAMINED
FROM performance_schema.events_statements_summary_by_digest 
WHERE DIGEST_TEXT LIKE '%SELECT%' 
ORDER BY AVG_TIMER_WAIT DESC 
LIMIT 10;
"

# PostgreSQL查询统计
psql -U postgres -c "
SELECT 
    query,
    calls,
    mean_time,
    rows,
    shared_blks_hit,
    shared_blks_read
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
"

# MongoDB操作统计
mongo --eval "
db.currentOp().inprog.forEach(function(op) {
    print('Operation: ' + op.op);
    print('Namespace: ' + op.ns);
    print('Duration: ' + op.secs_running + ' seconds');
    print('---');
});
"
```

### 系统资源监控
```bash
# 查看数据库进程资源使用
ps aux | grep -E "(mysql|postgres|mongod|redis)" | grep -v grep

# 查看数据库进程IO统计
iotop -p $(pgrep -f "mysqld|postgres|mongod|redis")

# 查看数据库连接数
netstat -an | grep :3306 | grep ESTABLISHED | wc -l  # MySQL
netstat -an | grep :5432 | grep ESTABLISHED | wc -l  # PostgreSQL
netstat -an | grep :27017 | grep ESTABLISHED | wc -l # MongoDB

# 查看数据库端口监听
ss -tulnp | grep -E "(3306|5432|27017|6379)"
```

### 性能分析工具
```bash
# MySQL慢查询分析
mysqldumpslow /var/log/mysql/slow.log

# 使用pt-query-digest分析
pt-query-digest /var/log/mysql/slow.log

# PostgreSQL日志分析
pgbadger /var/log/postgresql/postgresql-*.log

# MongoDB性能分析
mongostat --host hostname --port port

# Redis性能监控
redis-cli --latency -h hostname -p port
```

---

## 查询优化

### 执行计划分析
```sql
-- MySQL执行计划
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'user@example.com';

-- PostgreSQL执行计划
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- 查看查询成本
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT * FROM users WHERE email = 'user@example.com';
```

### 索引优化查询
```sql
-- MySQL索引使用分析
SHOW INDEX FROM table_name;

-- 查看未使用索引
SELECT 
    object_schema,
    object_name,
    index_name,
    count_read,
    count_write
FROM performance_schema.table_io_waits_summary_by_index_usage 
WHERE index_name IS NOT NULL 
AND count_read = 0 
ORDER BY count_write DESC;

-- PostgreSQL索引统计
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_scan ASC;

-- 索引大小分析
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS size
FROM pg_indexes 
WHERE tablename = 'table_name'
ORDER BY pg_relation_size(indexname::regclass) DESC;
```

### 查询重写优化
```sql
-- MySQL子查询优化
-- 原始查询
SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers WHERE status = 'active');

-- 优化后（使用JOIN）
SELECT o.* FROM orders o 
JOIN customers c ON o.customer_id = c.id 
WHERE c.status = 'active';

-- PostgreSQL窗口函数优化
-- 原始查询
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) as rn
    FROM products
) ranked WHERE rn <= 3;

-- 优化后
SELECT DISTINCT ON (category) *
FROM products 
ORDER BY category, price DESC;
```

---

## 备份恢复

### MySQL备份恢复
```bash
# 完整备份
mysqldump -u root -p --single-transaction --routines --triggers database_name > backup.sql

# 增量备份
mysqlbinlog --start-datetime="2024-01-01 00:00:00" /var/log/mysql/mysql-bin.000001 > incremental.sql

# 压缩备份
mysqldump -u root -p database_name | gzip > backup.sql.gz

# 恢复备份
mysql -u root -p database_name < backup.sql

# 恢复压缩备份
gunzip < backup.sql.gz | mysql -u root -p database_name

# 物理备份（使用Percona XtraBackup）
xtrabackup --backup --target-dir=/backup/mysql/
xtrabackup --prepare --target-dir=/backup/mysql/
```

### PostgreSQL备份恢复
```bash
# 逻辑备份
pg_dump -U postgres -h localhost database_name > backup.sql

# 压缩备份
pg_dump -U postgres database_name | gzip > backup.sql.gz

# 自定义格式备份（支持并行恢复）
pg_dump -U postgres -Fc database_name > backup.dump

# 恢复逻辑备份
psql -U postgres database_name < backup.sql

# 恢复自定义格式备份
pg_restore -U postgres -d database_name backup.dump

# 物理备份
pg_basebackup -U postgres -D /backup/postgres/ -Ft -z -P

# 时间点恢复配置
# 在postgresql.conf中设置：
# wal_level = replica
# archive_mode = on
# archive_command = 'cp %p /archive/%f'
```

### MongoDB备份恢复
```bash
# 逻辑备份
mongodump --host hostname --port port --db database_name --out /backup/

# 压缩备份
mongodump --host hostname --gzip --archive=/backup/backup.archive

# 恢复备份
mongorestore --host hostname --port port /backup/database_name/

# 恢复压缩备份
mongorestore --host hostname --gzip --archive=/backup/backup.archive

# Oplog备份
mongodump --host hostname --oplog

# 分片集群备份
mongodump --host config_server_host --db config
```

### Redis备份恢复
```bash
# RDB持久化备份
# 自动由Redis配置触发，文件位置在redis.conf中设置

# AOF持久化
# 实时追加日志，默认启用

# 手动触发保存
redis-cli BGSAVE

# 备份RDB文件
cp /var/lib/redis/dump.rdb /backup/

# 恢复RDB文件
cp /backup/dump.rdb /var/lib/redis/
systemctl restart redis

# AOF重写
redis-cli BGREWRITEAOF
```

---

## 复制同步

### MySQL主从复制
```sql
-- 主库配置检查
SHOW MASTER STATUS;

-- 从库配置检查
SHOW SLAVE STATUS\G

-- 查看复制延迟
SHOW SLAVE STATUS\G | grep Seconds_Behind_Master

-- 跳过复制错误
STOP SLAVE;
SET GLOBAL sql_slave_skip_counter = 1;
START SLAVE;

-- 重置复制
RESET SLAVE ALL;
```

### PostgreSQL流复制
```sql
-- 查看复制槽
SELECT * FROM pg_replication_slots;

-- 查看WAL发送者状态
SELECT * FROM pg_stat_replication;

-- 查看复制延迟
SELECT 
    client_addr,
    state,
    sync_state,
    pg_size_pretty(pg_current_wal_lsn() - replay_lsn) AS lag
FROM pg_stat_replication;

-- 创建复制槽
SELECT pg_create_physical_replication_slot('slot_name');

-- 删除复制槽
SELECT pg_drop_replication_slot('slot_name');
```

### MongoDB复制集
```javascript
// 查看复制集状态
rs.status()

// 查看复制延迟
db.printSlaveReplicationInfo()

// 查看oplog状态
db.printReplicationInfo()

// 添加副本集成员
rs.add("hostname:port")

// 移除副本集成员
rs.remove("hostname:port")

// 重新配置副本集
cfg = rs.conf()
cfg.members[0].priority = 2
rs.reconfig(cfg)
```

### Redis主从复制
```bash
# 查看复制信息
redis-cli INFO replication

# 配置从库
redis-cli SLAVEOF master_host master_port

# 断开主从关系
redis-cli SLAVEOF NO ONE

# 查看从库延迟
redis-cli INFO replication | grep -E "(master_repl_offset|slave_repl_offset)"

# 配置哨兵监控
# sentinel.conf配置示例
sentinel monitor mymaster master_host master_port 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
```

---

## 安全管理

### 用户权限审计
```sql
-- MySQL用户权限检查
SELECT 
    User,
    Host,
    Select_priv,
    Insert_priv,
    Update_priv,
    Delete_priv,
    Create_priv,
    Drop_priv
FROM mysql.user 
WHERE User != '';

-- PostgreSQL用户权限检查
SELECT 
    r.rolname,
    r.rolsuper,
    r.rolinherit,
    r.rolcreaterole,
    r.rolcreatedb,
    r.rolcanlogin,
    ARRAY(SELECT b.rolname
          FROM pg_catalog.pg_auth_members m
          JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)
          WHERE m.member = r.oid) as memberof
FROM pg_catalog.pg_roles r
WHERE r.rolname !~ '^pg_';

-- MongoDB用户权限检查
db.getSiblingDB('admin').system.users.find().pretty()
```

### 连接安全检查
```bash
# 查看数据库连接来源
netstat -an | grep :3306 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr

# MySQL连接白名单检查
mysql -u root -p -e "SELECT host,user FROM mysql.user WHERE user != '';"

# PostgreSQL连接限制检查
psql -U postgres -c "SHOW max_connections;"
psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# SSL连接检查
mysql -u root -p -e "SHOW VARIABLES LIKE '%ssl%';"
psql -U postgres -c "SELECT name, setting FROM pg_settings WHERE name LIKE '%ssl%';"
```

### 安全配置检查
```sql
-- MySQL安全配置
SHOW VARIABLES LIKE 'validate_password%';
SHOW VARIABLES LIKE 'sql_mode';
SHOW VARIABLES LIKE 'log_error';

-- PostgreSQL安全配置
SHOW ssl;
SHOW log_statement;
SHOW password_encryption;

-- 审计日志配置
-- MySQL: general_log, slow_query_log
-- PostgreSQL: log_statement, log_duration
-- MongoDB: system.profile
```

---

## 连接池管理

### 连接池监控
```bash
# 查看当前连接数
mysql -u root -p -e "SHOW STATUS LIKE 'Threads_connected';"
psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# 查看最大连接数配置
mysql -u root -p -e "SHOW VARIABLES LIKE 'max_connections';"
psql -U postgres -c "SHOW max_connections;"

# 查看连接池使用情况
# (具体命令取决于使用的连接池实现)
```

### 连接池配置优化
```yaml
# MySQL连接池配置示例
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000

# PostgreSQL连接池配置示例
spring:
  datasource:
    hikari:
      maximum-pool-size: 25
      minimum-idle: 10
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
```

### 连接泄漏检测
```sql
-- MySQL长连接检测
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
WHERE TIME > 300 
AND COMMAND != 'Sleep';

-- PostgreSQL长事务检测
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
WHERE state_change < NOW() - INTERVAL '5 minutes'
AND state != 'idle';
```

---

## 索引管理

### 索引性能分析
```sql
-- MySQL索引使用统计
SELECT 
    object_schema,
    object_name,
    index_name,
    count_read,
    count_write,
    sum_number_of_bytes_read,
    sum_number_of_bytes_write
FROM performance_schema.table_io_waits_summary_by_index_usage 
WHERE index_name IS NOT NULL 
ORDER BY sum_number_of_bytes_read DESC;

-- PostgreSQL索引效率分析
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes 
JOIN pg_index USING (indexrelid)
WHERE idx_scan > 0 
ORDER BY idx_tup_read / NULLIF(idx_scan, 0) DESC;

-- 索引碎片分析
SELECT 
    tblpages,
    est_pages,
    est_pages_ff,
    tblpages/est_pages_ff AS ratio
FROM pgstattuple('table_name');
```

### 索引优化建议
```sql
-- MySQL索引优化工具
-- 使用pt-index-usage分析索引使用情况
pt-index-usage /var/log/mysql/slow.log --host localhost --user root --password

-- PostgreSQL索引建议
-- 使用pg_qualstats扩展收集查询条件统计
CREATE EXTENSION pg_qualstats;
SELECT * FROM pg_qualstats_pretty();

-- 索引重建
-- MySQL
ALTER TABLE table_name ENGINE=InnoDB;

-- PostgreSQL
REINDEX TABLE table_name;
```

---

## 故障排查

### 常见错误诊断
```bash
# MySQL错误日志查看
tail -f /var/log/mysql/error.log
grep -i "error\|warning" /var/log/mysql/error.log

# PostgreSQL错误日志查看
tail -f /var/log/postgresql/postgresql-*.log
journalctl -u postgresql -f

# MongoDB错误日志查看
tail -f /var/log/mongodb/mongod.log
mongo --eval "db.adminCommand('getLog', 'global')"

# Redis错误日志查看
tail -f /var/log/redis/redis-server.log
redis-cli INFO server | grep error
```

### 性能瓶颈分析
```bash
# 系统层面分析
top
iostat -x 1
vmstat 1

# 数据库锁等待分析
# MySQL
SHOW ENGINE INNODB STATUS\G | grep -A 20 "TRANSACTIONS"

# PostgreSQL
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

# 死锁检测
# MySQL
SHOW ENGINE INNODB STATUS\G | grep -A 50 "LATEST DETECTED DEADLOCK"

# PostgreSQL
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.query AS blocked_statement,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

### 磁盘空间问题
```bash
# 查看数据库文件大小
# MySQL
du -sh /var/lib/mysql/*

# PostgreSQL
du -sh /var/lib/postgresql/*/main/*

# MongoDB
du -sh /var/lib/mongodb/*

# 查看表空间使用
# MySQL
SELECT 
    table_schema,
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size(MB)'
FROM information_schema.tables 
ORDER BY (data_length + index_length) DESC;

# PostgreSQL
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 自动化运维

### 监控脚本示例
```bash
#!/bin/bash
# database_monitor.sh - 数据库监控脚本

# 配置
DB_HOST="localhost"
DB_USER="monitor"
DB_PASS="password"
ALERT_EMAIL="admin@example.com"

# MySQL监控
check_mysql() {
    mysql -h$DB_HOST -u$DB_USER -p$DB_PASS -e "SELECT 1" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "MySQL数据库连接失败" | mail -s "Database Alert" $ALERT_EMAIL
    fi
    
    # 检查连接数
    connections=$(mysql -h$DB_HOST -u$DB_USER -p$DB_PASS -e "SHOW STATUS LIKE 'Threads_connected'" | awk 'NR==2{print $2}')
    max_connections=$(mysql -h$DB_HOST -u$DB_USER -p$DB_PASS -e "SHOW VARIABLES LIKE 'max_connections'" | awk 'NR==2{print $2}')
    usage_percent=$((connections * 100 / max_connections))
    
    if [ $usage_percent -gt 80 ]; then
        echo "MySQL连接数使用率过高: ${usage_percent}%" | mail -s "Database Alert" $ALERT_EMAIL
    fi
}

# PostgreSQL监控
check_postgresql() {
    psql -h$DB_HOST -U$DB_USER -c "SELECT 1" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "PostgreSQL数据库连接失败" | mail -s "Database Alert" $ALERT_EMAIL
    fi
}

# MongoDB监控
check_mongodb() {
    mongo --host $DB_HOST --eval "db.adminCommand('ping')" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "MongoDB数据库连接失败" | mail -s "Database Alert" $ALERT_EMAIL
    fi
}

# 执行检查
check_mysql
check_postgresql
check_mongodb
```

### 备份自动化脚本
```bash
#!/bin/bash
# database_backup.sh - 数据库自动备份脚本

BACKUP_DIR="/backup/database"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# MySQL备份
backup_mysql() {
    mysqldump -u root -p$password --single-transaction --routines --triggers database_name | \
    gzip > $BACKUP_DIR/mysql_backup_${DATE}.sql.gz
    
    # 清理旧备份
    find $BACKUP_DIR -name "mysql_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
}

# PostgreSQL备份
backup_postgresql() {
    pg_dump -U postgres database_name | gzip > $BACKUP_DIR/pg_backup_${DATE}.sql.gz
    
    # 清理旧备份
    find $BACKUP_DIR -name "pg_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
}

# 执行备份
backup_mysql
backup_postgresql

# 发送备份完成通知
echo "Database backup completed at $(date)" | mail -s "Backup Report" admin@example.com
```

---

## 最佳实践

### 配置优化建议
```ini
# MySQL配置优化
[mysqld]
# 连接相关
max_connections = 200
max_connect_errors = 100000

# 缓冲区设置
innodb_buffer_pool_size = 2G
innodb_log_file_size = 256M
key_buffer_size = 128M

# 查询优化
query_cache_type = 1
query_cache_size = 64M
tmp_table_size = 64M
max_heap_table_size = 64M

# 日志设置
slow_query_log = 1
long_query_time = 1
log_queries_not_using_indexes = 1

# PostgreSQL配置优化
# postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
max_connections = 100
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
```

### 监控告警设置
```yaml
# Prometheus告警规则示例
groups:
- name: database.alerts
  rules:
  - alert: DatabaseDown
    expr: up{job=~"mysql|postgresql|mongodb"} == 0
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Database instance {{ $labels.instance }} down"
      
  - alert: HighConnectionUsage
    expr: (mysql_global_status_threads_connected / mysql_global_variables_max_connections) * 100 > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High connection usage on {{ $labels.instance }}"
      
  - alert: SlowQueries
    expr: rate(mysql_global_status_slow_queries[5m]) > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High rate of slow queries on {{ $labels.instance }}"
```

### 安全加固建议
```bash
# 数据库安全加固清单
# 1. 修改默认端口
# 2. 禁用root远程登录
# 3. 定期更新和打补丁
# 4. 启用SSL加密连接
# 5. 实施最小权限原则
# 6. 定期审计和日志分析
# 7. 配置防火墙规则
# 8. 启用审计日志
# 9. 定期备份和恢复测试
# 10. 实施访问控制策略
```

---