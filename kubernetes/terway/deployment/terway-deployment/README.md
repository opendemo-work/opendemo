# 🚀 Terway 生产级部署配置完整指南

> 企业级阿里云Terway CNI网络插件部署、配置和管理的完整解决方案

## 📋 案例概述

本案例提供阿里云Terway网络插件的企业级部署和配置方案，涵盖从基础安装到高可用架构的完整实践，确保在生产环境中能够稳定、高效地提供网络服务。

### 🔧 核心能力覆盖

- **高可用部署**: 多副本架构、滚动更新、故障自愈
- **性能优化**: ENI资源配置、网络策略优化、QoS调优
- **配置管理**: 自动化部署、配置版本控制、动态更新
- **安全加固**: 安全组集成、网络隔离、访问控制
- **监控告警**: 性能指标、健康检查、故障告警
- **运维管理**: 自动化运维、配置备份、版本管理

### 🎯 适用场景

- 企业级阿里云Kubernetes集群网络
- 高并发网络流量场景
- 多区域部署环境
- 安全合规要求严格的环境
- 需要精细化网络管理的生产环境

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群状态
kubectl cluster-info
kubectl get nodes

# 验证阿里云环境
aliyun sts GetCallerIdentity

# 创建生产环境命名空间
kubectl create namespace terway-prod
```

### 2. 生产级部署配置

```bash
# 部署高可用Terway
kubectl apply -f terway-production.yaml -n kube-system

# 验证部署状态
kubectl get pods -n kube-system -l app=terway
kubectl describe daemonset terway -n kube-system
```

---

## 📚 核心配置详解

### 1. 高可用部署架构

#### 1.1 DaemonSet部署配置

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: terway
  namespace: kube-system
  labels:
    app: terway
spec:
  selector:
    matchLabels:
      app: terway
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: terway
    spec:
      priorityClassName: system-node-critical
      serviceAccountName: terway
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
      tolerations:
        - operator: Exists
          effect: NoSchedule
        - operator: Exists
          effect: NoExecute
      containers:
      - name: terway
        image: registry.cn-hangzhou.aliyuncs.com/acs/terway:v1.4.0
        imagePullPolicy: IfNotPresent
        securityContext:
          privileged: true
        env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: aliyun-credentials
              key: access-key-id
        - name: ACCESS_KEY_SECRET
          valueFrom:
            secretKeyRef:
              name: aliyun-credentials
              key: access-key-secret
        - name: REGION
          value: "cn-hangzhou"
        - name: CLUSTER_ID
          value: "k8s-cluster-prod"
        volumeMounts:
        - name: cni-bin
          mountPath: /opt/cni/bin
        - name: cni-conf
          mountPath: /etc/cni/net.d
        - name: host-var-run
          mountPath: /var/run
        - name: host-var-lib
          mountPath: /var/lib
        - name: host-etc
          mountPath: /etc
        - name: host-opt
          mountPath: /opt
        - name: log
          mountPath: /var/log/terway
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 1Gi
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - |
              if [ -f /var/run/terway/terway.sock ]; then
                echo "Terway socket exists"
              else
                exit 1
              fi
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
      volumes:
      - name: cni-bin
        hostPath:
          path: /opt/cni/bin
      - name: cni-conf
        hostPath:
          path: /etc/cni/net.d
      - name: host-var-run
        hostPath:
          path: /var/run
      - name: host-var-lib
        hostPath:
          path: /var/lib
      - name: host-etc
        hostPath:
          path: /etc
      - name: host-opt
        hostPath:
          path: /opt
      - name: log
        hostPath:
          path: /var/log/terway
```

#### 1.2 RBAC权限配置

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: terway
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: terway
rules:
- apiGroups: [""]
  resources: ["nodes", "namespaces", "pods", "services", "endpoints"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["networking.k8s.io"]
  resources: ["networkpolicies"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["crd.projectcalico.org"]
  resources: ["blockaffinities", "ipamblocks", "ipamhandles"]
  verbs: ["get", "list", "create", "update", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: terway
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: terway
subjects:
- kind: ServiceAccount
  name: terway
  namespace: kube-system
```

### 2. 生产级配置管理

#### 2.1 核心配置文件

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-config
  namespace: kube-system
data:
  eni_conf: |
    {
      "version": "1",
      "access_key": "",
      "secret_key": "",
      "region": "cn-hangzhou",
      "vswitches": ["vsw-xxxxxxxxx", "vsw-yyyyyyyyy"],
      "security_group": "sg-xxxxxxxxx",
      "eni_tags": {
        "KubernetesCluster": "prod-cluster",
        "Environment": "production"
      },
      "eni_count_max": 5,
      "eni_count_min": 1,
      "eni_gc_threshold": 3,
      "eni_gc_interval": 300,
      "eni_create_retry": 3,
      "eni_create_timeout": 300
    }
  cni_conf: |
    {
      "cniVersion": "0.3.1",
      "name": "terway",
      "type": "terway",
      "eni_conf": "/etc/eni/eni_conf",
      "log_level": "info",
      "log_file": "/var/log/terway/cni.log",
      "eni_gc_enable": true,
      "eni_gc_interval": 3600
    }
```

#### 2.2 网络策略配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-network-policy
  namespace: kube-system
data:
  network_policy: |
    {
      "default_policy": "accept",
      "policies": [
        {
          "name": "allow-internal",
          "selector": {
            "namespace": "production"
          },
          "ingress": [
            {
              "from": [
                {
                  "namespaceSelector": {
                    "matchLabels": {
                      "name": "frontend"
                    }
                  }
                }
              ],
              "ports": [
                {
                  "protocol": "TCP",
                  "port": 80
                }
              ]
            }
          ]
        }
      ]
    }
```

### 3. 资源调优配置

#### 3.1 性能优化参数

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: terway-optimized
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - name: terway
        env:
        # 性能调优参数
        - name: GOGC
          value: "20"
        - name: GOMAXPROCS
          value: "2"
        # 网络优化参数
        - name: TERWAY_ENI_MAX_CONCURRENT
          value: "10"
        - name: TERWAY_ROUTE_TABLE_ID_BASE
          value: "100"
        resources:
          requests:
            cpu: 200m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 2Gi
```

---

## 🔧 高级配置选项

### 1. 多网卡配置

```yaml
apiVersion: terway.aliyun.com/v1beta1
kind: MultiENIConfig
metadata:
  name: terway-multi-eni
  namespace: kube-system
spec:
  eniConfigs:
  - eniID: eni-primary
    subnetID: vsw-primary-zone-a
    securityGroupID: sg-primary
    primary: true
    zone: cn-hangzhou-a
  - eniID: eni-secondary
    subnetID: vsw-secondary-zone-b
    securityGroupID: sg-secondary
    primary: false
    zone: cn-hangzhou-b
  routingPolicy:
    defaultENI: eni-primary
    policyRoutes:
    - destination: 10.0.0.0/8
      eni: eni-primary
    - destination: 172.16.0.0/12
      eni: eni-secondary
```

### 2. QoS配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-qos-config
  namespace: kube-system
data:
  qos_conf: |
    {
      "bandwidth_limit": {
        "default_egress_bandwidth": "100Mbps",
        "default_ingress_bandwidth": "100Mbps"
      },
      "priority_classes": {
        "high_priority": {
          "egress_bandwidth": "1Gbps",
          "ingress_bandwidth": "1Gbps",
          "tc_class_id": 1
        },
        "medium_priority": {
          "egress_bandwidth": "500Mbps",
          "ingress_bandwidth": "500Mbps",
          "tc_class_id": 2
        },
        "low_priority": {
          "egress_bandwidth": "100Mbps",
          "ingress_bandwidth": "100Mbps",
          "tc_class_id": 3
        }
      }
    }
```

### 3. 安全增强配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-security-config
  namespace: kube-system
data:
  security_conf: |
    {
      "network_isolation": {
        "enable": true,
        "default_policy": "drop",
        "allowed_cidrs": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
      },
      "security_group_sync": {
        "enable": true,
        "sync_interval": 300,
        "rules": [
          {
            "direction": "ingress",
            "protocol": "tcp",
            "port_range": "80/80",
            "source_cidr": "0.0.0.0/0"
          },
          {
            "direction": "ingress",
            "protocol": "tcp",
            "port_range": "443/443",
            "source_cidr": "0.0.0.0/0"
          }
        ]
      }
    }
```

---

## 📊 监控和告警

### 1. Prometheus监控配置

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: terway-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: terway
  namespaceSelector:
    matchNames:
      - kube-system
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### 2. 告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: terway-alerts
  namespace: monitoring
spec:
  groups:
  - name: terway.rules
    rules:
    - alert: TerwayDown
      expr: up{job="terway"} == 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Terway is down"
        description: "Terway has disappeared from Prometheus target discovery"
    
    - alert: TerwayHighLatency
      expr: histogram_quantile(0.99, rate(terway_network_latency_seconds_bucket[5m])) > 0.1
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Terway high latency"
        description: "Terway 99th percentile network latency is higher than 100ms"
    
    - alert: TerwayENICreationFailures
      expr: rate(terway_eni_creation_failures_total[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Terway ENI creation failures"
        description: "Terway ENI creation failure rate is higher than 10%"
```

---

## 🚨 故障排查

### 1. 常见问题诊断

```bash
# 1. 检查Terway状态
kubectl get pods -n kube-system -l app=terway
kubectl describe pod -n kube-system -l app=terway

# 2. 查看日志
kubectl logs -n kube-system -l app=terway --tail=100

# 3. 验证网络连通性
kubectl exec -it <pod-name> -n <namespace> -- ping 8.8.8.8

# 4. 检查配置
kubectl get configmap terway-config -n kube-system -o yaml
```

### 2. 性能调优检查

```bash
# 1. 资源使用情况
kubectl top pods -n kube-system -l app=terway

# 2. 网络接口状态
kubectl exec -it <terway-pod> -n kube-system -- ip addr show
kubectl exec -it <terway-pod> -n kube-system -- ip route show

# 3. ENI状态检查
kubectl exec -it <terway-pod> -n kube-system -- curl http://localhost:10248/debug/pprof/
```

---

## 🧪 实践练习

### 练习1：高可用部署
部署三副本Terway并验证故障切换能力。

### 练习2：性能调优
调整ENI配置和QoS参数，观察网络性能变化。

### 练习3：监控配置
配置完整的监控告警体系。

### 练习4：安全加固
实施网络隔离和安全组同步配置。

---

## 📚 扩展阅读

### 官方文档
- [Terway官方文档](https://github.com/AliyunContainerService/terway)
- [阿里云Kubernetes网络指南](https://help.aliyun.com/document_detail/86987.html)

### 相关案例
- [Terway基础入门](../terway-basics/)
- [Terway高级特性](../terway-advanced/)
- [网络故障排查](../../network/network-troubleshooting/)

### 进阶主题
- 多集群网络管理
- 混合云网络架构
- 网络策略深度优化
- 安全合规最佳实践

---

## 📋 清理资源

```bash
# 删除测试资源
kubectl delete namespace terway-prod

# 恢复默认配置
kubectl apply -f https://raw.githubusercontent.com/AliyunContainerService/terway/master/deploy/terway.yaml

# 重置副本数
kubectl scale daemonset terway -n kube-system --replicas=0
```

---

> **💡 提示**: Terway是阿里云专为Kubernetes优化的CNI网络插件，生产环境部署时务必做好充分测试和监控。