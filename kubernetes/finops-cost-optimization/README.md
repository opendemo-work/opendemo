# FinOps Cost Optimization

Kubernetes成本优化与FinOps实践。

## FinOps原则

```
FinOps生命周期:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Inform    │ -> │  Optimize   │ -> │   Operate   │
│   (告知)     │    │   (优化)    │    │   (运营)    │
└─────────────┘    └─────────────┘    └─────────────┘
      │                   │                  │
      ▼                   ▼                  ▼
  成本可见性          资源优化            持续监控
  成本分摊            折扣利用            预算告警
```

## 成本监控工具

### Kubecost安装
```bash
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace

# 访问
kubectl port-forward -n kubecost svc/kubecost-cost-analyzer 9090
```

## 资源优化策略

```yaml
# 资源请求/限制优化
apiVersion: apps/v1
kind: Deployment
metadata:
  name: optimized-app
spec:
  template:
    spec:
      containers:
        - name: app
          resources:
            requests:
              cpu: "100m"      # 基于实际使用设置
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
---
# 自动伸缩
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: optimized-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## 成本优化检查清单

- [ ] 设置资源请求和限制
- [ ] 启用HPA
- [ ] 使用Spot/Preemptible实例
- [ ] 清理未使用的资源
- [ ] 优化存储类型
- [ ] 设置预算告警

## 学习要点

1. FinOps方法论
2. 成本可见性
3. 资源优化
4. 自动伸缩
5. 预算管理
