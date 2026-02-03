# KServe 自动扩缩容配置演示

## 简介
本演示展示了如何在 KServe 中配置模型推理服务的自动扩缩容行为，包括基于请求并发数和CPU使用率的两种典型场景。KServe 是构建在 Knative 和 Istio 之上的高性能机器学习模型服务框架。

## 学习目标
- 理解 KServe 的自动扩缩容机制
- 掌握基于并发请求数的扩缩容配置方法
- 掌握基于 CPU 使用率的扩缩容配置方法
- 学会验证扩缩容效果

## 环境要求
- Kubernetes 集群 (v1.23+)
- kubectl 命令行工具
- KServe v0.10.0 已安装
- Istio v1.16+ 已安装
- Knative Serving v1.9+ 已安装

## 安装依赖步骤
```bash
# 1. 安装 Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=default -y

# 2. 安装 Knative Serving
kubectl apply -f https://github.com/knative/serving/releases/download/v1.9.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/v1.9.0/serving-core.yaml

# 3. 安装 KServe
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.10.0/kserve.yaml
```

## 文件说明
- `autoscale-concurrency.yaml`: 基于请求并发数的自动扩缩容配置
- `autoscale-cpu.yaml`: 基于 CPU 使用率的自动扩缩容配置

## 逐步实操指南

### 步骤1: 创建命名空间
```bash
kubectl create namespace kserve-test
```
**预期输出:** `namespace/kserve-test created`

### 步骤2: 部署基于并发数的扩缩容服务
```bash
kubectl apply -f autoscale-concurrency.yaml
```
**预期输出:** `inferenceservice.serving.kserve.io/concurrency-model created`

### 步骤3: 验证服务状态
```bash
kubectl get inferenceservice concurrency-model -n kserve-test
```
**预期输出:** STATUS 应为 `Ready`

### 步骤4: 部署基于CPU的扩缩容服务
```bash
kubectl apply -f autoscale-cpu.yaml
```
**预期 output:** `inferenceservice.serving.kserve.io/cpu-model created`

### 步骤5: 查看扩缩容配置
```bash
kubectl get inferenceservice -n kserve-test -o yaml
```

## 代码解析

### autoscale-concurrency.yaml 关键点
- `targetUtilizationPercentage: 70`：当平均并发请求数达到目标值的70%时开始扩容
- `containerConcurrency: 100`：每个Pod最多处理100个并发请求
- `minReplicas: 1`：最少保持1个副本
- `maxReplicas: 10`：最多扩展到10个副本

### autoscale-cpu.yaml 关键点
- `metrics: cpu`：使用CPU使用率作为扩缩容指标
- `target: 50`：目标CPU使用率为50%
- 资源限制设置确保HPA有据可依

## 预期输出示例
```bash
NAME               URL                                           READY   PREV   LATEST   AGE
concurrency-model  http://concurrency-model.kserve-test.example.com  True    1      1        2m
cpu-model          http://cpu-model.kserve-test.example.com           True    1      1        1m
```

## 常见问题解答

**Q: 扩缩容没有触发？**
A: 检查是否安装了 Knative Serving Autoscaler，并确认监控组件正常运行。

**Q: 如何查看当前指标？**
A: 使用命令 `kubectl get hpa -n kserve-test` 查看水平Pod自动伸缩器状态。

**Q: 为什么最小副本数不能设为0？**
A: KServe 支持0副本，但需要启用 `enable-scale-to-zero` 特性门控。

## 扩展学习建议
- 学习 Knative Pod Autoscaler 的工作原理
- 尝试自定义指标进行扩缩容
- 探索 KServe 的多模型服务和A/B测试功能
- 研究生产环境中的容量规划策略