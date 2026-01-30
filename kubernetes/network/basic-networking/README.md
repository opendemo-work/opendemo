# Kubernetes网络实战指南

## 1. 案例概述

本案例提供了Kubernetes网络的全面实战指南，涵盖了Kubernetes网络的各个方面，包括：
- Pod网络与通信
- Service网络与服务发现
- Ingress网络与外部访问
- Network Policy与网络安全
- CNI插件配置
- DNS配置与解析
- 网络故障排查

通过本案例，您将深入了解Kubernetes网络的工作原理和最佳实践，掌握Kubernetes网络的配置和管理技能。

## 2. 环境准备

- Kubernetes集群（v1.20+）
- kubectl命令行工具
- 网络测试工具（如ping、nc、curl等）
- CNI插件（如Flannel、Calico、Cilium等）

## 3. Kubernetes网络架构

Kubernetes网络架构由以下几个主要组件组成：

### 3.1 Pod网络

Pod网络是Kubernetes网络的基础，为Pod提供了内部通信能力。每个Pod都有一个唯一的IP地址，Pod内的容器共享这个IP地址。

**关键特性**：
- 每个Pod获取一个唯一的IP地址
- Pod内的容器共享网络命名空间
- 所有Pod可以直接通信，无需NAT
- Pod网络由CNI插件实现

**配置示例**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: network-test
spec:
  containers:
  - name: busybox
    image: busybox:1.35
    command: ["sleep", "3600"]
```

### 3.2 Service网络

Service网络为Pod提供了稳定的访问点，实现了服务发现和负载均衡。

**关键特性**：
- 为一组Pod提供稳定的虚拟IP地址
- 自动实现负载均衡
- 支持多种服务类型（ClusterIP、NodePort、LoadBalancer、ExternalName）
- 通过标签选择器关联Pod

**配置示例**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  type: NodePort
  ports:
  - name: http
    port: 80
    targetPort: 80
    nodePort: 30080
```

### 3.3 Ingress网络

Ingress网络用于管理外部访问到集群内服务的HTTP和HTTPS路由。

**关键特性**：
- 提供HTTP/HTTPS路由
- 支持域名和路径匹配
- 支持TLS终止
- 支持负载均衡
- 需要Ingress控制器（如Nginx Ingress、Traefik等）

**配置示例**：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80
```

### 3.4 Network Policy

Network Policy用于定义Pod间的网络通信规则，实现网络安全隔离。

**关键特性**：
- 基于标签选择器定义通信规则
- 支持入站（Ingress）和出站（Egress）规则
- 基于协议、端口和源/目标IP定义规则
- 默认为允许所有通信

**配置示例**：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: nginx-network-policy
spec:
  podSelector:
    matchLabels:
      app: nginx
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: allowed
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
```

## 4. CNI插件配置

CNI（Container Network Interface）插件负责实现Kubernetes的Pod网络。常见的CNI插件包括：

### 4.1 Flannel

Flannel是一个简单易用的CNI插件，使用VXLAN或UDP实现Pod间通信。

**配置示例**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-flannel-cfg
  namespace: kube-system
data:
  cni-conf.json: |
    {
      "name": "cbr0",
      "cniVersion": "0.3.1",
      "plugins": [
        {
          "type": "flannel",
          "delegate": {
            "hairpinMode": true,
            "isDefaultGateway": true
          }
        },
        {
          "type": "portmap",
          "capabilities": {
            "portMappings": true
          }
        }
      ]
    }
  net-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
```

### 4.2 Calico

Calico是一个功能强大的CNI插件，支持网络策略和多种网络后端。

**配置示例**：

```yaml
apiVersion: operator.tigera.io/v1
type: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
    - blockSize: 26
      cidr: 10.244.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()
```

### 4.3 Cilium

Cilium是一个基于eBPF的CNI插件，提供了高性能的网络和网络安全功能。

**配置示例**：

```yaml
apiVersion: helm.cilium.io/v1
kind: CiliumHelmConfig
metadata:
  name: cilium
  namespace: kube-system
spec:
  helmValues:
    cluster: {
      id: 1,
      name: "default"
    }
    ipam: {
      mode: "cluster-pool"
    }
    k8sServiceHost: "<kube-apiserver-host>"
    k8sServicePort: "<kube-apiserver-port>"
```

## 5. DNS配置与解析

Kubernetes DNS服务负责为集群内的Pod和Service提供域名解析服务。

### 5.1 CoreDNS配置

CoreDNS是Kubernetes默认的DNS服务，负责解析集群内的域名。

**配置示例**：

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
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

### 5.2 DNS解析规则

Kubernetes中的DNS解析规则如下：

| 资源类型 | 域名格式 | 示例 |
|----------|----------|------|
| Service（ClusterIP） | `<service-name>.<namespace>.svc.<cluster-domain>` | `nginx.default.svc.cluster.local` |
| Service（Headless） | `<service-name>.<namespace>.svc.<cluster-domain>` | `mysql-headless.default.svc.cluster.local` |
| Pod | `<pod-ip>.<namespace>.pod.<cluster-domain>` | `10-244-1-5.default.pod.cluster.local` |
| Pod（主机名） | `<pod-hostname>.<service-name>.<namespace>.svc.<cluster-domain>` | `web-0.nginx-headless.default.svc.cluster.local` |

## 6. 网络故障排查

### 6.1 常见网络问题

1. **Pod无法通信**
2. **Service无法访问**
3. **Ingress无法访问**
4. **DNS解析失败**
5. **Network Policy限制**

### 6.2 排查工具

```bash
# 查看Pod网络状态
kubectl describe pod <pod-name>

# 测试Pod间通信
kubectl exec -it <pod-name> -- ping <target-pod-ip>

# 测试Service访问
kubectl exec -it <pod-name> -- curl <service-name>.<namespace>.svc.cluster.local

# 测试DNS解析
kubectl exec -it <pod-name> -- nslookup <service-name>.<namespace>.svc.cluster.local

# 查看CNI插件状态
kubectl get pods -n kube-system | grep -E 'flannel|calico|cilium|coredns'

# 查看网络命名空间
ip netns list

# 查看网络接口
kubectl exec -it <pod-name> -- ip a

# 查看路由表
kubectl exec -it <pod-name> -- ip route
```

## 7. 最佳实践

### 7.1 Pod网络最佳实践

- 为Pod配置适当的网络资源限制
- 使用就绪探针和存活探针监控Pod网络状态
- 避免在Pod内使用固定的IP地址
- 优先使用Service名称进行通信，而非直接使用Pod IP
- 为跨AZ部署的Pod配置合适的网络拓扑策略

### 7.2 Service网络最佳实践

- 根据服务类型选择合适的Service类型（ClusterIP、NodePort、LoadBalancer）
- 为Service配置适当的会话亲和性
- 使用Headless Service实现Pod间直接通信
- 为Service配置健康检查
- 对高流量Service考虑使用HPA（Horizontal Pod Autoscaler）
- 为关键Service配置Service拓扑感知路由

### 7.3 Ingress网络最佳实践

- 使用IngressClassName指定Ingress控制器
- 为Ingress配置TLS证书
- 配置适当的Ingress规则优先级
- 监控Ingress控制器的性能和健康状态
- 为高流量Ingress配置Ingress控制器的水平扩展
- 使用Ingress策略实现流量控制和安全防护

### 7.4 Network Policy最佳实践

- 遵循最小权限原则配置Network Policy
- 为所有Namespace配置默认的Network Policy
- 定期审查和更新Network Policy规则
- 使用Network Policy模拟工具测试规则效果
- 为不同环境（开发、测试、生产）配置不同的Network Policy策略
- 考虑使用Network Policy管理工具（如Calico Policy Advisor）

### 7.5 DNS最佳实践

- 为Service配置清晰的名称
- 避免使用过长的Service名称
- 监控CoreDNS的性能和健康状态
- 为关键Service配置适当的DNS缓存策略
- 配置CoreDNS的资源限制和自动扩展
- 考虑使用DNS策略优化Pod的DNS解析

## 8. 高级网络功能

### 8.1 网络策略高级用法

#### 8.1.1 基于命名空间的网络隔离

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: namespace-isolation
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: production
    - namespaceSelector:
        matchLabels:
          name: monitoring
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
```

#### 8.1.2 基于IP地址范围的访问控制

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ip-based-access
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
  - Ingress
  ingress:
  - from:
    - ipBlock:
        cidr: 192.168.1.0/24
        except:
        - 192.168.1.100/32
    ports:
    - protocol: TCP
      port: 5432
```

### 8.2 CNI插件对比与选择

| CNI插件 | 网络模型 | 性能 | 网络策略 | 高级功能 | 易用性 | 适用场景 |
|---------|----------|------|----------|----------|--------|----------|
| Flannel | VXLAN/UDP | 中 | 无 | 基本 | 高 | 简单部署、小规模集群 |
| Calico | BGP/IPIP | 高 | 强 | 网络可视化、流量日志 | 中 | 大规模集群、复杂网络策略 |
| Cilium | eBPF | 极高 | 强 | 服务网格集成、负载均衡、安全监控 | 中 | 高性能要求、服务网格场景 |
| Weave Net | VXLAN | 中 | 强 | 多集群互联 | 高 | 快速部署、多集群场景 |
| Canal | BGP/IPIP | 高 | 强 | 结合Flannel和Calico优点 | 中 | 平衡性能和功能的场景 |

### 8.3 网络性能优化

1. **选择合适的CNI插件**：根据集群规模和性能需求选择合适的CNI插件
2. **优化CNI插件配置**：
   - 对于Calico，考虑使用BGP而非IPIP以提高性能
   - 对于Flannel，考虑使用Host-GW模式（同子网）
3. **配置节点网络资源**：为节点配置足够的网络带宽和CPU资源
4. **优化Pod网络资源**：为Pod配置适当的网络资源限制
5. **使用网络加速技术**：
   - RDMA（Remote Direct Memory Access）用于高性能计算场景
   - SR-IOV（Single Root I/O Virtualization）用于虚拟机和容器共享网卡
6. **优化Service配置**：
   - 对于高流量Service，考虑使用Local模式的EndpointSlice
   - 配置适当的Service拓扑感知路由

### 8.4 多集群网络互联

#### 8.4.1 使用Submariner实现多集群互联

Submariner是一个用于连接多个Kubernetes集群的开源项目，支持跨集群的Pod和Service通信。

**配置示例**：

```yaml
# 部署Submariner Broker
kubectl create namespace submariner-operator
helm repo add submariner-latest https://submariner-io.github.io/submariner-charts/charts
helm install submariner-broker submariner-latest/submariner-broker --namespace submariner-operator

# 加入集群到Broker
subctl join broker-info.subm --clusterid cluster1 --natt=false
```

#### 8.4.2 使用Karmada实现多集群网络管理

Karmada是一个Kubernetes多集群管理系统，支持跨集群的服务发现和网络管理。

**配置示例**：

```yaml
apiVersion: policy.karmada.io/v1alpha1
kind: PropagationPolicy
metadata:
  name: nginx-propagation
spec:
  resourceSelectors:
    - apiVersion: apps/v1
      kind: Deployment
      name: nginx
  placement:
    clusterAffinity:
      clusterNames:
        - cluster1
        - cluster2
  schedulerName: default-scheduler
  replicaScheduling:
    replicaDivisionPreference: Weighted
    replicaSchedulingType: Divided
    weightPreference:
      staticWeightList:
        - targetCluster:
            clusterNames:
              - cluster1
          weight: 1
        - targetCluster:
            clusterNames:
              - cluster2
          weight: 1
```

### 8.5 Service网格集成

Service网格（如Istio、Linkerd、Consul）提供了更高级的网络功能，包括流量管理、安全、可观测性等。

#### 8.5.1 Istio集成

```yaml
# 部署Istio
istioctl install --set profile=default -y

# 为命名空间启用自动注入
kubectl label namespace default istio-injection=enabled

# 部署示例应用
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.18/samples/bookinfo/platform/kube/bookinfo.yaml

# 配置Istio VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: bookinfo
  namespace: default
spec:
  hosts:
  - "*"
  gateways:
  - bookinfo-gateway
  http:
  - match:
    - uri:
        exact: /productpage
    - uri:
        prefix: /static
    - uri:
        exact: /login
    - uri:
        exact: /logout
    - uri:
        prefix: /api/v1/products
    route:
    - destination:
        host: productpage
        port:
          number: 9080
```

#### 8.5.2 Linkerd集成

```yaml
# 部署Linkerd
linkerd install | kubectl apply -f -
linkerd check

# 为命名空间注入Linkerd
kubectl annotate namespace default linkerd.io/inject=enabled

# 部署示例应用
kubectl apply -f https://run.linkerd.io/emojivoto.yml

# 查看服务拓扑
linkerd viz stat deployment
linkerd viz graph deploy/emojivoto-web

## 9. 案例部署与测试

### 9.1 部署测试Pod

```yaml
# pod-test.yaml
apiVersion: v1
kind: Pod
metadata:
  name: network-test
spec:
  containers:
  - name: busybox
    image: busybox:1.35
    command: ["sleep", "3600"]
    ports:
    - containerPort: 8080
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx-test
spec:
  containers:
  - name: nginx
    image: nginx:1.23
    ports:
    - containerPort: 80
```

```bash
kubectl apply -f pod-test.yaml
```

### 9.2 部署测试Service

```yaml
# service-test.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    run: nginx-test
  type: NodePort
  ports:
  - name: http
    port: 80
    targetPort: 80
    nodePort: 30080
---
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  selector:
    run: nginx-test
  clusterIP: None
  ports:
  - name: http
    port: 80
    targetPort: 80
```

```bash
kubectl apply -f service-test.yaml
```

### 9.3 部署测试Ingress

```yaml
# ingress-test.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: nginx.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80
```

```bash
kubectl apply -f ingress-test.yaml
```

### 9.4 部署测试Network Policy

```yaml
# networkpolicy-test.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: nginx-network-policy
spec:
  podSelector:
    matchLabels:
      run: nginx-test
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: allowed
    ports:
    - protocol: TCP
      port: 80
```

```bash
kubectl apply -f networkpolicy-test.yaml
```

### 9.5 测试网络通信

```bash
# 测试Pod间通信
kubectl exec -it network-test -- ping nginx-test

# 测试Service访问
kubectl exec -it network-test -- curl nginx-service

# 测试DNS解析
kubectl exec -it network-test -- nslookup nginx-service

# 测试Ingress访问
curl -H "Host: nginx.example.com" http://<ingress-ip>
```

## 10. 版本兼容性

| Kubernetes版本 | 兼容性 |
|---------------|--------|
| v1.20.x       | ✅     |
| v1.21.x       | ✅     |
| v1.22.x       | ✅     |
| v1.23.x       | ✅     |
| v1.24.x       | ✅     |
| v1.25.x       | ✅     |
| v1.26.x       | ✅     |
| v1.27.x       | ✅     |
| v1.28.x       | ✅     |
| v1.29.x       | ✅     |

## 11. 总结

本案例提供了Kubernetes网络的全面实战指南，涵盖了Kubernetes网络的各个方面。通过学习本案例，您可以：

- 深入理解Kubernetes网络架构
- 掌握Pod网络、Service网络和Ingress网络的配置和管理
- 了解CNI插件的选择和配置
- 掌握DNS配置和解析规则
- 学习网络故障排查方法
- 应用Kubernetes网络最佳实践
- 理解高级网络功能如Service网格、多集群互联等

Kubernetes网络是Kubernetes集群的核心组件之一，良好的网络配置和管理对于确保集群的稳定性和性能至关重要。通过本案例的学习和实践，您将能够构建和管理高效、可靠和安全的Kubernetes网络环境，适应从简单到复杂的各种业务场景。