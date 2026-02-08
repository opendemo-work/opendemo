# Database 技术栈命名大全

本文件定义了数据库技术栈中各类对象、配置、监控指标的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、数据库对象命名规范

### 1.1 表命名规范
```sql
-- 核心业务表
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    order_status ENUM('pending', 'processing', 'completed', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 关联关系表
CREATE TABLE user_roles (
    user_id BIGINT,
    role_id INT,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- 历史记录表
CREATE TABLE order_history (
    history_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    status_from VARCHAR(20),
    status_to VARCHAR(20) NOT NULL,
    changed_by VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

### 1.2 索引命名规范
```sql
-- 主键索引（自动生成）
-- ALTER TABLE users ADD PRIMARY KEY (user_id);

-- 唯一索引
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- 普通索引
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_status_created ON orders(order_status, created_at);

-- 复合索引
CREATE INDEX idx_user_orders_status_date ON orders(user_id, order_status, created_at);
CREATE INDEX idx_products_category_price ON products(category_id, price DESC);

-- 全文索引
CREATE FULLTEXT INDEX idx_articles_content ON articles(content);
CREATE FULLTEXT INDEX idx_products_name_desc ON products(name, description);
```

### 1.3 视图命名规范
```sql
-- 基础视图
CREATE VIEW user_summary AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username, u.email;

-- 复杂业务视图
CREATE VIEW order_analytics_daily AS
SELECT 
    DATE(o.created_at) as order_date,
    COUNT(*) as order_count,
    SUM(total_amount) as daily_revenue,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT user_id) as unique_customers
FROM orders o
WHERE o.order_status = 'completed'
GROUP BY DATE(o.created_at)
ORDER BY order_date DESC;

-- 性能优化视图
CREATE VIEW user_recent_activity AS
SELECT 
    u.user_id,
    u.username,
    COALESCE(recent_orders.last_order_date, '1970-01-01') as last_activity,
    recent_orders.recent_order_count,
    CASE 
        WHEN recent_orders.last_order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 'active'
        WHEN recent_orders.last_order_date >= DATE_SUB(NOW(), INTERVAL 90 DAY) THEN 'inactive'
        ELSE 'churned'
    END as user_status
FROM users u
LEFT JOIN (
    SELECT 
        user_id,
        MAX(created_at) as last_order_date,
        COUNT(*) as recent_order_count
    FROM orders 
    WHERE created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)
    GROUP BY user_id
) recent_orders ON u.user_id = recent_orders.user_id;
```

## 二、存储过程和函数命名规范

### 2.1 存储过程命名
```sql
-- 数据操作存储过程
DELIMITER //

CREATE PROCEDURE sp_create_user(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255),
    OUT p_user_id BIGINT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    INSERT INTO users (username, email, password_hash)
    VALUES (p_username, p_email, p_password_hash);
    
    SET p_user_id = LAST_INSERT_ID();
    
    -- 记录审计日志
    INSERT INTO audit_logs (table_name, record_id, action, created_at)
    VALUES ('users', p_user_id, 'INSERT', NOW());
    
    COMMIT;
END //

-- 批量处理存储过程
CREATE PROCEDURE sp_process_pending_orders(
    IN p_batch_size INT DEFAULT 1000,
    OUT p_processed_count INT
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_order_id BIGINT;
    DECLARE v_cursor CURSOR FOR 
        SELECT order_id FROM orders 
        WHERE order_status = 'pending' 
        LIMIT p_batch_size;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    SET p_processed_count = 0;
    
    OPEN v_cursor;
    
    read_loop: LOOP
        FETCH v_cursor INTO v_order_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- 处理单个订单
        CALL sp_process_single_order(v_order_id);
        SET p_processed_count = p_processed_count + 1;
    END LOOP;
    
    CLOSE v_cursor;
END //

-- 报表生成存储过程
CREATE PROCEDURE sp_generate_monthly_report(
    IN p_year INT,
    IN p_month INT,
    OUT p_report_id BIGINT
)
BEGIN
    DECLARE v_start_date DATE;
    DECLARE v_end_date DATE;
    
    SET v_start_date = DATE(CONCAT(p_year, '-', p_month, '-01'));
    SET v_end_date = LAST_DAY(v_start_date);
    
    -- 生成报告数据
    INSERT INTO monthly_reports (report_year, report_month, generated_at)
    VALUES (p_year, p_month, NOW());
    
    SET p_report_id = LAST_INSERT_ID();
    
    -- 填充报告详情
    INSERT INTO report_details (report_id, metric_name, metric_value)
    SELECT 
        p_report_id,
        'total_revenue',
        SUM(total_amount)
    FROM orders 
    WHERE created_at BETWEEN v_start_date AND v_end_date
    AND order_status = 'completed';
    
END //
```

### 2.2 函数命名规范
```sql
-- 校验函数
DELIMITER //

CREATE FUNCTION fn_validate_email(p_email VARCHAR(100))
RETURNS BOOLEAN
READS SQL DATA
DETERMINISTIC
BEGIN
    IF p_email IS NULL OR p_email = '' THEN
        RETURN FALSE;
    END IF;
    
    IF p_email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END //

-- 计算函数
CREATE FUNCTION fn_calculate_order_total(p_order_id BIGINT)
RETURNS DECIMAL(10,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(10,2) DEFAULT 0.00;
    
    SELECT SUM(quantity * unit_price) INTO v_total
    FROM order_items
    WHERE order_id = p_order_id;
    
    RETURN COALESCE(v_total, 0.00);
END //

-- 转换函数
CREATE FUNCTION fn_format_phone_number(p_phone VARCHAR(20))
RETURNS VARCHAR(20)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_formatted VARCHAR(20);
    
    -- 移除所有非数字字符
    SET v_formatted = REGEXP_REPLACE(p_phone, '[^0-9]', '');
    
    -- 格式化为标准格式
    IF LENGTH(v_formatted) = 10 THEN
        RETURN CONCAT('(', SUBSTRING(v_formatted, 1, 3), ') ', 
                     SUBSTRING(v_formatted, 4, 3), '-', 
                     SUBSTRING(v_formatted, 7, 4));
    ELSE
        RETURN p_phone;
    END IF;
END //
```

## 三、触发器命名规范

### 3.1 数据完整性触发器
```sql
-- 更新时间戳触发器
DELIMITER //

CREATE TRIGGER tr_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END //

-- 审计日志触发器
CREATE TRIGGER tr_orders_audit_insert
    AFTER INSERT ON orders
    FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (
        table_name, 
        record_id, 
        action, 
        old_values, 
        new_values, 
        created_at
    ) VALUES (
        'orders',
        NEW.order_id,
        'INSERT',
        NULL,
        JSON_OBJECT(
            'order_id', NEW.order_id,
            'user_id', NEW.user_id,
            'total_amount', NEW.total_amount,
            'order_status', NEW.order_status
        ),
        NOW()
    );
END //

-- 业务规则触发器
CREATE TRIGGER tr_inventory_check
    BEFORE INSERT ON order_items
    FOR EACH ROW
BEGIN
    DECLARE v_stock_quantity INT;
    
    SELECT stock_quantity INTO v_stock_quantity
    FROM products 
    WHERE product_id = NEW.product_id;
    
    IF v_stock_quantity < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient inventory for this product';
    END IF;
END //
```

## 四、配置和参数命名规范

### 4.1 数据库配置参数
```sql
-- 连接池配置
SET GLOBAL max_connections = 200;
SET GLOBAL thread_cache_size = 50;
SET GLOBAL connection_timeout = 60;

-- 缓存配置
SET GLOBAL innodb_buffer_pool_size = 1073741824;  -- 1GB
SET GLOBAL query_cache_size = 67108864;           -- 64MB
SET GLOBAL tmp_table_size = 33554432;             -- 32MB

-- 日志配置
SET GLOBAL general_log = 'ON';
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2.0;
SET GLOBAL log_output = 'TABLE';

-- 复制配置
SET GLOBAL binlog_format = 'ROW';
SET GLOBAL sync_binlog = 1;
SET GLOBAL expire_logs_days = 7;
```

### 4.2 会话变量命名
```sql
-- 查询优化变量
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';
SET SESSION sort_buffer_size = 2097152;  -- 2MB
SET SESSION join_buffer_size = 262144;   -- 256KB
SET SESSION read_rnd_buffer_size = 524288; -- 512KB

-- 事务控制变量
SET SESSION transaction_isolation = 'READ-COMMITTED';
SET SESSION autocommit = 0;
SET SESSION lock_wait_timeout = 50;
```

## 五、监控和性能指标命名

### 5.1 性能监控查询
```sql
-- 连接状态监控
SELECT 
    VARIABLE_NAME,
    VARIABLE_VALUE
FROM information_schema.GLOBAL_STATUS 
WHERE VARIABLE_NAME IN (
    'Threads_connected',
    'Threads_running',
    'Connections',
    'Max_used_connections'
);

-- 查询性能统计
SELECT 
    DIGEST_TEXT,
    COUNT_STAR,
    AVG_TIMER_WAIT/1000000000 as avg_latency_sec,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest
WHERE SCHEMA_NAME = 'your_database'
ORDER BY AVG_TIMER_WAIT DESC
LIMIT 10;

-- 缓冲池使用情况
SELECT 
    pool_id,
    block_id,
    state,
    chunk_size
FROM information_schema.INNODB_BUFFER_PAGE
WHERE table_name = '`your_database`.`your_table`';

-- 锁等待分析
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
```

### 5.2 慢查询分析
```sql
-- 慢查询日志分析
SELECT 
    start_time,
    user_host,
    query_time,
    lock_time,
    rows_sent,
    rows_examined,
    db,
    sql_text
FROM mysql.slow_log
WHERE start_time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY query_time DESC
LIMIT 20;

-- 实时慢查询监控
SELECT 
    ID,
    USER,
    HOST,
    DB,
    COMMAND,
    TIME,
    STATE,
    INFO
FROM information_schema.PROCESSLIST
WHERE TIME > 5  -- 执行超过5秒的查询
AND COMMAND != 'Sleep'
ORDER BY TIME DESC;
```

## 六、备份和恢复命名规范

### 6.1 备份文件命名
```bash
# 完整备份命名
backup_full_${DATABASE_NAME}_${DATE}_${TIMESTAMP}.sql.gz
backup_full_production_20231201_143022.sql.gz

# 增量备份命名
backup_incremental_${DATABASE_NAME}_${DATE}_${TIMESTAMP}.sql.gz
backup_incremental_production_20231201_143022.sql.gz

# 二进制日志备份
backup_binlog_${DATABASE_NAME}_${DATE}_${TIMESTAMP}.tar.gz
backup_binlog_production_20231201_143022.tar.gz

# 表级备份
backup_table_${DATABASE_NAME}_${TABLE_NAME}_${DATE}_${TIMESTAMP}.sql.gz
backup_table_production_users_20231201_143022.sql.gz
```

### 6.2 恢复脚本命名
```bash
#!/bin/bash
# restore_database.sh - 数据库恢复脚本

DATABASE_NAME=$1
BACKUP_FILE=$2
RESTORE_POINT=$3  # 可选的时间点

# 恢复前检查
validate_backup_integrity() {
    if [[ ! -f "$BACKUP_FILE" ]]; then
        echo "ERROR: Backup file $BACKUP_FILE not found"
        exit 1
    fi
    
    if ! gzip -t "$BACKUP_FILE"; then
        echo "ERROR: Backup file integrity check failed"
        exit 1
    fi
}

# 完整恢复
perform_full_restore() {
    echo "Starting full database restore..."
    
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" << EOF
    DROP DATABASE IF EXISTS ${DATABASE_NAME};
    CREATE DATABASE ${DATABASE_NAME};
EOF
    
    gunzip -c "$BACKUP_FILE" | mysql -u root -p"${MYSQL_ROOT_PASSWORD}" ${DATABASE_NAME}
    
    echo "Full restore completed"
}

# 时间点恢复
perform_point_in_time_recovery() {
    local recovery_timestamp=$1
    
    echo "Starting point-in-time recovery to $recovery_timestamp..."
    
    # 应用完整备份
    perform_full_restore
    
    # 应用二进制日志
    mysqlbinlog \
        --start-datetime="$(date -d "$recovery_timestamp" '+%Y-%m-%d %H:%M:%S')" \
        /var/log/mysql/mysql-bin.* | \
        mysql -u root -p"${MYSQL_ROOT_PASSWORD}" ${DATABASE_NAME}
    
    echo "Point-in-time recovery completed"
}

# 主函数
main() {
    validate_backup_integrity
    
    if [[ -n "$RESTORE_POINT" ]]; then
        perform_point_in_time_recovery "$RESTORE_POINT"
    else
        perform_full_restore
    fi
    
    # 验证恢复结果
    verify_restored_data
}

main "$@"
```

## 七、高可用和复制命名规范

### 7.1 主从复制配置
```sql
-- 主库配置
[mysqld]
server_id = 1
log_bin = mysql-bin
binlog_format = ROW
expire_logs_days = 7
sync_binlog = 1
innodb_flush_log_at_trx_commit = 1

-- 从库配置
[mysqld]
server_id = 2
relay_log = relay-bin
read_only = 1
skip_slave_start = 1

-- 复制用户创建
CREATE USER 'repl_user'@'%' IDENTIFIED BY 'secure_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
FLUSH PRIVILEGES;

-- 启动复制
CHANGE MASTER TO
    MASTER_HOST='master-host',
    MASTER_USER='repl_user',
    MASTER_PASSWORD='secure_password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=107;

START SLAVE;
```

### 7.2 集群节点命名
```bash
# MySQL集群节点
mysql-primary-01.dc1.company.com     # 主数据中心主节点
mysql-secondary-01.dc1.company.com   # 主数据中心从节点1
mysql-secondary-02.dc1.company.com   # 主数据中心从节点2
mysql-primary-01.dc2.company.com     # 灾备数据中心主节点

# PostgreSQL集群
postgres-primary.dc1.company.com     # 主节点
postgres-standby-1.dc1.company.com   # 热备节点1
postgres-standby-2.dc1.company.com   # 热备节点2
postgres-async.dc2.company.com       # 异步备节点

# Redis集群
redis-master-01.dc1.company.com:6379    # 主节点1
redis-slave-01.dc1.company.com:6379     # 从节点1
redis-master-02.dc1.company.com:6380    # 主节点2
redis-slave-02.dc1.company.com:6380     # 从节点2
```

## 八、安全和权限命名规范

### 8.1 用户和角色命名
```sql
-- 应用用户
CREATE USER 'app_user'@'%' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON production_db.* TO 'app_user'@'%';

-- 只读用户
CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'readonly_password';
GRANT SELECT ON production_db.* TO 'readonly_user'@'%';

-- 管理员用户
CREATE USER 'db_admin'@'localhost' IDENTIFIED BY 'admin_password';
GRANT ALL PRIVILEGES ON *.* TO 'db_admin'@'localhost' WITH GRANT OPTION;

-- 服务账户
CREATE USER 'backup_user'@'localhost' IDENTIFIED BY 'backup_password';
GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER ON production_db.* TO 'backup_user'@'localhost';

-- 应用特定角色
CREATE ROLE 'app_read_role';
CREATE ROLE 'app_write_role';
CREATE ROLE 'app_admin_role';

GRANT SELECT ON production_db.* TO 'app_read_role';
GRANT INSERT, UPDATE, DELETE ON production_db.* TO 'app_write_role';
GRANT ALL ON production_db.* TO 'app_admin_role';

-- 用户分配角色
GRANT 'app_read_role' TO 'reporting_user'@'%';
GRANT 'app_write_role' TO 'api_user'@'%';
GRANT 'app_admin_role' TO 'power_user'@'%';
```

### 8.2 审计和监控
```sql
-- 审计日志表
CREATE TABLE audit_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(64) NOT NULL,
    record_id VARCHAR(64),
    action ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    old_values JSON,
    new_values JSON,
    user_name VARCHAR(80),
    client_ip VARCHAR(45),
    session_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_table_action (table_name, action),
    INDEX idx_audit_created_at (created_at)
);

-- 登录审计
CREATE TABLE login_audit (
    audit_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(80) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP NULL,
    client_ip VARCHAR(45),
    user_agent TEXT,
    login_status ENUM('SUCCESS', 'FAILED') NOT NULL,
    failure_reason VARCHAR(255),
    INDEX idx_login_user_time (user_name, login_time),
    INDEX idx_login_status_time (login_status, login_time)
);

-- 敏感操作监控
DELIMITER //

CREATE TRIGGER tr_sensitive_data_access
    AFTER SELECT ON users
    FOR EACH ROW
BEGIN
    IF NEW.ssn IS NOT NULL OR NEW.credit_card IS NOT NULL THEN
        INSERT INTO sensitive_data_access_log (
            user_name,
            table_name,
            record_id,
            accessed_fields,
            access_time
        ) VALUES (
            USER(),
            'users',
            NEW.user_id,
            CASE 
                WHEN NEW.ssn IS NOT NULL AND NEW.credit_card IS NOT NULL THEN 'ssn,credit_card'
                WHEN NEW.ssn IS NOT NULL THEN 'ssn'
                WHEN NEW.credit_card IS NOT NULL THEN 'credit_card'
            END,
            NOW()
        );
    END IF;
END //
```

## 九、故障排查和诊断命名规范

### 9.1 性能诊断查询
```sql
-- 锁等待诊断
SELECT 
    p.ID as process_id,
    p.USER,
    p.HOST,
    p.DB,
    p.COMMAND,
    p.TIME as duration_seconds,
    p.STATE,
    p.INFO as current_query,
    t.trx_id,
    t.trx_state,
    t.trx_started,
    t.trx_isolation_level
FROM information_schema.PROCESSLIST p
JOIN information_schema.innodb_trx t ON p.ID = t.trx_mysql_thread_id
WHERE p.TIME > 10
ORDER BY p.TIME DESC;

-- 索引使用分析
SELECT 
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    s.INDEX_NAME,
    s.COLUMN_NAME,
    s.SEQ_IN_INDEX,
    s.CARDINALITY,
    t.TABLE_ROWS,
    ROUND((s.CARDINALITY / t.TABLE_ROWS) * 100, 2) as selectivity_pct
FROM information_schema.STATISTICS s
JOIN information_schema.TABLES t ON s.TABLE_SCHEMA = t.TABLE_SCHEMA 
    AND s.TABLE_NAME = t.TABLE_NAME
WHERE t.TABLE_SCHEMA = 'your_database'
    AND s.NON_UNIQUE = 0
ORDER BY t.TABLE_NAME, s.INDEX_NAME, s.SEQ_IN_INDEX;

-- 表碎片分析
SELECT 
    table_schema,
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb,
    ROUND((data_free / 1024 / 1024), 2) AS free_space_mb,
    ROUND((data_free / (data_length + index_length)) * 100, 2) AS fragmentation_pct
FROM information_schema.tables
WHERE table_schema = 'your_database'
    AND data_free > 0
ORDER BY fragmentation_pct DESC;
```

### 9.2 容量规划查询
```sql
-- 数据库增长趋势
SELECT 
    DATE(FROM_UNIXTIME(UNIX_TIMESTAMP(ts) - MOD(UNIX_TIMESTAMP(ts), 86400))) as day,
    ROUND(SUM(variable_value)/1024/1024/1024, 2) as size_gb
FROM (
    SELECT 
        ts,
        variable_value
    FROM metrics.db_size_history
    WHERE metric_name = 'data_length'
        AND ts >= DATE_SUB(NOW(), INTERVAL 30 DAY)
) daily_sizes
GROUP BY DATE(FROM_UNIXTIME(UNIX_TIMESTAMP(ts) - MOD(UNIX_TIMESTAMP(ts), 86400)))
ORDER BY day;

-- 表增长分析
SELECT 
    table_name,
    ROUND((data_length + index_length) / 1024 / 1024, 2) as current_size_mb,
    table_rows,
    ROUND((data_length + index_length) / table_rows, 2) as avg_row_size_bytes,
    create_time,
    update_time
FROM information_schema.tables
WHERE table_schema = 'your_database'
ORDER BY (data_length + index_length) DESC;
```

## 十、最佳实践示例

### 10.1 数据库健康检查脚本
```bash
#!/bin/bash
# database_health_check.sh - 数据库健康检查脚本

DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"3306"}
DB_USER=${DB_USER:-"monitor"}
DB_PASSWORD=${DB_PASSWORD:-"monitor_password"}
DB_NAME=${DB_NAME:-"production_db"}

# 健康检查阈值
CONNECTION_THRESHOLD=80
QUERY_LATENCY_THRESHOLD_MS=1000
REPLICATION_LAG_THRESHOLD_SEC=30

# 检查数据库连接
check_connection() {
    if mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" \
        -e "SELECT 1" >/dev/null 2>&1; then
        echo "OK: Database connection successful"
        return 0
    else
        echo "CRITICAL: Database connection failed"
        return 1
    fi
}

# 检查连接数
check_connections() {
    local current_connections=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" \
        -e "SHOW STATUS LIKE 'Threads_connected';" -sN | awk '{print $2}')
    local max_connections=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" \
        -e "SHOW VARIABLES LIKE 'max_connections';" -sN | awk '{print $2}')
    local usage_percent=$((current_connections * 100 / max_connections))
    
    if [[ $usage_percent -gt $CONNECTION_THRESHOLD ]]; then
        echo "WARNING: High connection usage ${usage_percent}% (${current_connections}/${max_connections})"
        return 1
    else
        echo "OK: Connection usage ${usage_percent}% (${current_connections}/${max_connections})"
        return 0
    fi
}

# 检查查询性能
check_query_performance() {
    local start_time=$(date +%s%3N)
    mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" \
        -e "SELECT SLEEP(0.001);" >/dev/null 2>&1
    local end_time=$(date +%s%3N)
    local latency=$((end_time - start_time))
    
    if [[ $latency -gt $QUERY_LATENCY_THRESHOLD_MS ]]; then
        echo "WARNING: Query latency high: ${latency}ms"
        return 1
    else
        echo "OK: Query latency: ${latency}ms"
        return 0
    fi
}

# 检查复制延迟
check_replication_lag() {
    local lag_seconds=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" \
        -e "SHOW SLAVE STATUS\G" 2>/dev/null | \
        grep "Seconds_Behind_Master" | awk '{print $2}')
    
    if [[ -z "$lag_seconds" ]] || [[ "$lag_seconds" == "NULL" ]]; then
        echo "INFO: Not a replication slave or replication not configured"
        return 0
    elif [[ $lag_seconds -gt $REPLICATION_LAG_THRESHOLD_SEC ]]; then
        echo "WARNING: Replication lag: ${lag_seconds} seconds"
        return 1
    else
        echo "OK: Replication lag: ${lag_seconds} seconds"
        return 0
    fi
}

# 主检查函数
main() {
    local exit_code=0
    
    echo "=== Database Health Check Report ==="
    echo "Time: $(date)"
    echo "Host: $DB_HOST:$DB_PORT"
    echo ""
    
    check_connection || exit_code=2
    check_connections || [[ $exit_code -eq 0 ]] && exit_code=1
    check_query_performance || [[ $exit_code -eq 0 ]] && exit_code=1
    check_replication_lag || [[ $exit_code -eq 0 ]] && exit_code=1
    
    echo ""
    echo "=== Summary ==="
    case $exit_code in
        0) echo "Overall Status: OK" ;;
        1) echo "Overall Status: WARNING" ;;
        2) echo "Overall Status: CRITICAL" ;;
    esac
    
    exit $exit_code
}

main "$@"
```

### 10.2 自动化维护脚本
```sql
-- 数据库维护存储过程
DELIMITER //

CREATE PROCEDURE sp_database_maintenance()
BEGIN
    DECLARE v_start_time TIMESTAMP;
    DECLARE v_end_time TIMESTAMP;
    DECLARE v_status VARCHAR(20) DEFAULT 'SUCCESS';
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            @sqlstate = RETURNED_SQLSTATE,
            @errno = MYSQL_ERRNO,
            @text = MESSAGE_TEXT;
        
        SET v_status = 'FAILED';
        INSERT INTO maintenance_log (
            maintenance_type,
            start_time,
            end_time,
            status,
            error_message
        ) VALUES (
            'DATABASE_MAINTENANCE',
            v_start_time,
            NOW(),
            v_status,
            CONCAT(@sqlstate, ':', @errno, ':', @text)
        );
        
        RESIGNAL;
    END;
    
    SET v_start_time = NOW();
    
    -- 记录维护开始
    INSERT INTO maintenance_log (
        maintenance_type,
        start_time,
        status
    ) VALUES (
        'DATABASE_MAINTENANCE',
        v_start_time,
        'RUNNING'
    );
    
    -- 清理旧的日志数据
    DELETE FROM audit_logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
    DELETE FROM login_audit WHERE login_time < DATE_SUB(NOW(), INTERVAL 180 DAY);
    
    -- 优化表
    OPTIMIZE TABLE users, orders, products;
    
    -- 更新统计信息
    ANALYZE TABLE users, orders, products;
    
    -- 检查表完整性
    CHECK TABLE users, orders, products;
    
    SET v_end_time = NOW();
    
    -- 记录维护完成
    UPDATE maintenance_log 
    SET end_time = v_end_time,
        status = v_status
    WHERE maintenance_type = 'DATABASE_MAINTENANCE'
    AND start_time = v_start_time;
    
END //
```

---

**注意事项：**
1. 所有数据库对象命名应遵循一致的命名约定
2. 生产环境中必须启用审计日志和监控
3. 定期进行备份验证和恢复演练
4. 权限分配应遵循最小权限原则
5. 性能监控应该实时进行，及时发现瓶颈