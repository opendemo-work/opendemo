# Kubernetes Workloads

Kubernetes工作负载管理深度演示，涵盖Deployment、StatefulSet、DaemonSet等。

## 工作负载类型

```
工作负载选择指南:
                    需要持久存储?
                         │
            ┌────────────┼────────────┐
            否                        是
            │                         │
      需要调度到      需要每个节点运行?    StatefulSet
      所有节点?            │
            │        ┌────┴────┐
       ┌────┴────┐   是        否
       是        否  │          │
       │          │ DaemonSet  Deployment
    DaemonSet   Deployment (无状态)
    (监控代理)   (Web应用)
```

## Deployment进阶

### 滚动更新策略
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # 可超出25%
      maxUnavailable: 25%  # 最少保持75%可用
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: web
        image: nginx:1.20
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]
```

### 自动扩缩容
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

## StatefulSet管理

### 有状态应用部署
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kafka
spec:
  serviceName: kafka-headless
  replicas: 3
  podManagementPolicy: Parallel
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0
  template:
    spec:
      containers:
      - name: kafka
        image: confluentinc/cp-kafka:7.0
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: KAFKA_BROKER_ID
          value: "$(POD_NAME)"
```

## Job与CronJob

```yaml
# 并行批处理任务
apiVersion: batch/v1
kind: Job
metadata:
  name: data-processing
spec:
  parallelism: 5           # 同时运行5个Pod
  completions: 10          # 总共完成10个
  completionMode: Indexed  # 索引模式
  template:
    spec:
      containers:
      - name: processor
        image: data-processor:latest
        env:
        - name: JOB_COMPLETION_INDEX
          valueFrom:
            fieldRef:
              fieldPath: metadata.annotations['batch.kubernetes.io/job-completion-index']
      restartPolicy: OnFailure
```

## 学习要点

1. 工作负载选型策略
2. 滚动更新与回滚
3. 有状态应用管理
4. 批处理任务设计
5. 自动扩缩容策略
