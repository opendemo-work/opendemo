# 数据库备份恢复策略实战演示

## 🎯 学习目标

通过本案例你将掌握企业级数据库备份恢复的核心技能：

- 制定完整的备份策略和恢复计划
- 实施多种备份技术（物理备份、逻辑备份、增量备份）
- 建立自动化备份和恢复流程
- 执行灾难恢复演练和验证
- 监控备份作业和健康检查
- 满足合规性备份要求

## 🛠️ 环境准备

### 系统要求
- 已完成数据库安装配置环境
- 具备基础备份恢复概念理解
- 准备充足的存储空间（建议备份存储为生产数据的3倍）
- 网络带宽满足备份传输需求

### 前置条件验证
```bash
# 验证数据库服务状态
systemctl is-active mysqld postgresql-14 mongod redis

# 检查存储空间
df -h /data /backup
free -h

# 验证网络连通性
ping backup-server.example.com
```

## 📁 项目结构

```
backup-strategy-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 备份恢复脚本
│   ├── mysql_backup_restore.sh        # MySQL备份恢复脚本
│   ├── postgresql_backup_restore.sh   # PostgreSQL备份恢复脚本
│   ├── mongodb_backup_restore.sh      # MongoDB备份恢复脚本
│   ├── redis_backup_restore.sh        # Redis备份恢复脚本
│   ├── incremental_backup_manager.py  # 增量备份管理器
│   └── disaster_recovery_orchestrator.sh # 灾难恢复编排器
├── configs/                           # 配置文件
│   ├── backup_policies/               # 备份策略配置
│   ├── retention_rules/               # 保留规则配置
│   ├── automation_jobs/               # 自动化作业配置
│   └── monitoring_alerts/             # 监控告警配置
├── templates/                         # 模板文件
│   ├── backup_job_templates/          # 备份作业模板
│   ├── recovery_plan_templates/       # 恢复计划模板
│   └── compliance_checklists/         # 合规检查清单
├── examples/                          # 实际案例
│   ├── full_backup_scenarios/         # 完整备份场景
│   ├── point_in_time_recovery/        # 时间点恢复案例
│   ├── cross_region_backup/           # 跨区域备份方案
│   └── disaster_recovery_drills/      # 灾难恢复演练
└── docs/                              # 详细文档
    ├── backup_strategy_guide.md       # 备份策略指南
    ├── recovery_procedures.md         # 恢复流程文档
    ├── compliance_requirements.md     # 合规要求文档
    └── best_practices.md              # 最佳实践指南
```

## 📊 企业级备份策略设计

### 备份策略框架
```yaml
# 企业级备份策略配置
backup_strategy:
  # 3-2-1备份原则
  principle: "3-2-1"
  copies: 3          # 至少保留3个数据副本
  media_types: 2     # 使用至少2种不同存储介质
  offsite: 1         # 至少1个副本存放在异地
  
  # 备份频率策略
  frequency:
    full_backup: "daily"        # 每日完整备份
    incremental_backup: "hourly" # 每小时增量备份
    transaction_log: "realtime"  # 实时事务日志备份
    archive_backup: "weekly"     # 每周归档备份
  
  # 保留周期策略
  retention:
    daily_backups: "7 days"      # 日备保留7天
    weekly_backups: "4 weeks"    # 周备保留4周
    monthly_backups: "12 months" # 月备保留12个月
    yearly_backups: "7 years"    # 年备保留7年
    compliance_archive: "forever" # 合规归档永久保存
  
  # 恢复时间目标(RTO)和恢复点目标(RPO)
  sla_targets:
    rto: "4 hours"    # 恢复时间目标
    rpo: "1 hour"     # 恢复点目标
    critical_systems_rto: "1 hour"
    critical_systems_rpo: "15 minutes"
```

## 🔧 核心备份技术实现

### 1. MySQL企业级备份方案

```bash
#!/bin/bash
# MySQL企业级备份恢复脚本

BACKUP_BASE_DIR="/backup/mysql"
LOG_FILE="/var/log/mysql_backup.log"
RETENTION_DAYS=7

# 日志函数
log_message() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

# 完整备份函数
perform_full_backup() {
  local backup_dir="$BACKUP_BASE_DIR/full/$(date +%Y%m%d_%H%M%S)"
  local backup_name="mysql_full_$(date +%Y%m%d_%H%M%S).sql"
  
  mkdir -p "$backup_dir"
  log_message "开始执行MySQL完整备份: $backup_name"
  
  # 使用mysqldump进行完整备份
  mysqldump \
    --single-transaction \
    --routines \
    --triggers \
    --master-data=2 \
    --flush-logs \
    --all-databases \
    --result-file="$backup_dir/$backup_name" \
    --user=backup_user \
    --password=backup_password
  
  if [ $? -eq 0 ]; then
    log_message "MySQL完整备份成功: $backup_name"
    # 压缩备份文件
    gzip "$backup_dir/$backup_name"
    return 0
  else
    log_message "MySQL完整备份失败: $backup_name"
    return 1
  fi
}

# 增量备份函数
perform_incremental_backup() {
  local backup_dir="$BACKUP_BASE_DIR/incremental/$(date +%Y%m%d_%H%M%S)"
  local binlog_dir="/var/lib/mysql/binlog"
  
  mkdir -p "$backup_dir"
  log_message "开始执行MySQL增量备份"
  
  # 备份二进制日志
  local last_binlog=$(mysql -u backup_user -pbackup_password -e "SHOW MASTER STATUS\G" | grep File | awk '{print $2}')
  cp $binlog_dir/mysql-bin.* "$backup_dir/"
  
  # 记录备份位置
  echo "$last_binlog" > "$backup_dir/backup_position.txt"
  
  log_message "MySQL增量备份完成"
  return 0
}

# 物理热备份（使用Percona XtraBackup）
perform_physical_backup() {
  local backup_dir="$BACKUP_BASE_DIR/physical/$(date +%Y%m%d_%H%M%S)"
  
  mkdir -p "$backup_dir"
  log_message "开始执行MySQL物理热备份"
  
  xtrabackup \
    --backup \
    --target-dir="$backup_dir" \
    --user=backup_user \
    --password=backup_password \
    --parallel=4
  
  if [ $? -eq 0 ]; then
    log_message "MySQL物理备份成功"
    # 创建备份归档
    tar -czf "$backup_dir.tar.gz" -C "$backup_dir" .
    return 0
  else
    log_message "MySQL物理备份失败"
    return 1
  fi
}

# 恢复函数
restore_from_backup() {
  local backup_file=$1
  local restore_point=$2
  
  log_message "开始从备份恢复: $backup_file"
  
  # 停止MySQL服务
  systemctl stop mysqld
  
  # 清理现有数据
  rm -rf /var/lib/mysql/*
  
  if [[ $backup_file == *.tar.gz ]]; then
    # 物理备份恢复
    tar -xzf "$backup_file" -C /tmp/restore_temp
    xtrabackup --prepare --target-dir=/tmp/restore_temp
    xtrabackup --copy-back --target-dir=/tmp/restore_temp
  else
    # 逻辑备份恢复
    gunzip -c "$backup_file" | mysql -u root -p
  fi
  
  # 调整权限
  chown -R mysql:mysql /var/lib/mysql
  
  # 启动MySQL服务
  systemctl start mysqld
  
  # 如果指定了恢复时间点，则应用二进制日志
  if [ -n "$restore_point" ]; then
    apply_binary_logs "$restore_point"
  fi
  
  log_message "MySQL恢复完成"
}

# 应用二进制日志到指定时间点
apply_binary_logs() {
  local restore_datetime=$1
  local binlog_files=$(find /backup/mysql/binlog -name "mysql-bin.*" -newermt "$restore_datetime")
  
  for binlog in $binlog_files; do
    mysqlbinlog --stop-datetime="$restore_datetime" "$binlog" | mysql -u root -p
  done
}

# 备份验证函数
verify_backup_integrity() {
  local backup_file=$1
  
  log_message "验证备份完整性: $backup_file"
  
  if [[ $backup_file == *.sql.gz ]]; then
    # 验证SQL备份
    gunzip -c "$backup_file" | head -100 | mysql -u backup_user -pbackup_password -e "SELECT 1;"
  elif [[ $backup_file == *.tar.gz ]]; then
    # 验证物理备份
    tar -tzf "$backup_file" > /dev/null
  fi
  
  if [ $? -eq 0 ]; then
    log_message "备份验证通过: $backup_file"
    return 0
  else
    log_message "备份验证失败: $backup_file"
    return 1
  fi
}

# 清理过期备份
cleanup_expired_backups() {
  log_message "清理过期备份文件"
  
  find "$BACKUP_BASE_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
  find "$BACKUP_BASE_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
  find "$BACKUP_BASE_DIR" -name "mysql-bin.*" -mtime +$RETENTION_DAYS -delete
  
  log_message "过期备份清理完成"
}

# 主执行逻辑
main() {
  case "$1" in
    full)
      perform_full_backup
      ;;
    incremental)
      perform_incremental_backup
      ;;
    physical)
      perform_physical_backup
      ;;
    restore)
      restore_from_backup "$2" "$3"
      ;;
    verify)
      verify_backup_integrity "$2"
      ;;
    cleanup)
      cleanup_expired_backups
      ;;
    *)
      echo "Usage: $0 {full|incremental|physical|restore|verify|cleanup} [args]"
      exit 1
      ;;
  esac
}

# 执行主函数
main "$@"
```

### 2. PostgreSQL备份恢复方案

```bash
#!/bin/bash
# PostgreSQL企业级备份恢复脚本

BACKUP_BASE_DIR="/backup/postgresql"
PG_DATA_DIR="/data/postgresql"
LOG_FILE="/var/log/postgresql_backup.log"

# 基础备份函数
perform_base_backup() {
  local backup_label="base_backup_$(date +%Y%m%d_%H%M%S)"
  local backup_dir="$BACKUP_BASE_DIR/base/$backup_label"
  
  mkdir -p "$backup_dir"
  echo "$(date): 开始基础备份 $backup_label" >> $LOG_FILE
  
  # 使用pg_basebackup进行基础备份
  pg_basebackup \
    --host=localhost \
    --username=replicator \
    --pgdata="$backup_dir" \
    --wal-method=stream \
    --checkpoint=fast \
    --progress \
    --verbose
  
  if [ $? -eq 0 ]; then
    echo "$(date): 基础备份完成 $backup_label" >> $LOG_FILE
    # 创建备份标签
    echo "$backup_label" > "$backup_dir/backup_label"
    return 0
  else
    echo "$(date): 基础备份失败 $backup_label" >> $LOG_FILE
    return 1
  fi
}

# WAL归档备份
setup_wal_archiving() {
  # 在postgresql.conf中配置WAL归档
  cat >> /data/postgresql/postgresql.conf << EOF
# WAL归档配置
archive_mode = on
archive_command = 'cp %p /backup/postgresql/wal/%f'
archive_timeout = 300
EOF
  
  # 创建WAL归档目录
  mkdir -p /backup/postgresql/wal
  chown postgres:postgres /backup/postgresql/wal
  
  # 重新加载配置
  systemctl reload postgresql-14
}

# 逻辑备份（pg_dump）
perform_logical_backup() {
  local database_name=$1
  local backup_file="$BACKUP_BASE_DIR/logical/${database_name}_$(date +%Y%m%d_%H%M%S).sql"
  
  mkdir -p "$(dirname "$backup_file")"
  
  pg_dump \
    --host=localhost \
    --username=backup_user \
    --dbname="$database_name" \
    --format=custom \
    --compress=9 \
    --file="$backup_file" \
    --verbose
  
  if [ $? -eq 0 ]; then
    echo "$(date): 逻辑备份完成 $database_name" >> $LOG_FILE
    return 0
  else
    echo "$(date): 逻辑备份失败 $database_name" >> $LOG_FILE
    return 1
  fi
}

# 恢复到指定时间点
point_in_time_recovery() {
  local target_time=$1
  local recovery_base=$2
  
  echo "$(date): 开始时间点恢复到 $target_time" >> $LOG_FILE
  
  # 停止PostgreSQL
  systemctl stop postgresql-14
  
  # 清理现有数据
  rm -rf $PG_DATA_DIR/*
  
  # 恢复基础备份
  cp -r "$recovery_base"/* $PG_DATA_DIR/
  
  # 创建recovery.conf
  cat > $PG_DATA_DIR/recovery.conf << EOF
restore_command = 'cp /backup/postgresql/wal/%f %p'
recovery_target_time = '$target_time'
recovery_target_action = 'promote'
EOF
  
  # 调整权限
  chown -R postgres:postgres $PG_DATA_DIR
  
  # 启动PostgreSQL（进入恢复模式）
  systemctl start postgresql-14
  
  echo "$(date): 时间点恢复启动完成" >> $LOG_FILE
}

# 备份验证
verify_postgresql_backup() {
  local backup_dir=$1
  
  # 验证基础备份完整性
  pg_verifybackup "$backup_dir"
  
  if [ $? -eq 0 ]; then
    echo "$(date): 备份验证通过 $backup_dir" >> $LOG_FILE
    return 0
  else
    echo "$(date): 备份验证失败 $backup_dir" >> $LOG_FILE
    return 1
  fi
}
```

### 3. MongoDB备份恢复方案

```javascript
// MongoDB企业级备份恢复脚本

// 配置备份参数
const BACKUP_CONFIG = {
  baseDir: "/backup/mongodb",
  retentionDays: 7,
  compressionLevel: 6
};

// 完整备份函数
function performFullBackup() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = `${BACKUP_CONFIG.baseDir}/full/${timestamp}`;
  
  console.log(`开始MongoDB完整备份: ${timestamp}`);
  
  // 创建备份目录
  fs.mkdirSync(backupPath, { recursive: true });
  
  // 执行mongodump
  const backupCmd = `mongodump --host localhost --port 27017 \
                    --out ${backupPath} \
                    --gzip \
                    --archive=${backupPath}/full_backup.archive`;
  
  const result = execSync(backupCmd, { stdio: 'inherit' });
  
  if (result.status === 0) {
    console.log(`完整备份成功: ${backupPath}`);
    return backupPath;
  } else {
    console.error(`完整备份失败: ${result.stderr}`);
    throw new Error('Backup failed');
  }
}

// 增量备份（Oplog备份）
function performIncrementalBackup(lastTs) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = `${BACKUP_CONFIG.baseDir}/incremental/${timestamp}`;
  
  console.log(`开始MongoDB增量备份: ${timestamp}`);
  
  // 获取当前oplog时间戳
  const db = connect("localhost:27017/admin");
  const oplogInfo = db.runCommand({ replSetGetStatus: 1 });
  const currentTs = oplogInfo.date;
  
  // 备份oplog
  const oplogBackupCmd = `mongodump --host localhost --port 27017 \
                         --db local --collection oplog.rs \
                         --query '{"ts": {"$gte": Timestamp(${lastTs})}}' \
                         --out ${backupPath}/oplog`;
  
  execSync(oplogBackupCmd, { stdio: 'inherit' });
  
  // 保存时间戳信息
  fs.writeFileSync(`${backupPath}/timestamp.json`, JSON.stringify({
    from: lastTs,
    to: currentTs,
    createdAt: new Date()
  }));
  
  console.log(`增量备份完成: ${backupPath}`);
  return currentTs;
}

// 分片集群备份
function backupShardedCluster() {
  const configDB = connect("localhost:27017/config");
  const shards = configDB.shards.find().toArray();
  
  const backupResults = [];
  
  // 备份每个分片
  shards.forEach(shard => {
    const shardConn = connect(shard.host);
    const shardBackup = performFullBackup(shardConn);
    backupResults.push({
      shardId: shard._id,
      backupPath: shardBackup
    });
  });
  
  // 备份配置服务器
  const configBackup = performFullBackup(configDB);
  backupResults.push({
    shardId: "config",
    backupPath: configBackup
  });
  
  return backupResults;
}

// 恢复函数
function restoreFromBackup(backupPath, targetTime = null) {
  console.log(`开始从备份恢复: ${backupPath}`);
  
  // 停止MongoDB服务
  execSync('systemctl stop mongod', { stdio: 'inherit' });
  
  // 清理现有数据
  execSync('rm -rf /data/mongodb/*', { stdio: 'inherit' });
  
  // 恢复数据
  const restoreCmd = `mongorestore --host localhost --port 27017 \
                     --drop \
                     --gzip \
                     --archive=${backupPath}/full_backup.archive`;
  
  execSync(restoreCmd, { stdio: 'inherit' });
  
  // 如果指定了恢复时间点，则应用oplog
  if (targetTime) {
    applyOplogToPointInTime(targetTime);
  }
  
  // 启动MongoDB服务
  execSync('systemctl start mongod', { stdio: 'inherit' });
  
  console.log('MongoDB恢复完成');
}

// Oplog时间点恢复
function applyOplogToPointInTime(targetTime) {
  const oplogBackup = findOplogBackup(targetTime);
  
  const applyCmd = `mongorestore --host localhost --port 27017 \
                   --oplogReplay \
                   --oplogLimit="${targetTime}" \
                   ${oplogBackup}/oplog`;
  
  execSync(applyCmd, { stdio: 'inherit' });
}

// 备份验证
function verifyBackupIntegrity(backupPath) {
  console.log(`验证备份完整性: ${backupPath}`);
  
  // 检查备份文件存在性
  if (!fs.existsSync(backupPath)) {
    throw new Error('Backup directory not found');
  }
  
  // 验证备份元数据
  const metadata = JSON.parse(fs.readFileSync(`${backupPath}/metadata.json`));
  
  // 执行校验查询
  const testConn = connect("localhost:27017/test");
  const docCount = testConn.getSiblingDB('test').test_collection.count();
  
  console.log(`备份验证通过，文档数量: ${docCount}`);
  return true;
}
```

### 4. Redis备份恢复方案

```bash
#!/bin/bash
# Redis企业级备份恢复脚本

REDIS_CLI="redis-cli"
BACKUP_DIR="/backup/redis"
LOG_FILE="/var/log/redis_backup.log"

# RDB持久化备份
perform_rdb_backup() {
  local backup_name="redis_rdb_$(date +%Y%m%d_%H%M%S).rdb"
  local backup_path="$BACKUP_DIR/rdb/$backup_name"
  
  echo "$(date): 开始RDB备份 $backup_name" >> $LOG_FILE
  
  # 触发RDB快照
  $REDIS_CLI BGSAVE
  
  # 等待快照完成
  while [ $($REDIS_CLI LASTSAVE) -eq 0 ]; do
    sleep 1
  done
  
  # 复制RDB文件
  cp /data/redis/dump.rdb "$backup_path"
  
  # 压缩备份
  gzip "$backup_path"
  
  if [ $? -eq 0 ]; then
    echo "$(date): RDB备份成功 $backup_name" >> $LOG_FILE
    return 0
  else
    echo "$(date): RDB备份失败 $backup_name" >> $LOG_FILE
    return 1
  fi
}

# AOF持久化备份
perform_aof_backup() {
  local backup_name="redis_aof_$(date +%Y%m%d_%H%M%S).aof"
  local backup_path="$BACKUP_DIR/aof/$backup_name"
  
  echo "$(date): 开始AOF备份 $backup_name" >> $LOG_FILE
  
  # 重写AOF文件以压缩大小
  $REDIS_CLI BGREWRITEAOF
  
  # 等待重写完成
  sleep 10
  
  # 复制AOF文件
  cp /data/redis/appendonly.aof "$backup_path"
  
  # 压缩备份
  gzip "$backup_path"
  
  echo "$(date): AOF备份完成 $backup_name" >> $LOG_FILE
}

# 混合备份策略
perform_hybrid_backup() {
  # 同时执行RDB和AOF备份
  perform_rdb_backup &
  perform_aof_backup &
  
  wait
  
  echo "$(date): 混合备份完成" >> $LOG_FILE
}

# 主从架构备份
backup_redis_cluster() {
  local master_ip=$1
  local backup_label="cluster_backup_$(date +%Y%m%d_%H%M%S)"
  
  echo "$(date): 开始集群备份 $backup_label" >> $LOG_FILE
  
  # 获取集群节点信息
  local nodes=$($REDIS_CLI -h $master_ip CLUSTER NODES | grep "master")
  
  # 为每个主节点执行备份
  echo "$nodes" | while read node; do
    local node_ip=$(echo $node | awk '{print $2}' | cut -d: -f1)
    local node_port=$(echo $node | awk '{print $2}' | cut -d: -f2)
    
    $REDIS_CLI -h $node_ip -p $node_port BGSAVE
  done
  
  echo "$(date): 集群备份完成 $backup_label" >> $LOG_FILE
}

# 恢复函数
restore_redis_data() {
  local backup_file=$1
  local backup_type=$2  # rdb or aof
  
  echo "$(date): 开始Redis数据恢复" >> $LOG_FILE
  
  # 停止Redis服务
  systemctl stop redis
  
  # 清理现有数据
  rm -f /data/redis/dump.rdb /data/redis/appendonly.aof
  
  # 恢复备份文件
  if [ "$backup_type" = "rdb" ]; then
    gunzip -c "$backup_file" > /data/redis/dump.rdb
  elif [ "$backup_type" = "aof" ]; then
    gunzip -c "$backup_file" > /data/redis/appendonly.aof
  fi
  
  # 调整权限
  chown redis:redis /data/redis/*
  
  # 启动Redis服务
  systemctl start redis
  
  echo "$(date): Redis恢复完成" >> $LOG_FILE
}

# 备份验证
verify_redis_backup() {
  local backup_file=$1
  
  echo "$(date): 验证Redis备份 $backup_file" >> $LOG_FILE
  
  # 检查文件完整性
  if [[ $backup_file == *.gz ]]; then
    gunzip -t "$backup_file"
  else
    file "$backup_file" | grep -q "data"
  fi
  
  if [ $? -eq 0 ]; then
    echo "$(date): Redis备份验证通过" >> $LOG_FILE
    return 0
  else
    echo "$(date): Redis备份验证失败" >> $LOG_FILE
    return 1
  fi
}

# 自动化备份调度
setup_backup_schedule() {
  # 创建crontab条目
  crontab -l > /tmp/current_crontab
  
  # 添加定时备份任务
  cat >> /tmp/current_crontab << EOF
# Redis备份任务
0 */4 * * * $0 perform_rdb_backup >> $LOG_FILE 2>&1
0 2 * * * $0 perform_aof_backup >> $LOG_FILE 2>&1
0 3 * * 0 $0 backup_redis_cluster >> $LOG_FILE 2>&1
EOF
  
  crontab /tmp/current_crontab
  rm /tmp/current_crontab
  
  echo "$(date): 备份调度配置完成" >> $LOG_FILE
}
```

## 🔄 自动化备份管理平台

### Python备份编排器
```python
#!/usr/bin/env python3
"""
企业级备份管理平台
支持多数据库统一备份调度和监控
"""

import os
import json
import logging
import schedule
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class BackupJob:
    """备份作业配置"""
    job_id: str
    database_type: str
    database_name: str
    backup_type: str  # full, incremental, logical
    schedule: str
    retention_days: int
    storage_path: str
    enabled: bool = True

class BackupManager:
    """备份管理器"""
    
    def __init__(self, config_file: str = "/etc/backup_manager.json"):
        self.config_file = config_file
        self.jobs = []
        self.logger = self._setup_logging()
        self.load_configuration()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/var/log/backup_manager.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_configuration(self):
        """加载备份配置"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.jobs = [BackupJob(**job) for job in config.get('jobs', [])]
            self.logger.info(f"加载了 {len(self.jobs)} 个备份作业")
        except FileNotFoundError:
            self.logger.warning("配置文件不存在，使用默认配置")
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置"""
        default_jobs = [
            {
                "job_id": "mysql_daily_full",
                "database_type": "mysql",
                "database_name": "all_databases",
                "backup_type": "full",
                "schedule": "0 2 * * *",
                "retention_days": 7,
                "storage_path": "/backup/mysql"
            }
        ]
        
        config = {"jobs": default_jobs}
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.jobs = [BackupJob(**job) for job in default_jobs]
    
    def execute_backup_job(self, job: BackupJob):
        """执行备份作业"""
        try:
            self.logger.info(f"开始执行备份作业: {job.job_id}")
            
            # 根据数据库类型选择相应的备份脚本
            script_map = {
                'mysql': '/opt/scripts/mysql_backup_restore.sh',
                'postgresql': '/opt/scripts/postgresql_backup_restore.sh',
                'mongodb': '/opt/scripts/mongodb_backup_restore.sh',
                'redis': '/opt/scripts/redis_backup_restore.sh'
            }
            
            script_path = script_map.get(job.database_type)
            if not script_path or not os.path.exists(script_path):
                raise FileNotFoundError(f"备份脚本不存在: {script_path}")
            
            # 执行备份命令
            cmd = [script_path, job.backup_type]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            
            if result.returncode == 0:
                self.logger.info(f"备份作业成功: {job.job_id}")
                self._record_backup_success(job)
            else:
                self.logger.error(f"备份作业失败: {job.job_id}, 错误: {result.stderr}")
                self._record_backup_failure(job, result.stderr)
                
        except Exception as e:
            self.logger.error(f"执行备份作业异常: {job.job_id}, 错误: {str(e)}")
            self._record_backup_failure(job, str(e))
    
    def _record_backup_success(self, job: BackupJob):
        """记录备份成功"""
        record = {
            "job_id": job.job_id,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "backup_path": f"{job.storage_path}/{job.backup_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        self._save_backup_record(record)
    
    def _record_backup_failure(self, job: BackupJob, error: str):
        """记录备份失败"""
        record = {
            "job_id": job.job_id,
            "status": "failed",
            "timestamp": datetime.now().isoformat(),
            "error": error
        }
        self._save_backup_record(record)
    
    def _save_backup_record(self, record: Dict):
        """保存备份记录"""
        record_file = "/var/log/backup_records.json"
        records = []
        
        # 读取现有记录
        if os.path.exists(record_file):
            with open(record_file, 'r') as f:
                records = json.load(f)
        
        # 添加新记录
        records.append(record)
        
        # 保存记录
        with open(record_file, 'w') as f:
            json.dump(records, f, indent=2)
    
    def cleanup_expired_backups(self):
        """清理过期备份"""
        self.logger.info("开始清理过期备份")
        
        for job in self.jobs:
            if not job.enabled:
                continue
                
            cutoff_date = datetime.now() - timedelta(days=job.retention_days)
            backup_dir = job.storage_path
            
            # 清理过期文件
            cmd = f"find {backup_dir} -name '*.{job.backup_type}*' -mtime +{job.retention_days} -delete"
            subprocess.run(cmd, shell=True)
            
        self.logger.info("过期备份清理完成")
    
    def health_check(self):
        """健康检查"""
        self.logger.info("执行备份系统健康检查")
        
        # 检查存储空间
        df_output = subprocess.check_output(['df', '/backup'], text=True)
        usage_percent = int(df_output.split('\n')[1].split()[4].rstrip('%'))
        
        if usage_percent > 90:
            self.logger.warning(f"备份存储空间使用率过高: {usage_percent}%")
        
        # 检查最近备份状态
        self._check_recent_backups()
    
    def _check_recent_backups(self):
        """检查最近备份状态"""
        record_file = "/var/log/backup_records.json"
        if not os.path.exists(record_file):
            return
        
        with open(record_file, 'r') as f:
            records = json.load(f)
        
        # 检查24小时内备份状态
        recent_time = datetime.now() - timedelta(hours=24)
        recent_records = [r for r in records if datetime.fromisoformat(r['timestamp']) > recent_time]
        
        failed_count = len([r for r in recent_records if r['status'] == 'failed'])
        if failed_count > 0:
            self.logger.warning(f"最近24小时有 {failed_count} 个备份失败")

# 使用示例
def main():
    manager = BackupManager()
    
    # 设置定时任务
    schedule.every().day.at("02:00").do(lambda: manager.execute_backup_job(manager.jobs[0]))
    schedule.every().day.at("03:00").do(manager.cleanup_expired_backups)
    schedule.every().hour.do(manager.health_check)
    
    # 运行调度器
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
```

## 🧪 备份恢复验证测试

### 自动化验证脚本
```bash
#!/bin/bash
# 备份恢复验证测试套件

TEST_RESULTS=()

# MySQL备份验证
test_mysql_backup() {
  echo "=== MySQL备份验证 ==="
  
  # 执行完整备份
  /opt/scripts/mysql_backup_restore.sh full
  local backup_file=$(ls -t /backup/mysql/full/*.sql.gz | head -1)
  
  # 验证备份文件
  if [ -f "$backup_file" ] && [ -s "$backup_file" ]; then
    TEST_RESULTS+=("MySQL备份文件验证: 通过")
    echo "✅ MySQL备份文件存在且非空"
  else
    TEST_RESULTS+=("MySQL备份文件验证: 失败")
    echo "❌ MySQL备份文件异常"
    return
  fi
  
  # 验证备份完整性
  gunzip -t "$backup_file"
  if [ $? -eq 0 ]; then
    TEST_RESULTS+=("MySQL备份完整性验证: 通过")
    echo "✅ MySQL备份完整性验证通过"
  else
    TEST_RESULTS+=("MySQL备份完整性验证: 失败")
    echo "❌ MySQL备份完整性验证失败"
  fi
}

# PostgreSQL备份验证
test_postgresql_backup() {
  echo "=== PostgreSQL备份验证 ==="
  
  # 执行基础备份
  /opt/scripts/postgresql_backup_restore.sh base
  local backup_dir=$(ls -td /backup/postgresql/base/* | head -1)
  
  # 验证备份目录
  if [ -d "$backup_dir" ] && [ -f "$backup_dir/backup_label" ]; then
    TEST_RESULTS+=("PostgreSQL备份目录验证: 通过")
    echo "✅ PostgreSQL备份目录结构正确"
  else
    TEST_RESULTS+=("PostgreSQL备份目录验证: 失败")
    echo "❌ PostgreSQL备份目录异常"
    return
  fi
  
  # 验证备份完整性
  pg_verifybackup "$backup_dir"
  if [ $? -eq 0 ]; then
    TEST_RESULTS+=("PostgreSQL备份完整性验证: 通过")
    echo "✅ PostgreSQL备份完整性验证通过"
  else
    TEST_RESULTS+=("PostgreSQL备份完整性验证: 失败")
    echo "❌ PostgreSQL备份完整性验证失败"
  fi
}

# MongoDB备份验证
test_mongodb_backup() {
  echo "=== MongoDB备份验证 ==="
  
  # 执行完整备份
  mongodump --host localhost --out /tmp/mongo_test_backup --gzip
  local backup_dir="/tmp/mongo_test_backup"
  
  # 验证备份文件
  if [ -d "$backup_dir" ] && [ -n "$(find $backup_dir -name '*.bson.gz')" ]; then
    TEST_RESULTS+=("MongoDB备份文件验证: 通过")
    echo "✅ MongoDB备份文件存在"
  else
    TEST_RESULTS+=("MongoDB备份文件验证: 失败")
    echo "❌ MongoDB备份文件异常"
  fi
  
  # 清理测试备份
  rm -rf "$backup_dir"
}

# 生成综合测试报告
generate_backup_test_report() {
  echo "=== 备份恢复测试综合报告 ==="
  
  local total_tests=${#TEST_RESULTS[@]}
  local passed_tests=0
  
  for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
    if [[ $result == *"通过"* ]]; then
      ((passed_tests++))
    fi
  done
  
  echo ""
  echo "测试总结:"
  echo "总测试项: $total_tests"
  echo "通过项: $passed_tests"
  echo "通过率: $((passed_tests * 100 / total_tests))%"
  
  # 保存报告
  local report_file="/tmp/backup_test_report_$(date +%Y%m%d_%H%M%S).txt"
  printf "%s\n" "${TEST_RESULTS[@]}" > "$report_file"
  echo "详细报告已保存: $report_file"
}

# 执行所有测试
test_mysql_backup
test_postgresql_backup
test_mongodb_backup
generate_backup_test_report
```

## 📚 最佳实践总结

### 企业级备份策略要点
1. **3-2-1原则**: 3个副本、2种介质、1个异地
2. **分层备份**: 完整备份+增量备份+事务日志
3. **自动化调度**: 定时执行，减少人工干预
4. **多重验证**: 备份完成后立即验证完整性
5. **定期演练**: 定期执行恢复演练验证有效性
6. **监控告警**: 实时监控备份状态和存储空间

### 合规性要求
- **金融行业**: 满足巴塞尔协议III的数据保留要求
- **医疗行业**: 符合HIPAA的6年数据保留规定
- **电商行业**: 满足PCI-DSS的备份和恢复要求
- **一般企业**: 遵循SOX法案的审计要求

---
> **💡 提示**: 备份不是目的，能够在需要时快速恢复才是关键。建议定期进行恢复演练，确保备份的有效性。