<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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
🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
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
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl create namespace kserve-test
```
**预期输出:** `namespace/kserve-test created`

### 步骤2: 部署基于并发数的扩缩容服务
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f autoscale-concurrency.yaml
```
**预期输出:** `inferenceservice.serving.kserve.io/concurrency-model created`

### 步骤3: 验证服务状态
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
kubectl get inferenceservice concurrency-model -n kserve-test
```
**预期输出:** STATUS 应为 `Ready`

### 步骤4: 部署基于CPU的扩缩容服务
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f autoscale-cpu.yaml
```
**预期 output:** `inferenceservice.serving.kserve.io/cpu-model created`

### 步骤5: 查看扩缩容配置
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
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
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
