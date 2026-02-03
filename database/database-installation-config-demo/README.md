# 企业级数据库安装配置实战演示

## 🎯 学习目标

通过本案例你将掌握企业级数据库的标准化安装和配置技能：

- 多种数据库系统的标准化安装流程
- 生产环境配置最佳实践
- 安全加固和性能调优配置
- 高可用架构的初始配置
- 自动化部署和配置管理
- 监控告警的基础配置

## 🛠️ 环境准备

### 系统要求
- **操作系统**: CentOS 8.x / RHEL 8.x / Ubuntu 20.04+
- **硬件配置**: 
  - CPU: 4核以上 (生产环境建议8核+)
  - 内存: 8GB以上 (生产环境建议16GB+)
  - 存储: SSD存储，容量根据业务需求规划
  - 网络: 千兆网络，低延迟
- **权限要求**: root或sudo权限
- **防火墙**: 开放相应端口 (MySQL:3306, PostgreSQL:5432, MongoDB:27017, Redis:6379)

### 依赖安装
```bash
# 系统基础工具
sudo yum update -y
sudo yum install -y wget curl git vim net-tools lsof iotop sysstat

# 时间同步
sudo yum install -y chrony
sudo systemctl enable chronyd && sudo systemctl start chronyd
timedatectl set-timezone Asia/Shanghai

# 文件系统优化
echo 'vm.swappiness = 1' >> /etc/sysctl.conf
echo 'vm.dirty_ratio = 15' >> /etc/sysctl.conf
echo 'vm.dirty_background_ratio = 5' >> /etc/sysctl.conf
sysctl -p

# 创建专用用户
sudo useradd -r -s /sbin/nologin mysql
sudo useradd -r -s /sbin/nologin postgres
sudo useradd -r -s /sbin/nologin mongod
```

## 📁 项目结构

```
database-installation-config-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 安装脚本
│   ├── mysql_install.sh               # MySQL安装脚本
│   ├── postgresql_install.sh          # PostgreSQL安装脚本
│   ├── mongodb_install.sh             # MongoDB安装脚本
│   ├── redis_install.sh               # Redis安装脚本
│   ├── security_hardening.sh          # 安全加固脚本
│   └── performance_tuning.sh          # 性能调优脚本
├── configs/                           # 配置文件
│   ├── mysql.cnf                      # MySQL生产配置
│   ├── postgresql.conf                # PostgreSQL生产配置
│   ├── mongodb.conf                   # MongoDB生产配置
│   ├── redis.conf                     # Redis生产配置
│   ├── systemd/                       # 系统服务配置
│   └── security/                      # 安全配置文件
├── templates/                         # 部署模板
│   ├── docker-compose.yml             # Docker部署模板
│   ├── k8s-manifests/                 # Kubernetes部署清单
│   └── ansible-playbooks/             # Ansible自动化剧本
└── docs/                              # 详细文档
    ├── installation_guide.md          # 安装详细指南
    ├── security_checklist.md          # 安全检查清单
    ├── performance_benchmark.md       # 性能基准测试
    └── troubleshooting.md             # 故障排除手册
```

## 🔧 核心安装技术详解

### 1. MySQL 8.0 企业版安装

```bash
#!/bin/bash
# MySQL 8.0 企业级安装脚本

MYSQL_VERSION="8.0.35"
INSTALL_DIR="/opt/mysql"
DATA_DIR="/data/mysql"
LOG_DIR="/var/log/mysql"

# 下载MySQL RPM包
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-${MYSQL_VERSION}-1.el8.x86_64.rpm-bundle.tar
tar -xf mysql-${MYSQL_VERSION}-1.el8.x86_64.rpm-bundle.tar

# 安装依赖包
sudo yum install -y ncurses-compat-libs openssl-devel

# 按顺序安装RPM包
sudo rpm -ivh mysql-community-common-${MYSQL_VERSION}-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-client-plugins-${MYSQL_VERSION}-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-libs-${MYSQL_VERSION}-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-client-${MYSQL_VERSION}-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-icu-data-files-${MYSQL_VERSION}-1.el8.x86_64.rpm
sudo rpm -ivh mysql-community-server-${MYSQL_VERSION}-1.el8.x86_64.rpm

# 创建数据目录
sudo mkdir -p ${DATA_DIR} ${LOG_DIR}
sudo chown -R mysql:mysql ${DATA_DIR} ${LOG_DIR}

# 初始化数据库
sudo mysqld --initialize --user=mysql --datadir=${DATA_DIR}
TEMP_PASSWORD=$(sudo grep 'temporary password' ${LOG_DIR}/mysqld.log | awk '{print $NF}')

# 启动服务
sudo systemctl enable mysqld
sudo systemctl start mysqld

# 安全配置
mysql_secure_installation << EOF
${TEMP_PASSWORD}
y
new_password
new_password
y
y
y
y
EOF

echo "MySQL安装完成，临时密码: ${TEMP_PASSWORD}"
```

### 2. PostgreSQL 14 企业版安装

```bash
#!/bin/bash
# PostgreSQL 14 企业级安装脚本

PG_VERSION="14"
INSTALL_DIR="/opt/postgresql"
DATA_DIR="/data/postgresql"
LOG_DIR="/var/log/postgresql"

# 添加PostgreSQL官方仓库
sudo dnf install -y epel-release
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# 安装PostgreSQL
sudo dnf -qy module disable postgresql
sudo dnf install -y postgresql${PG_VERSION}-server postgresql${PG_VERSION}-contrib

# 创建数据目录
sudo mkdir -p ${DATA_DIR} ${LOG_DIR}
sudo chown -R postgres:postgres ${DATA_DIR} ${LOG_DIR}

# 初始化数据库集群
sudo -u postgres /usr/pgsql-${PG_VERSION}/bin/initdb -D ${DATA_DIR}

# 配置服务
sudo cp /usr/lib/systemd/system/postgresql-${PG_VERSION}.service /etc/systemd/system/
sudo sed -i "s|Environment=PGDATA=/var/lib/pgsql/${PG_VERSION}/data|Environment=PGDATA=${DATA_DIR}|g" /etc/systemd/system/postgresql-${PG_VERSION}.service

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable postgresql-${PG_VERSION}
sudo systemctl start postgresql-${PG_VERSION}

# 创建管理员用户
sudo -u postgres createuser -s admin
sudo -u postgres createdb admin

echo "PostgreSQL安装完成"
```

### 3. MongoDB 6.0 企业版安装

```bash
#!/bin/bash
# MongoDB 6.0 企业级安装脚本

MONGO_VERSION="6.0"
INSTALL_DIR="/opt/mongodb"
DATA_DIR="/data/mongodb"
LOG_DIR="/var/log/mongodb"

# 添加MongoDB官方仓库
cat > /etc/yum.repos.d/mongodb-org-6.0.repo << EOF
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/8/mongodb-org/6.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
EOF

# 安装MongoDB
sudo yum install -y mongodb-org

# 创建数据目录
sudo mkdir -p ${DATA_DIR} ${LOG_DIR}
sudo chown -R mongod:mongod ${DATA_DIR} ${LOG_DIR}

# 配置文件修改
cat > /etc/mongod.conf << EOF
storage:
  dbPath: ${DATA_DIR}
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2

systemLog:
  destination: file
  logAppend: true
  path: ${LOG_DIR}/mongod.log

net:
  port: 27017
  bindIp: 0.0.0.0

processManagement:
  fork: true
  pidFilePath: /var/run/mongodb/mongod.pid

security:
  authorization: enabled

replication:
  replSetName: rs0
EOF

# 启动服务
sudo systemctl enable mongod
sudo systemctl start mongod

# 初始化副本集
mongo --eval "
rs.initiate({
  _id: 'rs0',
  members: [
    {_id: 0, host: 'localhost:27017'}
  ]
})
"

echo "MongoDB安装完成"
```

### 4. Redis 7.0 企业版安装

```bash
#!/bin/bash
# Redis 7.0 企业级安装脚本

REDIS_VERSION="7.0.8"
INSTALL_DIR="/opt/redis"
DATA_DIR="/data/redis"
LOG_DIR="/var/log/redis"

# 下载编译安装
wget http://download.redis.io/releases/redis-${REDIS_VERSION}.tar.gz
tar -xf redis-${REDIS_VERSION}.tar.gz
cd redis-${REDIS_VERSION}
make PREFIX=${INSTALL_DIR} install

# 创建目录结构
sudo mkdir -p ${DATA_DIR} ${LOG_DIR} ${INSTALL_DIR}/conf
sudo chown -R redis:redis ${DATA_DIR} ${LOG_DIR}

# 配置文件
cat > ${INSTALL_DIR}/conf/redis.conf << EOF
# 网络配置
bind 0.0.0.0
port 6379
timeout 0
tcp-keepalive 300

# 安全配置
protected-mode yes
requirepass your_strong_password_here

# 持久化配置
save 900 1
save 300 10
save 60 10000
dbfilename dump.rdb
dir ${DATA_DIR}
appendonly yes
appendfilename "appendonly.aof"

# 性能配置
maxmemory 2gb
maxmemory-policy allkeys-lru
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes

# 日志配置
logfile ${LOG_DIR}/redis.log
loglevel notice

# 集群配置
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 15000
EOF

# 系统服务配置
cat > /etc/systemd/system/redis.service << EOF
[Unit]
Description=Redis persistent key-value database
After=network.target

[Service]
Type=forking
User=redis
Group=redis
ExecStart=${INSTALL_DIR}/bin/redis-server ${INSTALL_DIR}/conf/redis.conf
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable redis
sudo systemctl start redis

echo "Redis安装完成"
```

## 🔒 安全加固配置

### 系统级安全加固
```bash
#!/bin/bash
# 数据库服务器安全加固脚本

# 1. 防火墙配置
sudo firewall-cmd --permanent --add-port=3306/tcp    # MySQL
sudo firewall-cmd --permanent --add-port=5432/tcp    # PostgreSQL
sudo firewall-cmd --permanent --add-port=27017/tcp   # MongoDB
sudo firewall-cmd --permanent --add-port=6379/tcp    # Redis
sudo firewall-cmd --reload

# 2. SELinux配置
sudo setsebool -P mysql_connect_any 1
sudo setsebool -P nis_enabled 1

# 3. 文件权限加固
chmod 700 /data/mysql /data/postgresql /data/mongodb /data/redis
chown mysql:mysql /data/mysql
chown postgres:postgres /data/postgresql
chown mongod:mongod /data/mongodb
chown redis:redis /data/redis

# 4. SSH安全配置
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart sshd

# 5. 系统审计
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf
```

### 数据库级安全配置
```sql
-- MySQL安全配置
-- 1. 删除匿名用户
DELETE FROM mysql.user WHERE User='';
FLUSH PRIVILEGES;

-- 2. 禁止root远程登录
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
FLUSH PRIVILEGES;

-- 3. 创建应用用户
CREATE USER 'app_user'@'%' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_database.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

-- 4. 启用SSL连接
-- 在my.cnf中添加:
-- [mysqld]
-- ssl-ca=/path/to/ca.pem
-- ssl-cert=/path/to/server-cert.pem
-- ssl-key=/path/to/server-key.pem
```

## ⚡ 性能调优配置

### 内核参数优化
```bash
# 内核参数调优
cat >> /etc/sysctl.conf << EOF
# 内存管理
vm.swappiness = 1
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.overcommit_memory = 1

# 网络优化
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.ip_local_port_range = 1024 65535

# 文件系统
fs.file-max = 1000000
fs.aio-max-nr = 1048576
EOF

sysctl -p
```

### 数据库性能参数
```ini
# MySQL性能配置 (my.cnf)
[mysqld]
# 内存配置
innodb_buffer_pool_size = 4G
innodb_log_file_size = 512M
innodb_log_buffer_size = 64M

# 连接配置
max_connections = 1000
max_connect_errors = 100000
thread_cache_size = 100

# 查询优化
query_cache_type = 1
query_cache_size = 256M
tmp_table_size = 256M
max_heap_table_size = 256M

# 日志配置
slow_query_log = 1
long_query_time = 1
log_queries_not_using_indexes = 1
```

## 🧪 验证测试

### 安装验证脚本
```bash
#!/bin/bash
# 数据库安装验证脚本

echo "=== 数据库安装验证 ==="

# 1. 服务状态检查
echo "1. 服务状态检查:"
services=("mysqld" "postgresql-14" "mongod" "redis")
for service in "${services[@]}"; do
    if systemctl is-active --quiet $service; then
        echo "✅ $service 运行正常"
    else
        echo "❌ $service 运行异常"
    fi
done

# 2. 端口监听检查
echo -e "\n2. 端口监听检查:"
netstat -tlnp | grep -E "(3306|5432|27017|6379)"

# 3. 基本连接测试
echo -e "\n3. 基本连接测试:"
mysql -u root -p -e "SELECT VERSION();" 2>/dev/null && echo "✅ MySQL连接成功"
psql -U postgres -c "SELECT VERSION();" 2>/dev/null && echo "✅ PostgreSQL连接成功"
mongo --eval "db.version()" 2>/dev/null && echo "✅ MongoDB连接成功"
redis-cli ping 2>/dev/null | grep "PONG" && echo "✅ Redis连接成功"

# 4. 性能基准测试
echo -e "\n4. 性能基准测试:"
sysbench --db-driver=mysql --mysql-user=root --mysql-password=password \
         --mysql-db=test --table-size=1000000 --tables=10 \
         oltp_read_write --threads=16 --time=60 run

echo "验证完成"
```

## 📚 扩展学习

### 自动化部署方案
- **Ansible**: 编排式自动化部署
- **Docker**: 容器化一键部署
- **Kubernetes**: 云原生存储编排
- **Terraform**: 基础设施即代码

### 监控集成
- **Prometheus**: 指标收集和告警
- **Grafana**: 数据可视化面板
- **ELK Stack**: 日志分析平台
- **Zabbix**: 传统监控方案

### 高可用方案
- **MySQL**: MHA + GTID复制
- **PostgreSQL**: Patroni + etcd
- **MongoDB**: Replica Set + Sharding
- **Redis**: Redis Sentinel + Cluster

---
> **💡 提示**: 企业级数据库部署需要充分考虑业务需求、安全要求和运维能力，建议在正式环境中先进行充分测试。