# 🆘 数据库灾难恢复方案指南

> 企业级数据库灾难恢复体系，涵盖备份策略、恢复演练、异地容灾等完整DR方案，确保业务连续性和数据安全，满足RTO/RPO企业级要求

## 📋 案例概述

本案例提供完整的数据库灾难恢复解决方案，通过实施科学的备份策略、定期恢复演练和完善的技术架构，确保在各种灾难场景下能够快速恢复业务，最大程度减少数据丢失和业务中断时间。

### 🎯 学习目标

- 掌握3-2-1备份原则和多种备份策略
- 理解RTO/RPO指标和业务连续性规划
- 实施自动化备份和恢复流程
- 设计异地容灾和多活架构
- 建立灾难恢复演练和验证机制

### ⏱️ 学习时长

- **理论学习**: 4小时
- **实践操作**: 6小时
- **总计**: 10小时

---

## 🔄 灾难恢复框架

### DR级别定义

```
┌─────────────────────────────────────────────────┐
│              RTO/RPO 指标体系                   │
├─────────────────────────────────────────────────┤
│ 级别 | RTO目标 | RPO目标 | 适用场景              │
├─────────────────────────────────────────────────┤
│ 1级  | < 1小时 | < 1分钟 | 核心交易系统          │
│ 2级  | < 4小时 | < 1小时 | 重要业务系统          │
│ 3级  | < 1天   | < 1天   | 一般业务系统          │
│ 4级  | < 1周   | < 1周   | 非关键系统            │
└─────────────────────────────────────────────────┘
```

### 灾难恢复架构

```
┌─────────────────────────────────────────────────┐
│              主数据中心                         │
│  ├─ 实时备份                                    │
│  ├─ 本地存储                                    │
│  └─ 监控告警                                    │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│              备份数据中心                       │
│  ├─ 异地备份                                    │
│  ├─ 热备/温备                                   │
│  └─ 自动故障切换                                │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│              灾难恢复站点                       │
│  ├─ 冷备环境                                    │
│  ├─ 完整恢复能力                                │
│  └─ 手动激活机制                                │
└─────────────────────────────────────────────────┘
```

---

## 💾 MySQL灾难恢复方案

### 1. 备份策略设计

#### 3-2-1备份原则实施
```bash
#!/bin/bash
# mysql_backup_strategy.sh - MySQL备份策略脚本

BACKUP_BASE="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
WEEKDAY=$(date +%u)

# 目录结构
DAILY_DIR="$BACKUP_BASE/daily"
WEEKLY_DIR="$BACKUP_BASE/weekly"
MONTHLY_DIR="$BACKUP_BASE/monthly"
ARCHIVE_DIR="$BACKUP_BASE/archive"

# 创建目录
mkdir -p $DAILY_DIR $WEEKLY_DIR $MONTHLY_DIR $ARCHIVE_DIR

# 全量备份函数
full_backup() {
    local backup_file="$DAILY_DIR/full_$DATE.sql.gz"
    
    mysqldump \
        --single-transaction \
        --routines \
        --triggers \
        --master-data=2 \
        --flush-logs \
        --all-databases \
        | gzip > $backup_file
    
    # 验证备份完整性
    gunzip -t $backup_file
    
    # 保留最近7天的全量备份
    find $DAILY_DIR -name "full_*.sql.gz" -mtime +7 -delete
}

# 增量备份函数
incremental_backup() {
    local binlog_dir="/var/log/mysql"
    local backup_file="$DAILY_DIR/binlog_$DATE.tar.gz"
    
    # 备份二进制日志
    tar -czf $backup_file -C $binlog_dir .
    
    # 清理已备份的日志
    mysql -e "PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 3 DAY);"
}

# 差异备份函数
differential_backup() {
    local backup_file="$WEEKLY_DIR/diff_$DATE.sql.gz"
    local last_full=$(ls -t $DAILY_DIR/full_*.sql.gz | head -1)
    
    mysqldump \
        --single-transaction \
        --routines \
        --triggers \
        --master-data=2 \
        --flush-logs \
        --all-databases \
        --where="DATE(update_time) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)" \
        | gzip > $backup_file
}

# 月度归档备份
monthly_archive() {
    local archive_file="$ARCHIVE_DIR/monthly_$(date +%Y%m).tar.gz"
    
    # 归档当月所有备份
    tar -czf $archive_file -C $BACKUP_BASE .
    
    # 上传到云存储
    aws s3 cp $archive_file s3://company-backups/mysql/
}

# 根据日期执行相应备份
case $WEEKDAY in
    1) # 周一 - 全量备份
        full_backup
        ;;
    7) # 周日 - 差异备份 + 月度归档
        differential_backup
        if [ $(date +%d) -eq 01 ]; then
            monthly_archive
        fi
        ;;
    *) # 其他日子 - 增量备份
        incremental_backup
        ;;
esac

# 备份验证
verify_backup() {
    local latest_backup=$(ls -t $DAILY_DIR/*.gz | head -1)
    local temp_db="backup_verify_$$"
    
    # 创建临时数据库进行验证
    mysql -e "CREATE DATABASE $temp_db;"
    
    # 恢复备份进行验证
    gunzip -c $latest_backup | mysql $temp_db
    
    # 检查表结构完整性
    mysql -e "USE $temp_db; SHOW TABLES;" > /dev/null
    
    # 清理验证数据库
    mysql -e "DROP DATABASE $temp_db;"
    
    echo "Backup verification completed: $latest_backup"
}

# 执行验证
verify_backup
```

#### 备份监控和告警
```bash
#!/bin/bash
# backup_monitor.sh - 备份监控脚本

BACKUP_DIR="/backup/mysql"
ALERT_EMAIL="dba@company.com"
LOG_FILE="/var/log/backup_monitor.log"

# 检查备份完整性
check_backup_integrity() {
    local today=$(date +%Y%m%d)
    local backup_files=$(find $BACKUP_DIR -name "*$today*" -type f)
    
    if [ -z "$backup_files" ]; then
        echo "$(date): Backup files not found for today" >> $LOG_FILE
        send_alert "MISSING_BACKUP" "No backup files found for $today"
        return 1
    fi
    
    # 验证文件大小
    for file in $backup_files; do
        local size=$(stat -c%s "$file")
        if [ $size -lt 1048576 ]; then # 小于1MB可能有问题
            echo "$(date): Small backup file detected: $file ($size bytes)" >> $LOG_FILE
            send_alert "SMALL_BACKUP" "Small backup file: $file"
        fi
    done
}

# 检查备份空间
check_disk_space() {
    local usage=$(df $BACKUP_DIR | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ $usage -gt 85 ]; then
        echo "$(date): High disk usage: ${usage}%" >> $LOG_FILE
        send_alert "DISK_SPACE_WARNING" "Backup disk usage: ${usage}%"
    fi
}

# 发送告警邮件
send_alert() {
    local alert_type=$1
    local message=$2
    
    echo "Subject: Database Backup Alert - $alert_type
    
$message
    
Time: $(date)
System: $(hostname)
" | mail -s "Database Backup Alert - $alert_type" $ALERT_EMAIL
}

# 执行检查
check_backup_integrity
check_disk_space
```

### 2. 恢复演练方案

#### 点-in-Time恢复(PITR)
```bash
#!/bin/bash
# pitr_recovery.sh - Point-in-Time Recovery脚本

TARGET_TIME="2024-01-15 14:30:00"
BACKUP_DIR="/backup/mysql"
RESTORE_DB="recovery_test"

# 准备恢复环境
prepare_recovery() {
    # 停止MySQL服务
    systemctl stop mysqld
    
    # 备份当前数据目录
    cp -r /var/lib/mysql /var/lib/mysql.backup.$(date +%Y%m%d_%H%M%S)
    
    # 清理数据目录
    rm -rf /var/lib/mysql/*
    
    # 启动MySQL（初始化空实例）
    systemctl start mysqld
}

# 恢复全量备份
restore_full_backup() {
    local full_backup=$(find $BACKUP_DIR/daily -name "full_*.sql.gz" -newermt "$TARGET_TIME" | sort | head -1)
    
    if [ -z "$full_backup" ]; then
        echo "No suitable full backup found"
        exit 1
    fi
    
    echo "Restoring full backup: $full_backup"
    gunzip -c $full_backup | mysql
    
    # 获取二进制日志位置
    local binlog_info=$(gunzip -c $full_backup | grep "CHANGE MASTER" | tail -1)
    echo "Binary log position: $binlog_info"
}

# 恢复增量数据
restore_incremental() {
    local start_time=$(mysql -e "SHOW MASTER STATUS\G" | grep File | awk '{print $2}')
    
    # 应用二进制日志到指定时间点
    mysqlbinlog \
        --start-datetime="$TARGET_TIME" \
        --stop-datetime="$TARGET_TIME" \
        /var/log/mysql/mysql-bin.* \
        | mysql
    
    echo "Incremental recovery completed to $TARGET_TIME"
}

# 验证恢复结果
verify_recovery() {
    local table_count=$(mysql -e "USE $RESTORE_DB; SHOW TABLES;" | wc -l)
    local row_count=$(mysql -e "USE $RESTORE_DB; SELECT COUNT(*) FROM users;" | tail -1)
    
    echo "Recovery Verification:"
    echo "Tables restored: $table_count"
    echo "User records: $row_count"
    
    # 数据一致性检查
    mysql -e "USE $RESTORE_DB; CHECKSUM TABLE users, orders;"
}

# 执行PITR恢复
prepare_recovery
restore_full_backup
restore_incremental
verify_recovery
```

---

## 🐘 PostgreSQL灾难恢复方案

### 1. WAL备份和恢复

#### 连续归档配置
```conf
# postgresql.conf WAL配置
wal_level = replica
archive_mode = on
archive_command = 'rsync -av %p /backup/postgresql/wal/%f'
archive_timeout = 300
max_wal_senders = 3
wal_keep_segments = 32
hot_standby = on

# 恢复配置
restore_command = 'cp /backup/postgresql/wal/%f "%p"'
recovery_target_time = '2024-01-15 14:30:00'
recovery_target_action = 'pause'
```

#### 基础备份脚本
```bash
#!/bin/bash
# postgres_base_backup.sh

BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)

# 执行基础备份
pg_basebackup \
    --host=localhost \
    --username=replication_user \
    --pgdata=/backup/postgresql/base_$DATE \
    --format=tar \
    --gzip \
    --progress \
    --verbose

# 创建备份标签
echo "BASE BACKUP COMPLETED: $DATE" > /backup/postgresql/base_$DATE/backup_label

# 验证备份完整性
cd /backup/postgresql/base_$DATE
for file in *.tar.gz; do
    gzip -t $file || echo "Corrupted backup file: $file"
done

echo "Base backup completed: base_$DATE"
```

#### PITR恢复流程
```bash
#!/bin/bash
# postgres_pitr_restore.sh

TARGET_TIME="2024-01-15 14:30:00"
BACKUP_DIR="/backup/postgresql"
RESTORE_DIR="/var/lib/pgsql/data_restored"

# 准备恢复环境
prepare_restore() {
    systemctl stop postgresql
    
    # 备份当前数据
    cp -r /var/lib/pgsql/data /var/lib/pgsql/data.backup.$(date +%Y%m%d_%H%M%S)
    
    # 清理目标目录
    rm -rf $RESTORE_DIR
    mkdir -p $RESTORE_DIR
}

# 恢复基础备份
restore_base_backup() {
    local base_backup=$(ls -t $BACKUP_DIR/base_* | head -1)
    
    # 解压基础备份
    cd $RESTORE_DIR
    tar -xzf $base_backup/*.tar.gz
    
    # 创建recovery.conf
    cat > $RESTORE_DIR/recovery.conf << EOF
restore_command = 'cp $BACKUP_DIR/wal/%f "%p"'
recovery_target_time = '$TARGET_TIME'
recovery_target_action = 'promote'
EOF
}

# 启动恢复
start_recovery() {
    chown -R postgres:postgres $RESTORE_DIR
    systemctl start postgresql
    
    # 等待恢复完成
    while ! pg_isready -q; do
        sleep 10
    done
    
    echo "Recovery completed. Check PostgreSQL logs for details."
}

# 验证恢复结果
verify_postgres_recovery() {
    psql -c "SELECT current_database(), now();" postgres
    psql -c "SELECT count(*) FROM pg_stat_user_tables;" myapp
}

prepare_restore
restore_base_backup
start_recovery
verify_postgres_recovery
```

---

## 🍃 MongoDB灾难恢复方案

### 1. 副本集备份策略

#### Oplog备份配置
```javascript
// MongoDB备份配置
cfg = {
    "_id": "backup_config",
    "version": 1,
    "members": [
        {
            "_id": 0,
            "host": "primary.mongodb.local:27017",
            "priority": 1
        },
        {
            "_id": 1,
            "host": "secondary1.mongodb.local:27017",
            "priority": 0.5,
            "hidden": true,
            "slaveDelay": 3600  // 1小时延迟备份
        },
        {
            "_id": 2,
            "host": "secondary2.mongodb.local:27017",
            "priority": 0,
            "arbiterOnly": true
        }
    ]
}

rs.initiate(cfg)
```

#### 备份脚本实现
```bash
#!/bin/bash
# mongodb_backup.sh

BACKUP_DIR="/backup/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
MONGO_HOST="mongodb-primary:27017"

# 全量备份
full_backup() {
    local backup_path="$BACKUP_DIR/full_$DATE"
    
    mongodump \
        --host $MONGO_HOST \
        --out $backup_path \
        --gzip \
        --oplog
    
    # 验证备份
    mongorestore \
        --host localhost:27018 \
        --db test_restore \
        $backup_path/* \
        --dryRun
}

# Oplog增量备份
oplog_backup() {
    local oplog_path="$BACKUP_DIR/oplog_$DATE"
    
    # 获取当前oplog位置
    local ts=$(mongo --host $MONGO_HOST --quiet --eval "
        db.printSlaveReplicationInfo();
        db.oplog.rs.find().sort({\$natural:-1}).limit(1).next()['ts'];
    ")
    
    # 备份oplog
    mongodump \
        --host $MONGO_HOST \
        --db local \
        --collection oplog.rs \
        --query "{ts: {\$gte: Timestamp($ts)}}" \
        --out $oplog_path
}

# 文件系统快照备份
snapshot_backup() {
    # 使用LVM快照
    lvcreate -L 10G -s -n mongo_snapshot /dev/vg0/mongo_data
    mkdir -p /mnt/mongo_snapshot
    mount /dev/vg0/mongo_snapshot /mnt/mongo_snapshot
    
    # 备份快照数据
    rsync -av /mnt/mongo_snapshot/ $BACKUP_DIR/snapshot_$DATE/
    
    # 清理快照
    umount /mnt/mongo_snapshot
    lvremove -f /dev/vg0/mongo_snapshot
}

# 执行备份策略
case $(date +%u) in
    1|4) # 周一、周四 - 全量备份
        full_backup
        ;;
    *) # 其他时间 - Oplog备份
        oplog_backup
        ;;
esac

# 每月初创建快照
if [ $(date +%d) -eq 01 ]; then
    snapshot_backup
fi
```

### 2. 灾难恢复流程

#### 副本集恢复
```bash
#!/bin/bash
# mongodb_disaster_recovery.sh

BACKUP_DIR="/backup/mongodb"
TARGET_TIME="2024-01-15T14:30:00Z"
RESTORE_DIR="/var/lib/mongo_restored"

# 准备恢复环境
prepare_mongo_restore() {
    systemctl stop mongod
    
    # 备份当前数据
    cp -r /var/lib/mongo /var/lib/mongo.backup.$(date +%Y%m%d_%H%M%S)
    
    # 清理恢复目录
    rm -rf $RESTORE_DIR
    mkdir -p $RESTORE_DIR
}

# 恢复全量数据
restore_mongo_full() {
    local full_backup=$(ls -t $BACKUP_DIR/full_* | head -1)
    
    mongorestore \
        --dbpath $RESTORE_DIR \
        $full_backup/* \
        --drop
    
    echo "Full restore completed from: $full_backup"
}

# 应用Oplog到指定时间点
apply_oplog_to_time() {
    local oplog_files=$(find $BACKUP_DIR -name "oplog_*" -newermt "$TARGET_TIME" | sort)
    
    for oplog_file in $oplog_files; do
        if [ -d "$oplog_file/local/oplog.rs.bson" ]; then
            mongorestore \
                --dbpath $RESTORE_DIR \
                --oplogReplay \
                --oplogLimit "$TARGET_TIME" \
                $oplog_file
        fi
    done
}

# 启动恢复后的MongoDB
start_restored_mongo() {
    # 修改配置指向恢复数据目录
    sed -i "s|dbpath=.*|dbpath=$RESTORE_DIR|" /etc/mongod.conf
    
    systemctl start mongod
    
    # 验证恢复结果
    mongo --eval "db.stats()" myapp
    mongo --eval "db.serverStatus()" admin
}

prepare_mongo_restore
restore_mongo_full
apply_oplog_to_time
start_restored_mongo
```

---

## 🔴 Redis灾难恢复方案

### 1. AOF和RDB混合备份

#### Redis配置优化
```conf
# redis.conf 备份配置
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

rdbcompression yes
rdbchecksum yes

dir /var/lib/redis
dbfilename dump.rdb

# 备份配置
replicaof redis-master 6379
replica-read-only yes
replica-priority 100
```

#### 备份同步脚本
```bash
#!/bin/bash
# redis_backup_sync.sh

BACKUP_DIR="/backup/redis"
DATE=$(date +%Y%m%d_%H%M%S)
REDIS_CLI="redis-cli -h localhost -p 6379"

# RDB备份
rdb_backup() {
    local backup_file="$BACKUP_DIR/rdb_$DATE.rdb"
    
    # 执行BGSAVE
    $REDIS_CLI BGSAVE
    
    # 等待备份完成
    while [ $($REDIS_CLI LASTSAVE) -lt $(date +%s) ]; do
        sleep 5
    done
    
    # 复制RDB文件
    cp /var/lib/redis/dump.rdb $backup_file
    
    # 验证备份文件
    redis-check-rdb $backup_file
    
    echo "RDB backup completed: $backup_file"
}

# AOF备份
aof_backup() {
    local backup_file="$BACKUP_DIR/aof_$DATE.aof"
    
    # 复制AOF文件
    cp /var/lib/redis/appendonly.aof $backup_file
    
    # 压缩备份
    gzip $backup_file
    
    echo "AOF backup completed: $backup_file.gz"
}

# 增量同步
incremental_sync() {
    local sync_file="$BACKUP_DIR/sync_$DATE.rdb"
    
    # 使用SLAVEOF进行同步
    $REDIS_CLI SLAVEOF backup-redis-server 6379
    
    # 等待同步完成
    sleep 30
    
    # 断开主从关系
    $REDIS_CLI SLAVEOF NO ONE
    
    # 复制同步数据
    cp /var/lib/redis/dump.rdb $sync_file
    
    echo "Incremental sync completed: $sync_file"
}

# 执行备份策略
case $(date +%u) in
    1|4) # 周一、周四 - 完整备份
        rdb_backup
        aof_backup
        ;;
    *) # 其他时间 - 增量同步
        incremental_sync
        ;;
esac

# 清理旧备份
find $BACKUP_DIR -name "*.rdb" -mtime +30 -delete
find $BACKUP_DIR -name "*.aof*" -mtime +7 -delete
```

### 2. 灾难恢复执行

#### Redis数据恢复
```bash
#!/bin/bash
# redis_recovery.sh

BACKUP_DIR="/backup/redis"
TARGET_TIME=$(date -d "1 hour ago" +%Y%m%d_%H%M%S)
RESTORE_DIR="/var/lib/redis_restored"

# 准备恢复环境
prepare_redis_restore() {
    systemctl stop redis
    
    # 备份当前数据
    cp -r /var/lib/redis /var/lib/redis.backup.$(date +%Y%m%d_%H%M%S)
    
    # 创建恢复目录
    mkdir -p $RESTORE_DIR
}

# 恢复RDB数据
restore_redis_rdb() {
    local rdb_backup=$(ls -t $BACKUP_DIR/rdb_*.rdb | head -1)
    
    if [ -f "$rdb_backup" ]; then
        cp $rdb_backup $RESTORE_DIR/dump.rdb
        chown redis:redis $RESTORE_DIR/dump.rdb
        echo "RDB restored from: $rdb_backup"
    else
        echo "No RDB backup found"
        exit 1
    fi
}

# 应用AOF增量数据
apply_redis_aof() {
    local aof_backup=$(ls -t $BACKUP_DIR/aof_*.aof.gz | head -1)
    
    if [ -f "$aof_backup" ]; then
        gunzip -c $aof_backup > $RESTORE_DIR/appendonly.aof
        chown redis:redis $RESTORE_DIR/appendonly.aof
        echo "AOF applied from: $aof_backup"
    fi
}

# 启动恢复后的Redis
start_restored_redis() {
    # 修改Redis配置指向恢复目录
    sed -i "s|dir .*|dir $RESTORE_DIR|" /etc/redis/redis.conf
    
    systemctl start redis
    
    # 验证数据恢复
    redis-cli INFO keyspace
    redis-cli DBSIZE
}

prepare_redis_restore
restore_redis_rdb
apply_redis_aof
start_restored_redis
```

---

## 📊 灾难恢复演练报告模板

### 月度DR演练报告

```markdown
# 数据库灾难恢复演练报告

## 演练基本信息
- **演练时间**: 2024年1月第三个周末
- **演练类型**: 全面灾难恢复演练
- **参与人员**: DBA团队、运维团队、业务代表
- **演练时长**: 8小时

## 演练场景和结果

### 场景1: 主机硬件故障
- **RTO目标**: < 4小时
- **实际RTO**: 3小时15分钟 ✓
- **RPO目标**: < 30分钟
- **实际RPO**: 15分钟 ✓
- **主要步骤耗时**:
  - 故障确认和启动DR: 15分钟
  - 备用实例激活: 30分钟
  - 数据同步验证: 1小时30分钟
  - 应用切换验证: 1小时

### 场景2: 数据中心断电
- **RTO目标**: < 24小时
- **实际RTO**: 18小时 ✓
- **RPO目标**: < 1小时
- **实际RPO**: 30分钟 ✓
- **关键成功因素**:
  - 异地备份数据完整
  - 自动化恢复脚本有效
  - 团队协作顺畅

## 发现的问题和改进建议

### 技术问题
1. **备份验证不充分**
   - 问题: 部分备份文件损坏未被及时发现
   - 改进: 增加每日备份验证机制

2. **网络带宽限制**
   - 问题: 异地数据同步速度较慢
   - 改进: 升级专线带宽，优化压缩算法

### 流程问题
1. **沟通协调不够**
   - 问题: 跨部门协调存在延迟
   - 改进: 建立标准化沟通流程和联系人清单

2. **文档更新滞后**
   - 问题: 部分恢复步骤文档过时
   - 改进: 建立文档版本控制和定期更新机制

## 下月改进计划
- [ ] 实施每日备份自动验证
- [ ] 升级异地同步网络基础设施
- [ ] 完善跨部门应急响应流程
- [ ] 建立DR演练知识库
```

---