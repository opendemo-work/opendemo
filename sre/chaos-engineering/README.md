# Chaos Engineering

混沌工程实践演示，通过受控实验提升系统可靠性。

## 什么是混沌工程

```
混沌工程原则:
┌─────────────────────────────────────────────────────────┐
│  1. 建立稳定状态的假设                                    │
│  2. 引入真实世界的故障                                    │
│  3. 在生产环境进行实验                                    │
│  4. 自动化持续运行                                        │
│  5. 最小化爆炸半径                                        │
└─────────────────────────────────────────────────────────┘
```

## 故障类型矩阵

```
故障分类:
┌─────────────────┬─────────────────┬─────────────────┐
│   基础设施层     │    应用层        │    依赖层       │
├─────────────────┼─────────────────┼─────────────────┤
│ • 节点故障      │ • 服务崩溃       │ • 网络延迟      │
│ • 磁盘故障      │ • 内存泄漏       │ • DNS故障      │
│ • 网络分区      │ • 线程死锁       │ • 数据库慢查   │
│ • 时钟漂移      │ • CPU饱和        │ • 缓存失效     │
└─────────────────┴─────────────────┴─────────────────┘
```

## Chaos Mesh实战

```bash
# 安装Chaos Mesh
curl -sSL https://mirrors.chaos-mesh.org/latest/install.sh | bash

# 网络延迟实验
kubectl apply -f - <<EOF
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay
spec:
  action: delay
  mode: one
  selector:
    namespaces:
      - default
    labelSelectors:
      app: web
  delay:
    latency: "100ms"
    correlation: "100"
    jitter: "0ms"
  duration: "5m"
EOF

# Pod故障实验
kubectl apply -f - <<EOF
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-failure
spec:
  action: pod-failure
  mode: fixed-percent
  value: "50"
  selector:
    namespaces:
      - default
    labelSelectors:
      app: api
  duration: "10m"
EOF
```

## Litmus混沌实验

```yaml
# Litmus实验定义
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: nginx-chaos
spec:
  appinfo:
    appns: 'default'
    applabel: 'app=nginx'
    appkind: 'deployment'
  # 定义稳态探针
  experiments:
  - name: pod-delete
    spec:
      probe:
      - name: "check-app-access"
        type: "httpProbe"
        mode: "Continuous"
        runProperties:
          probeTimeout: "5s"
          retry: 2
          interval: "5s"
          probePollingTimeout: "5s"
        httpProbe/inputs:
          url: "http://nginx.default.svc.cluster.local:80"
          insecureSkipVerify: false
          method:
            get:
              criteria: "=="
              responseCode: "200"
      components:
        env:
        - name: TOTAL_CHAOS_DURATION
          value: '30'
        - name: CHAOS_INTERVAL
          value: '10'
        - name: FORCE
          value: 'false'
```

## 游戏日演练

```
游戏日流程:
Week-1: 计划
  ├── 确定实验范围
  ├── 定义稳态指标
  └── 准备回滚方案

Week-2: 实验
  ├── 小范围验证
  ├── 扩大实验范围
  └── 记录系统行为

Week-3: 复盘
  ├── 分析实验结果
  ├── 制定改进措施
  └── 更新运行手册
```

## 安全边界控制

```yaml
# 自动停止条件
abortConditions:
  - metric: error_rate
    threshold: 5%
    duration: 2m
  - metric: latency_p99
    threshold: 2000ms
    duration: 1m
  - metric: availability
    threshold: 95%
    duration: 30s
```

## 学习要点

1. 混沌工程五大原则
2. 故障注入工具对比
3. 实验设计与执行
4. 安全边界控制
5. 游戏日演练组织
