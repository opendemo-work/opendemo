# ⚡ Terway 高级特性与自定义配置

> 企业级阿里云Terway网络插件高级功能、自定义配置和扩展开发完整指南

## 📋 案例概述

本案例深入探讨阿里云Terway网络插件的高级特性和自定义配置能力，涵盖多网卡管理、网络策略深度定制、性能优化等企业级功能，帮助企业构建灵活、安全的网络服务体系。

### 🔧 核心能力覆盖

- **多网卡管理**: 弹性网卡ENI多实例、网络隔离、路由策略
- **网络策略定制**: 精细化访问控制、安全组深度集成
- **性能优化**: QoS配置、带宽管理、延迟优化
- **混合云网络**: 与传统网络环境互联互通
- **扩展开发**: 自定义CNI插件、网络控制器开发
- **故障诊断**: 高级网络分析工具、性能监控

### 🎯 适用场景

- 复杂企业网络环境
- 多区域联合部署
- 需要自定义网络逻辑的场景
- 安全合规要求严格的环境
- 高性能网络服务需求

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查Terway版本
kubectl get pods -n kube-system -l app=terway -o jsonpath='{.items[0].spec.containers[0].image}'

# 创建测试环境
kubectl create namespace terway-advanced

# 部署测试应用
kubectl apply -f test-applications.yaml -n terway-advanced
```

### 2. 高级配置验证

```bash
# 验证多网卡配置
kubectl apply -f multi-eni-config.yaml -n kube-system

# 测试自定义网络策略
kubectl apply -f advanced-network-policy.yaml -n terway-advanced
```

---

## 📚 核心高级特性

### 1. 多网卡管理

#### 1.1 多ENI配置

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
    tags:
      Environment: production
      Tier: frontend
  - eniID: eni-secondary
    subnetID: vsw-secondary-zone-b
    securityGroupID: sg-secondary
    primary: false
    zone: cn-hangzhou-b
    tags:
      Environment: production
      Tier: backend
  - eniID: eni-tertiary
    subnetID: vsw-tertiary-zone-c
    securityGroupID: sg-tertiary
    primary: false
    zone: cn-hangzhou-c
    tags:
      Environment: production
      Tier: database
  routingPolicy:
    defaultENI: eni-primary
    policyRoutes:
    - destination: 10.0.0.0/8
      eni: eni-primary
      priority: 100
    - destination: 172.16.0.0/12
      eni: eni-secondary
      priority: 200
    - destination: 192.168.0.0/16
      eni: eni-tertiary
      priority: 300
```

#### 1.2 网络隔离配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-network-isolation
  namespace: kube-system
data:
  isolation_config: |
    {
      "network_domains": [
        {
          "name": "frontend-domain",
          "cidr": "10.10.0.0/16",
          "eni_selector": {
            "tags": {
              "Tier": "frontend"
            }
          },
          "allowed_destinations": [
            "10.20.0.0/16",
            "10.30.0.0/16"
          ]
        },
        {
          "name": "backend-domain",
          "cidr": "10.20.0.0/16",
          "eni_selector": {
            "tags": {
              "Tier": "backend"
            }
          },
          "allowed_destinations": [
            "10.30.0.0/16"
          ]
        },
        {
          "name": "database-domain",
          "cidr": "10.30.0.0/16",
          "eni_selector": {
            "tags": {
              "Tier": "database"
            }
          },
          "allowed_destinations": []
        }
      ]
    }
```

### 2. 网络策略深度定制

#### 2.1 精细化访问控制

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: terway-advanced-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: secure-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: trusted-namespace
    - ipBlock:
        cidr: 192.168.0.0/16
        except:
        - 192.168.100.0/24
    ports:
    - protocol: TCP
      port: 8080
      endPort: 8090
  - from:
    - podSelector:
        matchLabels:
          role: monitor
    ports:
    - protocol: TCP
      port: 9090
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database-namespace
    ports:
    - protocol: TCP
      port: 3306
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: UDP
      port: 53
```

#### 2.2 安全组深度集成

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-security-group-sync
  namespace: kube-system
data:
  sg_sync_config: |
    {
      "sync_rules": [
        {
          "name": "web-tier-sg",
          "selector": {
            "labels": {
              "tier": "web"
            }
          },
          "security_groups": ["sg-web-public", "sg-web-private"],
          "rules": [
            {
              "direction": "ingress",
              "protocol": "tcp",
              "port_range": "80/80",
              "source_cidr": "0.0.0.0/0",
              "description": "Allow HTTP from anywhere"
            },
            {
              "direction": "ingress",
              "protocol": "tcp",
              "port_range": "443/443",
              "source_cidr": "0.0.0.0/0",
              "description": "Allow HTTPS from anywhere"
            },
            {
              "direction": "egress",
              "protocol": "tcp",
              "port_range": "3306/3306",
              "destination_cidr": "10.20.0.0/16",
              "description": "Allow MySQL to backend"
            }
          ]
        }
      ]
    }
```

### 3. 性能优化配置

#### 3.1 QoS和带宽管理

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-qos-optimization
  namespace: kube-system
data:
  qos_config: |
    {
      "bandwidth_management": {
        "default_egress_bandwidth": "1Gbps",
        "default_ingress_bandwidth": "1Gbps",
        "application_profiles": [
          {
            "name": "high-priority",
            "selector": {
              "labels": {
                "priority": "high"
              }
            },
            "egress_bandwidth": "10Gbps",
            "ingress_bandwidth": "10Gbps",
            "latency_sla": "10ms"
          },
          {
            "name": "medium-priority",
            "selector": {
              "labels": {
                "priority": "medium"
              }
            },
            "egress_bandwidth": "1Gbps",
            "ingress_bandwidth": "1Gbps",
            "latency_sla": "50ms"
          },
          {
            "name": "low-priority",
            "selector": {
              "labels": {
                "priority": "low"
              }
            },
            "egress_bandwidth": "100Mbps",
            "ingress_bandwidth": "100Mbps",
            "latency_sla": "100ms"
          }
        ]
      },
      "traffic_shaping": {
        "tc_rules": [
          {
            "interface": "eth0",
            "class_id": 1,
            "rate": "1Gbps",
            "ceil": "2Gbps",
            "burst": "32KB"
          },
          {
            "interface": "eth1",
            "class_id": 2,
            "rate": "500Mbps",
            "ceil": "1Gbps",
            "burst": "16KB"
          }
        ]
      }
    }
```

#### 3.2 网络延迟优化

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-latency-optimization
  namespace: kube-system
data:
  latency_config: |
    {
      "kernel_parameters": {
        "net.core.rmem_default": "262144",
        "net.core.wmem_default": "262144",
        "net.core.rmem_max": "16777216",
        "net.core.wmem_max": "16777216",
        "net.ipv4.tcp_rmem": "4096 65536 16777216",
        "net.ipv4.tcp_wmem": "4096 65536 16777216",
        "net.ipv4.tcp_congestion_control": "bbr",
        "net.ipv4.tcp_low_latency": "1"
      },
      "route_optimization": {
        "mtu_discovery": "want",
        "window_scaling": true,
        "timestamping": true,
        "sack": true
      }
    }
```

### 4. 混合云网络配置

#### 4.1 VPN隧道配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-hybrid-network
  namespace: kube-system
data:
  hybrid_config: |
    {
      "vpn_connections": [
        {
          "name": "on-premise-vpn",
          "remote_gateway": "203.0.113.1",
          "local_subnet": "10.0.0.0/8",
          "remote_subnet": "192.168.0.0/16",
          "ike_version": "IKEv2",
          "encryption_algorithm": "AES256",
          "authentication_method": "PSK",
          "pre_shared_key": "your-psk-here"
        }
      ],
      "route_propagation": {
        "enable": true,
        "propagate_routes": [
          {
            "destination": "192.168.0.0/16",
            "nexthop": "203.0.113.1",
            "metric": 100
          }
        ]
      }
    }
```

#### 4.2 网络地址转换

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-nat-config
  namespace: kube-system
data:
  nat_config: |
    {
      "snat_rules": [
        {
          "name": "internet-snat",
          "source_cidr": "10.0.0.0/8",
          "nat_gateway_id": "ngw-xxxxxxxxx",
          "eip_allocation_id": "eip-xxxxxxxxx"
        }
      ],
      "dnat_rules": [
        {
          "name": "web-dnat",
          "external_ip": "203.0.113.100",
          "external_port": "80",
          "internal_ip": "10.0.1.100",
          "internal_port": "8080",
          "protocol": "tcp"
        }
      ]
    }
```

---

## 🔧 扩展开发

### 1. 自定义CNI插件

```go
// Go语言自定义CNI插件示例
package main

import (
    "encoding/json"
    "fmt"
    "net"
    "runtime"
    
    "github.com/containernetworking/cni/pkg/skel"
    "github.com/containernetworking/cni/pkg/types"
    "github.com/containernetworking/cni/pkg/types/current"
    "github.com/containernetworking/cni/pkg/version"
)

type NetConf struct {
    types.NetConf
    Master string `json:"master"`
    Mode   string `json:"mode"`
    MTU    int    `json:"mtu"`
}

func cmdAdd(args *skel.CmdArgs) error {
    // 解析网络配置
    conf := NetConf{}
    if err := json.Unmarshal(args.StdinData, &conf); err != nil {
        return fmt.Errorf("failed to parse network configuration: %v", err)
    }
    
    // 创建网络接口
    hostInterface, containerInterface, err := createVethPair(conf.Master, args.ContainerID)
    if err != nil {
        return fmt.Errorf("failed to create veth pair: %v", err)
    }
    
    // 配置网络参数
    if err := configureInterface(containerInterface, conf.MTU); err != nil {
        return fmt.Errorf("failed to configure interface: %v", err)
    }
    
    // 返回网络配置结果
    result := &current.Result{
        CNIVersion: current.ImplementedSpecVersion,
        Interfaces: []*current.Interface{
            {
                Name:    hostInterface.Name,
                Mac:     hostInterface.HardwareAddr.String(),
                Sandbox: "",
            },
            {
                Name:    containerInterface.Name,
                Mac:     containerInterface.HardwareAddr.String(),
                Sandbox: args.Netns,
            },
        },
        IPs: []*current.IPConfig{
            {
                Version: "4",
                Address: net.IPNet{
                    IP:   net.ParseIP("10.244.1.10"),
                    Mask: net.CIDRMask(24, 32),
                },
                Gateway: net.ParseIP("10.244.1.1"),
                Interface: current.Int(1),
            },
        },
    }
    
    return types.PrintResult(result, conf.CNIVersion)
}

func main() {
    skel.PluginMain(cmdAdd, nil, nil, version.All, "Terway Custom CNI Plugin")
}
```

### 2. 网络控制器开发

```go
// 自定义网络控制器
package controller

import (
    "context"
    "time"
    
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/cache"
    "k8s.io/client-go/util/workqueue"
)

type NetworkController struct {
    client    kubernetes.Interface
    workqueue workqueue.RateLimitingInterface
    informer  cache.SharedIndexInformer
}

func NewNetworkController(client kubernetes.Interface) *NetworkController {
    // 创建Pod Informer
    informer := cache.NewSharedIndexInformer(
        &cache.ListWatch{
            ListFunc: func(options metav1.ListOptions) (runtime.Object, error) {
                return client.CoreV1().Pods("").List(context.TODO(), options)
            },
            WatchFunc: func(options metav1.ListOptions) (watch.Interface, error) {
                return client.CoreV1().Pods("").Watch(context.TODO(), options)
            },
        },
        &corev1.Pod{},
        time.Second*30,
        cache.Indexers{},
    )
    
    controller := &NetworkController{
        client:    client,
        workqueue: workqueue.NewNamedRateLimitingQueue(workqueue.DefaultControllerRateLimiter(), "pods"),
        informer:  informer,
    }
    
    // 设置事件处理器
    informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
        AddFunc: controller.enqueuePod,
        UpdateFunc: func(old, new interface{}) {
            controller.enqueuePod(new)
        },
        DeleteFunc: controller.enqueuePod,
    })
    
    return controller
}

func (c *NetworkController) enqueuePod(obj interface{}) {
    key, err := cache.MetaNamespaceKeyFunc(obj)
    if err != nil {
        return
    }
    c.workqueue.Add(key)
}

func (c *NetworkController) Run(stopCh <-chan struct{}) {
    defer c.workqueue.ShutDown()
    
    go c.informer.Run(stopCh)
    
    if !cache.WaitForCacheSync(stopCh, c.informer.HasSynced) {
        return
    }
    
    for i := 0; i < 5; i++ {
        go c.runWorker()
    }
    
    <-stopCh
}
```

---

## 📊 监控和指标

### 1. 自定义指标收集

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: terway-advanced-monitoring
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
    interval: 15s
    path: /metrics
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'terway_(eni|network|qos)_.*'
      action: keep
```

### 2. 高级告警规则

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: terway-advanced-alerts
  namespace: monitoring
spec:
  groups:
  - name: terway.advanced.rules
    rules:
    - alert: TerwayMultiENIFailure
      expr: rate(terway_multi_eni_creation_failures_total[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Terway multi ENI creation failures"
        description: "Multi ENI creation failure rate exceeds 5%"
    
    - alert: TerwayNetworkIsolationBreach
      expr: terway_network_isolation_violations_total > 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Terway network isolation breach detected"
        description: "Network isolation policy violations detected"
    
    - alert: TerwayQoSViolation
      expr: terway_qos_violations_total > 10
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Terway QoS violations detected"
        description: "Quality of Service violations exceeded threshold"
```

---

## 🚨 故障排查和调试

### 1. 高级诊断工具

```bash
# 1. 网络连通性测试
kubectl exec -it <pod-name> -n <namespace> -- traceroute 8.8.8.8

# 2. 带宽测试
kubectl exec -it <pod-name> -n <namespace> -- iperf3 -c <server-ip> -t 30

# 3. 网络策略验证
kubectl exec -it <pod-name> -n <namespace> -- nc -zv <target-ip> <port>

# 4. 性能分析
kubectl exec -it <terway-pod> -n kube-system -- perf record -g -p $(pgrep terway)
```

### 2. 调试配置示例

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: terway-debug-config
  namespace: kube-system
data:
  debug_config: |
    {
      "debug_level": "trace",
      "log_format": "json",
      "profiling": {
        "enable": true,
        "port": 6060,
        "block_profile_rate": 1
      },
      "packet_capture": {
        "enable": true,
        "interfaces": ["eth0", "eni*"],
        "filters": ["tcp port 80", "udp port 53"]
      }
    }
```

---

## 🧪 实践练习

### 练习1：多网卡配置
配置多ENI环境并实现网络隔离。

### 练习2：网络策略定制
实现复杂的网络访问控制策略。

### 练习3：性能优化
调整QoS参数并测量性能改善。

### 练习4：混合云集成
配置VPN连接实现混合云网络。

---

## 📚 扩展阅读

### 官方文档
- [Terway高级配置](https://github.com/AliyunContainerService/terway/tree/master/docs)
- [阿里云网络产品](https://help.aliyun.com/product/27537.html)
- [CNI插件开发](https://github.com/containernetworking/cni)

### 相关案例
- [Terway生产部署](../deployment/terway-deployment/)
- [Terway监控运维](../monitoring-operations/)
- [Terway安全加固](../security-hardening/)

### 进阶主题
- 自定义网络协议支持
- 机器学习驱动的网络优化
- 边缘计算网络架构
- 量子安全网络

---

## 📋 清理资源

```bash
# 删除测试环境
kubectl delete namespace terway-advanced

# 恢复默认配置
kubectl apply -f https://raw.githubusercontent.com/AliyunContainerService/terway/master/deploy/terway.yaml

# 清理自定义配置
kubectl delete configmap terway-advanced-config -n kube-system
```

---

> **💡 提示**: Terway高级特性提供了强大的自定义能力，但需要谨慎使用以确保稳定性和安全性。