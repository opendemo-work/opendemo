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
