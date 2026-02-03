# 🌐 Kubernetes Service 生产级完整体系

> 企业级 Service 配置、管理、监控和故障排查的完整解决方案，满足生产环境所有需求

## 📋 案例概述

本案例提供 Kubernetes Service 的企业级完整实践体系，涵盖从基础配置到高级特性的全方位内容，确保在生产环境中能够安全、高效地管理和维护服务。

### 🔧 核心能力覆盖

- **多类型Service配置**: ClusterIP、NodePort、LoadBalancer、Headless、ExternalName
- **高级负载均衡**: 会话亲和性、健康检查、权重路由
- **安全加固**: 网络策略、RBAC控制、TLS加密
- **监控告警**: Prometheus指标、日志收集、性能分析
- **故障排查**: 诊断工具、常见问题解决、性能优化
- **生产最佳实践**: 配置管理、蓝绿部署、灰度发布

### 🎯 适用场景

- 企业级微服务架构
- 生产环境服务治理
- 高可用服务部署
- 安全合规要求
- 性能监控优化

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群状态
kubectl cluster-info
kubectl get nodes

# 创建生产环境命名空间
kubectl create namespace service-prod

# 验证权限
kubectl auth can-i create services -n service-prod
```

### 2. 部署基础应用

```bash
# 部署生产级应用
kubectl apply -f production-app.yaml -n service-prod

# 验证部署状态
kubectl get pods -n service-prod
kubectl get deployments -n service-prod
```

---

## 📚 核心组件详解

### 1. 多类型Service配置

#### 1.1 ClusterIP Service（生产推荐）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-clusterip
  namespace: service-prod
  labels:
    app: myapp
    version: v1.0
    environment: production
  annotations:
    # 服务发现标识
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "true"
    # 监控配置
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
spec:
  selector:
    app: myapp
    version: v1.0
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: metrics
      protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP
  # 会话亲和性配置
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

#### 1.2 LoadBalancer Service（外部访问）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-loadbalancer
  namespace: service-prod
  annotations:
    # AWS ELB配置
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:region:account:certificate/id"
    # 健康检查配置
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-protocol: "HTTP"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-port: "8080"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-path: "/health"
    service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval: "30"
spec:
  selector:
    app: myapp
  ports:
    - name: https
      protocol: TCP
      port: 443
      targetPort: 8443
  type: LoadBalancer
  loadBalancerSourceRanges:
    - "203.0.113.0/24"  # 白名单IP段
```

#### 1.3 Headless Service（有状态应用）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database-headless
  namespace: service-prod
spec:
  selector:
    app: database
    role: master
  ports:
    - name: postgres
      port: 5432
      targetPort: 5432
  clusterIP: None
  publishNotReadyAddresses: true  # 发布未就绪Pod地址
```

### 2. 高级负载均衡配置

#### 2.1 基于权重的路由

```yaml
apiVersion: v1
kind: Service
metadata:
  name: weighted-service
  namespace: service-prod
  annotations:
    # 自定义负载均衡权重
    service.kubernetes.io/topology-aware-hints: "auto"
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
# 配合EndpointSlice实现更精细的负载均衡
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: weighted-endpoints
  namespace: service-prod
  labels:
    kubernetes.io/service-name: weighted-service
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 8080
endpoints:
  - addresses:
      - "10.244.1.10"
    conditions:
      ready: true
    hostname: backend-v1
    zone: us-west-1a
    hints:
      forZones:
        - name: us-west-1a
  - addresses:
      - "10.244.2.15"
    conditions:
      ready: true
    hostname: backend-v2
    zone: us-west-1b
    hints:
      forZones:
        - name: us-west-1b
```

#### 2.2 健康检查和服务质量

```yaml
apiVersion: v1
kind: Service
metadata:
  name: health-checked-service
  namespace: service-prod
spec:
  selector:
    app: api-server
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
# 配合Pod健康检查
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  namespace: service-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
        - name: api
          image: mycompany/api-server:v1.0
          ports:
            - containerPort: 8080
          # 存活探针
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          # 就绪探针
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          # 启动探针（K8s 1.20+）
          startupProbe:
            httpGet:
              path: /startup
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 30
```

### 3. 安全加固配置

#### 3.1 网络策略控制

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: service-security-policy
  namespace: service-prod
spec:
  podSelector:
    matchLabels:
      app: backend-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # 允许前端应用访问
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
    # 允许监控系统访问metrics端口
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # 允许访问数据库
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
    # 允许DNS查询
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

#### 3.2 Service Account和RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: service-manager
  namespace: service-prod
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/ServiceManagerRole
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: service-operator
  namespace: service-prod
rules:
  - apiGroups: [""]
    resources: ["services", "endpoints", "pods"]
    verbs: ["get", "list", "watch", "update", "patch"]
  - apiGroups: ["discovery.k8s.io"]
    resources: ["endpointslices"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: service-manager-binding
  namespace: service-prod
subjects:
  - kind: ServiceAccount
    name: service-manager
    namespace: service-prod
roleRef:
  kind: Role
  name: service-operator
  apiGroup: rbac.authorization.k8s.io
```

### 4. 监控和告警配置

#### 4.1 Prometheus监控集成

```yaml
apiVersion: v1
kind: Service
metadata:
  name: monitored-service
  namespace: service-prod
  labels:
    app: business-app
  annotations:
    # Prometheus抓取配置
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
    prometheus.io/scheme: "https"
    # 自定义指标标签
    prometheus.io/probe: "business-app"
spec:
  selector:
    app: business-app
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080
    - name: metrics
      protocol: TCP
      port: 9090
      targetPort: 9090
---
# ServiceMonitor配置（Prometheus Operator）
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: business-app-monitor
  namespace: monitoring
  labels:
    team: backend
spec:
  selector:
    matchLabels:
      app: business-app
  namespaceSelector:
    matchNames:
      - service-prod
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
      scheme: https
      bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
      tlsConfig:
        caFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        insecureSkipVerify: false
```

#### 4.2 日志收集配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: logging-service
  namespace: service-prod
  annotations:
    # Fluentd日志收集标签
    fluentdConfiguration: |
      <source>
        @type tail
        path /var/log/containers/*_service-prod_*.log
        pos_file /var/log/fluentd-containers.log.pos
        tag kubernetes.*
        read_from_head true
        <parse>
          @type json
          time_format %Y-%m-%dT%H:%M:%S.%NZ
        </parse>
      </source>
spec:
  selector:
    app: log-aggregator
  ports:
    - protocol: TCP
      port: 24224
      targetPort: 24224
```

### 5. 故障排查工具

#### 5.1 诊断Pod配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: service-debugger
  namespace: service-prod
spec:
  containers:
    - name: debugger
      image: nicolaka/netshoot:latest
      command: ["/bin/bash"]
      args: ["-c", "while true; do sleep 30; done;"]
      env:
        - name: SERVICE_NAME
          value: "target-service"
      volumeMounts:
        - name: dockersock
          mountPath: "/var/run/docker.sock"
  volumes:
    - name: dockersock
      hostPath:
        path: /var/run/docker.sock
  tolerations:
    - operator: Exists
```

#### 5.2 常用诊断命令

```bash
# 服务状态检查
kubectl get services -n service-prod -o wide
kubectl describe service <service-name> -n service-prod

# 端点检查
kubectl get endpoints <service-name> -n service-prod
kubectl get endpointslices -n service-prod

# DNS解析测试
kubectl run dns-test --image=busybox:1.28 --rm -it -n service-prod -- nslookup <service-name>

# 网络连通性测试
kubectl run network-test --image=nicolaka/netshoot --rm -it -n service-prod -- \
  curl -v http://<service-name>.<namespace>.svc.cluster.local

# 性能测试
kubectl run perf-test --image=appropriate/curl --rm -it -n service-prod -- \
  ab -n 1000 -c 10 http://<service-name>/
```

---

## 🏭 生产环境最佳实践

### 1. 配置管理策略

```yaml
# 生产环境Service配置模板
apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.app.name }}-service
  namespace: {{ .Values.namespace }}
  labels:
    app: {{ .Values.app.name }}
    version: {{ .Values.app.version }}
    environment: {{ .Values.environment }}
    team: {{ .Values.team }}
    cost-center: {{ .Values.costCenter }}
  annotations:
    # 自动化标记
    kubernetes.io/change-cause: "{{ .Values.changeCause }}"
    # 安全合规标记
    security/classification: "{{ .Values.securityClassification }}"
    # SLA要求
    sla/tier: "{{ .Values.slaTier }}"
spec:
  selector:
    app: {{ .Values.app.name }}
    version: {{ .Values.app.version }}
  ports:
    {{- range .Values.ports }}
    - name: {{ .name }}
      protocol: {{ .protocol }}
      port: {{ .port }}
      targetPort: {{ .targetPort }}
    {{- end }}
  type: {{ .Values.serviceType }}
  {{- if eq .Values.serviceType "LoadBalancer" }}
  loadBalancerSourceRanges:
    {{- range .Values.allowedIPs }}
    - {{ . }}
    {{- end }}
  {{- end }}
  sessionAffinity: {{ .Values.sessionAffinity }}
  {{- if .Values.externalTrafficPolicy }}
  externalTrafficPolicy: {{ .Values.externalTrafficPolicy }}
  {{- end }}
```

### 2. 蓝绿部署配置

```yaml
# 蓝色环境
apiVersion: v1
kind: Service
metadata:
  name: app-blue
  namespace: service-prod
spec:
  selector:
    app: myapp
    version: v1.0
    color: blue
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

---
# 绿色环境
apiVersion: v1
kind: Service
metadata:
  name: app-green
  namespace: service-prod
spec:
  selector:
    app: myapp
    version: v2.0
    color: green
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

---
# 主服务（初始指向蓝色）
apiVersion: v1
kind: Service
metadata:
  name: app-production
  namespace: service-prod
spec:
  selector:
    app: myapp
    version: v1.0
    color: blue
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

### 3. 灰度发布策略

```yaml
# 金丝雀版本Service
apiVersion: v1
kind: Service
metadata:
  name: app-canary
  namespace: service-prod
  annotations:
    # 流量权重配置
    traffic.weight: "10"  # 10%流量
spec:
  selector:
    app: myapp
    version: v2.0-canary
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

---
# 稳定版本Service
apiVersion: v1
kind: Service
metadata:
  name: app-stable
  namespace: service-prod
spec:
  selector:
    app: myapp
    version: v1.0-stable
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

---

## 🚨 常见问题和解决方案

### 1. Service无法访问

**问题现象**: `Could not resolve host` 或 `Connection refused`

**诊断步骤**:
```bash
# 1. 检查Service是否存在
kubectl get svc -n service-prod

# 2. 检查Endpoints
kubectl get endpoints <service-name> -n service-prod

# 3. 检查Pod状态
kubectl get pods -n service-prod -l app=<app-label>

# 4. 检查网络策略
kubectl get networkpolicies -n service-prod

# 5. 测试DNS解析
kubectl run debug --image=busybox --rm -it -n service-prod -- nslookup <service-name>
```

**解决方案**:
```yaml
# 修正Service选择器
apiVersion: v1
kind: Service
metadata:
  name: fixed-service
  namespace: service-prod
spec:
  selector:
    app: correct-app-name  # 确保与Pod标签匹配
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

### 2. 负载均衡不均匀

**问题现象**: 某些Pod接收过多请求

**解决方案**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: balanced-service
  namespace: service-prod
  annotations:
    # 启用拓扑感知路由
    service.kubernetes.io/topology-aware-hints: "auto"
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  # 设置外部流量策略
  externalTrafficPolicy: Local
```

### 3. 健康检查失败

**问题现象**: Pod频繁重启或Service显示不可用

**解决方案**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: health-service
  namespace: service-prod
spec:
  selector:
    app: healthy-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
# 优化健康检查配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthy-app
  namespace: service-prod
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: app
          image: myapp:v1.0
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 60  # 增加初始延迟
            periodSeconds: 20
            timeoutSeconds: 10
            successThreshold: 1
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
            timeoutSeconds: 5
            successThreshold: 1
            failureThreshold: 3
```

---

## 📊 性能优化建议

### 1. 连接池优化

```yaml
apiVersion: v1
kind: Service
metadata:
  name: optimized-service
  namespace: service-prod
  annotations:
    # 连接超时优化
    service.alpha.kubernetes.io/connection-timeout: "30s"
    # 空闲连接保持
    service.alpha.kubernetes.io/keepalive-timeout: "600s"
spec:
  selector:
    app: optimized-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3小时会话保持
```

### 2. 资源限制配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: resource-managed-service
  namespace: service-prod
spec:
  selector:
    app: managed-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
# 配合资源配额
apiVersion: v1
kind: ResourceQuota
metadata:
  name: service-quota
  namespace: service-prod
spec:
  hard:
    services: "50"
    services.loadbalancers: "10"
    services.nodeports: "20"
```

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Service官方文档](https://kubernetes.io/docs/concepts/services-networking/service/)
- [网络策略文档](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [EndpointSlice文档](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)

### 相关案例
- [Ingress完整体系](../ingress-complete-demo/)
- [Service和Ingress集成](../service-ingress-integration-demo/)
- [网络策略管理](../../network/)

### 进阶主题
- Service Mesh集成（Istio、Linkerd）
- 多集群Service发现
- 高级负载均衡算法
- Service网格安全策略

---

## 🧪 实践练习

### 练习1：生产级Service部署
部署一个完整的Web应用，配置ClusterIP、LoadBalancer等多种Service类型，并实现健康检查和监控。

### 练习2：安全加固实践
为Service配置网络策略、RBAC权限和TLS加密，确保符合企业安全标准。

### 练习3：故障排查演练
模拟各种Service故障场景，练习使用诊断工具和解决方法。

### 练习4：性能优化
通过调整Service配置和负载均衡策略，优化服务性能和资源利用率。

---

## 📋 清理资源

```bash
# 删除生产环境命名空间
kubectl delete namespace service-prod

# 或单独删除资源
kubectl delete svc --all -n service-prod
kubectl delete deploy --all -n service-prod
kubectl delete networkpolicy --all -n service-prod
```

---

> **💡 提示**: 本案例提供了完整的Service生产级解决方案，建议结合实际业务场景进行定制化配置。定期审查和更新Service配置以适应业务发展需求。