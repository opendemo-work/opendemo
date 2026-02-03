# 🔐 数据库安全加固实践指南

> 企业级数据库安全防护体系，涵盖访问控制、网络安全、数据保护等全方位安全加固措施，确保数据库系统符合行业安全标准和合规要求

## 📋 案例概述

本案例提供完整的数据库安全加固方案，通过实施多层次的安全防护措施，保护数据库免受各种安全威胁，满足企业级安全合规要求。

### 🎯 学习目标

- 掌握数据库安全加固的核心技术和最佳实践
- 理解CIS安全基准和行业合规要求
- 实施访问控制、网络安全和数据保护措施
- 建立安全监控和审计机制
- 制定应急响应和漏洞修复流程

### ⏱️ 学习时长

- **理论学习**: 3小时
- **实践操作**: 4小时
- **总计**: 7小时

---

## 🛡️ 安全加固框架

### 安全层次模型

```
┌─────────────────────────────────────┐
│           应用层安全                │
│  - SQL注入防护                     │
│  - 输入验证                        │
│  - 权限最小化                      │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│           数据库层安全              │
│  - 访问控制                        │
│  - 身份认证                        │
│  - 审计日志                        │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│           系统层安全                │
│  - 操作系统加固                    │
│  - 网络安全                        │
│  - 物理安全                        │
└─────────────────────────────────────┘
```

---

## 🔧 MySQL安全加固实践

### 1. 基础安全配置

#### 删除默认账户
```sql
-- 删除匿名用户
DELETE FROM mysql.user WHERE User='';
FLUSH PRIVILEGES;

-- 删除test数据库
DROP DATABASE IF EXISTS test;

-- 限制root远程登录
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
FLUSH PRIVILEGES;
```

#### 设置强密码策略
```sql
-- 启用密码验证插件
INSTALL PLUGIN validate_password SONAME 'validate_password.so';

-- 配置密码策略
SET GLOBAL validate_password.policy = MEDIUM;
SET GLOBAL validate_password.length = 12;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.number_count = 1;
SET GLOBAL validate_password.special_char_count = 1;

-- 创建安全用户
CREATE USER 'app_user'@'%' IDENTIFIED BY 'ComplexPass123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
```

#### 配置文件安全设置
```ini
# /etc/my.cnf 安全配置
[mysqld]
# 网络安全
bind-address = 127.0.0.1
port = 3306
skip-networking = 0

# 认证安全
default_authentication_plugin = mysql_native_password
secure_auth = ON

# 日志安全
log_error = /var/log/mysql/error.log
log_warnings = 2
general_log = OFF
slow_query_log = ON
long_query_time = 2

# 数据安全
local_infile = OFF
skip_symbolic_links = YES
innodb_file_per_table = ON
innodb_flush_log_at_trx_commit = 1

# 审计安全
log_bin = /var/log/mysql/mysql-bin.log
binlog_format = ROW
expire_logs_days = 7
sync_binlog = 1
```

### 2. SSL/TLS加密配置

#### 生成SSL证书
```bash
# 创建证书目录
mkdir -p /etc/mysql/ssl
cd /etc/mysql/ssl

# 生成CA证书
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 3650 -key ca-key.pem -out ca.pem

# 生成服务器证书
openssl req -newkey rsa:2048 -days 3650 -nodes -keyout server-key.pem -out server-req.pem
openssl x509 -req -in server-req.pem -days 3650 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem

# 生成客户端证书
openssl req -newkey rsa:2048 -days 3650 -nodes -keyout client-key.pem -out client-req.pem
openssl x509 -req -in client-req.pem -days 3650 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem

# 设置权限
chmod 600 *.pem
chown mysql:mysql *.pem
```

#### 启用SSL连接
```ini
# /etc/my.cnf SSL配置
[mysqld]
ssl-ca = /etc/mysql/ssl/ca.pem
ssl-cert = /etc/mysql/ssl/server-cert.pem
ssl-key = /etc/mysql/ssl/server-key.pem
require_secure_transport = ON

# 强制SSL连接
[client]
ssl-ca = /etc/mysql/ssl/ca.pem
ssl-cert = /etc/mysql/ssl/client-cert.pem
ssl-key = /etc/mysql/ssl/client-key.pem
```

#### 验证SSL配置
```sql
-- 检查SSL状态
SHOW VARIABLES LIKE '%ssl%';

-- 查看当前连接是否使用SSL
SHOW STATUS LIKE 'Ssl_cipher';

-- 测试SSL连接
mysql -u app_user -p --ssl-mode=REQUIRED -h localhost
```

### 3. 访问控制强化

#### 细粒度权限管理
```sql
-- 创建应用专用用户
CREATE USER 'web_app'@'192.168.1.%' IDENTIFIED BY 'SecureWebPass123!';
GRANT SELECT, INSERT, UPDATE ON ecommerce.users TO 'web_app'@'192.168.1.%';
GRANT SELECT, INSERT, UPDATE ON ecommerce.orders TO 'web_app'@'192.168.1.%';
GRANT SELECT ON ecommerce.products TO 'web_app'@'192.168.1.%';

-- 创建只读分析用户
CREATE USER 'analyst'@'10.0.0.%' IDENTIFIED BY 'ReadOnlyPass456!';
GRANT SELECT ON ecommerce.* TO 'analyst'@'10.0.0.%';

-- 创建管理用户（严格限制）
CREATE USER 'db_admin'@'localhost' IDENTIFIED BY 'AdminSecurePass789!';
GRANT ALL PRIVILEGES ON *.* TO 'db_admin'@'localhost' WITH GRANT OPTION;
ALTER USER 'db_admin'@'localhost' ACCOUNT LOCK;
UNLOCK USER 'db_admin'@'localhost'; -- 仅在需要时解锁

-- 查看用户权限
SHOW GRANTS FOR 'web_app'@'192.168.1.%';
```

#### 连接限制和资源控制
```sql
-- 设置账户资源限制
ALTER USER 'web_app'@'192.168.1.%' 
WITH MAX_QUERIES_PER_HOUR 1000
     MAX_UPDATES_PER_HOUR 100
     MAX_CONNECTIONS_PER_HOUR 100
     MAX_USER_CONNECTIONS 10;

-- 创建受限用户组
CREATE ROLE 'app_role';
GRANT SELECT, INSERT, UPDATE ON myapp.* TO 'app_role';
GRANT 'app_role' TO 'web_app'@'192.168.1.%';
SET DEFAULT ROLE 'app_role' TO 'web_app'@'192.168.1.%';
```

### 4. 审计和监控

#### 启用审计日志
```sql
-- 安装审计插件
INSTALL PLUGIN audit_log SONAME 'audit_log.so';

-- 配置审计日志
SET GLOBAL audit_log_policy = ALL;
SET GLOBAL audit_log_format = JSON;
SET GLOBAL audit_log_rotate_on_size = 1073741824; -- 1GB
SET GLOBAL audit_log_rotations = 10;

-- 查看审计配置
SHOW VARIABLES LIKE 'audit_log%';
```

#### 自定义审计规则
```sql
-- 创建审计过滤器
CREATE AUDIT FILTER 'security_filter'
    ONLY_INCLUDE
        QUERY_DDL,
        QUERY_DML,
        CONNECT,
        TABLE_ACCESS;

-- 应用过滤器到用户
ALTER USER 'web_app'@'192.168.1.%' 
AUDIT BY 'security_filter';

-- 查看审计日志
SELECT * FROM mysql.audit_log_user;
SELECT * FROM mysql.audit_log_filter;
```

#### 实时安全监控
```bash
#!/bin/bash
# security_monitor.sh - 数据库安全监控脚本

LOG_FILE="/var/log/mysql/security_monitor.log"
ALERT_EMAIL="admin@company.com"

# 监控失败登录尝试
check_failed_logins() {
    mysql -e "SELECT user, host, COUNT(*) as attempts 
              FROM mysql.audit_log 
              WHERE event_type = 'CONNECT' AND status != 'SUCCESS'
              GROUP BY user, host 
              HAVING attempts > 5" >> $LOG_FILE
    
    if [ $? -eq 0 ] && [ -s $LOG_FILE ]; then
        mail -s "MySQL Security Alert - Failed Login Attempts" $ALERT_EMAIL < $LOG_FILE
    fi
}

# 监控异常查询模式
check_suspicious_queries() {
    mysql -e "SELECT user, host, COUNT(*) as query_count
              FROM mysql.audit_log 
              WHERE event_type = 'QUERY' 
              AND query_text REGEXP '(DROP|DELETE|UPDATE).*WHERE.*=.*OR.*='
              GROUP BY user, host 
              HAVING query_count > 10" >> $LOG_FILE
}

# 执行监控
check_failed_logins
check_suspicious_queries
```

---

## 🐘 PostgreSQL安全加固实践

### 1. 认证和授权安全

#### 配置pg_hba.conf
```conf
# /var/lib/pgsql/data/pg_hba.conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

# 应用特定连接
host    myapp           web_user        192.168.1.0/24          scram-sha-256
host    analytics       analyst         10.0.0.0/24             scram-sha-256

# 管理员连接（严格限制）
host    all             db_admin        127.0.0.1/32            cert

# 拒绝其他所有连接
host    all             all             0.0.0.0/0               reject
```

#### 强化用户管理
```sql
-- 创建安全用户
CREATE USER web_user WITH 
    PASSWORD 'SecureWebPassword123!'
    CONNECTION LIMIT 10
    VALID UNTIL '2024-12-31';

-- 创建角色和权限分配
CREATE ROLE app_users;
GRANT CONNECT ON DATABASE myapp TO app_users;
GRANT USAGE ON SCHEMA public TO app_users;

-- 授予具体表权限
GRANT SELECT, INSERT, UPDATE ON TABLE users TO web_user;
GRANT SELECT, INSERT, UPDATE ON TABLE orders TO web_user;
GRANT SELECT ON TABLE products TO web_user;

-- 创建只读用户
CREATE USER analyst WITH PASSWORD 'ReadOnlyPass456!';
GRANT app_users TO analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT SELECT ON TABLES TO analyst;
```

#### 启用SSL连接
```conf
# postgresql.conf SSL配置
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
ssl_ca_file = '/etc/ssl/certs/ca.crt'
ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'

# 强制SSL连接
password_encryption = scram-sha-256
```

### 2. 数据库级安全配置

#### 启用行级安全(RLS)
```sql
-- 启用RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 创建策略
CREATE POLICY user_data_isolation ON users
    FOR ALL TO web_user
    USING (tenant_id = current_setting('app.current_tenant')::integer);

-- 创建管理员策略
CREATE POLICY admin_access ON users
    FOR ALL TO db_admin
    USING (true);
```

#### 数据脱敏和视图安全
```sql
-- 创建安全视图
CREATE VIEW user_summary AS
SELECT 
    user_id,
    username,
    email_domain,
    registration_date,
    last_login
FROM (
    SELECT 
        user_id,
        username,
        SPLIT_PART(email, '@', 2) as email_domain,
        DATE(registration_date) as registration_date,
        DATE(last_login) as last_login
    FROM users
) masked_users;

-- 授予视图权限
GRANT SELECT ON user_summary TO analyst;
REVOKE SELECT ON users FROM analyst;
```

#### 启用审计扩展
```sql
-- 安装审计扩展
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- 配置审计日志
ALTER SYSTEM SET pgaudit.log = 'all, -misc';
ALTER SYSTEM SET pgaudit.log_level = 'log';
ALTER SYSTEM SET pgaudit.log_client = on;
ALTER SYSTEM SET log_statement = 'none';

-- 重新加载配置
SELECT pg_reload_conf();
```

---

## 🍃 MongoDB安全加固实践

### 1. 访问控制配置

#### 启用身份验证
```javascript
// 启动带认证的MongoDB
mongod --auth --port 27017 --dbpath /var/lib/mongo

// 创建管理员用户
use admin
db.createUser({
    user: "admin",
    pwd: "${DB_PASSWORD}",
    roles: [
        { role: "userAdminAnyDatabase", db: "admin" },
        { role: "dbAdminAnyDatabase", db: "admin" },
        { role: "readWriteAnyDatabase", db: "admin" }
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
    ]
})
```

#### 角色-Based权限管理
```javascript
// 创建自定义角色
use admin
db.createRole({
    role: "appUserRole",
    privileges: [
        {
            resource: { db: "myapp", collection: "users" },
            actions: [ "find", "insert", "update" ]
        },
        {
            resource: { db: "myapp", collection: "orders" },
            actions: [ "find", "insert", "update" ]
        }
    ],
    roles: []
})

// 分配角色给用户
db.grantRolesToUser("app_user", ["appUserRole"])
```

### 2. 网络安全配置

#### 配置绑定地址和端口
```yaml
# /etc/mongod.conf
net:
  port: 27017
  bindIp: 127.0.0.1,192.168.1.100
  maxIncomingConnections: 1000

security:
  authorization: enabled
  clusterAuthMode: keyFile
  keyFile: /opt/mongodb/keyfile
  javascriptEnabled: false
  redactClientLogData: true

setParameter:
  enableLocalhostAuthBypass: false
  authenticationMechanisms: "SCRAM-SHA-256"
```

#### SSL/TLS配置
```yaml
# SSL配置
net:
  ssl:
    mode: requireSSL
    PEMKeyFile: /etc/ssl/mongodb/server.pem
    CAFile: /etc/ssl/mongodb/ca.pem
    allowConnectionsWithoutCertificates: false
    allowInvalidCertificates: false
    allowInvalidHostnames: false
```

### 3. 审计和监控

#### 启用审计日志
```yaml
# 审计配置
auditLog:
  destination: file
  format: JSON
  path: /var/log/mongodb/audit.log
  filter: '{$or: [{atype: "authenticate"}, {atype: "createUser"}, {atype: "dropUser"}, {ns: {$ne: "local.system.profile"}}]}'
```

#### 安全监控脚本
```bash
#!/bin/bash
# mongodb_security_check.sh

MONGO_HOST="localhost:27017"
LOG_FILE="/var/log/mongodb/security_check.log"

# 检查未授权访问
check_unauthorized_access() {
    mongo --quiet --eval "
        db.adminCommand('listDatabases').databases.forEach(function(db){
            print('Database: ' + db.name);
            db.getSiblingDB(db.name).getCollectionNames().forEach(function(coll){
                print('  Collection: ' + coll);
            });
        });
    " >> $LOG_FILE
}

# 检查用户权限
check_user_permissions() {
    mongo admin --quiet --eval "
        db.system.users.find({},{_id:1,user:1,roles:1}).forEach(printjson);
    " >> $LOG_FILE
}

# 执行检查
check_unauthorized_access
check_user_permissions
```

---

## 🔴 Redis安全加固实践

### 1. 基础安全配置

#### 配置文件安全设置
```conf
# /etc/redis/redis.conf
# 网络安全
bind 127.0.0.1 192.168.1.100
port 6379
timeout 300
tcp-keepalive 300

# 认证安全
requirepass "SecureRedisPass123!"
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
rename-command CONFIG "SECURE_CONFIG_COMMAND"
rename-command SHUTDOWN "SECURE_SHUTDOWN_COMMAND"
rename-command DEBUG ""

# 持久化安全
save 900 1
save 300 10
save 60 10000
dbfilename dump.rdb
dir /var/lib/redis
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# 安全限制
maxmemory 2gb
maxmemory-policy allkeys-lru
notify-keyspace-events Ex
```

#### 用户和ACL配置
```redis
# Redis 6.0+ ACL配置
ACL SETUSER app_user on >AppSecurePass456! ~app:* &app:* +get +set +exists
ACL SETUSER cache_user on >CachePass789! ~cache:* &cache:* +get +set +del +expire
ACL SETUSER readonly_user on >ReadOnlyPass123! ~* &* +get

# 查看用户权限
ACL LIST
ACL GETUSER app_user

# 测试用户权限
AUTH app_user AppSecurePass456!
GET app:user:123
```

### 2. 网络和传输安全

#### 启用SSL/TLS
```conf
# TLS配置
tls-port 6380
tls-cert-file /etc/ssl/redis/redis.crt
tls-key-file /etc/ssl/redis/redis.key
tls-ca-cert-file /etc/ssl/redis/ca.crt
tls-auth-clients yes
```

#### 防火墙配置
```bash
# iptables规则
iptables -A INPUT -p tcp --dport 6379 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 6379 -j DROP

# 或使用firewalld
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="6379" accept'
firewall-cmd --reload
```

---

## 🛡️ 安全合规检查清单

### CIS基准检查项

#### MySQL CIS检查
- [ ] 移除测试数据库和匿名用户
- [ ] 禁用本地文件读取功能
- [ ] 启用SSL/TLS加密传输
- [ ] 配置强密码策略
- [ ] 限制用户权限最小化
- [ ] 启用审计日志记录
- [ ] 定期审查用户权限
- [ ] 实施连接限制和超时

#### PostgreSQL CIS检查
- [ ] 配置pg_hba.conf访问控制
- [ ] 启用SCRAM-SHA-256认证
- [ ] 禁用不必要的扩展
- [ ] 配置SSL连接强制
- [ ] 实施行级安全策略
- [ ] 启用审计日志
- [ ] 定期权限审查
- [ ] 数据库对象权限最小化

#### 通用安全要求
- [ ] 定期安全补丁更新
- [ ] 实施备份加密
- [ ] 配置网络隔离
- [ ] 启用入侵检测系统
- [ ] 建立安全事件响应流程
- [ ] 定期安全渗透测试
- [ ] 符合GDPR/CCPA等法规要求

---

## 🚨 应急响应预案

### 安全事件处理流程

#### 1. 发现阶段
```bash
# 实时监控脚本
#!/bin/bash
# security_incident_detector.sh

ALERT_EMAIL="security@company.com"
INCIDENT_LOG="/var/log/database_incidents.log"

detect_unusual_activity() {
    # 检测异常登录
    mysql -e "SELECT user, host, COUNT(*) as attempts 
              FROM mysql.general_log 
              WHERE command_type = 'Connect' 
              AND event_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
              GROUP BY user, host 
              HAVING attempts > 10" >> $INCIDENT_LOG
    
    # 检测大量删除操作
    mysql -e "SELECT user, host, COUNT(*) as deletes
              FROM mysql.general_log 
              WHERE argument LIKE 'DELETE%' 
              AND event_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
              GROUP BY user, host 
              HAVING deletes > 100" >> $INCIDENT_LOG
}

if [ -s "$INCIDENT_LOG" ]; then
    mail -s "Database Security Incident Detected" $ALERT_EMAIL < $INCIDENT_LOG
fi
```

#### 2. 响应阶段
```sql
-- 立即响应措施
-- 1. 锁定可疑账户
ALTER USER 'suspect_user'@'%' ACCOUNT LOCK;

-- 2. 终止可疑会话
SELECT Id, User, Host FROM information_schema.processlist 
WHERE User = 'suspect_user';

KILL 12345; -- 替换为实际连接ID

-- 3. 备份当前状态
mysqldump --single-transaction --routines --triggers 
          --master-data=2 myapp > incident_backup.sql

-- 4. 启用详细日志
SET GLOBAL general_log = 'ON';
SET GLOBAL slow_query_log = 'ON';
```

#### 3. 恢复阶段
```bash
#!/bin/bash
# incident_recovery.sh

BACKUP_DIR="/backup/incident_recovery"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 创建恢复点
mkdir -p $BACKUP_DIR/$TIMESTAMP

# 备份关键数据
mysqldump --single-transaction myapp users orders > $BACKUP_DIR/$TIMESTAMP/critical_tables.sql
cp /var/log/mysql/error.log $BACKUP_DIR/$TIMESTAMP/

# 恢复验证
mysql -e "CHECKSUM TABLE users, orders;" > $BACKUP_DIR/$TIMESTAMP/checksum_verify.txt

echo "Incident recovery point created: $BACKUP_DIR/$TIMESTAMP"
```

---

## 📊 安全评估报告模板

### 月度安全评估报告

```markdown
# 数据库安全月度评估报告

## 基本信息
- 报告周期: 2024年1月
- 评估日期: 2024-01-31
- 评估人员: DBA团队

## 安全指标统计
| 指标 | 数值 | 趋势 | 说明 |
|------|------|------|------|
| 安全漏洞数 | 2 | ↓ | 较上月减少1个 |
| 未授权访问尝试 | 15 | ↓ | 较上月减少30% |
| 成功攻击事件 | 0 | - | 本月无成功攻击 |
| 补丁更新及时率 | 98% | ↑ | 较上月提升5% |

## 主要安全事件
1. **事件类型**: 暴力破解尝试
   **影响范围**: MySQL实例
   **处理结果**: IP封禁，加强认证
   **预防措施**: 启用fail2ban

2. **事件类型**: 权限配置不当
   **影响范围**: PostgreSQL用户权限
   **处理结果**: 重新配置权限，启用RLS
   **预防措施**: 建立权限审查流程

## 改进建议
1. 实施零信任网络架构
2. 部署数据库活动监控(DAM)系统
3. 加强员工安全意识培训
4. 建立安全运营中心(SOC)

## 下月重点任务
- [ ] 部署数据库防火墙
- [ ] 实施动态数据脱敏
- [ ] 完成ISO 27001认证准备工作
- [ ] 开展红蓝对抗演练
```

---

## 🎯 最佳实践总结

### 关键安全原则

1. **纵深防御**: 实施多层安全防护
2. **最小权限**: 遵循权限最小化原则
3. **安全默认**: 默认配置应偏向安全
4. **持续监控**: 实时监控安全事件
5. **快速响应**: 建立应急响应机制

### 实施建议

- **分阶段实施**: 先基础加固，再高级防护
- **定期评估**: 每季度进行安全评估
- **持续改进**: 根据威胁情报更新防护措施
- **全员参与**: 建立全员安全意识
- **合规导向**: 确保符合相关法规要求

### 风险控制要点

- **访问控制**: 严格管理用户权限和访问路径
- **数据保护**: 实施加密和脱敏措施
- **网络安全**: 配置防火墙和网络隔离
- **审计监控**: 建立完整的审计和监控体系
- **应急准备**: 制定详细的应急预案和恢复计划

---