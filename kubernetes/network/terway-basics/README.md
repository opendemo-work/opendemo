# 🌐 Terway网络插件基础入门实战

> 全面掌握阿里云Terway CNI网络插件：从基础配置到高级网络策略管理的完整实践指南

## 📋 案例概述

本案例详细介绍阿里云Terway网络插件的基础知识和实践操作，帮助用户理解和掌握云原生网络解决方案的核心技能。

### 🔧 核心技能点

- **Terway基本概念**: 理解阿里云CNI插件的工作原理和优势
- **基础配置部署**: Terway插件安装、配置和初始化
- **网络策略管理**: Pod间通信控制、安全组集成
- **IP地址管理**: 弹性网卡ENI、IP地址池配置
- **服务发现集成**: 与CoreDNS、Service的协同工作
- **性能监控**: 网络性能指标采集和分析

### 🎯 适用人群

- 阿里云Kubernetes用户
- 云原生网络工程师
- DevOps工程师
- 系统管理员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查集群环境
kubectl cluster-info
kubectl get nodes

# 创建专用命名空间
kubectl create namespace terway-demo

# 验证阿里云凭证配置
aliyun sts GetCallerIdentity
```

### 2. Terway插件部署

```bash
# 下载Terway部署文件
wget https://github.com/AliyunContainerService/terway/releases/download/v1.3.0/terway.yaml

# 部署Terway插件
kubectl apply -f terway.yaml

# 验证部署状态
kubectl get pods -n kube-system | grep terway
```

---

## 📚 详细教程

### 1. Terway核心概念

#### 1.1 什么是Terway

Terway是阿里云开发的Kubernetes CNI网络插件，专为阿里云环境优化，提供高性能的容器网络解决方案。

**核心特性**：
- 基于弹性网卡ENI的网络方案
- 支持Pod独立IP地址
- 与阿里云安全组深度集成
- 高性能网络转发能力

#### 1.2 网络架构

```
Pod → ENI → VPC网络 → 安全组 → 外部网络
```

### 2. 基础配置部署

#### 2.1 Terway配置文件

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: terway
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: terway
  template:
    metadata:
      labels:
        app: terway
    spec:
      containers:
      - name: terway
        image: registry.cn-hangzhou.aliyuncs.com/acs/terway:v1.3.0
        env:
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
        securityContext:
          privileged: true
        volumeMounts:
        - name: cni-bin
          mountPath: /opt/cni/bin
        - name: cni-conf
          mountPath: /etc/cni/net.d
      volumes:
      - name: cni-bin
        hostPath:
          path: /opt/cni/bin
      - name: cni-conf
        hostPath:
          path: /etc/cni/net.d
```

#### 2.2 阿里云凭证配置

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: aliyun-credentials
  namespace: kube-system
type: Opaque
data:
  access-key-id: <base64-encoded-access-key-id>
  access-key-secret: <base64-encoded-access-key-secret>
```

### 3. 网络策略配置

#### 3.1 基础网络策略

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: terway-basic-policy
  namespace: terway-demo
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/8
    ports:
    - protocol: TCP
      port: 53
```

#### 3.2 安全组集成配置

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
      "vswitches": ["vsw-xxxxxx"],
      "security_group": "sg-xxxxxx",
      "eni_tags": {
        "KubernetesCluster": "my-cluster"
      }
    }
```

### 4. IP地址管理

#### 4.1 IP地址池配置

```yaml
apiVersion: terway.aliyun.com/v1beta1
kind: IPAMPool
metadata:
  name: terway-ip-pool
  namespace: kube-system
spec:
  cidr: 172.20.0.0/16
  gateway: 172.20.0.1
  excludeIPs:
  - 172.20.0.1
  - 172.20.0.2
  maxIPs: 1000
  minIPs: 100
```

#### 4.2 弹性网卡配置

```yaml
apiVersion: terway.aliyun.com/v1beta1
kind: ENIAttachment
metadata:
  name: terway-eni-attachment
  namespace: kube-system
spec:
  eniID: eni-xxxxxx
  instanceID: i-xxxxxx
  primaryIP: 192.168.1.100
```

### 5. 服务发现集成

#### 5.1 CoreDNS配置优化

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

#### 5.2 Service网络配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: terway-test-service
  namespace: terway-demo
spec:
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
  loadBalancerIP: 47.xx.xx.xx
```

---

## 🔧 实践操作

### 1. Terway部署验证

```bash
# 1. 检查Terway Pod状态
kubectl get pods -n kube-system | grep terway

# 2. 查看Terway日志
kubectl logs -n kube-system -l app=terway

# 3. 验证CNI配置
cat /etc/cni/net.d/10-terway.conf

# 4. 测试网络连通性
kubectl run debug-pod --image=busybox --rm -it -- sh
ping 8.8.8.8
nslookup kubernetes.default
```

### 2. 网络策略测试

```bash
# 1. 部署测试应用
kubectl apply -f test-apps.yaml -n terway-demo

# 2. 验证网络策略
kubectl get networkpolicies -n terway-demo

# 3. 测试跨命名空间通信
kubectl exec -it frontend-pod -n frontend -- ping web-service.terway-demo.svc.cluster.local

# 4. 验证安全组规则
aliyun ecs DescribeSecurityGroupAttribute --SecurityGroupId sg-xxxxxx
```

### 3. 性能监控配置

```bash
# 1. 部署监控组件
kubectl apply -f terway-monitoring.yaml

# 2. 查看网络指标
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# 访问 http://localhost:9090 查看指标

# 3. 监控关键指标
# terway_eni_used
# terway_ip_used
# terway_network_latency
```

---

## 📊 监控和日志

### 1. 关键监控指标

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
  endpoints:
  - port: metrics
    interval: 30s
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-alerts
  namespace: monitoring
data:
  alerts.yaml: |
    groups:
    - name: terway.alerts
      rules:
      - alert: HighENIUsage
        expr: terway_eni_used / terway_eni_total > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "ENI使用率过高"
          description: "ENI使用率达到 {{ $value }}%"
```

### 2. 日志收集配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/terway/*.log
      pos_file /var/log/terway.log.pos
      tag terway.*
      <parse>
        @type json
      </parse>
    </source>
    
    <match terway.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
    </match>
```

---

## ⚠️ 常见问题和解决方案

### 1. Pod网络不通

**问题现象**: Pod无法访问外部网络或集群内部服务

**可能原因**:
- Terway插件未正确安装
- 安全组规则配置错误
- VPC路由表配置问题
- IP地址冲突

**解决步骤**:
```bash
# 1. 检查Terway状态
kubectl get pods -n kube-system | grep terway
kubectl describe pod -n kube-system <terway-pod-name>

# 2. 验证安全组配置
aliyun ecs DescribeSecurityGroupAttribute --SecurityGroupId sg-xxxxxx

# 3. 检查VPC路由
aliyun vpc DescribeRouteTableList --VpcId vpc-xxxxxx

# 4. 查看Pod网络配置
kubectl exec -it <pod-name> -- ip addr show
```

### 2. IP地址耗尽

**问题现象**: 新Pod无法分配IP地址，处于ContainerCreating状态

**解决步骤**:
```bash
# 1. 检查IP使用情况
kubectl get ippool -n kube-system

# 2. 扩展IP地址池
kubectl patch ippool terway-ip-pool -n kube-system -p '{"spec":{"maxIPs":2000}}' --type=merge

# 3. 清理未使用的IP
kubectl delete pod --all -n <namespace>
```

### 3. 网络性能问题

**问题现象**: 网络延迟高、吞吐量低

**解决步骤**:
```bash
# 1. 性能基准测试
kubectl run perf-test --image=network-multitool --rm -it -- sh
iperf3 -c <server-ip> -t 60

# 2. 检查ENI配置
aliyun ecs DescribeNetworkInterfaces --InstanceId i-xxxxxx

# 3. 优化MTU设置
kubectl patch configmap terway-config -n kube-system -p '{"data":{"mtu":"1500"}}' --type=merge
```

---

## 🧪 实践练习

### 练习1：基础网络配置
部署Terway插件并验证基本网络连通性。

### 练习2：网络策略实践
配置不同级别的网络访问控制策略。

### 练习3：安全组集成
实现Pod与阿里云安全组的深度集成。

### 练习4：性能优化
调优网络配置以获得最佳性能表现。

---

## 📚 扩展阅读

### 官方文档
- [Terway GitHub仓库](https://github.com/AliyunContainerService/terway)
- [阿里云容器服务文档](https://help.aliyun.com/document_detail/86987.html)
- [Kubernetes CNI规范](https://github.com/containernetworking/cni)

### 相关案例
- [CoreDNS基础配置](../coredns-basics/)
- [CSI Plugin存储管理](../csi-plugin-basics/)
- [网络组件生产实践](../network-production/)

### 进阶主题
- 多可用区网络架构
- 网络策略高级用法
- 与服务网格集成
- 混合云网络方案

---

## 📋 清理资源

```bash
# 删除测试应用
kubectl delete namespace terway-demo

# 卸载Terway插件
kubectl delete -f terway.yaml

# 清理配置文件
kubectl delete configmap terway-config -n kube-system
kubectl delete secret aliyun-credentials -n kube-system

# 删除监控配置
kubectl delete servicemonitor terway-monitor -n monitoring
```

---

> **💡 提示**: Terway是专为阿里云环境优化的网络插件，建议在阿里云Kubernetes服务中使用。在生产环境中使用时要注意IP地址规划和安全组配置。