# 🔐 数据库访问控制管理指南

> 企业级数据库访问控制体系，涵盖用户管理、权限分配、角色控制等完整的访问安全机制，确保数据访问的安全性和合规性

## 📋 案例概述

本案例详细介绍数据库访问控制系统的设计和实施，通过建立完善的用户管理、权限控制和审计机制，确保只有授权用户能够在规定范围内访问数据库资源。

### 🎯 学习目标

- 掌握数据库用户和角色管理体系
- 理解基于角色的访问控制(RBAC)原理
- 实施细粒度的权限控制策略
- 建立访问审计和监控机制
- 制定访问控制最佳实践和安全策略

### ⏱️ 学习时长

- **理论学习**: 3小时
- **实践操作**: 4小时
- **总计**: 7小时

---

## 🔐 访问控制基础理论

### RBAC模型架构

```
┌─────────────────────────────────────────────────┐
│                用户(User)                       │
│  - 系统用户                                     │
│  - 应用用户                                     │
│  - 管理用户                                     │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│                角色(Role)                       │
│  - 管理员角色                                   │
│  - 开发者角色                                   │
│  - 分析师角色                                   │
│  - 应用角色                                     │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│              权限(Permission)                   │
│  - 数据库级权限                                 │
│  - 表级权限                                     │
│  - 列级权限                                     │
│  - 行级权限                                     │
└─────────────────────────────────────────────────┘
```

### 访问控制层级

```
系统级访问控制
    ↓
数据库级访问控制
    ↓
模式级访问控制
    ↓
表级访问控制
    ↓
行级访问控制
    ↓
列级访问控制
```

---

## 🐬 MySQL访问控制实践

### 1. 用户管理基础

#### 用户创建和管理
```sql
-- 创建不同类型的用户
-- 应用程序用户
CREATE USER 'app_user'@'192.168.1.%' 
IDENTIFIED BY 'StrongAppPass123!' 
PASSWORD EXPIRE INTERVAL 90 DAY;

-- 管理员用户
CREATE USER 'db_admin'@'localhost' 
IDENTIFIED BY 'AdminSecurePass456!' 
ACCOUNT LOCK;

-- 只读分析用户
CREATE USER 'analyst'@'10.0.0.%' 
IDENTIFIED BY 'ReadOnlyPass789!';

-- 临时维护用户
CREATE USER 'maintenance'@'%' 
IDENTIFIED BY 'TempMaintenancePass!' 
VALID UNTIL '2024-12-31 23:59:59';

-- 查看用户信息
SELECT User, Host, authentication_string, password_expired 
FROM mysql.user 
WHERE User LIKE '%app%';
```

#### 用户属性配置
```sql
-- 设置用户资源限制
ALTER USER 'app_user'@'192.168.1.%' 
WITH MAX_QUERIES_PER_HOUR 1000
     MAX_UPDATES_PER_HOUR 100
     MAX_CONNECTIONS_PER_HOUR 50
     MAX_USER_CONNECTIONS 5;

-- 账户锁定管理
ALTER USER 'maintenance'@'%' ACCOUNT LOCK;
-- ALTER USER 'maintenance'@'%' ACCOUNT UNLOCK;

-- 密码策略设置
ALTER USER 'app_user'@'192.168.1.%' 
PASSWORD HISTORY 5 
PASSWORD REUSE INTERVAL 365 DAY 
FAILED_LOGIN_ATTEMPTS 3 
PASSWORD_LOCK_TIME 1;

-- 验证用户配置
SHOW CREATE USER 'app_user'@'192.168.1.%';
```

### 2. 权限管理体系

#### 细粒度权限分配
```sql
-- 数据库级权限
GRANT ALL PRIVILEGES ON ecommerce.* TO 'db_admin'@'localhost';
GRANT CREATE, ALTER, DROP ON analytics.* TO 'senior_dev'@'%';

-- 表级权限
GRANT SELECT, INSERT, UPDATE ON ecommerce.users TO 'app_user'@'192.168.1.%';
GRANT SELECT, INSERT, UPDATE ON ecommerce.orders TO 'app_user'@'192.168.1.%';
GRANT SELECT ON ecommerce.products TO 'app_user'@'192.168.1.%';

-- 列级权限
GRANT SELECT (user_id, username, email) ON ecommerce.users TO 'analyst'@'10.0.0.%';
GRANT UPDATE (last_login, login_count) ON ecommerce.users TO 'app_user'@'192.168.1.%';

-- 存储过程权限
GRANT EXECUTE ON PROCEDURE ecommerce.calculate_discount TO 'app_user'@'192.168.1.%';
GRANT CREATE ROUTINE ON ecommerce.* TO 'senior_dev'@'%';

-- 查看权限分配
SHOW GRANTS FOR 'app_user'@'192.168.1.%';
```

#### 角色-Based权限管理
```sql
-- 创建角色
CREATE ROLE 'app_role', 'readonly_role', 'admin_role';

-- 为角色分配权限
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce.* TO 'app_role';
GRANT SELECT ON ecommerce.* TO 'readonly_role';
GRANT ALL PRIVILEGES ON *.* TO 'admin_role';

-- 激活角色
SET DEFAULT ROLE 'app_role' TO 'app_user'@'192.168.1.%';
SET DEFAULT ROLE 'readonly_role' TO 'analyst'@'10.0.0.%';

-- 动态角色切换
SET ROLE 'app_role';
-- SET ROLE 'readonly_role';
-- SET ROLE NONE; -- 取消所有角色

-- 角色继承
CREATE ROLE 'senior_app_role';
GRANT 'app_role' TO 'senior_app_role';
GRANT CREATE, ALTER ON ecommerce.* TO 'senior_app_role';
```

### 3. 访问审计和监控

#### 启用审计日志
```sql
-- 安装审计插件
INSTALL PLUGIN audit_log SONAME 'audit_log.so';

-- 配置审计策略
SET GLOBAL audit_log_policy = ALL;
SET GLOBAL audit_log_format = JSON;
SET GLOBAL audit_log_rotate_on_size = 1073741824; -- 1GB

-- 针对特定用户的审计
CREATE AUDIT FILTER 'critical_users'
    ONLY_INCLUDE
        QUERY_DDL,
        QUERY_DML,
        CONNECT,
        TABLE_ACCESS;

ALTER USER 'db_admin'@'localhost' AUDIT BY 'critical_users';

-- 查看审计配置
SELECT * FROM mysql.audit_log_filter;
SELECT * FROM mysql.audit_log_user;
```

#### 访问监控脚本
```bash
#!/bin/bash
# mysql_access_monitor.sh - MySQL访问监控脚本

LOG_DIR="/var/log/mysql/access_monitor"
ALERT_EMAIL="security@company.com"

# 监控异常访问模式
monitor_suspicious_access() {
    local query="
        SELECT 
            user,
            host,
            COUNT(*) as access_count,
            MAX(event_time) as last_access
        FROM mysql.audit_log 
        WHERE event_time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
        AND event_type IN ('CONNECT', 'QUERY')
        GROUP BY user, host
        HAVING access_count > 100
        ORDER BY access_count DESC
    "
    
    mysql -e "$query" > $LOG_DIR/suspicious_access_$(date +%Y%m%d_%H%M%S).log
    
    if [ -s $LOG_DIR/suspicious_access_*.log ]; then
        mail -s "MySQL Suspicious Access Alert" $ALERT_EMAIL \
            < $LOG_DIR/suspicious_access_*.log
    fi
}

# 监控权限变更
monitor_privilege_changes() {
    local query="
        SELECT 
            user,
            host,
            event_time,
            command_class,
            sqltext
        FROM mysql.audit_log 
        WHERE event_time >= DATE_SUB(NOW(), INTERVAL 1 DAY)
        AND command_class IN ('grant', 'revoke', 'create_user', 'drop_user')
        ORDER BY event_time DESC
    "
    
    mysql -e "$query" > $LOG_DIR/privilege_changes_$(date +%Y%m%d).log
}

# 执行监控
mkdir -p $LOG_DIR
monitor_suspicious_access
monitor_privilege_changes
```

---

## 🐘 PostgreSQL访问控制实践

### 1. 用户和角色管理

#### 用户创建和配置
```sql
-- 创建不同类型用户
-- 应用用户
CREATE USER app_user WITH 
    PASSWORD 'AppSecurePass123!'
    CONNECTION LIMIT 10
    VALID UNTIL '2025-01-01';

-- 管理员用户
CREATE USER db_admin WITH 
    PASSWORD 'AdminSecurePass456!'
    SUPERUSER
    CREATEDB
    CREATEROLE;

-- 只读用户
CREATE USER analyst WITH 
    PASSWORD 'ReadOnlyPass789!'
    CONNECTION LIMIT 5;

-- 服务账户用户
CREATE USER service_account WITH 
    PASSWORD 'ServiceAccountPass!'
    NOLOGIN; -- 仅用于权限继承
```

#### 角色和组管理
```sql
-- 创建角色组
CREATE ROLE app_users;
CREATE ROLE readonly_users;
CREATE ROLE db_admins;

-- 角色继承关系
GRANT app_users TO db_admins;
GRANT readonly_users TO app_users;

-- 分配用户到角色组
GRANT app_users TO app_user;
GRANT readonly_users TO analyst;
GRANT db_admins TO db_admin;

-- 查看角色成员关系
SELECT 
    r.rolname as role_name,
    m.rolname as member_name
FROM pg_roles r
JOIN pg_auth_members am ON r.oid = am.roleid
JOIN pg_roles m ON m.oid = am.member
ORDER BY r.rolname, m.rolname;
```

### 2. 权限控制体系

#### 对象级权限管理
```sql
-- 数据库级权限
GRANT CONNECT ON DATABASE ecommerce TO app_users;
GRANT CREATE ON DATABASE analytics TO db_admins;

-- 模式级权限
GRANT USAGE ON SCHEMA public TO app_users;
GRANT CREATE ON SCHEMA reporting TO readonly_users;

-- 表级权限
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_users;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_users;

-- 序列权限
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO app_users;

-- 函数权限
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO app_users;

-- 默认权限设置
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_users;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO app_users;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT EXECUTE ON FUNCTIONS TO app_users;
```

#### 行级安全(RLS)控制
```sql
-- 启用行级安全
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 创建策略
CREATE POLICY user_data_isolation ON users
    FOR ALL TO app_users
    USING (tenant_id = current_setting('app.current_tenant')::integer);

CREATE POLICY order_access_control ON orders
    FOR SELECT TO app_users
    USING (user_id IN (
        SELECT id FROM users 
        WHERE tenant_id = current_setting('app.current_tenant')::integer
    ));

-- 管理员策略
CREATE POLICY admin_full_access ON users
    FOR ALL TO db_admins
    USING (true);

-- 查看策略信息
SELECT 
    polname,
    relname,
    polroles,
    polcmd,
    polqual
FROM pg_policy p
JOIN pg_class c ON p.polrelid = c.oid
WHERE relname IN ('users', 'orders');
```

### 3. 访问审计机制

#### 启用日志审计
```sql
-- 配置审计日志
ALTER SYSTEM SET log_statement = 'mod'; -- 记录DDL和DML
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_duration = on;

-- 启用详细查询日志
ALTER SYSTEM SET log_min_duration_statement = 1000; -- 超过1秒的查询

-- 重新加载配置
SELECT pg_reload_conf();

-- 创建审计视图
CREATE VIEW user_access_audit AS
SELECT 
    application_name,
    client_addr,
    client_hostname,
    backend_start,
    query_start,
    state_change,
    state,
    query
FROM pg_stat_activity 
WHERE state = 'active';
```

#### 审计查询示例
```sql
-- 用户活动监控
SELECT 
    usename,
    application_name,
    client_addr,
    COUNT(*) as query_count,
    MAX(query_start) as last_query_time
FROM pg_stat_statements s
JOIN pg_user u ON s.userid = u.usesysid
WHERE s.calls > 100
GROUP BY usename, application_name, client_addr
ORDER BY query_count DESC;

-- 权限变更审计
SELECT 
    query,
    usename,
    application_name,
    query_start
FROM pg_stat_statements 
WHERE query ILIKE '%GRANT%' OR query ILIKE '%REVOKE%'
ORDER BY query_start DESC
LIMIT 50;
```

---

## 🍃 MongoDB访问控制实践

### 1. 用户和角色体系

#### 用户创建和管理
```javascript
// 启用访问控制
// mongod --auth

// 创建管理员用户
use admin
db.createUser({
    user: "admin",
    pwd: "${DB_PASSWORD}",
    roles: [
        { role: "userAdminAnyDatabase", db: "admin" },
        { role: "dbAdminAnyDatabase", db: "admin" },
        { role: "readWriteAnyDatabase", db: "admin" },
        { role: "clusterAdmin", db: "admin" }
    ]
})

// 创建应用用户
use myapp
db.createUser({
    user: "app_user",
    pwd: "${DB_PASSWORD}",
    roles: [
        { role: "readWrite", db: "myapp" },
        { role: "read", db: "config" }
    ],
    customData: {
        department: "engineering",
        team: "backend",
        created_by: "admin"
    }
})

// 创建只读分析用户
db.createUser({
    user: "analyst",
    pwd: "${DB_PASSWORD}",
    roles: [
        { role: "read", db: "myapp" },
        { role: "read", db: "analytics" }
    ]
})
```

#### 自定义角色创建
```javascript
// 创建自定义应用角色
use admin
db.createRole({
    role: "appUserRole",
    privileges: [
        {
            resource: { db: "myapp", collection: "users" },
            actions: [ "find", "insert", "update", "remove" ]
        },
        {
            resource: { db: "myapp", collection: "orders" },
            actions: [ "find", "insert", "update" ]
        },
        {
            resource: { db: "myapp", collection: "" }, // 数据库级别
            actions: [ "collStats", "dbStats" ]
        }
    ],
    roles: []
})

// 创建受限分析师角色
db.createRole({
    role: "limitedAnalyst",
    privileges: [
        {
            resource: { db: "analytics", collection: "" },
            actions: [ "find", "collStats" ]
        }
    ],
    roles: [
        { role: "read", db: "reports" }
    ]
})

// 分配自定义角色
use myapp
db.grantRolesToUser("app_user", ["appUserRole"])
db.grantRolesToUser("analyst", ["limitedAnalyst"])
```

### 2. 权限控制和审计

#### 细粒度权限控制
```javascript
// 字段级权限控制
db.createRole({
    role: "piiViewer",
    privileges: [
        {
            resource: { db: "customers", collection: "profiles" },
            actions: [ "find" ],
            fields: { ssn: 0, credit_card: 0 } // 排除敏感字段
        }
    ],
    roles: []
})

// 集合级权限
db.createRole({
    role: "orderManager",
    privileges: [
        {
            resource: { db: "ecommerce", collection: "orders" },
            actions: [ "find", "insert", "update" ]
        },
        {
            resource: { db: "ecommerce", collection: "inventory" },
            actions: [ "find" ]
        }
    ],
    roles: []
})

// 系统级权限
db.createRole({
    role: "backupOperator",
    privileges: [
        { resource: { cluster: true }, actions: [ "listDatabases" ] },
        { resource: { db: "", collection: "" }, actions: [ "find" ] }
    ],
    roles: []
})
```

#### 访问审计配置
```javascript
// 启用审计日志
// mongod --auditDestination=file --auditFormat=JSON --auditPath=/var/log/mongodb/audit.log

// 配置审计过滤器
use admin
db.system.audit.settings.insert({
    auditAuthorizationSuccess: true,
    filter: {
        atype: { $in: [ "authenticate", "createUser", "dropUser", "grantRolesToUser", "revokeRolesFromUser" ] }
    }
})

// 审计日志查询
use admin
db.system.audit.find({
    atype: "authenticate",
    "param.user": "app_user"
}).sort({ ts: -1 }).limit(10)

// 权限变更审计
db.system.audit.find({
    atype: { $in: [ "createUser", "dropUser", "grantRolesToUser", "revokeRolesFromUser" ] }
}).sort({ ts: -1 })
```

### 3. 访问监控和告警

#### 实时监控脚本
```javascript
// MongoDB访问监控
function monitorAccessPatterns() {
    const oneHourAgo = new Date(Date.now() - 3600000);
    
    // 异常连接监控
    const suspiciousConnections = db.system.audit.find({
        atype: "authenticate",
        ts: { $gte: oneHourAgo },
        "result.failed": true
    }).count();
    
    if (suspiciousConnections > 10) {
        console.log(`Alert: ${suspiciousConnections} failed authentication attempts in last hour`);
        // 发送告警通知
    }
    
    // 权限变更监控
    const privilegeChanges = db.system.audit.find({
        atype: { $in: [ "grantRolesToUser", "revokeRolesFromUser" ] },
        ts: { $gte: oneHourAgo }
    }).toArray();
    
    privilegeChanges.forEach(change => {
        console.log(`Privilege change: ${JSON.stringify(change)}`);
    });
}

// 定期执行监控
setInterval(monitorAccessPatterns, 300000); // 每5分钟执行一次
```

---

## 🔴 Redis访问控制实践

### 1. 用户和权限管理

#### ACL用户创建
```redis
# Redis 6.0+ ACL配置

# 创建管理员用户
ACL SETUSER admin ON >AdminSecurePass123! ~* &* +@all

# 创建应用用户
ACL SETUSER app_user ON >AppSecurePass456! ~app:* &app:* +get +set +exists +expire

# 创建只读用户
ACL SETUSER readonly_user ON >ReadOnlyPass789! ~cache:* &cache:* +get +exists

# 创建受限用户
ACL SETUSER limited_user ON >LimitedPass123! ~session:* &session:* +get +set +del

# 查看用户权限
ACL LIST
ACL GETUSER app_user

# 测试用户权限
AUTH app_user AppSecurePass456!
GET app:user:123
SET app:counter 1
```

#### 权限模式配置
```redis
# 通配符权限模式
ACL SETUSER pattern_user ON >PatternPass456! ~*:user:* &*:user:* +get +set

# 命令类别权限
ACL SETUSER ops_user ON >OpsPass789! ~jobs:* &jobs:* +@read +@write +@hash

# 禁用危险命令
ACL SETUSER restricted_user ON >RestrictedPass123! ~data:* &data:* +get +set -flushall -flushdb -shutdown

# 时间限制用户
ACL SETUSER time_limited ON >TimePass456! ~temp:* &temp:* +get +set
ACL SETUSER time_limited ON >unix-time +86400  # 24小时后过期
```

### 2. 访问控制配置

#### 配置文件安全设置
```conf
# redis.conf 安全配置
bind 127.0.0.1 192.168.1.100
protected-mode yes
port 6379

# 启用ACL
aclfile /etc/redis/users.acl

# 密码认证
requirepass "DefaultSecurePass123!"

# 命令重命名（额外安全层）
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS "SECURE_KEYS_COMMAND"
rename-command CONFIG "SECURE_CONFIG_COMMAND"

# 连接限制
maxclients 1000
timeout 300
tcp-keepalive 300

# 内存保护
maxmemory 2gb
maxmemory-policy allkeys-lru
```

#### 用户ACL文件
```conf
# /etc/redis/users.acl
user admin on >AdminSecurePass123! ~* &* +@all
user app_user on >AppSecurePass456! ~app:* &app:* +get +set +exists +expire
user cache_user on >CachePass789! ~cache:* &cache:* +get +set +del +expire
user readonly_user on >ReadOnlyPass123! ~* &* +get +exists
user default off resetchannels -@all  # 禁用默认用户
```

### 3. 监控和审计

#### 访问日志配置
```bash
#!/bin/bash
# redis_access_monitor.sh

REDIS_CLI="redis-cli -h localhost -p 6379"
LOG_FILE="/var/log/redis/access.log"
ALERT_THRESHOLD=1000

# 监控命令执行频率
monitor_command_frequency() {
    local commands=$($REDIS_CLI INFO COMMANDSTATS | grep -E "(cmdstat_|calls)")
    
    echo "$(date): Command statistics" >> $LOG_FILE
    echo "$commands" >> $LOG_FILE
    
    # 检查高频命令
    local high_freq=$($REDIS_CLI INFO COMMANDSTATS | grep "calls:" | awk -F'[,=]' '{if($2>ENVIRON["ALERT_THRESHOLD"]) print $0}')
    if [ -n "$high_freq" ]; then
        echo "High frequency commands detected:" >> $LOG_FILE
        echo "$high_freq" >> $LOG_FILE
        # 发送告警
    fi
}

# 监控连接数
monitor_connections() {
    local connected_clients=$($REDIS_CLI INFO CLIENTS | grep connected_clients | cut -d: -f2)
    local blocked_clients=$($REDIS_CLI INFO CLIENTS | grep blocked_clients | cut -d: -f2)
    
    echo "$(date): Connected clients: $connected_clients, Blocked: $blocked_clients" >> $LOG_FILE
    
    if [ $connected_clients -gt 500 ]; then
        echo "WARNING: High connection count: $connected_clients" >> $LOG_FILE
    fi
}

# 执行监控
monitor_command_frequency
monitor_connections
```

---

## 🛡️ 访问控制最佳实践

### 安全原则遵循

#### 1. 最小权限原则
```sql
-- 反面示例：过度授权
GRANT ALL PRIVILEGES ON *.* TO 'app_user'@'%';

-- 正面示例：最小必要权限
GRANT SELECT, INSERT, UPDATE ON ecommerce.users TO 'app_user'@'192.168.1.%';
GRANT SELECT, INSERT, UPDATE ON ecommerce.orders TO 'app_user'@'192.168.1.%';
```

#### 2. 权限分离原则
```javascript
// 创建专门的角色
db.createRole({
    role: "userReader",
    privileges: [{ resource: { db: "app", collection: "users" }, actions: ["find"] }],
    roles: []
})

db.createRole({
    role: "userWriter", 
    privileges: [{ resource: { db: "app", collection: "users" }, actions: ["insert", "update"] }],
    roles: []
})

// 分别分配给不同用户
db.grantRolesToUser("reader_user", ["userReader"])
db.grantRolesToUser("writer_user", ["userWriter"])
```

#### 3. 定期审查机制
```bash
#!/bin/bash
# permission_audit.sh - 权限审计脚本

AUDIT_DATE=$(date +%Y%m%d)
REPORT_DIR="/var/reports/access_control"

# 生成权限报告
generate_permission_report() {
    # MySQL权限报告
    mysql -e "
        SELECT 
            User,
            Host,
            COUNT(*) as privilege_count
        FROM mysql.user 
        GROUP BY User, Host
        ORDER BY privilege_count DESC
    " > $REPORT_DIR/mysql_permissions_$AUDIT_DATE.csv
    
    # PostgreSQL角色报告
    psql -c "
        COPY (
            SELECT 
                r.rolname,
                r.rolsuper,
                r.rolinherit,
                COUNT(m.roleid) as member_count
            FROM pg_roles r
            LEFT JOIN pg_auth_members m ON r.oid = m.roleid
            GROUP BY r.rolname, r.rolsuper, r.rolinherit
            ORDER BY member_count DESC
        ) TO '$REPORT_DIR/postgres_roles_$AUDIT_DATE.csv' CSV HEADER
    "
}

# 检查闲置账户
check_inactive_accounts() {
    local inactive_mysql=$(
        mysql -e "
            SELECT User, Host, password_last_changed 
            FROM mysql.user 
            WHERE password_last_changed < DATE_SUB(NOW(), INTERVAL 90 DAY)
        "
    )
    
    if [ -n "$inactive_mysql" ]; then
        echo "Inactive MySQL accounts found:" >> $REPORT_DIR/inactive_accounts_$AUDIT_DATE.txt
        echo "$inactive_mysql" >> $REPORT_DIR/inactive_accounts_$AUDIT_DATE.txt
    fi
}

mkdir -p $REPORT_DIR
generate_permission_report
check_inactive_accounts

echo "Access control audit report generated: $REPORT_DIR"
```

### 合规性要求

#### 1. SOX合规检查清单
```markdown
# SOX合规访问控制检查清单

## 用户管理
- [ ] 所有数据库用户均有明确的业务用途
- [ ] 定期审查和清理闲置用户账户
- [ ] 实施用户生命周期管理流程
- [ ] 建立用户创建和删除审批机制

## 权限控制
- [ ] 遵循最小权限原则
- [ ] 实施角色-Based访问控制
- [ ] 定期审查权限分配合理性
- [ ] 建立权限变更审批流程

## 审计跟踪
- [ ] 启用完整的访问审计日志
- [ ] 审计日志安全存储和保护
- [ ] 定期审计日志分析和报告
- [ ] 建立异常访问告警机制

## 密码安全
- [ ] 实施强密码策略
- [ ] 定期密码轮换机制
- [ ] 多因素认证实施
- [ ] 密码安全存储和传输
```

#### 2. GDPR数据保护要求
```sql
-- 数据主体权利支持
-- 右到被遗忘权实现
CREATE PROCEDURE DeleteUserData(IN user_id INT)
BEGIN
    START TRANSACTION;
    
    DELETE FROM user_profiles WHERE id = user_id;
    DELETE FROM user_activities WHERE user_id = user_id;
    DELETE FROM user_preferences WHERE user_id = user_id;
    
    -- 记录删除操作
    INSERT INTO data_deletion_log (user_id, deleted_at, deleted_by)
    VALUES (user_id, NOW(), USER());
    
    COMMIT;
END;

-- 数据可移植性支持
CREATE VIEW user_data_export AS
SELECT 
    up.id,
    up.username,
    up.email,
    up.created_at,
    ua.activity_type,
    ua.activity_timestamp,
    up.last_updated
FROM user_profiles up
LEFT JOIN user_activities ua ON up.id = ua.user_id
WHERE up.id = @user_id;
```

---

## 📊 访问控制评估报告

### 月度访问控制评估模板

```markdown
# 数据库访问控制月度评估报告

## 评估周期
2024年1月访问控制评估

## 用户和权限现状

### 用户统计
- **总用户数**: 45个
- **活跃用户数**: 38个
- **闲置用户数**: 7个
- **管理员用户数**: 3个

### 权限分布
| 权限类型 | 用户数 | 占比 |
|---------|--------|------|
| 读写权限 | 25 | 55.6% |
| 只读权限 | 15 | 33.3% |
| 管理权限 | 5 | 11.1% |

## 安全评估结果

### 合规性检查
- **SOX合规**: ✓ 通过
- **GDPR合规**: ✓ 通过
- **内部安全政策**: ✓ 通过

### 风险评估
| 风险等级 | 问题数量 | 主要问题 |
|---------|----------|----------|
| 高风险 | 2 | 过度授权账户 |
| 中风险 | 5 | 权限分配不合理 |
| 低风险 | 8 | 审计配置待优化 |

## 改进建议

### 立即执行
1. 删除3个闲置用户账户
2. 重新审查2个过度授权账户
3. 完善审计日志配置

### 短期计划
1. 实施权限定期审查机制
2. 建立权限申请审批流程
3. 加强安全培训和意识

### 长期规划
1. 部署自动化权限管理系统
2. 实施零信任访问架构
3. 建立持续监控和告警体系

## ROI分析
- **安全投入**: 12人天安全审计工作
- **风险降低**: 预计减少80%权限相关安全风险
- **合规成本节约**: 避免潜在罚款约￥500,000
- **投资回报率**: 约400%
```

---