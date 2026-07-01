# MySQL高可用架构实践演示

## 🎯 学习目标

通过本案例你将掌握企业级MySQL高可用架构的核心技能：

- 设计和实施MySQL主从复制架构
- 配置GTID和半同步复制确保数据一致性
- 实现自动故障检测和切换机制
- 部署读写分离和负载均衡方案
- 建立完善的监控和告警体系
- 满足99.99%的可用性SLA要求

## 🛠️ 环境准备

### 系统要求
- 已完成MySQL数据库安装配置环境
- 具备基础复制概念理解
- 准备至少3台服务器节点
- 网络延迟小于5ms，带宽充足

### 前置条件验证
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 验证MySQL服务状态
systemctl is-active mysqld

# 检查网络连通性
ping mysql-master.example.com
ping mysql-slave1.example.com
ping mysql-slave2.example.com

# 验证时间同步
ntpq -p
chrony sources
```

## 📁 项目结构

```
mysql-high-availability-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 高可用脚本
│   ├── replication_setup.sh           # 复制配置脚本
│   ├── mha_manager_setup.sh           # MHA管理器配置
│   ├── proxysql_setup.sh              # ProxySQL配置脚本
│   ├── failover_test.sh               # 故障切换测试脚本
│   └── monitoring_setup.py            # 监控配置脚本
├── configs/                           # 配置文件
│   ├── master_slave_configs/          # 主从配置文件
│   ├── mha_configs/                   # MHA配置文件
│   ├── proxysql_configs/              # ProxySQL配置文件
│   └── monitoring_configs/            # 监控配置文件
├── examples/                          # 实际案例
│   ├── replication_scenarios/         # 复制场景案例
│   ├── failover_procedures/           # 故障切换流程
│   ├── scaling_strategies/            # 扩展策略案例
│   └── disaster_recovery/             # 灾难恢复方案
├── playbooks/                         # 自动化部署
│   ├── ansible_playbooks/             # Ansible部署剧本
│   ├── terraform_modules/             # Terraform模块
│   └── kubernetes_manifests/          # K8s部署清单
└── docs/                              # 详细文档
    ├── architecture_design.md         # 架构设计方案
    ├── deployment_guide.md            # 部署指南
    ├── operational_procedures.md      # 运维流程文档
    └── best_practices.md              # 最佳实践指南
```

## 🚀 快速开始

### 一键启动主从环境

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 进入案例目录
cd database/mysql-high-availability-demo

# 2. 启动 MySQL 主从容器并自动配置复制
./scripts/setup_replication.sh

# 3. 检查复制状态
./scripts/check_replication.sh

# 4. 清理环境
./scripts/teardown.sh
```

### 手动连接测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 连接主库（写节点）
mysql -h127.0.0.1 -P3306 -uroot -prootpass

# 连接从库（读节点）
mysql -h127.0.0.1 -P3307 -uroot -prootpass
```

---

## 📖 核心概念

### 1. 主从复制（Master-Slave Replication）

MySQL 主从复制允许将一个 MySQL 服务器（主库）的数据变更同步到一个或多个从库。写操作集中在主库，读操作可以分散到从库，从而提升读性能和可用性。

### 2. GTID（Global Transaction Identifier）

GTID 是 MySQL 5.6 引入的全局事务标识符，格式为 `source_id:transaction_id`。启用 GTID 后，从库可以自动定位需要复制的位置，简化故障切换和拓扑管理。

### 3. 半同步复制（Semi-Synchronous Replication）

半同步复制要求主库在提交事务时，至少等待一个从库确认收到日志。相比异步复制，它能显著降低主库故障时的数据丢失风险（RPO 更接近 0）。

### 4. 读写分离

通过 ProxySQL、MySQL Router 等中间件，将写请求路由到主库，读请求路由到从库。本案例使用端口区分主从（主库 3306，从库 3307）来模拟读写分离效果。

## 💻 代码示例

### 启动主从环境

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 进入案例目录
cd database/mysql-high-availability-demo

# 启动容器并配置复制
./scripts/setup_replication.sh
```

### 检查复制状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check_replication.sh
```

### 手动验证数据同步

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 在主库写入数据
docker exec mysql-master mysql -uroot -prootpass -e \
  "INSERT INTO demo.ha_test VALUES (2, 'manual_test') ON DUPLICATE KEY UPDATE name='manual_test';"

# 在从库查询（约 1-2 秒后）
docker exec mysql-slave mysql -uroot -prootpass -e "SELECT * FROM demo.ha_test;"
```

### 清理环境

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/teardown.sh
```

## 🏗️ 企业级高可用架构设计

### 高可用架构拓扑
```yaml
# MySQL高可用架构设计
high_availability_architecture:
  topology: "1主2从+MHA管理器+ProxySQL代理"
  
  components:
    master_node:
      role: "主数据库服务器"
      responsibilities:
        - 处理所有写操作
        - 实时同步数据到从库
        - 维护全局事务ID(GTID)
      specifications:
        - CPU: 8核以上
        - 内存: 32GB以上
        - 存储: SSD RAID 10
        - 网络: 万兆网络
    
    slave_nodes:
      - node_1:
          role: "从数据库服务器1"
          responsibilities:
            - 实时同步主库数据
            - 处理读请求负载
            - 作为故障切换候选
      - node_2:
          role: "从数据库服务器2"
          responsibilities:
            - 实时同步主库数据
            - 处理读请求负载
            - 作为故障切换候选
    
    mha_manager:
      role: "高可用管理器"
      responsibilities:
        - 监控主库健康状态
        - 自动故障检测
        - 执行故障切换
        - 配置VIP漂移
      deployment_options:
        - 独立服务器部署
        - 与从库共部署
        - 容器化部署
    
    proxysql:
      role: "数据库代理"
      responsibilities:
        - 读写分离路由
        - 负载均衡
        - 连接池管理
        - 查询缓存
      configuration:
        - 监听端口: 6033
        - 管理端口: 6032
        - 健康检查间隔: 1秒
    
    monitoring_system:
      components:
        - prometheus: "指标收集"
        - grafana: "可视化展示"
        - alertmanager: "告警管理"
        - consul: "服务发现"
```

## 🔧 核心高可用技术实现

### 1. MySQL主从复制配置

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
#!/bin/bash
# MySQL主从复制完整配置脚本

MASTER_HOST="mysql-master.example.com"
SLAVE_HOSTS=("mysql-slave1.example.com" "mysql-slave2.example.com")
REPLICATION_USER="repl_user"
REPLICATION_password: "${DB_PASSWORD}"

# 1. 主库配置
configure_master() {
  echo "配置MySQL主库..."
  
  # 在my.cnf中添加主库配置
  cat >> /etc/my.cnf << EOF
[mysqld]
# 基本复制配置
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
binlog-row-image = FULL

# GTID配置
gtid-mode = ON
enforce-gtid-consistency = ON

# 半同步复制
rpl-semi-sync-master-enabled = 1
rpl-semi-sync-master-timeout = 10000

# 其他重要配置
binlog-do-db = application_db
expire_logs_days = 7
max_connections = 2000
innodb_flush_log_at_trx_commit = 1
sync_binlog = 1
EOF
  
  # 重启MySQL服务
  systemctl restart mysqld
  
  # 创建复制用户
  mysql -u root -p << EOF
CREATE USER '${REPLICATION_USER}'@'%' IDENTIFIED BY '${REPLICATION_PASSWORD}';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO '${REPLICATION_USER}'@'%';
GRANT SELECT ON *.* TO '${REPLICATION_USER}'@'%';
FLUSH PRIVILEGES;
FLUSH TABLES WITH READ LOCK;
EOF
  
  # 获取主库状态信息
  MASTER_STATUS=$(mysql -u root -p -e "SHOW MASTER STATUS\G" | grep "File\|Position\|Executed_Gtid_Set")
  echo "主库状态信息:"
  echo "$MASTER_STATUS"
  
  # 解锁表
  mysql -u root -p -e "UNLOCK TABLES;"
  
  echo "主库配置完成"
}

# 2. 从库配置
configure_slaves() {
  echo "配置MySQL从库..."
  
  for slave_host in "${SLAVE_HOSTS[@]}"; do
    echo "配置从库: $slave_host"
    
    # SSH到从库执行配置
    ssh root@$slave_host << EOF
# 配置从库my.cnf
cat >> /etc/my.cnf << CONFIG_EOF
[mysqld]
# 基本复制配置
server-id = $(echo $slave_host | sed 's/[^0-9]*//g')
relay-log = relay-bin
log-slave-updates = 1
read-only = 1

# GTID配置
gtid-mode = ON
enforce-gtid-consistency = ON

# 半同步复制
rpl-semi-sync-slave-enabled = 1

# 其他配置
relay-log-recovery = 1
skip-slave-start = 1
CONFIG_EOF

# 重启MySQL服务
systemctl restart mysqld

# 配置主从复制
mysql -u root -p << MYSQL_EOF
CHANGE MASTER TO
  MASTER_HOST='${MASTER_HOST}',
  MASTER_USER='${REPLICATION_USER}',
  MASTER_password: "${DB_PASSWORD}",
  MASTER_AUTO_POSITION = 1;

START SLAVE;
MYSQL_EOF

# 验证复制状态
mysql -u root -p -e "SHOW SLAVE STATUS\G" | grep -E "(Slave_IO_Running|Slave_SQL_Running|Seconds_Behind_Master)"
EOF
  done
  
  echo "从库配置完成"
}

# 3. 复制状态验证
verify_replication() {
  echo "验证复制状态..."
  
  for slave_host in "${SLAVE_HOSTS[@]}"; do
    echo "检查从库 $slave_host 复制状态:"
    ssh root@$slave_host "mysql -u root -p -e 'SHOW SLAVE STATUS\G'" | \
      grep -E "(Slave_IO_Running|Slave_SQL_Running|Seconds_Behind_Master|Last_Error)"
  done
  
  # 测试数据同步
  echo "测试数据同步..."
  mysql -u root -p << EOF
CREATE DATABASE IF NOT EXISTS test_replication;
USE test_replication;
CREATE TABLE test_table (id INT PRIMARY KEY, data VARCHAR(100));
INSERT INTO test_table VALUES (1, 'Replication Test Data');
COMMIT;
EOF
  
  sleep 3
  
  for slave_host in "${SLAVE_HOSTS[@]}"; do
    echo "验证从库 $slave_host 数据同步:"
    ssh root@$slave_host "mysql -u root -p -e 'SELECT * FROM test_replication.test_table;'"
  done
}

# 4. 半同步复制配置
configure_semi_sync() {
  echo "配置半同步复制..."
  
  # 在主库启用半同步
  mysql -u root -p << EOF
INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';
SET GLOBAL rpl_semi_sync_master_enabled = 1;
SET GLOBAL rpl_semi_sync_master_timeout = 10000;
SET GLOBAL rpl_semi_sync_master_wait_no_slave = 1;
EOF
  
  # 在从库启用半同步
  for slave_host in "${SLAVE_HOSTS[@]}"; do
    ssh root@$slave_host << EOF
mysql -u root -p << MYSQL_EOF
INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';
SET GLOBAL rpl_semi_sync_slave_enabled = 1;
STOP SLAVE IO_THREAD;
START SLAVE IO_THREAD;
MYSQL_EOF
EOF
  done
  
  # 验证半同步状态
  mysql -u root -p -e "SHOW STATUS LIKE 'Rpl_semi_sync%';"
}

# 主执行函数
main() {
  case "$1" in
    setup-all)
      configure_master
      configure_slaves
      verify_replication
      configure_semi_sync
      echo "MySQL主从复制配置完成"
      ;;
    configure-master)
      configure_master
      ;;
    configure-slaves)
      configure_slaves
      ;;
    verify)
      verify_replication
      ;;
    semi-sync)
      configure_semi_sync
      ;;
    *)
      echo "Usage: $0 {setup-all|configure-master|configure-slaves|verify|semi-sync}"
      exit 1
      ;;
  esac
}

main "$@"
```

### 2. MHA高可用管理器配置

```perl
#!/usr/bin/perl
# MHA Manager配置脚本

use strict;
use warnings;
use MHA::ManagerConst;
use MHA::ManagerUtil;

# MHA配置参数
my $mha_config = {
    'user' => 'mha_user',
    'password' => 'MhaPass456!',
    'manager_workdir' => '/var/log/masterha/app1',
    'manager_log' => '/var/log/masterha/app1/manager.log',
    'remote_workdir' => '/var/log/masterha/app1',
    'master_binlog_dir' => '/var/lib/mysql',
    'master_ip_failover_script' => '/usr/local/bin/master_ip_failover',
    'master_ip_online_change_script' => '/usr/local/bin/master_ip_online_change',
    'ping_interval' => 3,
    'ping_type' => 'SELECT',
    'secondary_check_script' => '/usr/local/bin/masterha_secondary_check -s remote_host',
    'shutdown_script' => '',
    'ssh_user' => 'root',
    'master_bind' => ''
};

# 1. 创建MHA应用配置
sub create_mha_app_config {
    my $config_file = '/etc/masterha/app1.cnf';
    
    open(my $fh, '>', $config_file) or die "无法创建配置文件: $!";
    
    print $fh "[server default]\n";
    for my $key (keys %$mha_config) {
        print $fh "$key = $mha_config->{$key}\n";
    }
    
    print $fh "\n[server1]\n";
    print $fh "hostname=mysql-master.example.com\n";
    print $fh "candidate_master=1\n";
    
    print $fh "\n[server2]\n";
    print $fh "hostname=mysql-slave1.example.com\n";
    print $fh "candidate_master=1\n";
    
    print $fh "\n[server3]\n";
    print $fh "hostname=mysql-slave2.example.com\n";
    print $fh "no_master=1\n";
    
    close($fh);
    print "MHA应用配置文件创建完成: $config_file\n";
}

# 2. 配置VIP故障切换脚本
sub create_failover_script {
    my $failover_script = '/usr/local/bin/master_ip_failover';
    
    open(my $fh, '>', $failover_script) or die "无法创建故障切换脚本: $!";
    
    print $fh <<'EOF';
#!/bin/bash
# MHA VIP故障切换脚本

VIP="192.168.1.100/24"
GATEWAY="192.168.1.1"
INTERFACE="eth0"
SSH_USER="root"

OLD_MASTER_IP=$1
NEW_MASTER_IP=$2
NEW_MASTER_HOSTNAME=$3

# 验证参数
if [ -z "$OLD_MASTER_IP" ] || [ -z "$NEW_MASTER_IP" ]; then
    echo "参数不足"
    exit 1
fi

# 在旧主库上删除VIP
ssh $SSH_USER@$OLD_MASTER_IP "/sbin/ip addr del $VIP dev $INTERFACE 2>/dev/null || true"

# 在新主库上添加VIP
ssh $SSH_USER@$NEW_MASTER_IP "/sbin/ip addr add $VIP dev $INTERFACE"
ssh $SSH_USER@$NEW_MASTER_IP "/sbin/arping -U -c 3 -I $INTERFACE $VIP"

echo "VIP $VIP 已切换到 $NEW_MASTER_IP ($NEW_MASTER_HOSTNAME)"
exit 0
EOF
    
    close($fh);
    chmod 755 $failover_script;
    print "故障切换脚本创建完成: $failover_script\n";
}

# 3. 配置在线切换脚本
sub create_online_change_script {
    my $online_script = '/usr/local/bin/master_ip_online_change';
    
    open(my $fh, '>', $online_script) or die "无法创建在线切换脚本: $!";
    
    print $fh <<'EOF';
#!/bin/bash
# MHA在线VIP切换脚本

VIP="192.168.1.100/24"
INTERFACE="eth0"
SSH_USER="root"

OLD_MASTER_IP=$1
NEW_MASTER_IP=$2

# 验证参数
if [ -z "$OLD_MASTER_IP" ] || [ -z "$NEW_MASTER_IP" ]; then
    echo "参数不足"
    exit 1
fi

# 在旧主库上删除VIP
ssh $SSH_USER@$OLD_MASTER_IP "/sbin/ip addr del $VIP dev $INTERFACE"

# 在新主库上添加VIP
ssh $SSH_USER@$NEW_MASTER_IP "/sbin/ip addr add $VIP dev $INTERFACE"
ssh $SSH_USER@$NEW_MASTER_IP "/sbin/arping -U -c 3 -I $INTERFACE $VIP"

echo "在线VIP切换完成: $OLD_MASTER_IP -> $NEW_MASTER_IP"
exit 0
EOF
    
    close($fh);
    chmod 755 $online_script;
    print "在线切换脚本创建完成: $online_script\n";
}

# 4. 配置二次检查脚本
sub create_secondary_check_script {
    my $check_script = '/usr/local/bin/masterha_secondary_check';
    
    open(my $fh, '>', $check_script) or die "无法创建二次检查脚本: $!";
    
    print $fh <<'EOF';
#!/bin/bash
# MHA二次检查脚本

REMOTE_HOST=$1
MASTER_IP=$2

# 通过远程主机检查主库状态
ssh $REMOTE_HOST "mysql -h$MASTER_IP -u root -p -e 'SELECT 1;' 2>/dev/null"

if [ $? -eq 0 ]; then
    echo "二次检查通过: 主库 $MASTER_IP 可访问"
    exit 0
else
    echo "二次检查失败: 主库 $MASTER_IP 不可访问"
    exit 1
fi
EOF
    
    close($fh);
    chmod 755 $check_script;
    print "二次检查脚本创建完成: $check_script\n";
}

# 5. MHA健康检查
sub run_mha_check {
    my $app_name = "app1";
    
    print "执行MHA健康检查...\n";
    
    # 检查SSH连接
    system("masterha_check_ssh --conf=/etc/masterha/app1.cnf");
    
    # 检查复制状态
    system("masterha_check_repl --conf=/etc/masterha/app1.cnf");
    
    # 检查主库状态
    system("masterha_check_status --conf=/etc/masterha/app1.cnf");
}

# 6. 启动MHA Manager
sub start_mha_manager {
    my $app_name = "app1";
    
    print "启动MHA Manager...\n";
    
    system("nohup masterha_manager --conf=/etc/masterha/app1.cnf < /dev/null > /var/log/masterha/app1/manager.log 2>&1 &");
    
    # 验证启动状态
    sleep 5;
    if (system("masterha_check_status --conf=/etc/masterha/app1.cnf") == 0) {
        print "MHA Manager启动成功\n";
    } else {
        print "MHA Manager启动失败\n";
        exit 1;
    }
}

# 主执行函数
sub main {
    my $action = shift @ARGV || 'setup';
    
    if ($action eq 'setup') {
        create_mha_app_config();
        create_failover_script();
        create_online_change_script();
        create_secondary_check_script();
        run_mha_check();
        start_mha_manager();
        print "MHA高可用配置完成\n";
    } elsif ($action eq 'check') {
        run_mha_check();
    } elsif ($action eq 'start') {
        start_mha_manager();
    } else {
        print "用法: $0 [setup|check|start]\n";
        exit 1;
    }
}

main(@ARGV);
```

### 3. ProxySQL读写分离配置

```sql
-- ProxySQL读写分离完整配置

-- 1. 配置MySQL后端服务器
INSERT INTO mysql_servers (hostgroup_id, hostname, port, weight, status) 
VALUES 
(1, 'mysql-master.example.com', 3306, 1000, 'ONLINE'),  -- 写入组
(2, 'mysql-slave1.example.com', 3306, 100, 'ONLINE'),   -- 读取组
(2, 'mysql-slave2.example.com', 3306, 100, 'ONLINE');   -- 读取组

-- 2. 配置用户和密码
INSERT INTO mysql_users (username, password, default_hostgroup, active) 
VALUES ('app_user', 'AppPass789!', 1, 1);

-- 3. 配置读写分离规则
INSERT INTO mysql_query_rules (rule_id, active, match_digest, destination_hostgroup, apply) 
VALUES 
(1, 1, '^SELECT.*FOR UPDATE$', 1, 1),        -- SELECT ... FOR UPDATE 走写库
(2, 1, '^SELECT', 2, 1),                     -- 普通SELECT走读库
(3, 1, '^INSERT', 1, 1),                     -- INSERT走写库
(4, 1, '^UPDATE', 1, 1),                     -- UPDATE走写库
(5, 1, '^DELETE', 1, 1);                     -- DELETE走写库

-- 4. 配置连接池参数
UPDATE global_variables 
SET variable_value='8' 
WHERE variable_name='mysql-max_connections';

UPDATE global_variables 
SET variable_value='3000' 
WHERE variable_name='mysql-default_max_latency_ms';

-- 5. 配置监控参数
UPDATE global_variables 
SET variable_value='monitor_user' 
WHERE variable_name='mysql-monitor_username';

UPDATE global_variables 
SET variable_value='MonitorPass123!' 
WHERE variable_name='mysql-monitor_password';

UPDATE global_variables 
SET variable_value='2000' 
WHERE variable_name='mysql-monitor_connect_interval';

UPDATE global_variables 
SET variable_value='2000' 
WHERE variable_name='mysql-monitor_ping_interval';

-- 6. 配置故障检测和自动故障转移
INSERT INTO scheduler (id, active, interval_ms, filename, arg1) 
VALUES 
(1, 1, 3000, '/usr/bin/proxysql_galera_checker', ''),
(2, 1, 5000, '/usr/bin/proxysql_monitor', '');

-- 7. 配置查询缓存
INSERT INTO mysql_query_rules (rule_id, active, match_digest, destination_hostgroup, cache_ttl, apply) 
VALUES (10, 1, '^SELECT.*FROM config_table', 2, 30000, 1);

-- 8. 配置负载均衡权重
UPDATE mysql_servers 
SET weight=200 
WHERE hostname='mysql-slave1.example.com';

UPDATE mysql_servers 
SET weight=100 
WHERE hostname='mysql-slave2.example.com';

-- 9. 启用配置
LOAD MYSQL SERVERS TO RUNTIME;
LOAD MYSQL USERS TO RUNTIME;
LOAD MYSQL QUERY RULES TO RUNTIME;
LOAD MYSQL VARIABLES TO RUNTIME;
LOAD SCHEDULER TO RUNTIME;

-- 保存配置到磁盘
SAVE MYSQL SERVERS TO DISK;
SAVE MYSQL USERS TO DISK;
SAVE MYSQL QUERY RULES TO DISK;
SAVE MYSQL VARIABLES TO DISK;
SAVE SCHEDULER TO DISK;

-- 10. 监控和统计查询
-- 查看服务器状态
SELECT hostgroup_id, hostname, port, status, ConnUsed, MaxConnUsed, Queries 
FROM stats_mysql_connection_pool;

-- 查看查询统计
SELECT digest_text, count_star, sum_time, min_time, max_time 
FROM stats_mysql_query_digest 
ORDER BY sum_time DESC 
LIMIT 10;

-- 查看路由统计
SELECT hostgroup, srv_host, srv_port, status, Latency_us 
FROM stats_mysql_connection_pool;

-- 11. 故障切换测试
-- 模拟主库故障
UPDATE mysql_servers 
SET status='OFFLINE_SOFT' 
WHERE hostname='mysql-master.example.com';

-- 查看自动故障转移结果
SELECT hostgroup_id, hostname, port, status 
FROM runtime_mysql_servers;

-- 恢复主库
UPDATE mysql_servers 
SET status='ONLINE' 
WHERE hostname='mysql-master.example.com';
```

### 4. 高可用监控告警配置

```python
#!/usr/bin/env python3
"""
MySQL高可用监控告警系统
"""

import time
import json
import smtplib
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DatabaseNode:
    """数据库节点信息"""
    host: str
    port: int
    role: str  # master/slave
    status: str  # online/offline
    lag_seconds: int
    last_check: datetime

class MySQLHAMonitor:
    """MySQL高可用监控器"""
    
    def __init__(self, config_file: str = "/etc/mysql_ha_monitor.json"):
        self.config_file = config_file
        self.nodes = []
        self.alert_thresholds = {
            'replication_lag': 30,      # 复制延迟阈值(秒)
            'connection_failures': 3,   # 连接失败次数阈值
            'heartbeat_timeout': 10,    # 心跳超时阈值(秒)
            'cpu_usage': 80,           # CPU使用率阈值(%)
            'memory_usage': 85         # 内存使用率阈值(%)
        }
        self.load_configuration()
    
    def load_configuration(self):
        """加载监控配置"""
        default_config = {
            'nodes': [
                {'host': 'mysql-master.example.com', 'port': 3306, 'role': 'master'},
                {'host': 'mysql-slave1.example.com', 'port': 3306, 'role': 'slave'},
                {'host': 'mysql-slave2.example.com', 'port': 3306, 'role': 'slave'}
            ],
            'monitoring_interval': 30,  # 监控间隔(秒)
            'alert_channels': {
                'email': ['admin@example.com', 'dba@example.com'],
                'slack': '#database-alerts',
                'webhook': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
            }
        }
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = default_config
            self.save_configuration(config)
        
        self.nodes = [DatabaseNode(**node, status='unknown', lag_seconds=0, 
                                 last_check=datetime.now()) for node in config['nodes']]
        self.monitoring_interval = config.get('monitoring_interval', 30)
        self.alert_channels = config.get('alert_channels', {})
    
    def save_configuration(self, config: Dict):
        """保存配置文件"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2, default=str)
    
    def check_node_status(self, node: DatabaseNode) -> bool:
        """检查节点状态"""
        try:
            # 检查MySQL连接
            import mysql.connector
            conn = mysql.connector.connect(
                host=node.host,
                port=node.port,
                user='monitor_user',
                password: "${DB_PASSWORD}",
                connection_timeout=5
            )
            
            cursor = conn.cursor()
            
            # 检查复制状态
            if node.role == 'slave':
                cursor.execute("SHOW SLAVE STATUS")
                slave_status = cursor.fetchone()
                if slave_status:
                    lag_seconds = slave_status[32] or 0  # Seconds_Behind_Master
                    node.lag_seconds = lag_seconds
                    
                    # 检查复制线程状态
                    io_running = slave_status[10]  # Slave_IO_Running
                    sql_running = slave_status[11]  # Slave_SQL_Running
                    
                    node.status = 'online' if io_running == 'Yes' and sql_running == 'Yes' else 'offline'
                else:
                    node.status = 'offline'
            else:
                node.status = 'online'
                node.lag_seconds = 0
            
            conn.close()
            node.last_check = datetime.now()
            return True
            
        except Exception as e:
            node.status = 'offline'
            node.lag_seconds = -1
            node.last_check = datetime.now()
            print(f"节点 {node.host} 检查失败: {str(e)}")
            return False
    
    def check_system_resources(self, node: DatabaseNode) -> Dict:
        """检查系统资源使用情况"""
        try:
            # 通过SSH检查系统资源
            import paramiko
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(node.host, username='root', password: "${DB_PASSWORD}")
            
            # 检查CPU使用率
            stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
            cpu_usage = float(stdout.read().decode().strip())
            
            # 检查内存使用率
            stdin, stdout, stderr = ssh.exec_command("free | grep Mem | awk '{print ($3/$2)*100}'")
            memory_usage = float(stdout.read().decode().strip())
            
            ssh.close()
            
            return {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"系统资源检查失败 {node.host}: {str(e)}")
            return {'cpu_usage': -1, 'memory_usage': -1, 'timestamp': datetime.now().isoformat()}
    
    def detect_failures(self) -> List[Dict]:
        """检测故障并生成告警"""
        alerts = []
        
        # 检查主库状态
        master_nodes = [node for node in self.nodes if node.role == 'master']
        offline_masters = [node for node in master_nodes if node.status == 'offline']
        
        if offline_masters:
            alert = {
                'type': 'CRITICAL',
                'component': 'MASTER_DATABASE',
                'message': f'主库宕机: {[node.host for node in offline_masters]}',
                'timestamp': datetime.now().isoformat(),
                'severity': 'HIGH'
            }
            alerts.append(alert)
        
        # 检查复制延迟
        slave_nodes = [node for node in self.nodes if node.role == 'slave']
        high_lag_slaves = [node for node in slave_nodes 
                          if node.lag_seconds > self.alert_thresholds['replication_lag']]
        
        if high_lag_slaves:
            alert = {
                'type': 'WARNING',
                'component': 'REPLICATION_LAG',
                'message': f'复制延迟过高: {[f"{node.host}({node.lag_seconds}s)" for node in high_lag_slaves]}',
                'timestamp': datetime.now().isoformat(),
                'severity': 'MEDIUM'
            }
            alerts.append(alert)
        
        # 检查系统资源
        for node in self.nodes:
            if node.status == 'online':
                resources = self.check_system_resources(node)
                if resources['cpu_usage'] > self.alert_thresholds['cpu_usage']:
                    alert = {
                        'type': 'WARNING',
                        'component': 'SYSTEM_RESOURCES',
                        'message': f'{node.host} CPU使用率过高: {resources["cpu_usage"]:.1f}%',
                        'timestamp': datetime.now().isoformat(),
                        'severity': 'MEDIUM'
                    }
                    alerts.append(alert)
                
                if resources['memory_usage'] > self.alert_thresholds['memory_usage']:
                    alert = {
                        'type': 'WARNING',
                        'component': 'SYSTEM_RESOURCES',
                        'message': f'{node.host} 内存使用率过高: {resources["memory_usage"]:.1f}%',
                        'timestamp': datetime.now().isoformat(),
                        'severity': 'MEDIUM'
                    }
                    alerts.append(alert)
        
        return alerts
    
    def send_alerts(self, alerts: List[Dict]):
        """发送告警通知"""
        for alert in alerts:
            print(f"[{alert['timestamp']}] {alert['type']}: {alert['message']}")
            
            # 发送邮件告警
            if 'email' in self.alert_channels:
                self.send_email_alert(alert)
            
            # 发送Slack告警
            if 'slack' in self.alert_channels:
                self.send_slack_alert(alert)
            
            # 发送Webhook告警
            if 'webhook' in self.alert_channels:
                self.send_webhook_alert(alert)
    
    def send_email_alert(self, alert: Dict):
        """发送邮件告警"""
        try:
            smtp_server = "smtp.example.com"
            smtp_port = 587
            sender_email = "monitor@example.com"
            sender_password: "${DB_PASSWORD}"
            
            message = f"""Subject: [{alert['type']}] MySQL高可用告警
To: {', '.join(self.alert_channels['email'])}

告警时间: {alert['timestamp']}
告警类型: {alert['type']}
组件: {alert['component']}
消息: {alert['message']}
严重程度: {alert['severity']}
"""
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, self.alert_channels['email'], message)
            server.quit()
            
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
    
    def send_slack_alert(self, alert: Dict):
        """发送Slack告警"""
        try:
            webhook_url = self.alert_channels['webhook']
            payload = {
                "channel": self.alert_channels['slack'],
                "username": "MySQL Monitor",
                "text": f"[{alert['type']}] {alert['message']}",
                "icon_emoji": ":rotating_light:" if alert['type'] == 'CRITICAL' else ":warning:"
            }
            
            response = requests.post(webhook_url, json=payload)
            if response.status_code != 200:
                print(f"Slack告警发送失败: {response.text}")
                
        except Exception as e:
            print(f"Slack告警发送失败: {str(e)}")
    
    def send_webhook_alert(self, alert: Dict):
        """发送Webhook告警"""
        try:
            webhook_url = self.alert_channels['webhook']
            response = requests.post(webhook_url, json=alert)
            if response.status_code != 200:
                print(f"Webhook告警发送失败: {response.text}")
                
        except Exception as e:
            print(f"Webhook告警发送失败: {str(e)}")
    
    def generate_health_report(self) -> Dict:
        """生成健康报告"""
        online_nodes = [node for node in self.nodes if node.status == 'online']
        offline_nodes = [node for node in self.nodes if node.status == 'offline']
        
        avg_lag = sum(node.lag_seconds for node in self.nodes if node.lag_seconds >= 0) / len(self.nodes)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_nodes': len(self.nodes),
            'online_nodes': len(online_nodes),
            'offline_nodes': len(offline_nodes),
            'average_replication_lag': avg_lag,
            'nodes_status': [
                {
                    'host': node.host,
                    'role': node.role,
                    'status': node.status,
                    'lag_seconds': node.lag_seconds,
                    'last_check': node.last_check.isoformat()
                } for node in self.nodes
            ],
            'overall_health': 'GOOD' if len(offline_nodes) == 0 and avg_lag < 10 else 'WARNING'
        }
        
        return report
    
    def run_monitoring_loop(self):
        """运行监控循环"""
        print("开始MySQL高可用监控...")
        
        while True:
            try:
                # 检查所有节点状态
                for node in self.nodes:
                    self.check_node_status(node)
                
                # 检测故障并发送告警
                alerts = self.detect_failures()
                if alerts:
                    self.send_alerts(alerts)
                
                # 生成健康报告
                report = self.generate_health_report()
                print(f"健康报告: 在线{report['online_nodes']}/{report['total_nodes']}节点, "
                      f"平均延迟{report['average_replication_lag']:.1f}秒")
                
                # 保存报告到文件
                with open(f"/var/log/mysql_ha/health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                    json.dump(report, f, indent=2)
                
                time.sleep(self.monitoring_interval)
                
            except KeyboardInterrupt:
                print("监控程序已停止")
                break
            except Exception as e:
                print(f"监控循环异常: {str(e)}")
                time.sleep(60)  # 异常时等待1分钟后重试

# 使用示例
def main():
    monitor = MySQLHAMonitor()
    monitor.run_monitoring_loop()

if __name__ == "__main__":
    main()
```

## 🧪 高可用验证测试

### 自动化故障切换测试
🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
#!/bin/bash
# MySQL高可用验证测试套件

TEST_RESULTS=()

# 主库故障切换测试
test_master_failover() {
  echo "=== 主库故障切换测试 ==="
  
  # 获取当前主库
  local current_master=$(mysql -u root -p -e "SHOW MASTER STATUS\G" | grep "File" | head -1)
  echo "当前主库状态: $current_master"
  
  # 模拟主库故障
  echo "模拟主库故障..."
  systemctl stop mysqld  # 在主库上执行
  
  # 等待MHA检测并切换
  sleep 30
  
  # 检查新的主库
  local new_master=$(mysql -u root -p -e "SHOW MASTER STATUS\G" | grep "File" | head -1)
  echo "新主库状态: $new_master"
  
  if [ "$current_master" != "$new_master" ] && [ -n "$new_master" ]; then
    TEST_RESULTS+=("主库故障切换测试: 通过")
    echo "✅ 主库故障切换成功"
  else
    TEST_RESULTS+=("主库故障切换测试: 失败")
    echo "❌ 主库故障切换失败"
  fi
  
  # 恢复原主库
  systemctl start mysqld
  sleep 10
}

# 从库故障测试
test_slave_failure() {
  echo "=== 从库故障测试 ==="
  
  # 选择一个从库进行测试
  local test_slave="mysql-slave1.example.com"
  
  # 模拟从库故障
  echo "模拟从库 $test_slave 故障..."
  ssh root@$test_slave "systemctl stop mysqld"
  
  # 检查其他从库状态
  local remaining_slave="mysql-slave2.example.com"
  local slave_status=$(ssh root@$remaining_slave "mysql -u root -p -e 'SHOW SLAVE STATUS\G'" | grep "Slave_IO_Running")
  
  if echo "$slave_status" | grep -q "Yes"; then
    TEST_RESULTS+=("从库故障隔离测试: 通过")
    echo "✅ 从库故障隔离正常"
  else
    TEST_RESULTS+=("从库故障隔离测试: 失败")
    echo "❌ 从库故障隔离异常"
  fi
  
  # 恢复从库
  ssh root@$test_slave "systemctl start mysqld"
  sleep 15
}

# 读写分离测试
test_read_write_splitting() {
  echo "=== 读写分离测试 ==="
  
  # 测试写操作路由到主库
  echo "测试写操作路由..."
  mysql -h proxysql.example.com -P 6033 -u app_user -pAppPass789! << EOF
CREATE DATABASE IF NOT EXISTS test_routing;
USE test_routing;
CREATE TABLE test_table (id INT PRIMARY KEY, data VARCHAR(100));
INSERT INTO test_table VALUES (1, 'Write Test');
EOF
  
  # 测试读操作路由到从库
  echo "测试读操作路由..."
  local read_result=$(mysql -h proxysql.example.com -P 6033 -u app_user -pAppPass789! -e "SELECT @@hostname, COUNT(*) FROM test_routing.test_table;")
  
  if [ -n "$read_result" ]; then
    TEST_RESULTS+=("读写分离路由测试: 通过")
    echo "✅ 读写分离路由正常"
    echo "读取结果: $read_result"
  else
    TEST_RESULTS+=("读写分离路由测试: 失败")
    echo "❌ 读写分离路由异常"
  fi
}

# 负载均衡测试
test_load_balancing() {
  echo "=== 负载均衡测试 ==="
  
  # 并发读取测试
  echo "执行并发读取测试..."
  
  for i in {1..100}; do
    mysql -h proxysql.example.com -P 6033 -u app_user -pAppPass789! -e "SELECT COUNT(*) FROM test_routing.test_table;" &
  done
  
  wait
  
  # 检查各从库的查询分布
  local slave1_queries=$(ssh root@mysql-slave1.example.com "mysql -u root -p -e 'SHOW STATUS LIKE \"Questions\";' | tail -1 | awk '{print \$2}'")
  local slave2_queries=$(ssh root@mysql-slave2.example.com "mysql -u root -p -e 'SHOW STATUS LIKE \"Questions\";' | tail -1 | awk '{print \$2}'")
  
  local total_queries=$((slave1_queries + slave2_queries))
  local balance_ratio=$(echo "scale=2; $slave1_queries / $total_queries" | bc)
  
  if (( $(echo "$balance_ratio > 0.3 && $balance_ratio < 0.7" | bc -l) )); then
    TEST_RESULTS+=("负载均衡分布测试: 通过")
    echo "✅ 负载均衡分布正常 (比例: $balance_ratio)"
  else
    TEST_RESULTS+=("负载均衡分布测试: 失败")
    echo "❌ 负载均衡分布不均 (比例: $balance_ratio)"
  fi
}

# 复制延迟测试
test_replication_lag() {
  echo "=== 复制延迟测试 ==="
  
  # 插入大量数据测试复制延迟
  echo "插入测试数据..."
  mysql -h mysql-master.example.com -u root -p << EOF
USE test_routing;
INSERT INTO test_table (id, data) 
SELECT seq, CONCAT('Test data ', seq) 
FROM seq_1_to_10000;
EOF
  
  # 监控复制延迟
  for i in {1..30}; do
    local lag1=$(ssh root@mysql-slave1.example.com "mysql -u root -p -e 'SHOW SLAVE STATUS\G'" | grep "Seconds_Behind_Master" | awk '{print $2}')
    local lag2=$(ssh root@mysql-slave2.example.com "mysql -u root -p -e 'SHOW SLAVE STATUS\G'" | grep "Seconds_Behind_Master" | awk '{print $2}')
    
    echo "复制延迟 - Slave1: ${lag1}s, Slave2: ${lag2}s"
    
    if [ "$lag1" -lt 5 ] && [ "$lag2" -lt 5 ]; then
      TEST_RESULTS+=("复制延迟测试: 通过")
      echo "✅ 复制延迟在可接受范围内"
      return
    fi
    
    sleep 2
  done
  
  TEST_RESULTS+=("复制延迟测试: 失败")
  echo "❌ 复制延迟超出阈值"
}

# 生成高可用测试报告
generate_ha_test_report() {
  echo "=== MySQL高可用测试综合报告 ==="
  
  local total_tests=${#TEST_RESULTS[@]}
  local passed_tests=0
  
  for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
    if [[ $result == *"通过"* ]]; then
      ((passed_tests++))
    fi
  done
  
  echo ""
  echo "高可用测试总结:"
  echo "总测试项: $total_tests"
  echo "通过项: $passed_tests"
  echo "通过率: $((passed_tests * 100 / total_tests))%"
  
  # 评估高可用等级
  local ha_score=$((passed_tests * 100 / total_tests))
  if [ $ha_score -ge 90 ]; then
    echo "🏆 高可用等级: 优秀 (企业级高可用标准)"
  elif [ $ha_score -ge 75 ]; then
    echo "🥇 高可用等级: 良好 (符合生产环境要求)"
  elif [ $ha_score -ge 60 ]; then
    echo "🥈 高可用等级: 一般 (需要优化配置)"
  else
    echo "🥉 高可用等级: 较差 (存在高可用风险)"
  fi
  
  # 保存报告
  local report_file="/tmp/mysql_ha_test_report_$(date +%Y%m%d_%H%M%S).txt"
  printf "%s\n" "${TEST_RESULTS[@]}" > "$report_file"
  echo "详细测试报告已保存: $report_file"
}

# 执行所有高可用测试
test_master_failover
test_slave_failure
test_read_write_splitting
test_load_balancing
test_replication_lag
generate_ha_test_report
```

## 📚 最佳实践总结

### 高可用架构设计原则
1. **冗余设计**: 确保关键组件有多份副本
2. **故障隔离**: 单点故障不影响整体服务
3. **自动恢复**: 故障发生时能够自动检测和恢复
4. **数据一致性**: 保证数据在各节点间的一致性
5. **性能保障**: 高可用不应显著影响系统性能

### 关键技术要点
- **GTID复制**: 简化故障切换和数据一致性管理
- **半同步复制**: 确保数据不丢失的前提下提供高可用
- **MHA管理**: 成熟的自动故障切换解决方案
- **ProxySQL代理**: 高效的读写分离和负载均衡
- **全面监控**: 实时监控所有组件状态和性能指标

### 运维管理建议
- **定期演练**: 定期进行故障切换演练
- **文档完善**: 维护详细的架构和操作文档
- **人员培训**: 确保运维团队具备故障处理能力
- **持续优化**: 根据业务发展持续优化架构配置

---
> **💡 提示**: 高可用架构的实施需要充分考虑业务特点和成本预算，在满足SLA要求的前提下选择最适合的技术方案。