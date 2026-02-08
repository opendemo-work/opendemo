# Monitoring CLI命令详解

本文档详细解释监控系统常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. Prometheus管理命令

### 用途
Prometheus是CNCF孵化的开源系统监控和告警工具包，采用拉取模式收集时间序列数据，提供强大的查询语言PromQL和灵活的告警机制。

### 输出示例
```bash
# 启动Prometheus
$ prometheus --config.file=prometheus.yml --storage.tsdb.path=/data/prometheus --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries
level=info ts=2024-01-15T10:30:45.123Z caller=main.go:432 msg="Starting Prometheus" version="(version=2.40.0, branch=HEAD, revision=xxxxxx)"
level=info ts=2024-01-15T10:30:45.124Z caller=main.go:437 build_context="(go=go1.19.3, user=root@xxxxxx, date=20221122-14:56:00)"
level=info ts=2024-01-15T10:30:45.125Z caller=main.go:438 host_details="(Linux 5.15.0-56-generic #62-Ubuntu SMP Tue Nov 22 19:54:14 UTC 2022 x86_64 xxxx (none))"
level=info ts=2024-01-15T10:30:45.126Z caller=main.go:439 fd_limits="(soft=1048576, hard=1048576)"
level=info ts=2024-01-15T10:30:45.127Z caller=main.go:440 vm_limits="(soft=unlimited, hard=unlimited)"
level=info ts=2024-01-15T10:30:45.128Z caller=web.go:541 component=web msg="Start listening for connections" address=0.0.0.0:9090
level=info ts=2024-01-15T10:30:45.129Z caller=main.go:805 msg="Starting TSDB ..."
level=info ts=2024-01-15T10:30:45.130Z caller=main.go:821 msg="TSDB started"

# 检查Prometheus健康状态
$ curl http://localhost:9090/-/healthy
Prometheus is Healthy.

# 检查Prometheus就绪状态
$ curl http://localhost:9090/-/ready
Prometheus is Ready.

# 查看Targets状态
$ curl "http://localhost:9090/api/v1/targets" | jq '.data.activeTargets[] | {job: .labels.job, instance: .labels.instance, health: .health, lastScrape: .lastScrape}'
[
  {
    "job": "prometheus",
    "instance": "localhost:9090",
    "health": "up",
    "lastScrape": "2024-01-15T10:30:45.123Z"
  },
  {
    "job": "node",
    "instance": "localhost:9100",
    "health": "up",
    "lastScrape": "2024-01-15T10:30:42.456Z"
  }
]

# 执行PromQL查询
$ curl "http://localhost:9090/api/v1/query?query=up" | jq '.'
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "up",
          "instance": "localhost:9090",
          "job": "prometheus"
        },
        "value": [
          1705315845.123,
          "1"
        ]
      },
      {
        "metric": {
          "__name__": "up",
          "instance": "localhost:9100",
          "job": "node"
        },
        "value": [
          1705315845.123,
          "1"
        ]
      }
    ]
  }
}

# 查看告警状态
$ curl "http://localhost:9090/api/v1/alerts" | jq '.data.alerts[]'
{
  "labels": {
    "alertname": "HighCPUUsage",
    "severity": "warning"
  },
  "annotations": {
    "summary": "High CPU usage detected",
    "description": "CPU usage is above 80% for more than 5 minutes"
  },
  "state": "firing",
  "activeAt": "2024-01-15T10:25:30.123Z",
  "value": "85.67"
}
```

### 内容解析
- **启动信息**: 显示版本、构建信息、主机详情、文件描述符限制等
- **健康检查**: 返回简单的健康状态信息
- **Targets状态**: 显示监控目标的健康状况、最后抓取时间
- **查询结果**: 包含指标名称、标签、时间戳和值
- **告警信息**: 显示触发的告警及其状态和值

### 常用参数详解
- `--config.file`: 指定配置文件路径
- `--storage.tsdb.path`: 指定TSDB存储路径
- `--web.listen-address`: 指定监听地址和端口
- `--web.external-url`: 指定外部访问URL
- `--storage.tsdb.retention.time`: 数据保留时间

### 注意事项
- 确保配置文件语法正确
- 监控目标应保持可达性
- 合理设置数据保留策略
- 定期检查TSDB健康状态

### 生产安全风险
- ⚠️ 默认端口9090可能暴露敏感信息
- ⚠️ 未配置认证和授权机制
- ⚠️ 查询可能消耗大量系统资源
- ✅ 建议启用基本认证和TLS加密

---

## 2. Grafana管理命令

### 用途
Grafana是开源的可视化和分析平台，支持多种数据源，提供丰富的仪表板功能，是监控数据展示的首选工具。

### 输出示例
```bash
# 启动Grafana
$ systemctl start grafana-server
$ journalctl -u grafana-server -f
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Starting Grafana" logger=server version=9.3.2 commit=xxxxxx branch=HEAD compiled=2022-12-15T10:30:45Z
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Config loaded from" logger=settings file=/usr/share/grafana/conf/defaults.ini
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Config loaded from" logger=settings file=/etc/grafana/grafana.ini
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Path Home" logger=settings path=/usr/share/grafana
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Path Data" logger=settings path=/var/lib/grafana
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Path Logs" logger=settings path=/var/log/grafana
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Path Plugins" logger=settings path=/var/lib/grafana/plugins
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Path Provisioning" logger=settings path=/etc/grafana/provisioning
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="App mode production" logger=settings
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Connecting to DB" logger=sqlstore dbtype=sqlite3
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Starting DB migrations" logger=migrator
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="Starting plugin search" logger=plugins
Jan 15 10:30:45 server grafana-server[12345]: t=2024-01-15T10:30:45+0000 lvl=info msg="HTTP Server Listen" logger=http_server address=[::]:3000 protocol=http subUrl= socket=

# 检查Grafana健康状态
$ curl http://admin:admin@localhost:3000/api/health
{
  "commit": "xxxxxx",
  "database": "ok",
  "version": "9.3.2"
}

# 添加数据源
$ curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46YWRtaW4=" \
  -d '{
    "name":"Prometheus",
    "type":"prometheus",
    "url":"http://localhost:9090",
    "access":"proxy",
    "basicAuth":false,
    "isDefault":true
  }' \
  http://localhost:3000/api/datasources
{
  "datasource": {
    "id": 1,
    "uid": "xxxxxx",
    "orgId": 1,
    "name": "Prometheus",
    "type": "prometheus",
    "typeName": "Prometheus",
    "typeLogoUrl": "public/app/plugins/datasource/prometheus/img/prometheus_logo.svg",
    "access": "proxy",
    "url": "http://localhost:9090",
    "password": "",
    "user": "",
    "database": "",
    "basicAuth": false,
    "isDefault": true,
    "jsonData": {},
    "readOnly": false
  },
  "id": 1,
  "message": "Datasource added",
  "name": "Prometheus"
}

# 创建仪表板
$ curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Basic YWRtaW46YWRtaW4=" \
  -d @dashboard.json \
  http://localhost:3000/api/dashboards/db
{
  "id": 1,
  "slug": "system-monitoring",
  "status": "success",
  "uid": "xxxxxx",
  "url": "/d/xxxxxx/system-monitoring",
  "version": 1
}

# 导出仪表板
$ curl -H "Authorization: Basic YWRtaW46YWRtaW4=" \
  http://localhost:3000/api/dashboards/uid/xxxxxx > exported_dashboard.json

# 查看用户列表
$ curl -H "Authorization: Basic YWRtaW46YWRtaW4=" \
  http://localhost:3000/api/users
[
  {
    "id": 1,
    "name": "Admin",
    "login": "admin",
    "email": "admin@localhost",
    "isAdmin": true,
    "isDisabled": false,
    "lastSeenAt": "2024-01-15T10:30:45Z",
    "lastSeenAtAge": "< 1m"
  }
]
```

### 内容解析
- **启动日志**: 显示配置加载、路径设置、数据库连接等信息
- **健康检查**: 返回版本信息和数据库状态
- **数据源响应**: 包含数据源ID、UID、配置信息
- **仪表板操作**: 返回创建的仪表板ID、URL等信息
- **用户管理**: 显示用户基本信息和权限状态

### 常用参数详解
- `-H "Authorization: Basic"`: 基本认证头部
- `-H "Content-Type: application/json"`: JSON内容类型
- `isDefault`: 设置为默认数据源
- `access`: 访问模式(proxy/direct)

### 注意事项
- 首次登录后应立即修改默认密码
- 生产环境建议使用LDAP或OAuth认证
- 定期备份仪表板配置
- 控制用户权限分配

### 生产安全风险
- ⚠️ 默认凭据存在安全风险
- ⚠️ 未限制匿名访问可能导致信息泄露
- ⚠️ 插件可能引入安全漏洞
- ✅ 建议启用认证、配置防火墙规则

---

## 3. Elasticsearch管理命令

### 用途
Elasticsearch是基于Lucene的分布式搜索引擎，提供RESTful API，支持全文检索、结构化搜索、分析等，是ELK栈的核心组件。

### 输出示例
```bash
# 启动Elasticsearch
$ systemctl start elasticsearch
$ journalctl -u elasticsearch -f
[2024-01-15T10:30:45,123][INFO ][o.e.n.Node               ] [node-1] starting ...
[2024-01-15T10:30:45,234][INFO ][o.e.t.TransportService   ] [node-1] publish_address {192.168.1.100:9300}, bound_addresses {[::]:9300}
[2024-01-15T10:30:45,345][INFO ][o.e.c.s.MasterService    ] [node-1] elected-as-master ([1] nodes joined)[{node-1}{xxxxxx}{xxxxxx}{192.168.1.100}{192.168.1.100:9300}{cdfhilmrstw}{ml.machine_memory=8329453568, xpack.installed=true, transform.node=true}]
[2024-01-15T10:30:45,456][INFO ][o.e.c.s.ClusterApplierService] [node-1] master node changed {previous [], current [{node-1}{xxxxxx}{xxxxxx}{192.168.1.100}{192.168.1.100:9300}{cdfhilmrstw}{ml.machine_memory=8329453568, xpack.installed=true, transform.node=true}]}
[2024-01-15T10:30:45,567][INFO ][o.e.h.AbstractHttpServerTransport] [node-1] publish_address {192.168.1.100:9200}, bound_addresses {[::]:9200}
[2024-01-15T10:30:45,678][INFO ][o.e.n.Node               ] [node-1] started

# 检查集群健康状态
$ curl -X GET "localhost:9200/_cluster/health?pretty"
{
  "cluster_name" : "elasticsearch",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 5,
  "active_shards" : 5,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

# 查看节点信息
$ curl -X GET "localhost:9200/_nodes/stats?pretty" | jq '.nodes[].name, .nodes[].host, .nodes[].roles'
"node-1"
"192.168.1.100"
[
  "data",
  "ingest",
  "master",
  "remote_cluster_client",
  "transform"
]

# 创建索引
$ curl -X PUT "localhost:9200/my-application-logs-2024.01.15" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "30s"
  },
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "level": { "type": "keyword" },
      "message": { "type": "text" },
      "service": { "type": "keyword" },
      "host": { "type": "keyword" }
    }
  }
}'
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "my-application-logs-2024.01.15"
}

# 查看索引列表
$ curl -X GET "localhost:9200/_cat/indices?v&health=green&s=index"
health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases                xxxxxx                 1   0   41         0            38.1mb     38.1mb
green  open   my-application-logs-2024.01.15  xxxxxx                 3   1   12345      0            45.6mb     22.8mb

# 搜索日志
$ curl -X GET "localhost:9200/my-application-logs-2024.01.15/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "level": "ERROR" } },
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  },
  "sort": [
    { "@timestamp": { "order": "desc" } }
  ],
  "size": 10
}' | jq '.hits.hits[]._source | {timestamp: .["@timestamp"], level: .level, message: .message}'
{
  "timestamp": "2024-01-15T10:25:30.123Z",
  "level": "ERROR",
  "message": "Database connection failed"
}
{
  "timestamp": "2024-01-15T10:20:15.456Z",
  "level": "ERROR",
  "message": "Cache timeout occurred"
}
```

### 内容解析
- **启动日志**: 显示节点启动、集群选举、服务监听等过程
- **健康状态**: green(健康)、yellow(警告)、red(危险)三种状态
- **节点信息**: 包含节点名称、主机地址、角色等
- **索引创建**: 返回确认信息和分片状态
- **搜索结果**: 包含匹配文档的源数据

### 常用参数详解
- `_cluster/health`: 集群健康状态API
- `_nodes/stats`: 节点统计信息
- `_cat/indices`: 索引列表(人类可读格式)
- `number_of_shards`: 主分片数量
- `number_of_replicas`: 副本分片数量
- `refresh_interval`: 索引刷新间隔

### 注意事项
- 合理规划分片数量避免过多小分片
- 生产环境应配置集群而非单节点
- 定期清理过期索引
- 监控磁盘空间使用情况

### 生产安全风险
- ⚠️ 默认无认证，任何人都可访问
- ⚠️ REST API可能暴露敏感数据
- ⚠️ 未限制查询可能导致拒绝服务
- ✅ 建议启用X-Pack安全功能、配置防火墙

---

## 4. 告警管理命令

### 用途
Alertmanager处理来自Prometheus等客户端的告警，负责去重、分组、静默和通知发送，是监控告警系统的重要组件。

### 输出示例
```bash
# 启动Alertmanager
$ alertmanager --config.file=alertmanager.yml --storage.path=/data/alertmanager
level=info ts=2024-01-15T10:30:45.123Z caller=main.go:231 msg="Starting Alertmanager" version="(version=0.25.0, branch=HEAD, revision=xxxxxx)"
level=info ts=2024-01-15T10:30:45.124Z caller=cluster.go:181 component=cluster msg="setting advertise address explicitly" addr=192.168.1.100 port=9094
level=info ts=2024-01-15T10:30:45.125Z caller=main.go:536 msg="Waiting for notification and silences to settle..." timeout=1m0s
level=info ts=2024-01-15T10:30:45.126Z caller=main.go:560 msg="Listening for http" addr=:9093
level=info ts=2024-01-15T10:30:45.127Z caller=coordinator.go:113 component=configuration msg="Loading configuration file" file=alertmanager.yml
level=info ts=2024-01-15T10:30:45.128Z caller=coordinator.go:126 component=configuration msg="Completed loading of configuration file" file=alertmanager.yml

# 查看告警状态
$ curl http://localhost:9093/api/v2/alerts | jq '.[] | {labels: .labels, status: .status.state, startsAt: .startsAt}'
[
  {
    "labels": {
      "alertname": "HighCPUUsage",
      "instance": "server01",
      "job": "node",
      "severity": "warning"
    },
    "status": "active",
    "startsAt": "2024-01-15T10:25:30.123Z"
  },
  {
    "labels": {
      "alertname": "LowDiskSpace",
      "instance": "server02",
      "job": "node",
      "severity": "critical"
    },
    "status": "suppressed",
    "startsAt": "2024-01-15T10:20:15.456Z"
  }
]

# 查看Silences(静默规则)
$ curl http://localhost:9093/api/v2/silences | jq '.[] | {id: .id, matchers: .matchers, startsAt: .startsAt, endsAt: .endsAt, createdBy: .createdBy, comment: .comment}'
[
  {
    "id": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "matchers": [
      {
        "name": "alertname",
        "value": "HighCPUUsage",
        "isRegex": false
      },
      {
        "name": "instance",
        "value": "maintenance-server",
        "isRegex": false
      }
    ],
    "startsAt": "2024-01-15T10:00:00Z",
    "endsAt": "2024-01-15T12:00:00Z",
    "createdBy": "admin",
    "comment": "Scheduled maintenance"
  }
]

# 创建静默规则
$ curl -X POST http://localhost:9093/api/v2/silences -H "Content-Type: application/json" -d '
{
  "matchers": [
    {
      "name": "alertname",
      "value": "HighMemoryUsage",
      "isRegex": false
    }
  ],
  "startsAt": "2024-01-15T10:30:00Z",
  "endsAt": "2024-01-15T11:30:00Z",
  "createdBy": "admin",
  "comment": "Memory upgrade in progress"
}'
{
  "silenceID": "yyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
}

# 查看接收者配置
$ curl http://localhost:9093/api/v2/receivers | jq '.[] | {name: .name, emailConfigs: .emailConfigs, webhookConfigs: .webhookConfigs}'
[
  {
    "name": "team-mails",
    "emailConfigs": [
      {
        "to": "team@example.com",
        "from": "alerts@example.com",
        "smarthost": "smtp.example.com:587",
        "authUsername": "alerts@example.com"
      }
    ],
    "webhookConfigs": [
      {
        "url": "https://hooks.slack.com/services/xxxxxx"
      }
    ]
  }
]
```

### 内容解析
- **启动信息**: 显示版本、集群配置、监听地址等
- **告警状态**: active(活跃)、suppressed(抑制)等状态
- **静默规则**: 包含匹配器、时间范围、创建者等信息
- **接收者配置**: 显示邮件、Webhook等通知配置

### 常用参数详解
- `--config.file`: Alertmanager配置文件
- `--storage.path`: 数据存储路径
- `matchers`: 告警匹配规则
- `startsAt/endsAt`: 静默时间段
- `createdBy/comment`: 创建者和备注信息

### 注意事项
- 配置合理的告警分组和抑制规则
- 定期清理过期的静默规则
- 测试通知渠道的可用性
- 监控Alertmanager自身的健康状态

### 生产安全风险
- ⚠️ 未保护的API端点可能被恶意利用
- ⚠️ 邮件配置可能暴露SMTP凭据
- ⚠️ Webhook URL可能包含敏感信息
- ✅ 建议启用认证、使用密钥管理服务

---

## 5. 日志收集命令

### 用途
Filebeat和Logstash等工具用于收集、解析和转发日志数据到Elasticsearch或其他存储系统，是日志管理管道的重要组件。

### 输出示例
```bash
# 启动Filebeat
$ filebeat -c filebeat.yml -e
2024-01-15T10:30:45.123Z	INFO	instance/beat.go:665	Home path: [/usr/share/filebeat] Config path: [/etc/filebeat] Data path: [/var/lib/filebeat] Logs path: [/var/log/filebeat]
2024-01-15T10:30:45.124Z	INFO	instance/beat.go:673	Beat ID: xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
2024-01-15T10:30:45.125Z	INFO	[monitoring]	log/log.go:118	Metrics logging every 30s
2024-01-15T10:30:45.126Z	INFO	instance/beat.go:471	filebeat stopped.
2024-01-15T10:30:45.127Z	INFO	[publisher]	pipeline/module.go:113	Beat name: server01
2024-01-15T10:30:45.128Z	INFO	instance/beat.go:471	filebeat started.

# 查看Filebeat状态
$ filebeat export status
{
  "monitoring": {
    "enabled": true,
    "elasticsearch": {
      "hosts": [
        "localhost:9200"
      ]
    }
  },
  "output": {
    "elasticsearch": {
      "hosts": [
        "localhost:9200"
      ]
    }
  },
  "pipeline": {
    "clients": 1,
    "events": {
      "acked": 12345,
      "active": 0,
      "batches": 678,
      "failed": 0,
      "filtered": 0,
      "published": 12345,
      "retry": 0,
      "dropped": 0
    }
  }
}

# 启动Logstash
$ logstash -f /etc/logstash/conf.d/logstash.conf
Sending Logstash logs to /var/log/logstash which is now configured via log4j2.properties
[2024-01-15T10:30:45,123][INFO ][logstash.runner          ] Starting Logstash {"logstash.version"=>"8.6.0"}
[2024-01-15T10:30:45,234][INFO ][logstash.agent           ] Successfully started Logstash API endpoint {:port=>9600}
[2024-01-15T10:30:46,345][INFO ][org.reflections.Reflections] Reflections took 234 ms to scan 1 urls, producing 24 keys and 48 values 
[2024-01-15T10:30:47,456][INFO ][logstash.inputs.beats    ][main] Beats inputs: Starting input listener {:address=>"0.0.0.0:5044"}
[2024-01-15T10:30:47,567][INFO ][logstash.agent           ] Pipelines running {:count=>1, :running_pipelines=>[:main], :non_running_pipelines=>[]}

# 测试Logstash配置
$ logstash -t -f /etc/logstash/conf.d/logstash.conf
Configuration OK

# 查看Logstash性能指标
$ curl -s localhost:9600/_node/stats | jq '.pipelines.main.events'
{
  "in": 12345,
  "filtered": 12345,
  "out": 12345,
  "duration_in_millis": 456789,
  "queue_push_duration_in_millis": 12345
}
```

### 内容解析
- **Filebeat启动**: 显示路径配置、Beat ID、监控设置等
- **状态信息**: 包含事件处理统计、客户端连接数等
- **Logstash启动**: 显示版本信息、插件加载、输入监听等
- **性能指标**: 事件流入流出数量、处理耗时等

### 常用参数详解
- `-c CONFIG_FILE`: 指定配置文件
- `-e`: 输出日志到stderr
- `export status`: 导出运行状态
- `-t`: 测试配置文件语法

### 注意事项
- 合理配置日志轮转避免磁盘满
- 监控Filebeat和Logstash的性能指标
- 定期清理过期的日志数据
- 配置适当的缓冲区大小

### 生产安全风险
- ⚠️ 日志文件可能包含敏感信息
- ⚠️ 未加密传输可能暴露日志内容
- ⚠️ 配置错误可能导致数据丢失
- ✅ 建议启用TLS、配置日志脱敏

---

**总结**: 以上是监控系统常用的CLI工具详解。在生产环境中使用这些工具时，务必注意网络安全、访问控制和数据保护，确保监控系统的安全性和可靠性。