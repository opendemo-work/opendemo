# Kubernetes 技术栈命名大全

本文件定义了Kubernetes技术栈中各类资源、配置、标签等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、核心资源命名规范

### 1.1 Namespace命名
```yaml
# 环境隔离命名空间
apiVersion: v1
kind: Namespace
metadata:
  name: production        # 生产环境
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging          # 预发布环境
---
apiVersion: v1
kind: Namespace
metadata:
  name: development      # 开发环境
---
apiVersion: v1
kind: Namespace
metadata:
  name: testing          # 测试环境

# 业务域命名空间
apiVersion: v1
kind: Namespace
metadata:
  name: frontend         # 前端服务
---
apiVersion: v1
kind: Namespace
metadata:
  name: backend          # 后端服务
---
apiVersion: v1
kind: Namespace
metadata:
  name: database         # 数据库服务
---
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring       # 监控系统
```

### 1.2 Deployment命名
```yaml
# 应用部署命名规范
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-deployment           # 应用名称-资源类型
  namespace: production
  labels:
    app: web-app                     # 应用标识
    version: v1.2.3                  # 版本号
    environment: production          # 环境标识
    tier: frontend                   # 层级标识
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        version: v1.2.3
        environment: production
        tier: frontend
    spec:
      containers:
      - name: web-app-container      # 容器名称
        image: registry.example.com/web-app:v1.2.3
```

### 1.3 Service命名
```yaml
# 服务资源命名
apiVersion: v1
kind: Service
metadata:
  name: web-app-service             # 应用名称-service
  namespace: production
  labels:
    app: web-app
    environment: production
spec:
  selector:
    app: web-app
  ports:
  - name: http                      # 端口名称
    port: 80
    targetPort: 8080
  type: ClusterIP

---
# 负载均衡服务
apiVersion: v1
kind: Service
metadata:
  name: web-app-lb                  # 应用名称-lb
  namespace: production
spec:
  selector:
    app: web-app
  ports:
  - name: https
    port: 443
    targetPort: 8443
  type: LoadBalancer
  loadBalancerIP: 192.168.1.100
```

## 二、标签和注解规范

### 2.1 标准标签命名
```yaml
# 必需标签
metadata:
  labels:
    # 应用标识标签
    app.kubernetes.io/name: web-app           # 应用名称
    app.kubernetes.io/instance: web-app-prod  # 应用实例
    app.kubernetes.io/version: v1.2.3         # 应用版本
    
    # 管理标签
    app.kubernetes.io/component: frontend     # 组件类型
    app.kubernetes.io/part-of: ecommerce      # 所属应用
    app.kubernetes.io/managed-by: helm        # 管理工具
    
    # 环境标签
    environment: production                   # 环境标识
    tier: frontend                           # 层级标识
    release: stable                          # 发布状态

# 自定义业务标签
metadata:
  labels:
    # 业务域标签
    business-domain: user-management         # 业务域
    service-type: stateless                  # 服务类型
    criticality: high                        # 重要性等级
    
    # 运维标签
    monitoring: enabled                      # 监控开关
    backup: daily                            # 备份策略
    retention: 30d                           # 保留期限
```

### 2.2 注解命名规范
```yaml
# 标准注解
metadata:
  annotations:
    # 版本控制注解
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"apps/v1","kind":"Deployment",...}
    
    # 滚动更新注解
    deployment.kubernetes.io/revision: "3"
    
    # 时间戳注解
    kubernetes.io/change-cause: "Rolling update to v1.2.3"
    last-update-time: "2023-12-01T10:30:00Z"

# 自定义注解
metadata:
  annotations:
    # 配置管理注解
    config checksum/config-map: abc123def456
    config checksum/secret: xyz789uvw012
    
    # 安全注解
    iam.amazonaws.com/role: arn:aws:iam::123456789:role/web-app-role
    seccomp.security.alpha.kubernetes.io/pod: docker/default
    
    # 监控注解
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
    
    # 日志注解
    fluentd.logging.k8s.io/enabled: "true"
    fluentd.logging.k8s.io/format: "json"
```

## 三、配置管理命名规范

### 3.1 ConfigMap命名
```yaml
# 应用配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-app-config              # 应用名称-config
  namespace: production
data:
  app.properties: |
    server.port=8080
    logging.level=INFO
    database.pool.size=20
  
  nginx.conf: |
    server {
      listen 80;
      location / {
        proxy_pass http://web-app-service;
      }
    }

---
# 环境特定配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-app-config-production   # 应用名称-config-环境
  namespace: production
data:
  database.url: "jdbc:postgresql://postgres.production:5432/webapp"
  redis.host: "redis.production"
  api.endpoint: "https://api.production.company.com"

---
# 版本化配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-app-config-v1-2-3       # 应用名称-config-版本
  namespace: production
```

### 3.2 Secret命名
```yaml
# 应用密钥
apiVersion: v1
kind: Secret
metadata:
  name: web-app-secrets             # 应用名称-secrets
  namespace: production
type: Opaque
data:
  database-password: base64_encoded_password
  api-key: base64_encoded_key
  jwt-secret: base64_encoded_secret

---
# TLS证书密钥
apiVersion: v1
kind: Secret
metadata:
  name: web-app-tls                 # 应用名称-tls
  namespace: production
type: kubernetes.io/tls
data:
  tls.crt: base64_encoded_certificate
  tls.key: base64_encoded_private_key

---
# 镜像拉取密钥
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials        # registry-credentials
  namespace: production
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: base64_encoded_docker_config
```

## 四、存储资源命名规范

### 4.1 PersistentVolumeClaim命名
```yaml
# 应用持久化存储
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: web-app-storage             # 应用名称-storage
  namespace: production
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd

---
# 数据库存储
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data               # 服务名称-data
  namespace: database
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: premium-ssd

---
# 日志存储
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: web-app-logs                # 应用名称-logs
  namespace: production
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 50Gi
  storageClassName: standard
```

### 4.2 StorageClass命名
```yaml
# 存储类别定义
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd                    # 性能等级-存储类型
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iopsPerGB: "50"
  fsType: ext4
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer

---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: premium-ssd
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
volumeBindingMode: Immediate

---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
volumeBindingMode: WaitForFirstConsumer
```

## 五、网络资源命名规范

### 5.1 Ingress命名
```yaml
# 应用入口
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress            # 应用名称-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - web-app.company.com
    secretName: web-app-tls
  rules:
  - host: web-app.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80

---
# API网关入口
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-gateway-ingress        # 服务名称-ingress
  namespace: production
spec:
  rules:
  - host: api.company.com
    http:
      paths:
      - path: /v1/users
        pathType: Prefix
        backend:
          service:
            name: user-service
            port:
              number: 80
      - path: /v1/orders
        pathType: Prefix
        backend:
          service:
            name: order-service
            port:
              number: 80
```

### 5.2 NetworkPolicy命名
```yaml
# 默认拒绝策略
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all           # 策略类型-作用范围
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# 允许内部通信
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-internal-traffic     # 策略类型-流量方向
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: backend
    ports:
    - protocol: TCP
      port: 8080

---
# 允许外部访问
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-access      # 策略类型-访问来源
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
```

## 六、监控和日志命名规范

### 6.1 ServiceMonitor命名
```yaml
# 应用监控配置
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: web-app-monitor            # 应用名称-monitor
  namespace: monitoring
  labels:
    app: web-app
    release: prometheus-operator
spec:
  selector:
    matchLabels:
      app: web-app
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
    scheme: http

---
# 数据库监控
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: postgres-monitor           # 服务名称-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: postgres
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
```

### 6.2 PodMonitor命名
```yaml
# 独立Pod监控
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: batch-job-monitor          # 应用类型-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      job-type: batch-processing
  podMetricsEndpoints:
  - port: metrics
    interval: 60s
```

## 七、批处理和定时任务命名

### 7.1 Job命名
```yaml
# 一次性任务
apiVersion: batch/v1
kind: Job
metadata:
  name: database-backup-job        # 任务类型-任务名称
  namespace: production
spec:
  template:
    spec:
      containers:
      - name: backup-container
        image: postgres:13
        command: ["/backup-script.sh"]
      restartPolicy: Never

---
# 数据迁移任务
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration-v1-2-3      # 任务类型-版本标识
  namespace: production
spec:
  completions: 1
  parallelism: 1
  template:
    spec:
      containers:
      - name: migration-container
        image: migration-tool:latest
        env:
        - name: MIGRATION_VERSION
          value: "v1.2.3"
```

### 7.2 CronJob命名
```yaml
# 定时备份任务
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-database-backup     # 频率-任务类型
  namespace: production
spec:
  schedule: "0 2 * * *"           # 每天凌晨2点执行
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup-container
            image: backup-tool:latest
            env:
            - name: BACKUP_SCHEDULE
              value: "daily"
          restartPolicy: OnFailure

---
# 定时报表任务
apiVersion: batch/v1
kind: CronJob
metadata:
  name: weekly-report-generation   # 频率-任务类型
  namespace: production
spec:
  schedule: "0 0 * * 1"            # 每周一凌晨执行
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: report-container
            image: reporting-tool:latest
```

## 八、安全和权限命名规范

### 8.1 Role和RoleBinding命名
```yaml
# 应用角色定义
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: web-app-role               # 应用名称-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]

---
# 角色绑定
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: web-app-role-binding       # 应用名称-role-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: web-app-sa
  namespace: production
roleRef:
  kind: Role
  name: web-app-role
  apiGroup: rbac.authorization.k8s.io
```

### 8.2 ServiceAccount命名
```yaml
# 应用服务账户
apiVersion: v1
kind: ServiceAccount
metadata:
  name: web-app-sa                 # 应用名称-sa
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/web-app-role

---
# 监控服务账户
apiVersion: v1
kind: ServiceAccount
metadata:
  name: monitoring-sa              # 功能名称-sa
  namespace: monitoring
```

## 九、故障排查和诊断命名规范

### 9.1 临时调试Pod命名
```yaml
# 调试容器
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod-web-app          # debug-目标应用
  namespace: production
spec:
  containers:
  - name: debugger
    image: nicolaka/netshoot:latest
    command: ["/bin/bash"]
    args: ["-c", "while true; do sleep 30; done;"]
    env:
    - name: TARGET_APP
      value: "web-app"

---
# 网络测试Pod
apiVersion: v1
kind: Pod
metadata:
  name: network-test-pod           # 功能-测试类型
  namespace: production
spec:
  containers:
  - name: network-tester
    image: busybox:latest
    command: ["sleep", "3600"]
```

### 9.2 问题诊断资源
```yaml
# 性能分析Job
apiVersion: batch/v1
kind: Job
metadata:
  name: perf-analysis-web-app      # 分析类型-目标应用
  namespace: production
spec:
  template:
    spec:
      containers:
      - name: profiler
        image: profiler:latest
        command: ["/profiler.sh"]
        args: ["--target", "web-app-deployment"]
      restartPolicy: Never

---
# 日志收集DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector-debug        # 功能-调试标识
  namespace: production
spec:
  selector:
    matchLabels:
      app: log-collector-debug
  template:
    metadata:
      labels:
        app: log-collector-debug
    spec:
      containers:
      - name: log-collector
        image: fluentd:latest
        # 专门用于问题诊断的日志收集配置
```

## 十、最佳实践示例

### 10.1 生产环境Deployment模板
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-deployment
  namespace: production
  labels:
    app.kubernetes.io/name: web-app
    app.kubernetes.io/instance: web-app-prod
    app.kubernetes.io/version: v1.2.3
    app.kubernetes.io/component: frontend
    app.kubernetes.io/part-of: ecommerce-platform
    app.kubernetes.io/managed-by: kustomize
    environment: production
    tier: frontend
    criticality: high
    monitoring: enabled
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        version: v1.2.3
        environment: production
        tier: frontend
        criticality: high
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
        checksum/config: abc123def456
    spec:
      serviceAccountName: web-app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: web-app
        image: registry.company.com/web-app:v1.2.3
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "INFO"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: web-app-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: logs-volume
          mountPath: /app/logs
      volumes:
      - name: config-volume
        configMap:
          name: web-app-config-production
      - name: logs-volume
        persistentVolumeClaim:
          claimName: web-app-logs
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web-app
              topologyKey: kubernetes.io/hostname
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "web-app"
        effect: "NoSchedule"
```

### 10.2 监控和告警配置
```yaml
# PrometheusRule定义
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: web-app-alerts
  namespace: monitoring
spec:
  groups:
  - name: web-app.rules
    rules:
    - alert: WebAppHighErrorRate
      expr: rate(http_requests_total{status=~"5..", app="web-app"}[5m]) > 0.05
      for: 2m
      labels:
        severity: warning
        team: frontend
      annotations:
        summary: "High error rate for web application"
        description: "Error rate above 5% for more than 2 minutes"

    - alert: WebAppHighLatency
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{app="web-app"}[5m])) > 1
      for: 1m
      labels:
        severity: critical
        team: frontend
      annotations:
        summary: "High latency for web application"
        description: "95th percentile latency above 1 second"

    - alert: WebAppDown
      expr: absent(up{app="web-app"}) == 1
      for: 1m
      labels:
        severity: critical
        team: frontend
      annotations:
        summary: "Web application is down"
        description: "Web application has disappeared from Prometheus target discovery"
```

### 10.3 故障恢复脚本
```bash
#!/bin/bash
# k8s_troubleshooting.sh - Kubernetes故障排查脚本

NAMESPACE=${1:-"production"}
APP_NAME=${2:-"web-app"}

# 集群健康检查
check_cluster_health() {
    echo "=== Cluster Health Check ==="
    
    # 检查节点状态
    echo "Node status:"
    kubectl get nodes -o wide
    
    # 检查组件状态
    echo -e "\nComponent status:"
    kubectl get componentstatuses
    
    # 检查事件
    echo -e "\nRecent events:"
    kubectl get events --sort-by='.lastTimestamp' -n $NAMESPACE | tail -10
}

# 应用状态检查
check_app_status() {
    echo -e "\n=== Application Status Check ($APP_NAME) ==="
    
    # 检查Deployment
    echo "Deployment status:"
    kubectl get deployment $APP_NAME-deployment -n $NAMESPACE -o wide
    
    # 检查Pod状态
    echo -e "\nPod status:"
    kubectl get pods -l app=$APP_NAME -n $NAMESPACE -o wide
    
    # 检查服务
    echo -e "\nService status:"
    kubectl get service $APP_NAME-service -n $NAMESPACE
    
    # 检查Ingress
    echo -e "\nIngress status:"
    kubectl get ingress $APP_NAME-ingress -n $NAMESPACE
}

# 资源使用检查
check_resource_usage() {
    echo -e "\n=== Resource Usage Check ==="
    
    # CPU和内存使用
    echo "Top resource consumers:"
    kubectl top pods -n $NAMESPACE | grep $APP_NAME
    
    # 检查资源配额
    echo -e "\nResource quotas:"
    kubectl describe resourcequota -n $NAMESPACE
    
    # 检查限制范围
    echo -e "\nLimit ranges:"
    kubectl describe limitrange -n $NAMESPACE
}

# 网络连接检查
check_network_connectivity() {
    echo -e "\n=== Network Connectivity Check ==="
    
    # 创建调试Pod
    kubectl run debug-pod --image=nicolaka/netshoot:latest -n $NAMESPACE --restart=Never -- sleep 3600
    
    # 等待Pod就绪
    kubectl wait --for=condition=ready pod/debug-pod -n $NAMESPACE --timeout=60s
    
    # 测试服务连接
    echo "Testing service connectivity:"
    kubectl exec debug-pod -n $NAMESPACE -- curl -s -o /dev/null -w "%{http_code}" http://$APP_NAME-service.$NAMESPACE.svc.cluster.local:80/health
    
    # 清理调试Pod
    kubectl delete pod debug-pod -n $NAMESPACE
}

# 日志分析
analyze_logs() {
    echo -e "\n=== Log Analysis ==="
    
    # 获取最近的错误日志
    echo "Recent error logs:"
    kubectl logs -l app=$APP_NAME -n $NAMESPACE --tail=50 | grep -i "error\|exception\|fatal" || echo "No errors found"
    
    # 获取Pod描述信息
    echo -e "\nPod descriptions:"
    kubectl describe pods -l app=$APP_NAME -n $NAMESPACE | grep -A 10 "Events:"
}

# 主执行函数
main() {
    echo "Starting Kubernetes troubleshooting for namespace: $NAMESPACE, app: $APP_NAME"
    echo "Timestamp: $(date)"
    echo "========================================"
    
    check_cluster_health
    check_app_status
    check_resource_usage
    check_network_connectivity
    analyze_logs
    
    echo -e "\n========================================"
    echo "Troubleshooting completed at: $(date)"
}

# 执行主函数
main "$@"
```

---

**注意事项：**
1. 所有资源命名应遵循一致的命名约定和层次结构
2. 标签使用标准化的键值对，便于管理和查询
3. 生产环境中必须配置适当的资源限制和健康检查
4. 安全相关的配置必须严格控制访问权限
5. 监控告警命名应便于快速定位问题根源