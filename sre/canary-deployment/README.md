# Canary Deployment

金丝雀发布策略演示。

## 发布策略对比

```
部署策略演进:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Big Bang  │  │  Rolling    │  │   Canary    │  │   Blue/Green│
│   全量发布   │  │   滚动更新   │  │   金丝雀    │  │   蓝绿部署  │
├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤
│ 高风险      │  │ 中风险      │  │ 低风险      │  │ 低风险      │
│ 简单        │  │ 较简单      │  │ 复杂        │  │ 中等        │
│ 快速        │  │ 中等        │  │ 慢速        │  │ 快速        │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## Flagger金丝雀发布

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: frontend
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  service:
    port: 80
    gateways:
    - frontend-gateway
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
    webhooks:
    - name: load-test
      url: http://flagger-loadtester.test/
      timeout: 5s
      metadata:
        cmd: "hey -z 1m -q 10 -c 2 http://frontend-canary/"
```

## 流量渐进

```
金丝雀流量分配:
Time 0:  100% stable  0% canary
Time 5:   90% stable 10% canary
Time 10:  80% stable 20% canary
Time 15:  70% stable 30% canary
Time 20:  50% stable 50% canary  ← 最大权重
Time 25:   0% stable 100% canary ← 提升完成
```

## 自动回滚

```yaml
automatedRollback:
  enabled: true
  conditions:
    - metric: error_rate
      threshold: 1%
      duration: 2m
    - metric: latency_p99
      threshold: 1000ms
      duration: 1m
    - manual_trigger: true
```

## 学习要点

1. 金丝雀vs蓝绿对比
2. 流量切分策略
3. 指标监控与回滚
4. 渐进式发布流程
