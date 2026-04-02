# Chaos Engineering Production

生产级混沌工程实践。

## 混沌工程原则

混沌工程通过受控实验验证系统韧性：

```
混沌实验流程:
1. 定义稳态假设 (Define Steady State)
   ↓
2. 引入真实世界事件 (Introduce Real-world Events)
   ↓
3. 验证假设 (Verify Hypothesis)
   ↓
4. 分析结果 (Analyze Results)
   ↓
5. 修复并改进 (Fix and Improve)
```

## Chaos Mesh安装

```bash
# Helm安装
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh \
  --namespace chaos-mesh \
  --create-namespace

# 验证
kubectl get pods -n chaos-mesh
```

## 常见故障实验

```yaml
# Pod故障 - 随机杀死Pod
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill
spec:
  action: pod-kill
  mode: one
  duration: "30s"
  selector:
    labelSelectors:
      app: backend
  scheduler:
    cron: "@every 5m"

---
# 网络延迟
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay
spec:
  action: delay
  mode: all
  selector:
    labelSelectors:
      app: backend
  delay:
    latency: "100ms"
    correlation: "100"
    jitter: "0ms"
  duration: "5m"

---
# CPU压力测试
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: cpu-stress
spec:
  mode: all
  selector:
    labelSelectors:
      app: backend
  stressors:
    cpu:
      workers: 4
      load: 80
  duration: "10m"
```

## 实验安全检查清单

```markdown
✅ 已确认实验范围
✅ 已通知相关团队
✅ 已设置自动回滚
✅ 已准备监控看板
✅ 已定义停止条件
✅ 非生产环境已验证
```

## 自动化混沌实验

```bash
# CI/CD集成
chaos run experiment.yaml --report-path=./report

# 安全检查
chaos verify experiment.yaml

# 自动回滚
chaos run experiment.yaml --rollback-on-failure
```

## 学习要点

1. 混沌工程原则
2. 故障注入类型
3. 安全实验规范
4. 自动化集成
5. 可观测性
