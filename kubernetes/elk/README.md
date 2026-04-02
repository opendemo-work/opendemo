# ELK Stack

ELK (Elasticsearch, Logstash, Kibana) 日志分析栈演示，展示完整的日志收集、处理、分析流程。

## 什么是ELK

ELK Stack是三个开源项目的组合：
- **Elasticsearch**: 分布式搜索和分析引擎
- **Logstash**: 服务器端数据处理管道
- **Kibana**: 数据可视化平台

```
ELK架构:
┌─────────────────────────────────────────────────────┐
│                   Kibana                            │
│              (可视化展示)                            │
└────────────────────┬────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │ Elasticsearch│
              │  (存储索引)  │
              └──────┬──────┘
                     │
               ┌─────┴─────┐
               │  Logstash │
               │ (处理管道)│
               └─────┬─────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │  Beats  │  │  Beats  │  │  Beats  │
   │(Filebeat)│ │(Metricbeat)│ │(Heartbeat)│
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │ App Logs│  │ Metrics │  │  Uptime │
   └─────────┘  └─────────┘  └─────────┘
```

## Kubernetes上部署ELK

### 1. 创建Namespace

```bash
kubectl create namespace elk
```

### 2. 部署Elasticsearch

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: elk
spec:
  serviceName: elasticsearch
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
        resources:
          limits:
            memory: 4Gi
            cpu: "2"
        ports:
        - containerPort: 9200
          name: rest
        - containerPort: 9300
          name: inter-node
        env:
        - name: cluster.name
          value: elk-cluster
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: discovery.seed_hosts
          value: "elasticsearch-0.elasticsearch,elasticsearch-1.elasticsearch,elasticsearch-2.elasticsearch"
        - name: cluster.initial_master_nodes
          value: "elasticsearch-0,elasticsearch-1,elasticsearch-2"
        - name: ES_JAVA_OPTS
          value: "-Xms2g -Xmx2g"
        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi
```

### 3. 部署Logstash

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: logstash-config
  namespace: elk
data:
  logstash.conf: |
    input {
      beats {
        port => 5044
      }
    }
    filter {
      if [fields][logtype] == "nginx" {
        grok {
          match => { "message" => "%{COMBINEDAPACHELOG}" }
        }
      }
      date {
        match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
      }
    }
    output {
      elasticsearch {
        hosts => ["elasticsearch:9200"]
        index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
      }
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logstash
  namespace: elk
spec:
  replicas: 2
  selector:
    matchLabels:
      app: logstash
  template:
    metadata:
      labels:
        app: logstash
    spec:
      containers:
      - name: logstash
        image: docker.elastic.co/logstash/logstash:8.5.0
        ports:
        - containerPort: 5044
        volumeMounts:
        - name: config
          mountPath: /usr/share/logstash/pipeline
      volumes:
      - name: config
        configMap:
          name: logstash-config
```

### 4. 部署Kibana

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: elk
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      containers:
      - name: kibana
        image: docker.elastic.co/kibana/kibana:8.5.0
        ports:
        - containerPort: 5601
        env:
        - name: ELASTICSEARCH_HOSTS
          value: '["http://elasticsearch:9200"]'
        - name: SERVER_HOST
          value: "0.0.0.0"
---
apiVersion: v1
kind: Service
metadata:
  name: kibana
  namespace: elk
spec:
  type: LoadBalancer
  selector:
    app: kibana
  ports:
  - port: 5601
    targetPort: 5601
```

### 5. 部署Filebeat

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: filebeat-config
  namespace: elk
data:
  filebeat.yml: |
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
        - add_kubernetes_metadata:
            host: ${NODE_NAME}
            matchers:
            - logs_path:
                logs_path: "/var/log/containers/"
    
    output.logstash:
      hosts: ["logstash:5044"]
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: filebeat
  namespace: elk
spec:
  selector:
    matchLabels:
      app: filebeat
  template:
    metadata:
      labels:
        app: filebeat
    spec:
      serviceAccountName: filebeat
      terminationGracePeriodSeconds: 30
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
      containers:
      - name: filebeat
        image: docker.elastic.co/beats/filebeat:8.5.0
        args: ["-c", "/etc/filebeat.yml", "-e"]
        env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        volumeMounts:
        - name: config
          mountPath: /etc/filebeat.yml
          subPath: filebeat.yml
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: filebeat-config
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## Logstash过滤器示例

### 解析Nginx日志
```ruby
filter {
  grok {
    match => { 
      "message" => "%{IPORHOST:clientip} %{HTTPDUSER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] \"%{WORD:verb} %{DATA:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:response} (?:%{NUMBER:bytes}|-) \"%{DATA:referrer}\" \"%{DATA:agent}\""
    }
  }
  
  geoip {
    source => "clientip"
  }
  
  useragent {
    source => "agent"
    target => "useragent"
  }
}
```

### 解析JSON日志
```ruby
filter {
  json {
    source => "message"
    target => "parsed"
  }
  
  mutate {
    add_field => {
      "level" => "%{[parsed][level]}"
      "service" => "%{[parsed][service]}"
    }
    remove_field => ["parsed"]
  }
}
```

## Kibana使用技巧

### 1. 创建可视化
- 柱状图: 按状态码统计
- 饼图: 按服务分布
- 折线图: 请求趋势
- 热力图: 地理位置分布

### 2. 创建仪表板
```
┌─────────────────────────────────────────┐
│    今日请求量          错误率           │
│    ┌─────────┐        ┌─────────┐      │
│    │  15.2K  │        │  0.5%   │      │
│    └─────────┘        └─────────┘      │
├─────────────────────────────────────────┤
│         请求趋势图 (24小时)              │
│    ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄▃▂▁       │
├─────────────────────────────────────────┤
│  最近错误日志                           │
│  ┌─────────────────────────────────┐   │
│  │ 2024-01-15 ERROR ...            │   │
│  │ 2024-01-15 WARN ...             │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 告警配置

```yaml
# Watcher配置
PUT _watcher/watch/high_error_rate
{
  "trigger": {
    "schedule": { "interval": "5m" }
  },
  "input": {
    "search": {
      "request": {
        "indices": ["filebeat-*"],
        "body": {
          "query": {
            "bool": {
              "must": [
                { "match": { "level": "ERROR" } },
                { "range": { "@timestamp": { "gte": "now-5m" } } }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": { "ctx.payload.hits.total": { "gt": 10 } }
  },
  "actions": {
    "send_email": {
      "email": {
        "to": ["admin@example.com"],
        "subject": "High Error Rate Detected"
      }
    }
  }
}
```

## 学习要点

1. 日志收集管道设计
2. Logstash过滤器编写
3. 索引生命周期管理
4. Kibana可视化创建
5. 日志分析和故障排查
