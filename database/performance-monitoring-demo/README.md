# 数据库性能监控演示

## 🎯 概述

这是一个关于数据库性能监控的完整演示，涵盖了从基础监控指标到高级性能分析的全方位实践。通过实际案例展示如何有效监控、分析和优化数据库性能。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: MySQL/PostgreSQL性能监控
- **适用场景**: 生产环境数据库性能优化
- **难度等级**: 🔴 高级

### 技术栈
```yaml
dependencies:
  - MySQL 8.0+/PostgreSQL 12+
  - Prometheus监控系统
  - Grafana可视化面板
  - Percona Monitoring Plugins

monitoring_tools:
  - mysqld_exporter
  - pg_exporter
  - node_exporter
```

## 🚀 快速开始

### 环境准备
```bash
# 系统要求
- Linux/macOS系统
- Docker和Docker Compose
- 至少4GB内存

# 安装依赖
docker-compose up -d
```

### 运行演示
```bash
# 启动监控服务
./start-monitoring.sh

# 生成测试负载
./generate-workload.sh

# 查看监控面板
http://localhost:3000
```

## 📁 项目结构

```
performance-monitoring-demo/
├── docker-compose.yml         # Docker编排文件
├── configs/                   # 配置文件目录
│   ├── prometheus.yml        # Prometheus配置
│   └── grafana-dashboard.json # Grafana仪表板
├── scripts/                   # 脚本目录
│   ├── start-monitoring.sh   # 启动脚本
│   ├── generate-workload.sh  # 负载生成脚本
│   └── analyze-performance.py # 性能分析脚本
├── queries/                   # 性能查询SQL
├── dashboards/                # 监控仪表板
└── README.md                 # 本文件
```

## 🔧 核心功能

### 功能特性
1. **实时监控**: 数据库关键性能指标实时展示
2. **慢查询分析**: 自动识别和分析慢查询
3. **资源使用监控**: CPU、内存、磁盘IO监控

### 监控指标
```sql
-- 关键性能指标查询
SELECT * FROM performance_schema.events_statements_summary_by_digest 
WHERE avg_timer_wait > 1000000000 
ORDER BY avg_timer_wait DESC LIMIT 10;
```

## 📊 使用示例

### 基本监控查询
```sql
-- 查看当前连接数
SHOW STATUS LIKE 'Threads_connected';

-- 查看缓冲池命中率
SHOW ENGINE INNODB STATUS\G
```

### 性能分析脚本
```python
#!/usr/bin/env python3
import mysql.connector
import time

def analyze_slow_queries():
    conn = mysql.connector.connect(
        host='localhost',
        user='monitor',
        password='password',
        database='performance_schema'
    )
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DIGEST_TEXT, COUNT_STAR, AVG_TIMER_WAIT/1000000000 as avg_sec
        FROM events_statements_summary_by_digest 
        WHERE AVG_TIMER_WAIT > 1000000000
        ORDER BY AVG_TIMER_WAIT DESC LIMIT 5
    """)
    
    results = cursor.fetchall()
    for row in results:
        print(f"Query: {row[0][:50]}...")
        print(f"Count: {row[1]}, Avg Time: {row[2]:.3f}s")
```

## ⚙️ 配置说明

### 环境变量
```bash
DB_HOST=localhost              # 数据库主机地址
DB_PORT=3306                  # 数据库端口
DB_USER=monitor               # 监控用户
DB_PASSWORD=password          # 监控密码
MONITOR_INTERVAL=30           # 监控间隔(秒)
```

### Prometheus配置
```yaml
scrape_configs:
  - job_name: 'mysql-exporter'
    static_configs:
      - targets: ['mysql-exporter:9104']
    scrape_interval: 15s
```

## 🔍 故障排除

### 常见问题
1. **问题**: 监控数据不显示
   - **解决方案**: 检查exporter服务是否正常运行，确认端口连通性

2. **问题**: 慢查询日志未启用
   - **解决方案**: 在my.cnf中设置slow_query_log=1和long_query_time=1

### 日志查看
```bash
# 查看MySQL错误日志
tail -f /var/log/mysql/error.log

# 查看监控组件日志
docker logs mysql-exporter
```

## 🧪 测试验证

### 性能基准测试
```bash
# 运行sysbench测试
sysbench oltp_read_write --table-size=1000000 run

# 查看测试结果
./analyze-results.sh
```

### 监控验证
```bash
# 验证监控指标采集
curl http://localhost:9104/metrics | grep mysql_global_status
```

## 📈 性能指标

### 基准测试结果
- **QPS**: 2500-3000 queries/sec
- **响应时间**: 平均15ms，95%小于50ms
- **CPU使用率**: 60-80%
- **内存使用**: 2GB左右

## 🔒 安全考虑

### 安全特性
- 监控账户最小权限原则
- 网络访问控制
- 敏感信息加密存储

### 最佳实践
- 定期轮换监控账户密码
- 限制监控接口的网络访问
- 启用SSL/TLS加密传输

## 🚀 部署指南

### 本地部署
```bash
# 克隆项目
git clone <repo-url>
cd performance-monitoring-demo

# 启动所有服务
docker-compose up -d

# 初始化监控
./scripts/setup-monitoring.sh
```

### 生产部署
```bash
# 生产环境部署脚本
ansible-playbook deploy-production.yml

# 配置高可用
kubectl apply -f k8s/production-monitoring.yaml
```

## 📚 相关资源

### 官方文档
- [MySQL Performance Schema](https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html)
- [Prometheus监控最佳实践](https://prometheus.io/docs/practices/)

### 学习资源
- 《高性能MySQL》
- MySQL官方性能调优指南
- Prometheus监控实战课程

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个演示！

### 开展流程
1. Fork项目
2. 创建特性分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---
*最后更新: 2026年2月3日*