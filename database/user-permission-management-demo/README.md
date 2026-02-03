# 数据库用户权限管理实战演示

## 🎯 学习目标

通过本案例你将掌握企业级数据库用户权限管理的核心技能：

- 多层次用户体系设计和实现
- 精细化权限控制策略
- 角色-Based访问控制(RBAC)实践
- 审计和合规性权限管理
- 动态权限分配和回收机制
- 跨数据库系统的统一权限管理

## 🛠️ 环境准备

### 系统要求
- 已完成数据库安装配置环境
- 具备基础SQL操作能力
- 理解用户权限基本概念
- 熟悉企业组织架构特点

### 前置条件验证
```bash
# 验证数据库服务状态
systemctl is-active mysqld postgresql-14 mongod redis

# 验证管理员连接
mysql -u root -p -e "SELECT USER(), DATABASE();"
psql -U postgres -c "SELECT current_user, current_database();"
```

## 📁 项目结构

```
user-permission-management-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 权限管理脚本
│   ├── mysql_user_management.sh       # MySQL用户权限脚本
│   ├── postgresql_user_management.sh  # PostgreSQL用户权限脚本
│   ├── mongodb_user_management.sh     # MongoDB用户权限脚本
│   ├── redis_user_management.sh       # Redis用户权限脚本
│   └── unified_permission_manager.py  # 统一权限管理工具
├── configs/                           # 权限配置文件
│   ├── rbac_policy.json               # RBAC策略定义
│   ├── permission_templates/          # 权限模板
│   ├── audit_rules/                   # 审计规则配置
│   └── compliance_checklists/         # 合规检查清单
├── examples/                          # 实际应用案例
│   ├── enterprise_user_scenarios/     # 企业用户场景
│   ├── microservice_permissions/      # 微服务权限设计
│   ├── data_governance_cases/         # 数据治理案例
│   └── compliance_audit_examples/     # 合规审计示例
└── docs/                              # 详细文档
    ├── rbac_design_guide.md           # RBAC设计指南
    ├── permission_audit_manual.md     # 权限审计手册
    ├── compliance_framework.md        # 合规框架文档
    └── best_practices.md              # 最佳实践指南
```

## 🔐 核心权限管理技术详解

### 1. MySQL企业级用户权限管理

```sql
-- MySQL精细化权限管理体系

-- 1. 创建分层用户体系
-- 系统管理员账户
CREATE USER 'dba_admin'@'%' IDENTIFIED BY 'StrongPass123!';
GRANT ALL PRIVILEGES ON *.* TO 'dba_admin'@'%' WITH GRANT OPTION;
GRANT RELOAD, PROCESS, SUPER, REPLICATION CLIENT ON *.* TO 'dba_admin'@'%';

-- 应用管理员账户
CREATE USER 'app_admin'@'192.168.1.%' IDENTIFIED BY 'AppPass456!';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER 
ON app_database.* TO 'app_admin'@'192.168.1.%';

-- 只读分析师账户
CREATE USER 'analyst_ro'@'10.0.0.%' IDENTIFIED BY 'ReadOnly789!';
GRANT SELECT ON analytics_db.* TO 'analyst_ro'@'10.0.0.%';

-- 应用服务账户
CREATE USER 'app_service'@'192.168.1.%' IDENTIFIED BY 'ServicePass000!';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_database.users TO 'app_service'@'192.168.1.%';
GRANT SELECT, INSERT, UPDATE ON app_database.orders TO 'app_service'@'192.168.1.%';
GRANT SELECT ON app_database.products TO 'app_service'@'192.168.1.%';

-- 2. 实施基于角色的访问控制(RBAC)
-- 创建角色
CREATE ROLE 'app_developer', 'data_analyst', 'report_viewer';

-- 为角色分配权限
GRANT SELECT, INSERT, UPDATE, DELETE ON app_dev.* TO 'app_developer';
GRANT SELECT ON analytics.* TO 'data_analyst';
GRANT SELECT ON reports.* TO 'report_viewer';

-- 为用户分配角色
GRANT 'app_developer' TO 'dev_user'@'%';
GRANT 'data_analyst' TO 'analyst_user'@'%';
GRANT 'report_viewer' TO 'report_user'@'%';

-- 激活角色
SET DEFAULT ROLE ALL TO 'dev_user'@'%', 'analyst_user'@'%', 'report_user'@'%';

-- 3. 实施行级安全策略
-- 创建视图实现数据过滤
CREATE VIEW user_orders_filtered AS
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.department = USER();

-- 为特定用户组授予权限
GRANT SELECT ON user_orders_filtered TO 'sales_team'@'%';

-- 4. 审计和监控配置
-- 启用通用日志记录敏感操作
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = '/var/log/mysql/general.log';

-- 启用审计插件(企业版)
INSTALL PLUGIN audit_log SONAME 'audit_log.so';
SET GLOBAL audit_log_policy = ALL;
```

### 2. PostgreSQL高级权限管理

```sql
-- PostgreSQL企业级权限管理

-- 1. 创建安全的用户体系
-- 数据库超级用户(严格限制)
CREATE USER dba_super WITH SUPERUSER CREATEROLE CREATEDB 
PASSWORD 'SuperSecurePass2024!';

-- 应用架构师用户
CREATE USER app_architect WITH CREATEROLE PASSWORD 'ArchitectPass123!';
GRANT CREATE ON DATABASE app_production TO app_architect;

-- 应用服务用户
CREATE USER app_service WITH PASSWORD 'ServiceSecure456!';
GRANT CONNECT ON DATABASE app_production TO app_service;

-- 只读分析用户
CREATE USER analyst_ro WITH PASSWORD 'ReadOnlyAnalytics789!';
GRANT CONNECT ON DATABASE analytics TO analyst_ro;

-- 2. 实施模式级别的权限控制
-- 创建应用模式
CREATE SCHEMA app_core AUTHORIZATION app_architect;
CREATE SCHEMA app_reporting AUTHORIZATION app_architect;

-- 为不同用户组设置模式权限
GRANT USAGE ON SCHEMA app_core TO app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app_core TO app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app_core TO app_service;

GRANT USAGE ON SCHEMA app_reporting TO analyst_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA app_reporting TO analyst_ro;

-- 3. 实施行级安全(RLS)
-- 启用表的行级安全
ALTER TABLE customer_data ENABLE ROW LEVEL SECURITY;

-- 创建策略
CREATE POLICY customer_access_policy ON customer_data
FOR ALL TO app_service
USING (account_manager = CURRENT_USER);

CREATE POLICY analyst_view_policy ON customer_data
FOR SELECT TO analyst_ro
USING (region IN (SELECT region FROM user_regions WHERE username = CURRENT_USER));

-- 4. 创建安全的角色层次结构
-- 基础角色
CREATE ROLE app_readers;
CREATE ROLE app_writers;
CREATE ROLE app_admins;

-- 授予权限给角色
GRANT CONNECT ON DATABASE app_production TO app_readers;
GRANT USAGE ON SCHEMA app_core TO app_readers;
GRANT SELECT ON ALL TABLES IN SCHEMA app_core TO app_readers;

GRANT app_readers TO app_writers;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app_core TO app_writers;

GRANT app_writers TO app_admins;
GRANT CREATE ON SCHEMA app_core TO app_admins;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA app_core TO app_admins;

-- 5. 审计和合规配置
-- 启用审计日志
LOAD 'pgaudit';
SET pgaudit.log = 'ALL';
SET pgaudit.log_level = 'log';

-- 创建审计角色
CREATE ROLE audit_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA pg_catalog TO audit_reader;
```

### 3. MongoDB企业级权限控制

```javascript
// MongoDB企业级权限管理体系

// 1. 创建安全管理用户
use admin
db.createUser({
  user: "security_admin",
  pwd: "${DB_PASSWORD}",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
})

// 2. 创建应用数据库和用户体系
use app_production
db.createUser({
  user: "app_admin",
  pwd: "${DB_PASSWORD}",
  roles: [
    { role: "dbOwner", db: "app_production" },
    { role: "readWrite", db: "app_analytics" }
  ]
})

db.createUser({
  user: "app_service",
  pwd: "${DB_PASSWORD}",
  roles: [
    { role: "readWrite", db: "app_production" },
    { role: "read", db: "app_config" }
  ]
})

db.createUser({
  user: "analyst_ro",
  pwd: "${DB_PASSWORD}",
  roles: [
    { role: "read", db: "app_analytics" },
    { role: "read", db: "business_reports" }
  ]
})

// 3. 实施基于角色的访问控制
// 创建自定义角色
db.createRole({
  role: "app_developer",
  privileges: [
    {
      resource: { db: "app_development", collection: "" },
      actions: [ "find", "insert", "update", "remove", "createCollection" ]
    }
  ],
  roles: []
})

db.createRole({
  role: "data_scientist",
  privileges: [
    {
      resource: { db: "analytics", collection: "" },
      actions: [ "find", "aggregate" ]
    }
  ],
  roles: []
})

// 4. 实施字段级别权限控制
// 创建视图实现数据脱敏
db.createView(
  "customer_view",
  "customers",
  [
    {
      $project: {
        customer_id: 1,
        name: 1,
        email: 1,
        region: 1,
        // 脱敏敏感字段
        phone: { $concat: [{ $substr: ["$phone", 0, 3] }, "***-****"] },
        ssn: "***-**-" + { $substr: ["$ssn", 7, 4] }
      }
    }
  ]
)

// 为分析用户授予视图权限
db.grantRolesToUser("analyst_ro", [
  { role: "read", db: "app_production", collection: "customer_view" }
])

// 5. 审计和监控配置
// 启用审计日志
// 在mongod.conf中配置:
/*
auditLog:
  destination: file
  format: JSON
  path: /var/log/mongodb/audit.log
  filter: '{$or: [{atype: "authenticate"}, {atype: "createUser"}, {atype: "dropUser"}]}'
*/

// 6. 动态权限管理脚本
// JavaScript权限管理工具
function updateUserPermissions(username, dbName, newPermissions) {
  const user = db.getUser(username);
  if (!user) {
    throw new Error(`User ${username} not found`);
  }
  
  // 移除旧权限
  db.revokeRolesFromUser(username, user.roles);
  
  // 授予新权限
  db.grantRolesToUser(username, newPermissions);
  
  // 记录变更
  console.log(`Updated permissions for user ${username} in database ${dbName}`);
}

// 使用示例
updateUserPermissions(
  "app_service",
  "app_production",
  [
    { role: "readWrite", db: "app_production" },
    { role: "read", db: "reference_data" }
  ]
)
```

### 4. Redis企业级访问控制

```bash
#!/bin/bash
# Redis企业级权限管理脚本

REDIS_CLI="redis-cli"
REDIS_CONF="/opt/redis/conf/redis.conf"

# 1. 启用ACL访问控制
# 在redis.conf中启用ACL
echo "aclfile /opt/redis/conf/users.acl" >> $REDIS_CONF

# 2. 创建用户和权限规则
# 管理员用户
$REDIS_CLI ACL SETUSER admin on >AdminPass2024! ~* &* +@all

# 应用服务用户
$REDIS_CLI ACL SETUSER app_service on >AppService123! \
  ~app:* ~session:* ~cache:* \
  +get +set +del +expire +ttl +exists +mget +mset \
  -@admin -@dangerous

# 只读监控用户
$REDIS_CLI ACL SETUSER monitor_ro on >MonitorReadOnly456! \
  ~stats:* ~metrics:* ~health:* \
  +get +hlen +llen +scard +zcard +info +ping \
  -@write -@admin

# 缓存专用用户
$REDIS_CLI ACL SETUSER cache_user on >CacheUser789! \
  ~cache:* ~session:* \
  +get +set +del +expire +ttl +exists \
  -@hash -@set -@sortedset -@list -@stream

# 3. 实施基于频道的发布订阅权限
$REDIS_CLI ACL SETUSER pubsub_user on >PubSubPass321! \
  resetchannels \
  &notifications:* &events:* \
  +subscribe +psubscribe +publish

# 4. 创建权限模板
cat > /opt/redis/conf/user_templates.conf << EOF
# 应用用户模板
user app_template off resetchannels \
  ~app:* ~user:* ~session:* \
  +get +set +del +expire +ttl +exists +mget \
  -@admin -@dangerous -@scripting

# 分析用户模板
user analytics_template off resetchannels \
  ~analytics:* ~reports:* ~metrics:* \
  +get +hget +hgetall +smembers +zrange +lrange \
  -@write -@admin -@dangerous

# 微服务用户模板
user microservice_template off resetchannels \
  ~service:{service_name}:* \
  +get +set +del +expire +publish \
  -@admin -@dangerous
EOF

# 5. 权限验证和测试脚本
validate_redis_permissions() {
  echo "=== Redis权限验证 ==="
  
  # 测试管理员权限
  echo "测试管理员权限..."
  $REDIS_CLI -u admin -a AdminPass2024! ping
  if [ $? -eq 0 ]; then
    echo "✅ 管理员连接成功"
  else
    echo "❌ 管理员连接失败"
  fi
  
  # 测试应用用户权限
  echo "测试应用用户权限..."
  $REDIS_CLI -u app_service -a AppService123! set test:key "test_value"
  if [ $? -eq 0 ]; then
    echo "✅ 应用用户写入权限正常"
  else
    echo "❌ 应用用户写入权限异常"
  fi
  
  # 测试只读用户权限
  echo "测试只读用户权限..."
  $REDIS_CLI -u monitor_ro -a MonitorReadOnly456! get test:key
  $REDIS_CLI -u monitor_ro -a MonitorReadOnly456! set test:key2 "should_fail" 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "✅ 只读用户权限控制正常"
  else
    echo "❌ 只读用户权限控制异常"
  fi
}

# 6. 权限审计脚本
audit_redis_permissions() {
  echo "=== Redis权限审计 ==="
  
  # 列出所有用户
  echo "当前用户列表:"
  $REDIS_CLI ACL LIST
  
  # 检查权限配置
  echo "权限配置检查:"
  $REDIS_CLI ACL CAT
  $REDIS_CLI ACL USERS
  
  # 生成权限报告
  REPORT_FILE="/tmp/redis_permissions_$(date +%Y%m%d_%H%M%S).txt"
  $REDIS_CLI ACL LIST > $REPORT_FILE
  echo "权限审计报告已保存: $REPORT_FILE"
}

# 执行验证
validate_redis_permissions
audit_redis_permissions
```

## 📊 统一权限管理平台

### Python统一权限管理工具
```python
#!/usr/bin/env python3
"""
企业级统一权限管理平台
支持MySQL、PostgreSQL、MongoDB、Redis的统一权限管理
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PermissionRequest:
    """权限请求数据结构"""
    user_id: str
    database_type: str
    database_name: str
    permissions: List[str]
    ip_whitelist: List[str]
    validity_period: Optional[str] = None
    justification: str = ""

class DatabasePermissionManager(ABC):
    """数据库权限管理抽象基类"""
    
    @abstractmethod
    def create_user(self, username: str, password: str) -> bool:
        pass
    
    @abstractmethod
    def grant_permissions(self, username: str, permissions: List[str]) -> bool:
        pass
    
    @abstractmethod
    def revoke_permissions(self, username: str, permissions: List[str]) -> bool:
        pass
    
    @abstractmethod
    def audit_permissions(self, username: str) -> Dict:
        pass

class UnifiedPermissionManager:
    """统一权限管理器"""
    
    def __init__(self):
        self.managers = {}
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def register_manager(self, db_type: str, manager: DatabasePermissionManager):
        """注册数据库权限管理器"""
        self.managers[db_type] = manager
        self.logger.info(f"Registered {db_type} permission manager")
    
    def process_permission_request(self, request: PermissionRequest) -> Dict:
        """处理权限申请"""
        try:
            if request.database_type not in self.managers:
                raise ValueError(f"Unsupported database type: {request.database_type}")
            
            manager = self.managers[request.database_type]
            
            # 创建用户
            user_created = manager.create_user(request.user_id, self._generate_password())
            
            # 授予权限
            permissions_granted = manager.grant_permissions(
                request.user_id, 
                request.permissions
            )
            
            # 配置IP白名单
            self._configure_ip_whitelist(request.user_id, request.ip_whitelist)
            
            # 记录审计日志
            audit_info = manager.audit_permissions(request.user_id)
            
            return {
                "status": "success",
                "user_id": request.user_id,
                "permissions_granted": permissions_granted,
                "audit_info": audit_info,
                "validity_period": request.validity_period
            }
            
        except Exception as e:
            self.logger.error(f"Permission request failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _generate_password(self) -> str:
        """生成安全密码"""
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(16))
    
    def _configure_ip_whitelist(self, username: str, ip_list: List[str]):
        """配置IP白名单"""
        # 实现IP白名单配置逻辑
        self.logger.info(f"Configured IP whitelist for {username}: {ip_list}")

# 使用示例
def main():
    # 初始化统一权限管理器
    upm = UnifiedPermissionManager()
    
    # 处理权限申请
    request = PermissionRequest(
        user_id="app_user_001",
        database_type="mysql",
        database_name="app_production",
        permissions=["SELECT", "INSERT", "UPDATE"],
        ip_whitelist=["192.168.1.100", "10.0.0.0/24"],
        validity_period="2024-12-31",
        justification="应用服务账户权限申请"
    )
    
    result = upm.process_permission_request(request)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

## 🧪 权限验证测试

### 自动化权限测试脚本
```bash
#!/bin/bash
# 数据库权限验证测试套件

TEST_RESULTS=()

# MySQL权限测试
test_mysql_permissions() {
  echo "=== MySQL权限测试 ==="
  
  # 测试用户创建
  mysql -u root -p << EOF
  CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'TestPass123!';
  GRANT SELECT ON test_db.* TO 'test_user'@'localhost';
  FLUSH PRIVILEGES;
EOF
  
  # 验证权限
  if mysql -u test_user -pTestPass123! -e "USE test_db; SELECT 1;" 2>/dev/null; then
    TEST_RESULTS+=("MySQL权限测试: 通过")
    echo "✅ MySQL权限配置正常"
  else
    TEST_RESULTS+=("MySQL权限测试: 失败")
    echo "❌ MySQL权限配置异常"
  fi
}

# PostgreSQL权限测试
test_postgresql_permissions() {
  echo "=== PostgreSQL权限测试 ==="
  
  # 测试用户和权限
  psql -U postgres << EOF
  CREATE USER test_user WITH PASSWORD 'TestPass456!';
  CREATE DATABASE test_db OWNER test_user;
  GRANT CONNECT ON DATABASE test_db TO test_user;
EOF
  
  # 验证权限
  if psql -U test_user -d test_db -c "SELECT current_user;" 2>/dev/null; then
    TEST_RESULTS+=("PostgreSQL权限测试: 通过")
    echo "✅ PostgreSQL权限配置正常"
  else
    TEST_RESULTS+=("PostgreSQL权限测试: 失败")
    echo "❌ PostgreSQL权限配置异常"
  fi
}

# MongoDB权限测试
test_mongodb_permissions() {
  echo "=== MongoDB权限测试 ==="
  
  # 测试用户创建
  mongo admin << EOF
  db.createUser({
    user: "test_user",
    pwd: "${DB_PASSWORD}",
    roles: [{role: "read", db: "test_db"}]
  })
EOF
  
  # 验证权限
  if mongo test_db -u test_user -p TestPass789! --eval "db.stats()" 2>/dev/null; then
    TEST_RESULTS+=("MongoDB权限测试: 通过")
    echo "✅ MongoDB权限配置正常"
  else
    TEST_RESULTS+=("MongoDB权限测试: 失败")
    echo "❌ MongoDB权限配置异常"
  fi
}

# 生成测试报告
generate_test_report() {
  echo "=== 权限测试报告 ==="
  for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
  done
  
  # 保存报告
  REPORT_FILE="/tmp/permission_test_report_$(date +%Y%m%d_%H%M%S).txt"
  printf "%s\n" "${TEST_RESULTS[@]}" > "$REPORT_FILE"
  echo "测试报告已保存: $REPORT_FILE"
}

# 执行所有测试
test_mysql_permissions
test_postgresql_permissions
test_mongodb_permissions
generate_test_report
```

## 📚 最佳实践总结

### 企业级权限管理原则
1. **最小权限原则**: 用户只获得完成工作的最小必要权限
2. **职责分离**: 不同职责的用户拥有不同的权限集合
3. **定期审查**: 定期审计和清理不必要的权限
4. **动态管理**: 根据业务变化及时调整权限配置
5. **审计追踪**: 完整记录所有权限变更和使用情况

### 合规性要求
- **SOX合规**: 严格的访问控制和审计要求
- **HIPAA合规**: 医疗数据的特殊保护要求
- **GDPR合规**: 个人数据保护和隐私权要求
- **PCI-DSS合规**: 支付卡数据的安全处理要求

---
> **💡 提示**: 权限管理是数据库安全的核心，建议结合企业的安全策略和合规要求，建立完善的权限管理体系。