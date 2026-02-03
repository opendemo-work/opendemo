# MongoDB副本集部署完整指南

## 🎯 概述

MongoDB副本集是实现高可用性和数据冗余的核心技术，通过多个节点的数据同步确保服务连续性和数据安全。本指南提供从基础部署到高级管理的完整副本集解决方案。

## 📋 目录

1. [副本集基础理论](#1-副本集基础理论)
2. [三节点副本集部署](#2-三节点副本集部署)
3. [成员管理与维护](#3-成员管理与维护)
4. [读写分离配置](#4-读写分离配置)
5. [故障处理与恢复](#5-故障处理与恢复)
6. [监控与性能优化](#6-监控与性能优化)

---

## 1. 副本集基础理论

### 1.1 副本集核心概念

#### 副本集架构
```mermaid
graph TD
    A[Primary节点] --> B[Secondary节点1]
    A --> C[Secondary节点2]
    A --> D[Arbiter节点]
    
    B --> E[读操作负载]
    C --> E
    
    F[写操作] --> A
    
    G[心跳检测] --> A
    G --> B
    G --> C
    G --> D
    
    subgraph "数据流向"
        A --> H[Oplog同步]
        H --> B
        H --> C
    end
```

#### 节点角色说明
```javascript
// 副本集节点角色定义
replica_set_roles = {
    primary: {
        description: "主节点 - 处理所有写操作",
        responsibilities: ["接受写请求", "维护oplog", "协调选举"],
        characteristics: ["唯一性", "权威性", "可读写"]
    },
    
    secondary: {
        description: "从节点 - 数据副本和读操作",
        responsibilities: ["数据同步", "读操作处理", "参与选举"],
        characteristics: ["数据冗余", "负载分担", "故障备用"]
    },
    
    arbiter: {
        description: "仲裁节点 - 只参与选举投票",
        responsibilities: ["选举投票", "不存储数据"],
        characteristics: ["轻量级", "节省资源", "奇数投票"]
    },
    
    hidden: {
        description: "隐藏节点 - 不对外提供服务",
        responsibilities: ["数据备份", "特殊查询"],
        characteristics: ["不可见性", "优先级为0", "特殊用途"]
    },
    
    delayed: {
        description: "延迟节点 - 延迟应用oplog",
        responsibilities: ["灾难恢复", "历史数据查询"],
        characteristics: ["时间延迟", "数据保护", "恢复能力"]
    }
};
```

### 1.2 选举机制详解

#### 选举触发条件
```javascript
// 选举触发场景分析
election_triggers = {
    primary_failure: {
        condition: "主节点不可达超过10秒",
        process: "从节点发起选举",
        duration: "通常30秒内完成"
    },
    
    network_partition: {
        condition: "网络分裂导致多数节点失联",
        process: "多数派节点选出新主",
        outcome: "少数派节点变为只读"
    },
    
    step_down: {
        condition: "主节点主动降级",
        process: "立即触发新选举",
        use_case: "维护操作、负载迁移"
    },
    
    member_reconfiguration: {
        condition: "副本集成员变更",
        process: "重新计算投票权重",
        requirement: "保持奇数个投票成员"
    }
};

// 选举优先级配置
configure_election_priority = function() {
    // 设置节点优先级
    cfg = rs.conf();
    
    // 主节点优先级最高
    cfg.members[0].priority = 2;
    
    // 从节点优先级中等
    cfg.members[1].priority = 1;
    cfg.members[2].priority = 1;
    
    // 隐藏节点优先级为0
    cfg.members[3].priority = 0;
    cfg.members[3].hidden = true;
    
    // 延迟节点配置
    cfg.members[4].priority = 0;
    cfg.members[4].slaveDelay = 3600;  // 延迟1小时
    
    rs.reconfig(cfg);
};
```

## 2. 三节点副本集部署

### 2.1 环境准备

#### 系统配置脚本
```bash
#!/bin/bash
# MongoDB副本集环境准备

prepare_replica_set_environment() {
    echo "=== MongoDB副本集环境准备 ==="
    
    # 1. 系统优化
    optimize_system() {
        # 内核参数优化
        echo "vm.swappiness = 1" >> /etc/sysctl.conf
        echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
        echo "net.ipv4.tcp_fin_timeout = 30" >> /etc/sysctl.conf
        sysctl -p
        
        # 文件系统优化
        echo "never" > /sys/kernel/mm/transparent_hugepage/enabled
        echo "never" > /sys/kernel/mm/transparent_hugepage/defrag
        
        # ulimit设置
        echo "* soft nofile 65536" >> /etc/security/limits.conf
        echo "* hard nofile 65536" >> /etc/security/limits.conf
        echo "* soft nproc 32768" >> /etc/security/limits.conf
        echo "* hard nproc 32768" >> /etc/security/limits.conf
    }
    
    # 2. MongoDB安装
    install_mongodb() {
        # 添加MongoDB仓库
        cat > /etc/yum.repos.d/mongodb-org-6.0.repo << EOF
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/6.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
EOF
        
        # 安装MongoDB
        yum install -y mongodb-org
        
        # 启动服务
        systemctl enable mongod
        systemctl start mongod
    }
    
    # 3. 网络配置
    configure_networking() {
        # 防火墙配置
        firewall-cmd --permanent --add-port=27017/tcp
        firewall-cmd --permanent --add-port=27018/tcp  # 副本集端口
        firewall-cmd --permanent --add-port=27019/tcp  # 配置端口
        firewall-cmd --reload
        
        # hosts文件配置
        cat >> /etc/hosts << EOF
192.168.1.10 mongo-primary
192.168.1.11 mongo-secondary-1
192.168.1.12 mongo-secondary-2
EOF
    }
    
    optimize_system
    install_mongodb
    configure_networking
    
    echo "环境准备完成"
}
```

### 2.2 副本集初始化

#### 主节点配置
```javascript
// 主节点初始化配置
init_primary_node = function() {
    // 1. 启动MongoDB实例
    // mongod --replSet myReplicaSet --dbpath /var/lib/mongo --port 27017
    
    // 2. 连接MongoDB
    // mongo --host mongo-primary --port 27017
    
    // 3. 初始化副本集
    rs.initiate({
        _id: "myReplicaSet",
        members: [
            { _id: 0, host: "mongo-primary:27017" },
            { _id: 1, host: "mongo-secondary-1:27017" },
            { _id: 2, host: "mongo-secondary-2:27017" }
        ]
    });
    
    // 4. 验证副本集状态
    rs.status();
    
    // 5. 创建管理员用户
    use admin;
    db.createUser({
        user: "admin",
        pwd: "${DB_PASSWORD}",
        roles: [ "root" ]
    });
    
    // 6. 创建应用用户
    use myapp;
    db.createUser({
        user: "appuser",
        pwd: "${DB_PASSWORD}",
        roles: [
            { role: "readWrite", db: "myapp" },
            { role: "read", db: "reporting" }
        ]
    });
};

// 副本集配置优化
optimize_replica_set_config = function() {
    var cfg = rs.conf();
    
    // 设置写关注
    cfg.settings = {
        getLastErrorModes: {
            waitForTwo: { 
                "mongo-secondary-1:27017": 1, 
                "mongo-secondary-2:27017": 1 
            }
        },
        getLastErrorDefaults: { w: "majority", wtimeout: 5000 }
    };
    
    // 配置心跳和选举参数
    cfg.settings.heartbeatTimeoutSecs = 10;
    cfg.settings.electionTimeoutMillis = 10000;
    
    rs.reconfig(cfg);
};
```

### 2.3 从节点加入

#### 从节点配置脚本
```bash
#!/bin/bash
# 从节点配置脚本

configure_secondary_node() {
    local primary_host=$1
    local node_name=$2
    
    echo "=== 配置从节点 ${node_name} ==="
    
    # 1. 创建MongoDB配置文件
    cat > /etc/mongod.conf << EOF
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 0.0.0.0

replication:
  replSetName: myReplicaSet

processManagement:
  fork: true
  pidFilePath: /var/run/mongodb/mongod.pid
EOF
    
    # 2. 启动MongoDB服务
    systemctl restart mongod
    
    # 3. 验证服务状态
    sleep 10
    mongo --eval "db.runCommand({ismaster: 1})"
    
    echo "从节点 ${node_name} 配置完成"
}

# 批量配置从节点
setup_all_secondaries() {
    configure_secondary_node "mongo-primary" "mongo-secondary-1"
    configure_secondary_node "mongo-primary" "mongo-secondary-2"
}
```

## 3. 成员管理与维护

### 3.1 成员状态管理

#### 成员操作命令
```javascript
// 副本集成员管理
replica_set_member_management = {
    // 添加新成员
    add_member: function(new_host) {
        rs.add(new_host);
    },
    
    // 移除成员
    remove_member: function(member_host) {
        rs.remove(member_host);
    },
    
    // 修改成员配置
    modify_member: function(member_id, new_config) {
        var cfg = rs.conf();
        Object.assign(cfg.members[member_id], new_config);
        rs.reconfig(cfg);
    },
    
    // 冻结成员（暂停选举参与）
    freeze_member: function(seconds) {
        db.adminCommand({replSetFreeze: seconds});
    },
    
    // 强制重新配置
    force_reconfig: function(new_config) {
        rs.reconfig(new_config, {force: true});
    }
};

// 成员状态监控
monitor_member_status = function() {
    var status = rs.status();
    
    status.members.forEach(function(member) {
        print("成员: " + member.name);
        print("  状态: " + member.stateStr);
        print("  延迟: " + member.pingMs + "ms");
        print("  最后心跳: " + member.lastHeartbeat);
        print("  Oplog延迟: " + member.optimeDate);
        print("---");
    });
    
    return status;
};
```

### 3.2 数据同步管理

#### 同步状态检查
```javascript
// 数据同步状态分析
analyze_sync_status = function() {
    var status = rs.printSlaveReplicationInfo();
    
    // 检查Oplog应用状态
    db.printSlaveReplicationInfo();
    
    // 检查复制延迟
    db.adminCommand({replSetGetStatus: 1}).members.forEach(function(member) {
        if (member.optime && member.optime.ts) {
            var delay = new Date() - member.optimeDate;
            print(member.name + " 延迟: " + delay + "ms");
        }
    });
    
    // 检查Oplog大小
    var localDb = db.getSiblingDB("local");
    var oplogStats = localDb.oplog.rs.stats();
    print("Oplog大小: " + oplogStats.size);
    print("Oplog存储: " + oplogStats.storageSize);
};

// 同步问题诊断
diagnose_sync_issues = function() {
    // 检查Oplog窗口
    var oplogInfo = db.getSiblingDB("local").system.replset.findOne();
    var oplogSize = db.getSiblingDB("local").oplog.rs.stats().maxSize;
    
    // 检查写操作频率
    var ops = db.currentOp();
    var writeOps = ops.inprog.filter(op => op.op === 'insert' || op.op === 'update' || op.op === 'delete');
    
    return {
        oplog_size: oplogSize,
        current_ops: writeOps.length,
        replication_lag: this.check_replication_lag()
    };
};
```

## 4. 读写分离配置

### 4.1 读偏好设置

#### 应用层读偏好配置
```javascript
// MongoDB读偏好配置
read_preference_configs = {
    // 主节点读取（默认）
    primary: {
        preference: "primary",
        use_case: "强一致性要求",
        example: "db.collection.find().readPref('primary')"
    },
    
    // 从节点读取
    secondary: {
        preference: "secondary",
        use_case: "读操作负载分担",
        example: "db.collection.find().readPref('secondary')"
    },
    
    // 主节点优先
    primaryPreferred: {
        preference: "primaryPreferred",
        use_case: "高可用读取",
        example: "db.collection.find().readPref('primaryPreferred')"
    },
    
    // 从节点优先
    secondaryPreferred: {
        preference: "secondaryPreferred",
        use_case: "性能优先读取",
        example: "db.collection.find().readPref('secondaryPreferred')"
    },
    
    // 最近节点读取
    nearest: {
        preference: "nearest",
        use_case: "地理位置优化",
        example: "db.collection.find().readPref('nearest')"
    }
};

// 连接字符串配置
connection_string_configs = {
    // 基础连接
    basic: "mongodb://mongo-primary,mongo-secondary-1,mongo-secondary-2/myapp",
    
    // 带读偏好
    with_read_pref: "mongodb://mongo-primary,mongo-secondary-1,mongo-secondary-2/myapp?readPreference=secondaryPreferred",
    
    // 带写关注
    with_write_concern: "mongodb://mongo-primary,mongo-secondary-1,mongo-secondary-2/myapp?w=majority&wtimeoutMS=5000",
    
    // 完整配置
    complete: "mongodb://admin:password@mongo-primary:27017,mongo-secondary-1:27017,mongo-secondary-2:27017/myapp?replicaSet=myReplicaSet&readPreference=secondaryPreferred&w=majority&retryWrites=true"
};
```

### 4.2 负载均衡配置

#### 应用层负载均衡
```python
# Python MongoDB连接池配置
from pymongo import MongoClient, ReadPreference
from pymongo.errors import ConnectionFailure

class MongoLoadBalancer:
    def __init__(self, connection_string):
        self.client = MongoClient(
            connection_string,
            read_preference=ReadPreference.SECONDARY_PREFERRED,
            maxPoolSize=50,
            minPoolSize=10,
            maxIdleTimeMS=30000,
            waitQueueTimeoutMS=5000
        )
        self.db = self.client.myapp
    
    def get_collection(self, collection_name):
        """获取集合连接"""
        return self.db[collection_name]
    
    def execute_read_operation(self, collection_name, operation, *args, **kwargs):
        """执行读操作"""
        collection = self.get_collection(collection_name)
        try:
            result = getattr(collection, operation)(*args, **kwargs)
            return result
        except ConnectionFailure as e:
            # 故障转移处理
            self.handle_connection_failure(e)
            raise
    
    def execute_write_operation(self, collection_name, operation, *args, **kwargs):
        """执行写操作"""
        collection = self.get_collection(collection_name)
        # 写操作总是路由到主节点
        with self.client.start_session() as session:
            result = getattr(collection, operation)(*args, **kwargs, session=session)
            return result

# 使用示例
balancer = MongoLoadBalancer("mongodb://localhost:27017,localhost:27018,localhost:27019/myapp?replicaSet=myReplicaSet")
users = balancer.execute_read_operation("users", "find", {"status": "active"})
new_user = balancer.execute_write_operation("users", "insert_one", {"name": "John", "email": "john@example.com"})
```

## 5. 故障处理与恢复

### 5.1 常见故障场景

#### 故障诊断脚本
```bash
#!/bin/bash
# MongoDB故障诊断脚本

diagnose_mongodb_issues() {
    echo "=== MongoDB故障诊断 ==="
    
    # 1. 服务状态检查
    check_service_status() {
        systemctl status mongod | grep Active
        mongo --eval "db.runCommand({ping: 1})" 2>/dev/null || echo "MongoDB连接失败"
    }
    
    # 2. 副本集状态检查
    check_replica_set_status() {
        mongo --eval "rs.status()" | grep -E "(stateStr|health|errmsg)"
    }
    
    # 3. 磁盘空间检查
    check_disk_space() {
        df -h /var/lib/mongo
        du -sh /var/lib/mongo/*
    }
    
    # 4. 内存使用检查
    check_memory_usage() {
        free -h
        ps aux | grep mongod | head -5
    }
    
    # 5. 网络连接检查
    check_network_connectivity() {
        netstat -tlnp | grep 27017
        telnet localhost 27017 < /dev/null 2>&1 && echo "端口可达" || echo "端口不可达"
    }
    
    check_service_status
    check_replica_set_status
    check_disk_space
    check_memory_usage
    check_network_connectivity
}

# 自动故障恢复
auto_recovery_procedures() {
    # 1. 重启MongoDB服务
    restart_mongodb() {
        systemctl restart mongod
        sleep 30
        mongo --eval "db.runCommand({ping: 1})" && echo "服务恢复成功" || echo "服务恢复失败"
    }
    
    # 2. 重新配置副本集
    reconfigure_replica_set() {
        local current_primary=$(mongo --quiet --eval "db.isMaster().primary")
        if [ -z "$current_primary" ]; then
            echo "需要重新配置副本集"
            # 执行重新配置逻辑
        fi
    }
    
    # 3. 数据文件修复
    repair_data_files() {
        if [ -f /var/lib/mongo/mongod.lock ]; then
            echo "检测到锁文件，可能需要修复"
            mongod --repair --dbpath /var/lib/mongo
        fi
    }
}
```

### 5.2 灾难恢复方案

#### 紧急恢复流程
```javascript
// 灾难恢复操作
disaster_recovery_procedures = {
    // 从备份恢复
    restore_from_backup: function(backup_path, restore_point) {
        // 1. 停止MongoDB服务
        // systemctl stop mongod
        
        // 2. 清理数据目录
        // rm -rf /var/lib/mongo/*
        
        // 3. 恢复备份数据
        // mongorestore --drop ${backup_path}
        
        // 4. 应用oplog（如果需要时间点恢复）
        // mongorestore --oplogReplay --oplogLimit ${restore_point} ${backup_path}
        
        // 5. 重启服务
        // systemctl start mongod
    },
    
    // 重新初始化副本集
    reinitialize_replica_set: function() {
        // 1. 在主节点执行
        rs.initiate({
            _id: "myReplicaSet",
            members: [
                { _id: 0, host: "new-primary:27017" }
            ]
        });
        
        // 2. 逐步添加成员
        rs.add("new-secondary-1:27017");
        rs.add("new-secondary-2:27017");
    },
    
    // 数据同步恢复
    resync_member: function(member_host) {
        // 1. 移除故障成员
        rs.remove(member_host);
        
        // 2. 清理成员数据
        // 在该成员上执行
        
        // 3. 重新添加成员
        rs.add(member_host);
    }
};
```

## 6. 监控与性能优化

### 6.1 监控指标体系

#### 核心监控指标
```javascript
// MongoDB监控指标收集
class MongoMonitor {
    constructor() {
        this.metrics = {};
    }
    
    collect_replica_set_metrics() {
        // 副本集状态指标
        var rs_status = rs.status();
        this.metrics.replica_set = {
            primary: rs_status.members.find(m => m.state === 1)?.name,
            secondaries: rs_status.members.filter(m => m.state === 2).length,
            arbiters: rs_status.members.filter(m => m.state === 7).length,
            avg_ping: this.calculate_avg_ping(rs_status.members)
        };
        
        // 复制延迟指标
        this.metrics.replication_lag = this.calculate_replication_lag();
        
        // 连接数指标
        var conn_stats = db.serverStatus().connections;
        this.metrics.connections = {
            current: conn_stats.current,
            available: conn_stats.available,
            total_created: conn_stats.totalCreated
        };
        
        return this.metrics;
    }
    
    calculate_replication_lag() {
        var primary_optime = db.adminCommand({replSetGetStatus: 1})
            .members.find(m => m.state === 1).optimeDate;
        
        var lags = db.adminCommand({replSetGetStatus: 1})
            .members.filter(m => m.state === 2)
            .map(m => new Date() - m.optimeDate);
        
        return {
            max_lag: Math.max(...lags),
            avg_lag: lags.reduce((a,b) => a+b, 0) / lags.length,
            lag_details: lags
        };
    }
    
    generate_alerts(metrics) {
        var alerts = [];
        
        // 复制延迟告警
        if (metrics.replication_lag.max_lag > 10000) {  // 10秒
            alerts.push({
                level: "critical",
                message: "复制延迟过高",
                value: metrics.replication_lag.max_lag
            });
        }
        
        // 连接数告警
        var conn_utilization = metrics.connections.current / 
                              (metrics.connections.current + metrics.connections.available);
        if (conn_utilization > 0.8) {
            alerts.push({
                level: "warning",
                message: "连接使用率过高",
                value: conn_utilization
            });
        }
        
        return alerts;
    }
}
```

### 6.2 性能优化建议

#### 性能调优配置
```javascript
// MongoDB性能优化
performance_optimization = {
    // 索引优化
    optimize_indexes: function() {
        // 查找未使用索引
        db.system.profile.find({millis: {$gt: 100}}).forEach(function(op) {
            if (op.ns && op.query) {
                print("慢查询: " + op.ns);
                print("查询: " + tojson(op.query));
                // 建议创建索引
            }
        });
    },
    
    // Oplog优化
    optimize_oplog: function() {
        // 检查Oplog使用率
        var oplog_stats = db.getSiblingDB("local").oplog.rs.stats();
        var usage_percent = (oplog_stats.size / oplog_stats.maxSize) * 100;
        
        if (usage_percent > 70) {
            print("Oplog使用率过高: " + usage_percent + "%");
            print("建议增加Oplog大小");
        }
    },
    
    // 写关注优化
    optimize_write_concern: function(workload_type) {
        var write_concern = {};
        
        switch(workload_type) {
            case "high_performance":
                write_concern = {w: 1, j: false};
                break;
            case "balanced":
                write_concern = {w: "majority", j: false};
                break;
            case "high_safety":
                write_concern = {w: "majority", j: true};
                break;
        }
        
        return write_concern;
    }
};

// 自动化优化脚本
auto_optimize_replica_set = function() {
    // 1. 分析当前性能
    var current_metrics = new MongoMonitor().collect_replica_set_metrics();
    
    // 2. 生成优化建议
    var recommendations = [];
    
    // 3. 应用优化配置
    if (current_metrics.replication_lag.avg_lag > 5000) {
        recommendations.push("增加Oplog大小");
        // 执行Oplog扩容
    }
    
    if (current_metrics.connections.current > 1000) {
        recommendations.push("增加连接池大小");
        // 调整连接池配置
    }
    
    return recommendations;
};
```

---

## 🔍 关键要点总结

### ✅ 副本集成功要素
- **合理的节点配置**：奇数个节点确保选举顺利进行
- **完善的监控体系**：实时监控副本集状态和性能指标
- **自动化的故障处理**：建立可靠的故障检测和恢复机制
- **性能优化策略**：根据业务特点优化读写分离和索引配置

### ⚠️ 常见风险提醒
- **网络分区风险**：可能导致脑裂和数据不一致
- **Oplog溢出风险**：写入密集场景下Oplog可能不够用
- **选举风暴风险**：频繁的成员变更可能影响稳定性
- **数据同步延迟**：网络或硬件问题可能导致同步延迟

### 🎯 最佳实践建议
1. **渐进式部署**：从简单配置开始，逐步增加复杂功能
2. **充分测试**：在生产环境部署前充分测试各种故障场景
3. **文档化配置**：详细记录所有配置参数和变更历史
4. **定期维护**：定期检查和优化副本集配置
5. **监控告警**：建立完善的监控告警体系

通过科学的MongoDB副本集设计和管理，可以构建高可用、高性能的NoSQL数据库架构，为现代应用提供可靠的数据服务支撑。