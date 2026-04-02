# EFK Stack

EFK (Elasticsearch, Fluentd, Kibana) 日志收集与分析栈演示。

## 什么是EFK

EFK是一个流行的日志收集、存储和分析解决方案：
- **Elasticsearch**: 分布式搜索和分析引擎
- **Fluentd**: 统一日志收集层
- **Kibana**: 数据可视化和探索工具

```
EFK架构:
┌─────────────────────────────────────────────────────┐
│                   Kibana                            │
│              (可视化和查询)                          │
└────────────────────┬────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │ Elasticsearch│
              │  (索引存储)  │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │ Fluentd │  │ Fluentd │  │ Fluentd │
   │(DaemonSet)│ │(DaemonSet)│ │(DaemonSet)│
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │ App Pod │  │ App Pod │  │ App Pod │
   └─────────┘  └─────────┘  └─────────┘
```

## 安装EFK

### 1. 创建Namespace

```bash
kubectl create namespace logging
```

### 2. 安装Elasticsearch

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: logging
spec:
  serviceName: elasticsearch
  replicas: 1
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
        image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
        resources:
          limits:
            memory: 2Gi
          requests:
            memory: 1Gi
        ports:
        - containerPort: 9200
          name: http
        env:
        - name: discovery.type
          value: single-node
        - name: ES_JAVA_OPTS
          value: "-Xms512m -Xmx512m"
        volumeMounts:
        - name: elasticsearch-data
          mountPath: /usr/share/elasticsearch/data
  volumeClaimTemplates:
  - metadata:
      name: elasticsearch-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch
  namespace: logging
spec:
  selector:
    app: elasticsearch
  ports:
  - port: 9200
    targetPort: 9200
```

### 3. 安装Kibana

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: logging
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
        image: docker.elastic.co/kibana/kibana:7.17.0
        ports:
        - containerPort: 5601
        env:
        - name: ELASTICSEARCH_HOSTS
          value: "http://elasticsearch:9200"
---
apiVersion: v1
kind: Service
metadata:
  name: kibana
  namespace: logging
spec:
  selector:
    app: kibana
  ports:
  - port: 5601
    targetPort: 5601
  type: NodePort
```

### 4. 安装Fluentd

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fluentd
  namespace: logging
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fluentd
rules:
- apiGroups: [""]
  resources: ["pods", "namespaces"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: fluentd
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: fluentd
subjects:
- kind: ServiceAccount
  name: fluentd
  namespace: logging
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccountName: fluentd
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## Fluentd配置

### 自定义配置
```
<source>
  @type tail
  path /var/log/containers/*.log
  pos_file /var/log/fluentd-containers.log.pos
  tag kubernetes.*
  <parse>
    @type json
  </parse>
</source>

<filter kubernetes.**>
  @type kubernetes_metadata
</filter>

<match kubernetes.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
</match>
```

## Kibana使用

### 1. 访问Kibana
```bash
kubectl port-forward svc/kibana -n logging 5601:5601
# 访问 http://localhost:5601
```

### 2. 创建索引模式
1. 进入 Management → Stack Management → Index Patterns
2. 创建索引模式 `logstash-*`
3. 选择时间字段 `@timestamp`

### 3. 搜索日志
```
# 搜索特定Pod日志
kubernetes.pod_name: "my-app-123"

# 搜索特定命名空间
kubernetes.namespace_name: "production"

# 搜索错误日志
level: "error"

# 组合查询
kubernetes.pod_name: "api-*" AND level: "error"
```

### 4. 创建仪表板
- 保存搜索查询
- 创建可视化图表
- 组合成仪表板

## 日志轮转与保留

```yaml
# Elasticsearch ILM策略
PUT _ilm/policy/logs_policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_age": "1d",
            "max_size": "50gb"
          }
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

## 性能优化

1. **Elasticsearch**: 调整JVM堆内存
2. **Fluentd**: 使用文件缓冲
3. **索引分片**: 合理设置分片数量

## 学习要点

1. 日志收集架构设计
2. 日志解析和过滤
3. 日志查询和可视化
4. 日志保留策略
5. 高可用部署
