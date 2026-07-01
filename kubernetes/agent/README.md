# Kubernetes Agent

Kubernetes集群智能代理与自动化运维演示。

## 什么是K8s Agent

K8s Agent是运行在集群中的智能组件，负责：
- 节点监控与自愈
- 资源自动调优
- 故障检测与恢复
- 安全审计与合规

## Agent架构模式

```
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Manager   │  │   Policy    │  │   Events    │     │
│  │   (策略)     │  │   Engine    │  │   Store     │     │
│  └──────┬──────┘  └─────────────┘  └─────────────┘     │
└─────────┼───────────────────────────────────────────────┘
          │
          │ gRPC/WebSocket
          │
┌─────────┼───────────────────────────────────────────────┐
│         ▼              Worker Nodes                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │    Agent    │  │    Agent    │  │    Agent    │     │
│  │  (DaemonSet)│  │  (DaemonSet)│  │  (DaemonSet)│     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │            │
│         ▼                ▼                ▼            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Node      │  │   Node      │  │   Node      │     │
│  │  Metrics    │  │  Metrics    │  │  Metrics    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## 核心功能

### 1. 节点自愈
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agent-config
data:
  config.yaml: |
    healing:
      enabled: true
      checks:
        - name: disk-pressure
          threshold: 85
          action: cleanup
        - name: memory-pressure
          threshold: 90
          action: evict-pods
        - name: pid-pressure
          threshold: 1000
          action: restart-containerd
```

### 2. 资源优化
```yaml
# Agent自动调整资源请求
optimization:
  enabled: true
  strategies:
    - type: vertical-pod-autoscaler
      mode: auto
    - type: node-problem-detector
      mode: active
```

## 部署Agent

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用DaemonSet部署
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: k8s-agent
spec:
  selector:
    matchLabels:
      app: k8s-agent
  template:
    metadata:
      labels:
        app: k8s-agent
    spec:
      serviceAccountName: agent-sa
      containers:
      - name: agent
        image: k8s-agent:latest
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
        volumeMounts:
        - name: config
          mountPath: /etc/agent
        - name: host-root
          mountPath: /host
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: agent-config
      - name: host-root
        hostPath:
          path: /
EOF
```

## 常用Agent工具

| 工具 | 用途 | 部署方式 |
|------|------|----------|
| node-problem-detector | 节点故障检测 | DaemonSet |
| kube-bench | CIS安全基线检查 | CronJob |
| kube-hunter | 渗透测试 | Manual |
| falco | 运行时安全 | DaemonSet |
| tetragon | eBPF安全观测 | DaemonSet |

## 学习要点

1. Agent架构设计模式
2. 节点监控与自愈机制
3. 安全审计自动化
4. 资源优化策略
5. 大规模集群管理

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
