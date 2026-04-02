# KubeSkoop Network Diagnosis

KubeSkoop容器网络诊断工具演示。

## 什么是KubeSkoop

阿里云开源的容器网络诊断工具，自动发现网络连通性问题：

```
诊断能力:
┌─────────────────────────────────────────────────────────┐
│                   KubeSkoop Agent                       │
│              (DaemonSet部署)                             │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ 链路发现 │  │ 策略检查 │  │ 抓包分析 │  │ 延迟测试 │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
├─────────────────────────────────────────────────────────┤
│                   Diagnosis Engine                      │
│              (自动问题定位)                               │
└─────────────────────────────────────────────────────────┘
```

## 安装部署

```bash
# 安装KubeSkoop
kubectl apply -f https://raw.githubusercontent.com/alibaba/kubeskoop/main/deploy/skoop.yaml

# 安装CLI
curl -fsSL https://raw.githubusercontent.com/alibaba/kubeskoop/main/install.sh | bash
```

## 网络诊断

```bash
# 诊断Pod间连通性
skoop diagnose --source pod/nginx-xxx --destination pod/mysql-xxx

# 检查Service连通性
skoop diagnose --source pod/nginx-xxx --destination svc/mysql

# 检查NodePort
skoop diagnose --source node/node1 --destination node/node2 --dport 30080
```

## 学习要点

1. 容器网络拓扑发现
2. 网络策略验证
3. eBPF抓包分析
4. 延迟诊断方法
