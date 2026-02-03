# 📋 数据库审计日志配置指南

> 企业级数据库审计体系，涵盖审计策略制定、日志收集分析、合规报告生成等完整的审计解决方案，满足SOX、GDPR等法规要求

## 📋 案例概述

本案例详细介绍数据库审计系统的规划、实施和管理，通过建立完善的审计日志收集、分析和报告机制，确保数据库操作的可追溯性和合规性。

### 🎯 学习目标

- 掌握数据库审计日志的配置和管理方法
- 理解各类审计事件的分类和重要性
- 实施审计日志的收集、存储和分析流程
- 建立合规性审计报告和监控机制
- 制定审计策略和 retention 策略

### ⏱️ 学习时长

- **理论学习**: 3小时
- **实践操作**: 4小时
- **总计**: 7小时

---

## 📊 审计体系架构

### 审计层次模型

```
┌─────────────────────────────────────────────────┐
│              应用层审计                         │
│  - 业务操作审计                                │
│  - 用户行为追踪                                │
│  - 会话管理审计                                │
└─────────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────┐
│              数据库层审计                       │
│  - SQL执行审计                                 │
│  - 权限变更审计                                │
│  - 数据访问审计                                │
└─────────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────┐
│              系统层审计                         │
│  - 系统操作审计                                │
│  - 安全事件审计                                │
│  - 配置变更审计                                │
└─────────────────────────────────────────────────┘
```

### 审计事件分类

```
审计事件类型
├── 访问事件
│   ├── 登录/登出
│   ├── 连接建立/断开
│   └── 权限验证
├── 数据操作事件
│   ├── SELECT查询
│   ├── INSERT/UPDATE/DELETE
│   ├── DDL操作
│   └── 存储过程执行
├── 管理事件
│   ├── 用户管理
│   ├── 权限变更
│   ├── 配置修改
│   └── 系统维护
└── 安全事件
    ├── 认证失败
    ├── 权限拒绝
    ├── 异常访问模式
    └── 安全违规
```

---

## 🐬 MySQL审计配置实践

### 1. 审计插件配置

#### 安装和启用审计插件
```sql
-- 检查审计插件支持
SHOW PLUGINS LIKE '%audit%';

-- 安装审计日志插件
INSTALL PLUGIN audit_log SONAME 'audit_log.so';

-- 验证插件安装
SELECT PLUGIN_NAME, PLUGIN_STATUS 
FROM INFORMATION_SCHEMA.PLUGINS 
WHERE PLUGIN_NAME = 'audit_log';

-- 基础配置
SET GLOBAL audit_log_policy = ALL;
SET GLOBAL audit_log_format = JSON;
SET GLOBAL audit_log_rotate_on_size = 1073741824; -- 1GB
SET GLOBAL audit_log_rotations = 10;
SET GLOBAL audit_log_flush = ON;
```

#### 审计策略配置
```sql
-- 配置审计策略
SET GLOBAL audit_log_policy = QUERIES; -- 只记录查询
-- SET GLOBAL audit_log_policy = ALL; -- 记录所有事件
-- SET GLOBAL audit_log_policy = LOGINS; -- 只记录登录事件
-- SET GLOBAL audit_log_policy = NONE; -- 不记录任何事件

-- 配置审计格式
SET GLOBAL audit_log_format = NEW; -- 新格式（推荐）
-- SET GLOBAL audit_log_format = OLD; -- 旧格式
-- SET GLOBAL audit_log_format = JSON; -- JSON格式

-- 配置详细程度
SET GLOBAL audit_log_connection_policy = ERRORS; -- 连接错误审计
SET GLOBAL audit_log_exclude_accounts = 'monitor@%,backup@%'; -- 排除特定账户
```

#### 自定义审计过滤器
```sql
-- 创建审计过滤器
CREATE AUDIT FILTER 'security_critical'
    ONLY_INCLUDE
        QUERY_DDL,
        QUERY_DML,
        CONNECT,
        TABLE_ACCESS;

CREATE AUDIT FILTER 'compliance_filter'
    ONLY_INCLUDE
        QUERY_DCL,
        CONNECT,
        DISCONNECT,
        TABLE_ACCESS;

-- 应用过滤器到用户
ALTER USER 'admin'@'localhost' AUDIT BY 'security_critical';
ALTER USER 'app_user'@'%' AUDIT BY 'compliance_filter';

-- 查看过滤器配置
SELECT * FROM mysql.audit_log_filter;
SELECT * FROM mysql.audit_log_user;
```

### 2. 审计日志管理

#### 日志文件配置
```ini
# /etc/my.cnf 审计日志配置
[mysqld]
# 审计插件配置
plugin-load = audit_log.so

# 基本审计设置
audit-log = FORCE_PLUS_PERMANENT
audit_log_policy = ALL
audit_log_format = JSON
audit_log_handler = FILE

# 日志文件设置
audit_log_file = /var/log/mysql/audit.log
audit_log_rotate_on_size = 1073741824
audit_log_rotations = 50
audit_log_flush = ON

# 性能优化
audit_log_buffer_size = 32M
audit_log_write_waits = 10
```

#### 日志轮转和清理
```bash
#!/bin/bash
# mysql_audit_log_rotation.sh

LOG_DIR="/var/log/mysql"
MAX_SIZE=1073741824  # 1GB
RETENTION_DAYS=90
COMPRESS_AGE=7

# 检查日志大小并轮转
rotate_audit_logs() {
    local current_size=$(stat -c%s "$LOG_DIR/audit.log")
    
    if [ $current_size -gt $MAX_SIZE ]; then
        local timestamp=$(date +%Y%m%d_%H%M%S)
        mv "$LOG_DIR/audit.log" "$LOG_DIR/audit.log.$timestamp"
        touch "$LOG_DIR/audit.log"
        chown mysql:mysql "$LOG_DIR/audit.log"
        echo "$(date): Audit log rotated - audit.log.$timestamp" >> /var/log/audit_maintenance.log
    fi
}

# 压缩旧日志
compress_old_logs() {
    find $LOG_DIR -name "audit.log.*" -mtime +$COMPRESS_AGE -exec gzip {} \; 2>/dev/null
}

# 清理过期日志
cleanup_expired_logs() {
    find $LOG_DIR -name "audit.log.*" -mtime +$RETENTION_DAYS -delete
    find $LOG_DIR -name "audit.log.*.gz" -mtime +$RETENTION_DAYS -delete
}

# 执行维护任务
rotate_audit_logs
compress_old_logs
cleanup_expired_logs

# 验证日志完整性
mysql -e "SELECT COUNT(*) as audit_events FROM mysql.audit_log;" >> /var/log/audit_maintenance.log
```

### 3. 审计数据分析

#### 日志解析和分析脚本
```python
#!/usr/bin/env python3
# audit_log_analyzer.py

import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class MySQLAuditAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.events = []
        
    def parse_log(self):
        """解析审计日志"""
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        self.events.append(event)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            print(f"Log file not found: {self.log_file}")
            return False
        return True
    
    def analyze_login_patterns(self):
        """分析登录模式"""
        login_events = [e for e in self.events if e.get('event_type') == 'CONNECT']
        
        # 统计登录失败
        failed_logins = [e for e in login_events if e.get('status') != 'SUCCESS']
        failed_by_user = Counter(e.get('user', 'unknown') for e in failed_logins)
        
        print("=== 登录失败统计 ===")
        for user, count in failed_by_user.most_common(10):
            print(f"{user}: {count} 次失败")
        
        # 统计异常时间登录
        late_logins = []
        for event in login_events:
            timestamp = datetime.fromisoformat(event.get('timestamp', '').replace('Z', '+00:00'))
            if timestamp.hour >= 22 or timestamp.hour <= 6:
                late_logins.append(event)
        
        print(f"\n深夜登录次数: {len(late_logins)}")
        
    def analyze_query_patterns(self):
        """分析查询模式"""
        query_events = [e for e in self.events if e.get('event_type') == 'QUERY']
        
        # 按用户统计查询量
        queries_by_user = Counter(e.get('user', 'unknown') for e in query_events)
        
        print("\n=== 查询量统计 ===")
        for user, count in queries_by_user.most_common(10):
            print(f"{user}: {count} 次查询")
        
        # 识别潜在危险查询
        dangerous_patterns = [
            r'\b(DROP|DELETE FROM)\b.*\bWHERE\b.*\b(1=1|OR 1=1)\b',
            r'\bUNION\b.*\bSELECT\b',
            r'\b(SELECT|INSERT|UPDATE|DELETE)\b.*\b\*\b'
        ]
        
        suspicious_queries = []
        for event in query_events:
            query = event.get('sqltext', '')
            for pattern in dangerous_patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    suspicious_queries.append(event)
                    break
        
        print(f"\n可疑查询数量: {len(suspicious_queries)}")
        
    def generate_compliance_report(self):
        """生成合规报告"""
        report = {
            'report_date': datetime.now().isoformat(),
            'total_events': len(self.events),
            'event_types': dict(Counter(e.get('event_type', 'unknown') for e in self.events)),
            'unique_users': len(set(e.get('user') for e in self.events if e.get('user'))),
            'time_range': self._get_time_range()
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def _get_time_range(self):
        """获取时间范围"""
        timestamps = [e.get('timestamp') for e in self.events if e.get('timestamp')]
        if not timestamps:
            return "无数据"
        
        min_time = min(timestamps)
        max_time = max(timestamps)
        return f"{min_time} 至 {max_time}"

# 使用示例
if __name__ == "__main__":
    analyzer = MySQLAuditAnalyzer("/var/log/mysql/audit.log")
    if analyzer.parse_log():
        analyzer.analyze_login_patterns()
        analyzer.analyze_query_patterns()
        print("\n=== 合规报告 ===")
        print(analyzer.generate_compliance_report())
```

---

## 🐘 PostgreSQL审计配置实践

### 1. 基础审计配置

#### 启用审计日志
```sql
-- 配置基本审计参数
ALTER SYSTEM SET log_statement = 'mod'; -- 记录DDL和DML语句
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_duration = on;
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';

-- 启用详细查询日志
ALTER SYSTEM SET log_min_duration_statement = 1000; -- 超过1秒的查询
ALTER SYSTEM SET log_statement_sample_rate = 1.0;

-- 重新加载配置
SELECT pg_reload_conf();
```

#### 安装审计扩展
```sql
-- 安装pgaudit扩展
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- 配置pgaudit
ALTER SYSTEM SET pgaudit.log = 'all, -misc';
ALTER SYSTEM SET pgaudit.log_catalog = on;
ALTER SYSTEM SET pgaudit.log_parameter = on;
ALTER SYSTEM SET pgaudit.log_relation = on;
ALTER SYSTEM SET pgaudit.log_statement_once = off;

-- 启用客户端日志
ALTER SYSTEM SET pgaudit.log_client = on;
ALTER SYSTEM SET pgaudit.log_level = 'log';

-- 重新加载配置
SELECT pg_reload_conf();
```

### 2. 高级审计功能

#### 对象级审计
```sql
-- 为特定表启用审计
ALTER TABLE users SET (log_select=true, log_insert=true, log_update=true, log_delete=true);
ALTER TABLE financial_transactions SET (log_all=true);

-- 创建审计策略
CREATE POLICY audit_policy ON audit_log_table
    FOR ALL
    USING (current_user = 'audit_admin');

-- 启用行级安全审计
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY audit_rls_policy ON sensitive_data
    FOR SELECT
    USING (pg_backend_pid() IN (
        SELECT pid FROM pg_stat_activity WHERE application_name = 'audit_monitor'
    ));
```

#### 自定义审计函数
```sql
-- 创建审计触发器函数
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
DECLARE
    audit_record JSON;
BEGIN
    audit_record := json_build_object(
        'table_name', TG_TABLE_NAME,
        'operation', TG_OP,
        'user_name', current_user,
        'session_user', session_user,
        'client_addr', inet_client_addr(),
        'timestamp', current_timestamp,
        'old_values', CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN row_to_json(OLD) END,
        'new_values', CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) END
    );
    
    -- 插入审计日志表
    INSERT INTO audit_log (event_data, event_time)
    VALUES (audit_record, current_timestamp);
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 为表创建审计触发器
CREATE TRIGGER users_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER transactions_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON financial_transactions
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

### 3. 审计日志分析

#### 审计视图创建
```sql
-- 创建审计分析视图
CREATE VIEW audit_summary AS
SELECT 
    date_trunc('hour', event_time) as hour_bucket,
    (event_data->>'operation')::text as operation,
    (event_data->>'user_name')::text as user_name,
    (event_data->>'table_name')::text as table_name,
    COUNT(*) as event_count
FROM audit_log
WHERE event_time >= current_date - interval '7 days'
GROUP BY 
    date_trunc('hour', event_time),
    (event_data->>'operation')::text,
    (event_data->>'user_name')::text,
    (event_data->>'table_name')::text
ORDER BY hour_bucket DESC, event_count DESC;

-- 创建用户活动视图
CREATE VIEW user_activity_audit AS
SELECT 
    (event_data->>'user_name')::text as user_name,
    (event_data->>'client_addr')::inet as client_ip,
    MIN(event_time) as first_activity,
    MAX(event_time) as last_activity,
    COUNT(*) as total_operations,
    COUNT(DISTINCT (event_data->>'table_name')::text) as tables_accessed
FROM audit_log
WHERE event_time >= current_date - interval '30 days'
GROUP BY 
    (event_data->>'user_name')::text,
    (event_data->>'client_addr')::inet
HAVING COUNT(*) > 100
ORDER BY total_operations DESC;
```

#### 审计报告生成
```sql
-- 生成合规性审计报告
CREATE OR REPLACE FUNCTION generate_audit_report(days_back INTEGER DEFAULT 30)
RETURNS TABLE (
    report_section TEXT,
    metric_name TEXT,
    metric_value BIGINT,
    description TEXT
) AS $$
BEGIN
    RETURN QUERY
    -- 用户活动统计
    SELECT 
        'User Activity' as report_section,
        'Active Users' as metric_name,
        COUNT(DISTINCT (event_data->>'user_name')::text) as metric_value,
        'Number of unique users in the period' as description
    FROM audit_log
    WHERE event_time >= current_date - interval '1 day' * days_back
    
    UNION ALL
    
    -- 敏感表访问统计
    SELECT 
        'Sensitive Data Access' as report_section,
        'Financial Table Queries' as metric_name,
        COUNT(*) as metric_value,
        'Queries on financial_transactions table' as description
    FROM audit_log
    WHERE (event_data->>'table_name')::text = 'financial_transactions'
    AND event_time >= current_date - interval '1 day' * days_back
    
    UNION ALL
    
    -- 异常活动检测
    SELECT 
        'Anomaly Detection' as report_section,
        'Failed Login Attempts' as metric_name,
        COUNT(*) as metric_value,
        'Authentication failure events' as description
    FROM pg_log
    WHERE log_message LIKE '%authentication failed%'
    AND log_time >= current_date - interval '1 day' * days_back;
END;
$$ LANGUAGE plpgsql;

-- 执行报告生成
SELECT * FROM generate_audit_report(30);
```

---

## 🍃 MongoDB审计配置实践

### 1. 审计系统配置

#### 启用审计日志
```javascript
// MongoDB配置文件启用审计
// /etc/mongod.conf
processManagement:
  fork: true
  pidFilePath: /var/run/mongodb/mongod.pid

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true

auditLog:
  destination: file
  format: JSON
  path: /var/log/mongodb/audit.log
  filter: '{$or: [{atype: "authenticate"}, {atype: "createUser"}, {atype: "dropUser"}, {atype: "grantRolesToUser"}, {atype: "revokeRolesFromUser"}, {ns: {$ne: "local.system.profile"}}]}'
```

#### 动态启用审计
```javascript
// 运行时启用审计（需要重启）
use admin
db.adminCommand({
    setParameter: 1,
    auditAuthorizationSuccess: true
})

// 配置审计过滤器
db.adminCommand({
    configureFailPoint: "auditFilter",
    mode: "alwaysOn",
    data: {
        filter: {
            $or: [
                { atype: "authenticate" },
                { atype: "createUser" },
                { atype: "dropUser" },
                { atype: { $in: ["grantRolesToUser", "revokeRolesFromUser"] } },
                { ns: { $not: /^local\.system\.profile/ } }
            ]
        }
    }
})
```

### 2. 审计事件分析

#### 审计日志解析脚本
```python
#!/usr/bin/env python3
# mongodb_audit_analyzer.py

import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re

class MongoDBAuditAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.events = []
        
    def parse_audit_log(self):
        """解析MongoDB审计日志"""
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        self.events.append(event)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            print(f"Audit log file not found: {self.log_file}")
            return False
        return True
    
    def analyze_authentication_events(self):
        """分析认证事件"""
        auth_events = [e for e in self.events if e.get('atype') == 'authenticate']
        
        # 统计认证结果
        auth_results = Counter(e.get('result', 0) for e in auth_events)
        print("=== 认证结果统计 ===")
        print(f"成功认证: {auth_results.get(0, 0)} 次")
        print(f"失败认证: {auth_results.get(18, 0)} 次")
        
        # 统计用户认证频率
        user_auth_attempts = Counter(e.get('param', {}).get('user', 'unknown') 
                                   for e in auth_events)
        
        print("\n=== 用户认证频率 ===")
        for user, count in user_auth_attempts.most_common(10):
            print(f"{user}: {count} 次")
            
        # 检测暴力破解尝试
        recent_auth_events = [e for e in auth_events 
                            if datetime.strptime(e.get('ts', ''), '%Y-%m-%dT%H:%M:%S.%fZ') 
                            > datetime.utcnow() - timedelta(hours=1)]
        
        failed_attempts = [e for e in recent_auth_events 
                         if e.get('result', 0) != 0]
        
        if len(failed_attempts) > 10:
            print(f"\n⚠️  警告: 1小时内检测到 {len(failed_attempts)} 次失败认证")
    
    def analyze_privilege_events(self):
        """分析权限变更事件"""
        privilege_events = [e for e in self.events 
                          if e.get('atype') in ['createUser', 'dropUser', 'grantRolesToUser', 'revokeRolesFromUser']]
        
        print("\n=== 权限变更事件 ===")
        event_types = Counter(e.get('atype') for e in privilege_events)
        for event_type, count in event_types.items():
            print(f"{event_type}: {count} 次")
        
        # 分析权限变更详情
        for event in privilege_events[-10:]:  # 最近10个事件
            param = event.get('param', {})
            print(f"- {event.get('atype')} by {event.get('users', [{}])[0].get('user', 'unknown')}")
            if 'user' in param:
                print(f"  用户: {param['user']}")
            if 'roles' in param:
                print(f"  角色: {param['roles']}")
    
    def analyze_data_access(self):
        """分析数据访问模式"""
        data_events = [e for e in self.events 
                     if e.get('atype') in ['find', 'insert', 'update', 'remove', 'count']]
        
        # 按集合统计访问量
        collection_access = Counter(e.get('ns', 'unknown') for e in data_events)
        
        print("\n=== 集合访问统计 ===")
        for collection, count in collection_access.most_common(10):
            print(f"{collection}: {count} 次操作")
        
        # 识别异常访问模式
        sensitive_collections = ['users', 'financial_data', 'personal_info']
        suspicious_access = [e for e in data_events 
                           if any(col in e.get('ns', '') for col in sensitive_collections)
                           and e.get('atype') == 'find']
        
        print(f"\n敏感数据访问次数: {len(suspicious_access)}")
        
        # 统计非工作时间访问
        off_hours_access = []
        for event in data_events:
            timestamp = datetime.strptime(event.get('ts', ''), '%Y-%m-%dT%H:%M:%S.%fZ')
            if timestamp.hour < 8 or timestamp.hour > 18:  # 非工作时间
                off_hours_access.append(event)
        
        print(f"非工作时间访问: {len(off_hours_access)} 次")

# 使用示例
if __name__ == "__main__":
    analyzer = MongoDBAuditAnalyzer("/var/log/mongodb/audit.log")
    if analyzer.parse_audit_log():
        analyzer.analyze_authentication_events()
        analyzer.analyze_privilege_events()
        analyzer.analyze_data_access()
```

### 3. 实时审计监控

#### 审计事件实时处理
```javascript
// MongoDB实时审计监控
use admin

// 创建审计事件处理器
function processAuditEvent(event) {
    const eventType = event.atype;
    const timestamp = new Date(event.ts);
    const user = event.users ? event.users[0].user : 'system';
    
    // 认证失败监控
    if (eventType === 'authenticate' && event.result !== 0) {
        console.log(`[${timestamp}] Authentication failed for user: ${user}`);
        
        // 记录到专门的失败日志集合
        db.audit_failures.insertOne({
            timestamp: timestamp,
            user: user,
            ip: event.remote ? event.remote.ip : 'unknown',
            userAgent: event.param ? event.param.userAgent : 'unknown'
        });
    }
    
    // 权限变更监控
    if (['createUser', 'dropUser', 'grantRolesToUser', 'revokeRolesFromUser'].includes(eventType)) {
        console.log(`[${timestamp}] Privilege change: ${eventType} by ${user}`);
        
        // 发送到安全通知系统
        db.security_notifications.insertOne({
            timestamp: timestamp,
            eventType: eventType,
            actor: user,
            target: event.param ? event.param.user : 'unknown',
            details: event.param
        });
    }
    
    // 敏感数据访问监控
    const sensitiveCollections = ['users', 'financial_records', 'personal_data'];
    if (event.ns && sensitiveCollections.some(col => event.ns.includes(col))) {
        console.log(`[${timestamp}] Sensitive data accessed: ${event.ns} by ${user}`);
        
        // 记录详细访问日志
        db.sensitive_access_log.insertOne({
            timestamp: timestamp,
            user: user,
            collection: event.ns,
            operation: eventType,
            clientIp: event.remote ? event.remote.ip : 'unknown'
        });
    }
}

// 启动实时审计监听
function startAuditMonitoring() {
    const tailCursor = db.system.profile.find({
        "ts": { $gte: new Date() }
    }, {
        tailable: true,
        awaitData: true
    });
    
    tailCursor.forEach(processAuditEvent);
}

// 执行监控（在后台运行）
// startAuditMonitoring();
```

---

## 🔴 Redis审计配置实践

### 1. 基础审计配置

#### 启用命令审计
```conf
# redis.conf 审计配置
# 启用慢查询日志（作为基础审计）
slowlog-log-slower-than 10000  # 记录超过10ms的命令
slowlog-max-len 1000           # 保留1000条慢查询记录

# 启用详细日志
loglevel notice
logfile /var/log/redis/redis-server.log

# 记录所有命令（谨慎使用，影响性能）
# monitor  # 可以在运行时启用，但不建议长期开启
```

#### 自定义审计脚本
```bash
#!/bin/bash
# redis_audit_monitor.sh

REDIS_CLI="redis-cli -h localhost -p 6379"
LOG_FILE="/var/log/redis/audit.log"
ALERT_THRESHOLD=100

# 监控命令执行统计
monitor_command_stats() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 获取命令统计
    local cmdstats=$($REDIS_CLI INFO COMMANDSTATS)
    
    echo "[$timestamp] Command Statistics:" >> $LOG_FILE
    echo "$cmdstats" >> $LOG_FILE
    
    # 检查高频命令
    echo "$cmdstats" | grep "calls:" | while read line; do
        local calls=$(echo "$line" | cut -d',' -f1 | cut -d'=' -f2)
        if [ "$calls" -gt "$ALERT_THRESHOLD" ]; then
            local cmd=$(echo "$line" | cut -d':' -f1)
            echo "[$timestamp] ALERT: High frequency command - $cmd: $calls calls" >> $LOG_FILE
        fi
    done
}

# 监控连接和客户端
monitor_connections() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    local connected_clients=$($REDIS_CLI INFO CLIENTS | grep connected_clients | cut -d':' -f2)
    local blocked_clients=$($REDIS_CLI INFO CLIENTS | grep blocked_clients | cut -d':' -f2)
    
    echo "[$timestamp] Connections - Connected: $connected_clients, Blocked: $blocked_clients" >> $LOG_FILE
    
    # 检查异常连接数
    if [ "$connected_clients" -gt 500 ]; then
        echo "[$timestamp] ALERT: High connection count: $connected_clients" >> $LOG_FILE
    fi
}

# 监控内存使用
monitor_memory() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    local used_memory=$($REDIS_CLI INFO MEMORY | grep used_memory_human | cut -d':' -f2)
    local used_memory_peak=$($REDIS_CLI INFO MEMORY | grep used_memory_peak_human | cut -d':' -f2)
    
    echo "[$timestamp] Memory Usage - Current: $used_memory, Peak: $used_memory_peak" >> $LOG_FILE
}

# 执行监控
monitor_command_stats
monitor_connections
monitor_memory
```

### 2. 高级审计实现

#### Lua脚本审计
```lua
-- audit_commands.lua - Redis Lua审计脚本
local function audit_command(command, args, client_info)
    local timestamp = redis.call('TIME')[1]
    local log_entry = {
        timestamp = timestamp,
        command = command,
        args = args,
        client_ip = client_info.ip,
        client_name = client_info.name or "unknown",
        db = redis.call('SELECT', 0)  -- 获取当前数据库
    }
    
    -- 记录到审计日志键
    redis.call('LPUSH', 'audit:commands', cjson.encode(log_entry))
    redis.call('LTRIM', 'audit:commands', 0, 9999)  -- 保留最近10000条记录
    
    -- 检查敏感命令
    local sensitive_commands = {'FLUSHALL', 'FLUSHDB', 'CONFIG', 'SHUTDOWN'}
    for _, sensitive_cmd in ipairs(sensitive_commands) do
        if command:upper() == sensitive_cmd then
            redis.call('LPUSH', 'audit:sensitive_commands', cjson.encode(log_entry))
            -- 可以在这里发送告警通知
            break
        end
    end
    
    return log_entry
end

-- 使用示例：在关键命令前调用审计
-- audit_command('SET', {'key', 'value'}, {ip='192.168.1.100', name='app_server'})
```

#### 审计日志分析
```python
#!/usr/bin/env python3
# redis_audit_analyzer.py

import redis
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class RedisAuditAnalyzer:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        
    def analyze_recent_commands(self, hours=24):
        """分析最近的命令执行情况"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # 获取审计日志
        audit_entries = self.redis_client.lrange('audit:commands', 0, -1)
        
        commands_counter = Counter()
        user_commands = defaultdict(list)
        
        for entry in audit_entries:
            try:
                log_data = json.loads(entry.decode('utf-8'))
                timestamp = datetime.fromtimestamp(int(log_data['timestamp']))
                
                if timestamp > cutoff_time:
                    command = log_data['command'].upper()
                    commands_counter[command] += 1
                    user_commands[log_data['client_name']].append(command)
                    
            except (json.JSONDecodeError, KeyError):
                continue
        
        print("=== 命令执行统计 ===")
        for command, count in commands_counter.most_common(10):
            print(f"{command}: {count} 次")
            
        print("\n=== 客户端命令分布 ===")
        for client, commands in list(user_commands.items())[:5]:
            print(f"{client}: {len(commands)} 个命令")
            
        return commands_counter
    
    def detect_anomalies(self):
        """检测异常行为"""
        # 检查敏感命令执行
        sensitive_commands = self.redis_client.lrange('audit:sensitive_commands', 0, -1)
        
        if sensitive_commands:
            print("\n⚠️  检测到敏感命令执行:")
            for cmd in sensitive_commands[-5:]:  # 最近5个
                try:
                    cmd_data = json.loads(cmd.decode('utf-8'))
                    print(f"- {cmd_data['command']} 执行于 {datetime.fromtimestamp(int(cmd_data['timestamp']))}")
                except json.JSONDecodeError:
                    continue
        
        # 检查高频命令模式
        recent_commands = self.redis_client.lrange('audit:commands', 0, 99)  # 最近100个命令
        command_sequence = []
        
        for cmd in recent_commands:
            try:
                cmd_data = json.loads(cmd.decode('utf-8'))
                command_sequence.append(cmd_data['command'].upper())
            except json.JSONDecodeError:
                continue
        
        # 简单的模式检测
        dangerous_patterns = [
            ['FLUSHALL'],
            ['FLUSHDB'],
            ['CONFIG', 'SET'],
            ['SHUTDOWN']
        ]
        
        for pattern in dangerous_patterns:
            if all(cmd in command_sequence for cmd in pattern):
                print(f"\n⚠️  检测到危险命令序列: {' -> '.join(pattern)}")

# 使用示例
if __name__ == "__main__":
    analyzer = RedisAuditAnalyzer()
    analyzer.analyze_recent_commands(24)
    analyzer.detect_anomalies()
```

---

## 📊 审计合规报告

### 标准化审计报告模板

```markdown
# 数据库审计合规报告

## 报告基本信息
- **报告周期**: 2024年1月
- **生成时间**: 2024-01-31
- **审计范围**: MySQL/PostgreSQL/MongoDB/Redis
- **合规标准**: SOX, GDPR, ISO 27001

## 审计概览

### 审计覆盖情况
| 数据库类型 | 审计启用状态 | 覆盖率 | 日志完整性 |
|-----------|-------------|--------|------------|
| MySQL | ✅ 已启用 | 100% | 完整 |
| PostgreSQL | ✅ 已启用 | 95% | 完整 |
| MongoDB | ✅ 已启用 | 90% | 完整 |
| Redis | ⚠️ 部分启用 | 70% | 基本完整 |

### 关键指标
- **总审计事件数**: 1,250,000 条
- **异常事件数**: 45 次
- **安全事件数**: 12 次
- **合规事件数**: 8 次

## 详细审计发现

### 1. 访问控制审计
#### 用户活动分析
- **活跃用户数**: 38 个
- **管理员活动**: 156 次
- **应用账户活动**: 890,000 次
- **异常登录尝试**: 23 次

#### 权限变更监控
- **用户创建**: 3 次
- **权限授予**: 15 次
- **权限撤销**: 2 次
- **账户锁定**: 1 次

### 2. 数据操作审计
#### 敏感数据访问
- **用户表查询**: 45,000 次
- **财务数据操作**: 12,000 次
- **个人数据访问**: 8,500 次
- **批量数据操作**: 3 次

#### 异常操作检测
- **大范围删除操作**: 2 次
- **非工作时间访问**: 156 次
- **并发异常操作**: 8 次

### 3. 系统安全审计
#### 认证安全
- **认证失败次数**: 189 次
- **暴力破解尝试**: 3 次
- **弱密码使用**: 0 次
- **多因子认证使用**: 100%

#### 配置变更
- **系统配置修改**: 12 次
- **安全参数调整**: 5 次
- **审计配置变更**: 2 次
- **备份配置修改**: 3 次

## 合规性评估

### SOX合规检查
- [✅] 用户访问日志完整记录
- [✅] 权限变更全程追踪
- [✅] 关键业务数据操作审计
- [✅] 定期审计报告生成
- [⚠️] 部分老旧系统审计覆盖不足

### GDPR合规检查
- [✅] 个人数据访问记录完整
- [✅] 数据主体权利行使追踪
- [✅] 数据处理活动日志
- [✅] 数据泄露事件记录
- [✅] 第三方数据处理监督

### ISO 27001合规检查
- [✅] 信息安全事件记录
- [✅] 访问控制有效性验证
- [✅] 系统配置变更管理
- [✅] 安全漏洞修复追踪
- [✅] 员工安全培训记录

## 风险评估和建议

### 高风险项
1. **Redis审计覆盖不完整** - 建议立即实施完整审计
2. **部分用户权限过大** - 需要重新审查和最小化权限
3. **老旧系统审计盲点** - 需要制定迁移计划

### 中风险项
1. **非工作时间访问较多** - 建议实施时间限制策略
2. **部分敏感操作缺乏多重验证** - 建议增加审批流程
3. **审计日志存储期限不足** - 建议延长存储时间

### 低风险项
1. **个别用户密码强度不足** - 建议加强密码策略
2. **部分审计告警阈值需要调整** - 建议优化配置

## 改进计划

### 短期行动 (1-3个月)
- [ ] 完善Redis审计配置
- [ ] 实施权限定期审查机制
- [ ] 优化审计告警策略
- [ ] 加强员工安全培训

### 中期规划 (3-6个月)
- [ ] 部署统一审计平台
- [ ] 实现审计数据智能分析
- [ ] 建立实时威胁检测系统
- [ ] 完善合规自动化报告

### 长期目标 (6-12个月)
- [ ] 实现零信任架构
- [ ] 部署AI驱动的安全分析
- [ ] 建立完整的安全运营中心
- [ ] 实现全流程自动化合规

## 结论

本期审计显示整体安全状况良好，审计体系基本完善，但仍需关注Redis审计覆盖和权限管理优化。建议按照改进计划逐步实施，持续提升数据库安全合规水平。

---
*报告生成时间: 2024-01-31 15:30:00*
*下次审计时间: 2024-02-28*