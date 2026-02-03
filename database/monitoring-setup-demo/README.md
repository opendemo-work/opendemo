# 数据库性能监控体系实战演示

## 🎯 学习目标

通过本案例你将掌握企业级数据库性能监控的核心技能：

- 构建全方位的数据库性能监控体系
- 实施实时性能指标收集和分析
- 建立智能告警和异常检测机制
- 设计可视化的监控仪表板
- 实现性能瓶颈的自动识别和诊断
- 满足生产环境的SLA监控要求

## 🛠️ 环境准备

### 系统要求
- 已完成数据库安装配置环境
- 具备基础监控概念理解
- 准备监控基础设施（Prometheus、Grafana等）
- 网络可达性确保监控数据收集

### 前置条件验证
```bash
# 验证数据库服务状态
systemctl is-active mysqld postgresql-14 mongod redis

# 验证监控基础设施
systemctl is-active prometheus grafana-server

# 检查网络连通性
ping prometheus-server.example.com
telnet grafana-server.example.com 3000
```

## 📁 项目结构

```
performance-monitoring-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 监控脚本
│   ├── mysql_monitoring_setup.sh      # MySQL监控配置脚本
│   ├── postgresql_monitoring_setup.sh # PostgreSQL监控配置脚本
│   ├── mongodb_monitoring_setup.sh    # MongoDB监控配置脚本
│   ├── redis_monitoring_setup.sh      # Redis监控配置脚本
│   ├── prometheus_config_generator.py # Prometheus配置生成器
│   └── grafana_dashboard_importer.py  # Grafana仪表板导入器
├── configs/                           # 配置文件
│   ├── prometheus/                    # Prometheus配置
│   ├── grafana/                       # Grafana配置
│   ├── alertmanager/                  # 告警管理配置
│   └── exporters/                     # 各种exporter配置
├── dashboards/                        # 监控仪表板
│   ├── mysql_performance.json         # MySQL性能仪表板
│   ├── postgresql_health.json         # PostgreSQL健康仪表板
│   ├── mongodb_cluster.json           # MongoDB集群仪表板
│   ├── redis_metrics.json             # Redis指标仪表板
│   └── unified_overview.json          # 统一概览仪表板
├── alerts/                            # 告警规则
│   ├── critical_alerts.yaml           # 关键告警规则
│   ├── warning_alerts.yaml            # 警告告警规则
│   ├── performance_alerts.yaml        # 性能告警规则
│   └── custom_business_alerts.yaml    # 业务定制告警
├── examples/                          # 实际案例
│   ├── performance_baselines/         # 性能基线案例
│   ├── anomaly_detection/             # 异常检测案例
│   ├── capacity_planning/             # 容量规划案例
│   └── troubleshooting_guides/        # 故障排查指南
└── docs/                              # 详细文档
    ├── monitoring_architecture.md     # 监控架构设计
    ├── metric_definitions.md          # 指标定义文档
    ├── alert_design_principles.md     # 告警设计原则
    └── best_practices.md              # 最佳实践指南
```

## 📊 企业级监控体系架构

### 监控架构设计
```yaml
# 企业级数据库监控体系架构
monitoring_architecture:
  layers:
    - data_collection:     # 数据收集层
        components:
          - database_exporters:    # 数据库exporter
            - mysqld_exporter
            - postgres_exporter
            - mongodb_exporter
            - redis_exporter
          - custom_exporters:      # 自定义exporter
            - business_metric_exporter
            - application_exporter
          - log_collectors:        # 日志收集器
            - filebeat
            - fluentd
            - promtail
    
    - data_processing:     # 数据处理层
        components:
          - prometheus:            # 指标存储和查询
            - tsdb_storage
            - rule_evaluation
            - alert_generation
          - loki:                  # 日志存储和查询
            - log_aggregation
            - log_parsing
          - alertmanager:          # 告警管理
            - routing
            - deduplication
            - notification
    
    - visualization:       # 可视化层
        components:
          - grafana:               # 仪表板展示
            - dashboard_templates
            - alert_visualization
            - drill_down_analysis
          - custom_ui:             # 定制界面
            - business_dashboards
            - executive_reports
    
    - integration:         # 集成层
        components:
          - notification_channels: # 通知渠道
            - email
            - slack
            - webhook
            - sms
          - automation_tools:      # 自动化工具
            - ansible_integration
            - terraform_modules
            - ci_cd_pipelines
```

## 🔧 核心监控技术实现

### 1. MySQL性能监控体系

```bash
#!/bin/bash
# MySQL企业级性能监控配置脚本

MONITORING_DIR="/opt/monitoring/mysql"
GRAFANA_DASHBOARD_ID=7362  # MySQL Overview dashboard

# 安装MySQL exporter
install_mysql_exporter() {
  local version="0.15.0"
  local arch=$(uname -m)
  
  echo "安装MySQL exporter $version"
  
  # 下载exporter
  wget https://github.com/prometheus/mysqld_exporter/releases/download/v${version}/mysqld_exporter-${version}.linux-${arch}.tar.gz
  tar -xf mysqld_exporter-${version}.linux-${arch}.tar.gz
  
  # 移动到系统目录
  sudo mv mysqld_exporter-${version}.linux-${arch}/mysqld_exporter /usr/local/bin/
  sudo chmod +x /usr/local/bin/mysqld_exporter
  
  # 创建监控用户
  mysql -u root -p << EOF
CREATE USER 'exporter'@'localhost' IDENTIFIED BY 'ExporterPass123!' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'localhost';
FLUSH PRIVILEGES;
EOF
}

# 配置MySQL exporter
configure_mysql_exporter() {
  echo "配置MySQL exporter"
  
  # 创建配置文件
  sudo mkdir -p $MONITORING_DIR/config
  sudo tee $MONITORING_DIR/config/my.cnf > /dev/null << EOF
[client]
user=exporter
password=ExporterPass123!
host=localhost
port=3306
EOF
  
  # 创建systemd服务
  sudo tee /etc/systemd/system/mysqld_exporter.service > /dev/null << EOF
[Unit]
Description=MySQL Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
ExecStart=/usr/local/bin/mysqld_exporter \
  --config.my-cnf=$MONITORING_DIR/config/my.cnf \
  --collect.global_status \
  --collect.global_variables \
  --collect.slave_status \
  --collect.info_schema.innodb_metrics \
  --collect.info_schema.processlist \
  --collect.info_schema.tables \
  --collect.perf_schema.tablelocks \
  --collect.perf_schema.eventsstatements \
  --collect.perf_schema.indexiowaits \
  --collect.perf_schema.tableiowaits

[Install]
WantedBy=default.target
EOF
  
  sudo systemctl daemon-reload
  sudo systemctl enable mysqld_exporter
  sudo systemctl start mysqld_exporter
}

# 配置Prometheus抓取
configure_prometheus_scraping() {
  echo "配置Prometheus抓取MySQL指标"
  
  # 添加抓取配置到prometheus.yml
  sudo tee -a /etc/prometheus/prometheus.yml > /dev/null << EOF

  - job_name: 'mysql'
    static_configs:
      - targets: ['localhost:9104']
    scrape_interval: 15s
    scrape_timeout: 10s
EOF
  
  sudo systemctl restart prometheus
}

# 导入Grafana仪表板
import_grafana_dashboard() {
  echo "导入MySQL Grafana仪表板"
  
  # 使用Grafana API导入仪表板
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${GRAFANA_API_KEY}" \
    -d @- http://localhost:3000/api/dashboards/db << EOF
{
  "dashboard": {
    "id": null,
    "title": "MySQL Performance Overview",
    "tags": ["mysql", "database", "performance"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Connection Statistics",
        "type": "graph",
        "targets": [
          {
            "expr": "mysql_global_status_threads_connected",
            "legendFormat": "Current Connections"
          },
          {
            "expr": "mysql_global_status_max_used_connections",
            "legendFormat": "Max Used Connections"
          }
        ]
      },
      {
        "title": "Query Performance",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(mysql_global_status_questions[5m])",
            "legendFormat": "Queries per Second"
          },
          {
            "expr": "rate(mysql_global_status_slow_queries[5m])",
            "legendFormat": "Slow Queries per Second"
          }
        ]
      },
      {
        "title": "Buffer Pool Usage",
        "type": "gauge",
        "targets": [
          {
            "expr": "mysql_global_status_innodb_buffer_pool_pages_free / mysql_global_status_innodb_buffer_pool_pages_total * 100",
            "legendFormat": "Buffer Pool Free %"
          }
        ]
      }
    ]
  },
  "overwrite": true
}
EOF
}

# 配置告警规则
configure_alerting_rules() {
  echo "配置MySQL告警规则"
  
  sudo tee /etc/prometheus/rules/mysql_alerts.yml > /dev/null << EOF
groups:
- name: mysql.rules
  rules:
  - alert: MySQLDown
    expr: mysql_up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "MySQL instance is down"
      description: "MySQL instance {{ \$labels.instance }} is not responding"

  - alert: HighConnectionUsage
    expr: mysql_global_status_threads_connected / mysql_global_variables_max_connections * 100 > 80
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High MySQL connection usage"
      description: "MySQL connection usage is {{ \$value }}% on {{ \$labels.instance }}"

  - alert: SlowQueryRateHigh
    expr: rate(mysql_global_status_slow_queries[5m]) > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High slow query rate"
      description: "Slow query rate is {{ \$value }} queries/sec on {{ \$labels.instance }}"
      
  - alert: BufferPoolHitRatioLow
    expr: mysql_global_status_innodb_buffer_pool_read_requests > 0 and
          (1 - mysql_global_status_innodb_buffer_pool_reads / mysql_global_status_innodb_buffer_pool_read_requests) < 0.95
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Low buffer pool hit ratio"
      description: "Buffer pool hit ratio is {{ \$value }} on {{ \$labels.instance }}"
EOF
  
  sudo systemctl restart prometheus
}

# 性能基线收集
collect_performance_baselines() {
  echo "收集群性能基线数据"
  
  local baseline_dir="/var/lib/mysql/baselines"
  mkdir -p $baseline_dir
  
  # 收集关键性能指标
  mysql -u exporter -pExporterPass123! << EOF > $baseline_dir/performance_baseline_$(date +%Y%m%d).sql
-- 性能基线数据收集
SELECT 
  'connection_stats' as metric_type,
  VARIABLE_VALUE as current_connections
FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
WHERE VARIABLE_NAME = 'Threads_connected';

SELECT 
  'query_stats' as metric_type,
  VARIABLE_VALUE as questions_per_second
FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
WHERE VARIABLE_NAME = 'Questions';

SELECT 
  'buffer_pool_stats' as metric_type,
  VARIABLE_VALUE as buffer_pool_pages_free
FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
WHERE VARIABLE_NAME = 'Innodb_buffer_pool_pages_free';
EOF
}

# 主执行函数
main() {
  case "$1" in
    install)
      install_mysql_exporter
      configure_mysql_exporter
      configure_prometheus_scraping
      import_grafana_dashboard
      configure_alerting_rules
      collect_performance_baselines
      echo "MySQL监控配置完成"
      ;;
    update-baselines)
      collect_performance_baselines
      echo "性能基线更新完成"
      ;;
    *)
      echo "Usage: $0 {install|update-baselines}"
      exit 1
      ;;
  esac
}

main "$@"
```

### 2. PostgreSQL监控体系

```python
#!/usr/bin/env python3
"""
PostgreSQL企业级监控配置管理器
"""

import yaml
import json
import requests
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

class PostgreSQLMonitor:
    """PostgreSQL监控管理器"""
    
    def __init__(self, config_file: str = "/etc/postgresql_monitor.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        self.exporter_port = 9187
    
    def load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            'database_connections': ['localhost:5432'],
            'monitoring_user': 'pg_monitor',
            'grafana_dashboard_id': 9628,
            'alert_thresholds': {
                'connections': 80,  # 连接使用率阈值
                'slow_queries': 5,   # 慢查询阈值
                'cache_hit_ratio': 95 # 缓存命中率阈值
            }
        }
        
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return default_config
    
    def install_postgres_exporter(self):
        """安装PostgreSQL exporter"""
        print("安装PostgreSQL exporter...")
        
        # 创建监控用户和权限
        setup_sql = """
        CREATE USER pg_monitor WITH PASSWORD 'MonitorPass123!';
        
        -- 授予必要的监控权限
        GRANT pg_monitor TO pg_monitor;
        GRANT SELECT ON pg_stat_database TO pg_monitor;
        GRANT SELECT ON pg_stat_user_tables TO pg_monitor;
        GRANT SELECT ON pg_stat_user_indexes TO pg_monitor;
        GRANT SELECT ON pg_statio_user_tables TO pg_monitor;
        
        -- 创建扩展（如果不存在）
        CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
        """
        
        subprocess.run([
            'psql', '-U', 'postgres', '-c', setup_sql
        ], check=True)
        
        # 下载并安装exporter
        subprocess.run([
            'wget', 'https://github.com/prometheus-community/postgres_exporter/releases/download/v0.12.0/postgres_exporter-0.12.0.linux-amd64.tar.gz'
        ])
        subprocess.run(['tar', '-xf', 'postgres_exporter-0.12.0.linux-amd64.tar.gz'])
        subprocess.run(['sudo', 'mv', 'postgres_exporter-0.12.0.linux-amd64/postgres_exporter', '/usr/local/bin/'])
        
        # 配置环境变量
        env_content = f"DATA_SOURCE_NAME=postgresql://pg_monitor:MonitorPass123!@localhost:5432/postgres?sslmode=disable"
        with open('/etc/postgres_exporter.env', 'w') as f:
            f.write(env_content)
    
    def configure_prometheus(self):
        """配置Prometheus抓取"""
        prometheus_config = {
            'scrape_configs': [{
                'job_name': 'postgresql',
                'static_configs': [{
                    'targets': [f'localhost:{self.exporter_port}']
                }],
                'scrape_interval': '15s',
                'scrape_timeout': '10s'
            }]
        }
        
        # 更新Prometheus配置
        config_path = '/etc/prometheus/prometheus.yml'
        with open(config_path, 'r') as f:
            current_config = yaml.safe_load(f)
        
        current_config['scrape_configs'].append(prometheus_config['scrape_configs'][0])
        
        with open(config_path, 'w') as f:
            yaml.dump(current_config, f)
        
        subprocess.run(['systemctl', 'restart', 'prometheus'])
    
    def create_grafana_dashboard(self):
        """创建Grafana仪表板"""
        dashboard_config = {
            'dashboard': {
                'title': 'PostgreSQL Performance Dashboard',
                'tags': ['postgresql', 'database', 'performance'],
                'panels': [
                    {
                        'title': 'Connection Statistics',
                        'type': 'graph',
                        'targets': [
                            {'expr': 'pg_stat_database_numbackends', 'legendFormat': '{{datname}} connections'},
                            {'expr': 'pg_settings_max_connections', 'legendFormat': 'Max connections'}
                        ]
                    },
                    {
                        'title': 'Cache Hit Ratio',
                        'type': 'gauge',
                        'targets': [
                            {'expr': 'pg_stat_database_blks_hit / (pg_stat_database_blks_hit + pg_stat_database_blks_read) * 100'}
                        ]
                    },
                    {
                        'title': 'Slow Queries',
                        'type': 'graph',
                        'targets': [
                            {'expr': 'rate(pg_stat_statements_mean_time_seconds[5m])', 'legendFormat': 'Avg query time'},
                            {'expr': 'rate(pg_stat_statements_calls[5m])', 'legendFormat': 'Query rate'}
                        ]
                    }
                ]
            }
        }
        
        # 调用Grafana API
        response = requests.post(
            'http://localhost:3000/api/dashboards/db',
            headers={
                'Authorization': f'Bearer {self.config.get("grafana_api_key")}',
                'Content-Type': 'application/json'
            },
            json=dashboard_config
        )
        
        return response.status_code == 200
    
    def setup_alerting_rules(self):
        """配置告警规则"""
        alert_rules = {
            'groups': [{
                'name': 'postgresql.rules',
                'rules': [
                    {
                        'alert': 'PostgreSQLDown',
                        'expr': 'pg_up == 0',
                        'for': '1m',
                        'labels': {'severity': 'critical'},
                        'annotations': {
                            'summary': 'PostgreSQL instance is down',
                            'description': 'PostgreSQL instance {{ $labels.instance }} is not responding'
                        }
                    },
                    {
                        'alert': 'HighConnectionUsage',
                        'expr': 'pg_stat_database_numbackends / pg_settings_max_connections * 100 > 80',
                        'for': '2m',
                        'labels': {'severity': 'warning'},
                        'annotations': {
                            'summary': 'High PostgreSQL connection usage',
                            'description': 'Connection usage is {{ $value }}% on {{ $labels.instance }}'
                        }
                    }
                ]
            }]
        }
        
        with open('/etc/prometheus/rules/postgresql_alerts.yml', 'w') as f:
            yaml.dump(alert_rules, f)
        
        subprocess.run(['systemctl', 'restart', 'prometheus'])

# 使用示例
def main():
    monitor = PostgreSQLMonitor()
    monitor.install_postgres_exporter()
    monitor.configure_prometheus()
    monitor.create_grafana_dashboard()
    monitor.setup_alerting_rules()
    print("PostgreSQL监控配置完成")

if __name__ == "__main__":
    main()
```

### 3. MongoDB监控体系

```javascript
// MongoDB企业级监控配置脚本

// 监控配置参数
const MONITORING_CONFIG = {
  exporterPort: 9216,
  grafanaDashboardId: 2583,
  alertThresholds: {
    connections: 80,
    memoryUsage: 85,
    replicationLag: 10, // seconds
    queryLatency: 100   // milliseconds
  }
};

// 安装MongoDB exporter
function installMongoDBExporter() {
  console.log("安装MongoDB exporter...");
  
  // 创建监控用户
  db.getSiblingDB("admin").createUser({
    user: "monitor",
    pwd: "${DB_PASSWORD}",
    roles: [
      { role: "clusterMonitor", db: "admin" },
      { role: "read", db: "local" }
    ]
  });
  
  // 下载并安装exporter
  const installCmd = `
    wget https://github.com/percona/mongodb_exporter/releases/download/v0.37.0/mongodb_exporter-0.37.0.linux-amd64.tar.gz
    tar -xf mongodb_exporter-0.37.0.linux-amd64.tar.gz
    sudo mv mongodb_exporter-0.37.0.linux-amd64/mongodb_exporter /usr/local/bin/
    sudo chmod +x /usr/local/bin/mongodb_exporter
  `;
  
  exec(installCmd);
}

// 配置MongoDB exporter服务
function configureExporterService() {
  console.log("配置MongoDB exporter服务...");
  
  const serviceConfig = `
[Unit]
Description=MongoDB Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Environment="MONGODB_URI=mongodb://monitor:MonitorPass456!@localhost:27017/admin"
ExecStart=/usr/local/bin/mongodb_exporter --collect.collection --collect.database --collect.indexusage --collect.topmetrics

[Install]
WantedBy=default.target
  `;
  
  fs.writeFileSync('/etc/systemd/system/mongodb_exporter.service', serviceConfig);
  
  // 启动服务
  exec('systemctl daemon-reload');
  exec('systemctl enable mongodb_exporter');
  exec('systemctl start mongodb_exporter');
}

// 配置Prometheus抓取
function configurePrometheusScraping() {
  console.log("配置Prometheus抓取MongoDB指标...");
  
  const prometheusConfig = {
    scrape_configs: [{
      job_name: 'mongodb',
      static_configs: [{
        targets: [`localhost:${MONITORING_CONFIG.exporterPort}`]
      }],
      scrape_interval: '15s',
      scrape_timeout: '10s'
    }]
  };
  
  // 更新Prometheus配置文件
  const currentConfig = yaml.load(fs.readFileSync('/etc/prometheus/prometheus.yml'));
  currentConfig.scrape_configs.push(prometheusConfig.scrape_configs[0]);
  fs.writeFileSync('/etc/prometheus/prometheus.yml', yaml.dump(currentConfig));
  
  exec('systemctl restart prometheus');
}

// 创建Grafana仪表板
function createGrafanaDashboard() {
  console.log("创建MongoDB Grafana仪表板...");
  
  const dashboard = {
    dashboard: {
      title: "MongoDB Cluster Performance",
      tags: ["mongodb", "database", "cluster"],
      panels: [
        {
          title: "Cluster Status",
          type: "stat",
          targets: [
            { expr: "mongodb_up", legendFormat: "Cluster Status" }
          ]
        },
        {
          title: "Operations Rate",
          type: "graph",
          targets: [
            { expr: "rate(mongodb_ss_opcounters_insert[5m])", legendFormat: "Inserts" },
            { expr: "rate(mongodb_ss_opcounters_query[5m])", legendFormat: "Queries" },
            { expr: "rate(mongodb_ss_opcounters_update[5m])", legendFormat: "Updates" }
          ]
        },
        {
          title: "Memory Usage",
          type: "gauge",
          targets: [
            { expr: "mongodb_ss_mem_resident / 1024 / 1024", legendFormat: "Resident Memory (MB)" }
          ]
        }
      ]
    }
  };
  
  // 调用Grafana API
  const response = http.post('http://localhost:3000/api/dashboards/db', {
    headers: {
      'Authorization': `Bearer ${process.env.GRAFANA_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dashboard)
  });
  
  return response.statusCode === 200;
}

// 配置告警规则
function setupAlertingRules() {
  console.log("配置MongoDB告警规则...");
  
  const alertRules = {
    groups: [{
      name: "mongodb.rules",
      rules: [
        {
          alert: "MongoDBDown",
          expr: "mongodb_up == 0",
          for: "1m",
          labels: { severity: "critical" },
          annotations: {
            summary: "MongoDB instance is down",
            description: "MongoDB instance {{ $labels.instance }} is not responding"
          }
        },
        {
          alert: "HighConnectionUsage",
          expr: "mongodb_ss_connections_current / mongodb_ss_connections_available * 100 > 80",
          for: "2m",
          labels: { severity: "warning" },
          annotations: {
            summary: "High MongoDB connection usage",
            description: "Connection usage is {{ $value }}% on {{ $labels.instance }}"
          }
        }
      ]
    }]
  };
  
  fs.writeFileSync('/etc/prometheus/rules/mongodb_alerts.yml', yaml.dump(alertRules));
  exec('systemctl restart prometheus');
}

// 执行监控配置
function setupMongoDBMonitoring() {
  installMongoDBExporter();
  configureExporterService();
  configurePrometheusScraping();
  createGrafanaDashboard();
  setupAlertingRules();
  
  console.log("MongoDB监控配置完成");
}

// 运行配置
setupMongoDBMonitoring();
```

### 4. Redis监控体系

```bash
#!/bin/bash
# Redis企业级监控配置脚本

REDIS_EXPORTER_VERSION="1.52.0"
EXPORTER_PORT=9121
GRAFANA_DASHBOARD_ID=763

# 安装Redis exporter
install_redis_exporter() {
  echo "安装Redis exporter $REDIS_EXPORTER_VERSION"
  
  wget https://github.com/oliver006/redis_exporter/releases/download/v${REDIS_EXPORTER_VERSION}/redis_exporter-v${REDIS_EXPORTER_VERSION}.linux-amd64.tar.gz
  tar -xf redis_exporter-v${REDIS_EXPORTER_VERSION}.linux-amd64.tar.gz
  
  sudo mv redis_exporter-v${REDIS_EXPORTER_VERSION}.linux-amd64/redis_exporter /usr/local/bin/
  sudo chmod +x /usr/local/bin/redis_exporter
}

# 配置Redis exporter服务
configure_redis_exporter() {
  echo "配置Redis exporter服务"
  
  sudo tee /etc/systemd/system/redis_exporter.service > /dev/null << EOF
[Unit]
Description=Redis Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Environment="REDIS_ADDR=redis://localhost:6379"
Environment="redis_password: "${DB_PASSWORD}"配置Prometheus抓取Redis指标"
  
  sudo tee -a /etc/prometheus/prometheus.yml > /dev/null << EOF

  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:${EXPORTER_PORT}']
    scrape_interval: 15s
    scrape_timeout: 10s
EOF
  
  sudo systemctl restart prometheus
}

# 创建Redis监控仪表板
create_redis_dashboard() {
  echo "创建Redis Grafana仪表板"
  
  local dashboard_json=$(cat << EOF
{
  "dashboard": {
    "title": "Redis Performance Dashboard",
    "tags": ["redis", "cache", "performance"],
    "panels": [
      {
        "title": "Redis Status",
        "type": "stat",
        "targets": [
          { "expr": "redis_up", "legendFormat": "Redis Status" }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "gauge",
        "targets": [
          { "expr": "redis_memory_used_bytes / redis_memory_max_bytes * 100", "legendFormat": "Memory Usage %" }
        ]
      },
      {
        "title": "Commands Processed",
        "type": "graph",
        "targets": [
          { "expr": "rate(redis_commands_processed_total[5m])", "legendFormat": "Commands/sec" }
        ]
      },
      {
        "title": "Connected Clients",
        "type": "graph",
        "targets": [
          { "expr": "redis_connected_clients", "legendFormat": "Connected Clients" }
        ]
      },
      {
        "title": "Hit Ratio",
        "type": "gauge",
        "targets": [
          { "expr": "redis_keyspace_hits_total / (redis_keyspace_hits_total + redis_keyspace_misses_total) * 100", "legendFormat": "Hit Ratio %" }
        ]
      }
    ]
  }
}
EOF
)
  
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${GRAFANA_API_KEY}" \
    -d "$dashboard_json" \
    http://localhost:3000/api/dashboards/db
}

# 配置Redis告警规则
configure_redis_alerts() {
  echo "配置Redis告警规则"
  
  sudo tee /etc/prometheus/rules/redis_alerts.yml > /dev/null << EOF
groups:
- name: redis.rules
  rules:
  - alert: RedisDown
    expr: redis_up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Redis instance is down"
      description: "Redis instance {{ \$labels.instance }} is not responding"

  - alert: HighMemoryUsage
    expr: redis_memory_used_bytes / redis_memory_max_bytes * 100 > 90
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High Redis memory usage"
      description: "Redis memory usage is {{ \$value }}% on {{ \$labels.instance }}"

  - alert: LowHitRatio
    expr: redis_keyspace_hits_total > 0 and 
          redis_keyspace_misses_total > 0 and
          (redis_keyspace_hits_total / (redis_keyspace_hits_total + redis_keyspace_misses_total)) < 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Low Redis hit ratio"
      description: "Redis hit ratio is {{ \$value }} on {{ \$labels.instance }}"
      
  - alert: HighConnectedClients
    expr: redis_connected_clients > 1000
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "High Redis connected clients"
      description: "Redis has {{ \$value }} connected clients on {{ \$labels.instance }}"
EOF
  
  sudo systemctl restart prometheus
}

# Redis性能基准测试
run_redis_benchmark() {
  echo "执行Redis性能基准测试"
  
  local benchmark_results="/var/log/redis/benchmark_$(date +%Y%m%d_%H%M%S).txt"
  
  # 执行基准测试
  redis-benchmark -h localhost -p 6379 -n 100000 -c 50 -t get,set,lpush,lpop -q > "$benchmark_results"
  
  echo "基准测试结果已保存: $benchmark_results"
  
  # 解析结果并记录到监控系统
  local get_ops=$(grep "GET" "$benchmark_results" | awk '{print $2}')
  local set_ops=$(grep "SET" "$benchmark_results" | awk '{print $2}')
  
  echo "GET操作性能: $get_ops ops/sec"
  echo "SET操作性能: $set_ops ops/sec"
}

# 主执行函数
main() {
  case "$1" in
    install)
      install_redis_exporter
      configure_redis_exporter
      configure_prometheus_redis
      create_redis_dashboard
      configure_redis_alerts
      run_redis_benchmark
      echo "Redis监控配置完成"
      ;;
    benchmark)
      run_redis_benchmark
      ;;
    *)
      echo "Usage: $0 {install|benchmark}"
      exit 1
      ;;
  esac
}

main "$@"
```

## 🎯 统一监控平台

### 监控编排管理器
```python
#!/usr/bin/env python3
"""
企业级统一监控平台编排器
支持多数据库监控的一体化管理
"""

import asyncio
import json
import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DatabaseMonitorConfig:
    """数据库监控配置"""
    database_type: str
    host: str
    port: int
    exporter_port: int
    dashboard_id: int
    enabled: bool = True

class UnifiedMonitoringPlatform:
    """统一监控平台管理器"""
    
    def __init__(self, config_file: str = "/etc/unified_monitoring.yaml"):
        self.config_file = config_file
        self.databases = []
        self.load_configuration()
    
    def load_configuration(self):
        """加载监控配置"""
        default_config = {
            'databases': [
                {
                    'database_type': 'mysql',
                    'host': 'localhost',
                    'port': 3306,
                    'exporter_port': 9104,
                    'dashboard_id': 7362,
                    'enabled': True
                },
                {
                    'database_type': 'postgresql',
                    'host': 'localhost',
                    'port': 5432,
                    'exporter_port': 9187,
                    'dashboard_id': 9628,
                    'enabled': True
                },
                {
                    'database_type': 'mongodb',
                    'host': 'localhost',
                    'port': 27017,
                    'exporter_port': 9216,
                    'dashboard_id': 2583,
                    'enabled': True
                },
                {
                    'database_type': 'redis',
                    'host': 'localhost',
                    'port': 6379,
                    'exporter_port': 9121,
                    'dashboard_id': 763,
                    'enabled': True
                }
            ]
        }
        
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
                self.databases = [DatabaseMonitorConfig(**db) for db in config.get('databases', [])]
        except FileNotFoundError:
            self.databases = [DatabaseMonitorConfig(**db) for db in default_config['databases']]
    
    async def deploy_monitoring_stack(self):
        """部署监控栈"""
        print("开始部署统一监控栈...")
        
        tasks = []
        for db_config in self.databases:
            if db_config.enabled:
                task = self.deploy_database_monitoring(db_config)
                tasks.append(task)
        
        await asyncio.gather(*tasks)
        print("监控栈部署完成")
    
    async def deploy_database_monitoring(self, config: DatabaseMonitorConfig):
        """部署单个数据库监控"""
        print(f"部署{config.database_type}监控...")
        
        # 根据数据库类型执行相应脚本
        script_map = {
            'mysql': './scripts/mysql_monitoring_setup.sh',
            'postgresql': './scripts/postgresql_monitoring_setup.sh',
            'mongodb': './scripts/mongodb_monitoring_setup.sh',
            'redis': './scripts/redis_monitoring_setup.sh'
        }
        
        script_path = script_map.get(config.database_type)
        if script_path:
            import subprocess
            result = subprocess.run([script_path, 'install'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{config.database_type}监控部署成功")
            else:
                print(f"{config.database_type}监控部署失败: {result.stderr}")
    
    def generate_unified_dashboard(self):
        """生成统一监控仪表板"""
        print("生成统一监控仪表板...")
        
        unified_dashboard = {
            'dashboard': {
                'title': 'Unified Database Performance Overview',
                'tags': ['unified', 'database', 'performance'],
                'panels': []
            }
        }
        
        # 为每个数据库添加概览面板
        panel_id = 1
        for db_config in self.databases:
            if db_config.enabled:
                panel = {
                    'id': panel_id,
                    'title': f'{db_config.database_type.upper()} Overview',
                    'type': 'graph',
                    'gridPos': {'x': ((panel_id-1) % 2) * 12, 'y': ((panel_id-1) // 2) * 8, 'w': 12, 'h': 8},
                    'targets': [
                        {
                            'expr': f'{db_config.database_type}_up',
                            'legendFormat': f'{db_config.database_type} Status'
                        }
                    ]
                }
                unified_dashboard['dashboard']['panels'].append(panel)
                panel_id += 1
        
        # 调用Grafana API创建仪表板
        import requests
        response = requests.post(
            'http://localhost:3000/api/dashboards/db',
            headers={
                'Authorization': f'Bearer {self.get_grafana_api_key()}',
                'Content-Type': 'application/json'
            },
            json=unified_dashboard
        )
        
        return response.status_code == 200
    
    def get_grafana_api_key(self) -> str:
        """获取Grafana API密钥"""
        # 从配置文件或环境变量获取API密钥
        return "your_grafana_api_key_here"
    
    def health_check(self):
        """健康检查"""
        print("执行监控系统健康检查...")
        
        import subprocess
        services = ['prometheus', 'grafana-server', 'alertmanager']
        
        for service in services:
            result = subprocess.run(['systemctl', 'is-active', service], capture_output=True, text=True)
            if result.stdout.strip() == 'active':
                print(f"✅ {service} 运行正常")
            else:
                print(f"❌ {service} 运行异常")

# 使用示例
async def main():
    platform = UnifiedMonitoringPlatform()
    await platform.deploy_monitoring_stack()
    platform.generate_unified_dashboard()
    platform.health_check()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🧪 监控验证测试

### 自动化监控测试套件
```bash
#!/bin/bash
# 数据库监控验证测试套件

TEST_RESULTS=()

# Prometheus连接测试
test_prometheus_connection() {
  echo "=== Prometheus连接测试 ==="
  
  local prometheus_url="http://localhost:9090"
  local response=$(curl -s -o /dev/null -w "%{http_code}" $prometheus_url/-/healthy)
  
  if [ "$response" = "200" ]; then
    TEST_RESULTS+=("Prometheus连接测试: 通过")
    echo "✅ Prometheus服务正常"
  else
    TEST_RESULTS+=("Prometheus连接测试: 失败")
    echo "❌ Prometheus服务异常"
  fi
}

# Grafana连接测试
test_grafana_connection() {
  echo "=== Grafana连接测试 ==="
  
  local grafana_url="http://localhost:3000"
  local response=$(curl -s -o /dev/null -w "%{http_code}" $grafana_url/api/health)
  
  if [ "$response" = "200" ]; then
    TEST_RESULTS+=("Grafana连接测试: 通过")
    echo "✅ Grafana服务正常"
  else
    TEST_RESULTS+=("Grafana连接测试: 失败")
    echo "❌ Grafana服务异常"
  fi
}

# 数据库Exporter测试
test_database_exporters() {
  echo "=== 数据库Exporter测试 ==="
  
  local exporters=(
    "mysql:http://localhost:9104/metrics"
    "postgresql:http://localhost:9187/metrics"
    "mongodb:http://localhost:9216/metrics"
    "redis:http://localhost:9121/metrics"
  )
  
  for exporter in "${exporters[@]}"; do
    local name=$(echo $exporter | cut -d: -f1)
    local url=$(echo $exporter | cut -d: -f2-)
    
    local response=$(curl -s -o /dev/null -w "%{http_code}" $url)
    if [ "$response" = "200" ]; then
      TEST_RESULTS+=("${name} Exporter测试: 通过")
      echo "✅ ${name} Exporter正常"
    else
      TEST_RESULTS+=("${name} Exporter测试: 失败")
      echo "❌ ${name} Exporter异常"
    fi
  done
}

# 告警规则测试
test_alerting_rules() {
  echo "=== 告警规则测试 ==="
  
  # 检查告警规则文件
  local rule_files=(
    "/etc/prometheus/rules/mysql_alerts.yml"
    "/etc/prometheus/rules/postgresql_alerts.yml"
    "/etc/prometheus/rules/mongodb_alerts.yml"
    "/etc/prometheus/rules/redis_alerts.yml"
  )
  
  for rule_file in "${rule_files[@]}"; do
    if [ -f "$rule_file" ]; then
      TEST_RESULTS+=("$(basename $rule_file) 存在性测试: 通过")
      echo "✅ $(basename $rule_file) 存在"
    else
      TEST_RESULTS+=("$(basename $rule_file) 存在性测试: 失败")
      echo "❌ $(basename $rule_file) 不存在"
    fi
  done
}

# 仪表板测试
test_grafana_dashboards() {
  echo "=== Grafana仪表板测试 ==="
  
  # 检查默认仪表板是否存在
  local dashboard_check=$(curl -s -H "Authorization: Bearer ${GRAFANA_API_KEY}" \
    "http://localhost:3000/api/search?query=MySQL" | jq '. | length')
  
  if [ "$dashboard_check" -gt 0 ]; then
    TEST_RESULTS+=("Grafana仪表板测试: 通过")
    echo "✅ Grafana仪表板存在"
  else
    TEST_RESULTS+=("Grafana仪表板测试: 失败")
    echo "❌ Grafana仪表板不存在"
  fi
}

# 生成测试报告
generate_monitoring_test_report() {
  echo "=== 监控系统测试综合报告 ==="
  
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
  local report_file="/tmp/monitoring_test_report_$(date +%Y%m%d_%H%M%S).txt"
  printf "%s\n" "${TEST_RESULTS[@]}" > "$report_file"
  echo "详细报告已保存: $report_file"
}

# 执行所有测试
test_prometheus_connection
test_grafana_connection
test_database_exporters
test_alerting_rules
test_grafana_dashboards
generate_monitoring_test_report
```

## 📚 最佳实践总结

### 监控体系设计原则
1. **全面覆盖**: 监控所有关键组件和指标
2. **分层告警**: 设置不同级别的告警阈值
3. **可视化友好**: 提供直观的仪表板和图表
4. **自动化响应**: 配置自动化的故障响应机制
5. **历史追溯**: 保留足够的历史数据用于分析
6. **性能影响最小**: 监控系统本身不应影响被监控系统性能

### 关键监控指标
- **可用性指标**: uptime、连接状态、服务健康检查
- **性能指标**: 响应时间、吞吐量、资源利用率
- **容量指标**: 存储使用率、连接数、缓存命中率
- **业务指标**: 交易成功率、用户响应时间、错误率

### 告警设计原则
- **避免告警疲劳**: 合理设置告警阈值和频率
- **分级处理**: critical/warning/info三级告警
- **上下文信息**: 提供足够的故障诊断信息
- **自动化处理**: 可自动恢复的问题配置自动处理

---
> **💡 提示**: 监控不是一次性工作，需要根据业务发展和系统变化持续优化调整监控策略和告警规则。