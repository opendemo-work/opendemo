# KubeEdge Edge Computing

边缘计算K8s解决方案实践。

## KubeEdge架构

```
云边协同架构:
┌─────────────────────────────────────────────────────────┐
│                      Cloud Core                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  CloudHub    │  │  EdgeController│  │ DeviceController│ │
│  │  (WebSocket) │  │  (Sync)      │  │  (Device Mgmt)│  │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└──────────────────────────┬──────────────────────────────┘
                           │ QUIC / WebSocket
┌──────────────────────────┴──────────────────────────────┐
│                       Edge Core                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  EdgeHub     │  │  MetaManager │  │  Edged       │   │
│  │  (Connect)   │  │  (Local DB)  │  │  (Kubelet)   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │  EventBus    │  │  ServiceBus│                       │
│  │  (MQTT)      │  │  (HTTP)    │                       │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                           │ MQTT
┌──────────────────────────┴──────────────────────────────┐
│                      Edge Devices                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Sensor   │  │ Camera   │  │ Actuator │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## 安装KubeEdge

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 安装Cloud Core
keadm init --advertise-address=192.168.1.100

# 边缘节点加入
keadm join --cloudcore-ipport=192.168.1.100:10000 \
  --token=<token>

# 验证
kubectl get nodes
```

## 边缘应用部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: edge-app
  labels:
    app: edge-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: edge-app
  template:
    metadata:
      labels:
        app: edge-app
    spec:
      nodeSelector:
        node-role.kubernetes.io/edge: ""
      containers:
        - name: app
          image: nginx:alpine
          resources:
            limits:
              memory: "256Mi"
              cpu: "500m"
```

## 设备管理

```yaml
apiVersion: devices.kubeedge.io/v1alpha2
kind: Device
metadata:
  name: temperature-sensor
spec:
  deviceModelRef:
    name: sensor-model
  nodeSelector:
    nodeSelectorTerms:
      - matchExpressions:
          - key: ""
            operator: In
            values:
              - edge-node-1
  propertyVisitors:
    - propertyName: temperature
      collectCycle: 5000
      reportCycle: 5000
```

## 学习要点

1. 云边协同架构
2. 离线自治能力
3. 设备管理
4. 边缘应用部署
5. 网络通信

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
