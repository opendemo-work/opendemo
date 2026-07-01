<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# KServe A/B 测试演示

本演示展示如何使用 KServe 在 Kubernetes 上实现机器学习模型的 A/B 测试，通过 Istio 的流量路由功能将请求按比例分发到不同版本的模型服务中。

## 学习目标

- 理解 KServe 如何支持多版本模型部署
- 掌握使用 InferenceService 进行 A/B 测试的配置方法
- 学会通过流量权重控制模型版本的请求分配
- 实践基于 Istio 的灰度发布策略

## 环境要求

- Python >= 3.8（用于发送测试请求）
- Kubernetes 集群（v1.25+）
- kubectl 命令行工具（v1.25+）
- Istio v1.18 或更高版本（已集成在 KServe 中）
- KServe v0.11.0 安装就绪
- 可访问的镜像仓库（如 Docker Hub）

## 安装依赖步骤

1. 安装 kubectl：https://kubernetes.io/docs/tasks/tools/install-kubectl/
2. 部署 Kubernetes 集群（推荐使用 Kind 或 Minikube 本地测试）
3. 安装 Istio：
   ```bash
   istioctl install --set profile=default -y
   ```
4. 安装 KServe：
   ```bash
   git clone https://github.com/kserve/kserve
   kubectl apply -f kserve/config/crd
   kubectl apply -f kserve/config/rbac
   kubectl apply -f kserve/config/manager
   ```

## 文件说明

- `ab-testing-inferenceservice.yaml`：定义 A/B 测试的 InferenceService 资源，包含两个模型版本（v1 和 v2），流量按 70%/30% 分配
- `test-request.py`：Python 脚本，向推理服务发送测试请求并打印响应结果

## 逐步实操指南

### 步骤 1：部署 A/B 测试服务

```bash
kubectl apply -f ab-testing-inferenceservice.yaml
```

**预期输出：**
```
inferenceservice.serving.kserve.io/ab-test-model created
```

### 步骤 2：等待服务就绪

```bash
kubectl wait --for=condition=Ready inferenceservice/ab-test-model --timeout=300s
```

**预期输出：**
```
inferenceservice.serving.kserve.io/ab-test-model condition met
```

### 步骤 3：获取服务入口网关 IP

```bash
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export SERVICE_HOSTNAME=$(kubectl get inferenceservice ab-test-model -o jsonpath='{.status.url}' | cut -d'/' -f3)
```

### 步骤 4：运行测试脚本发送请求

```bash
python test-request.py
```

**预期输出：**
```
请求响应来自模型版本: v1
请求响应来自模型版本: v2
...（根据流量权重分布）
```

## 代码解析

### ab-testing-inferenceservice.yaml

- `spec.predictor.componentSpecs`：定义两个独立的模型预测器（v1 和 v2），使用不同的容器镜像
- `traffic` 字段：设置流量权重，70% 到 v1，30% 到 v2
- 每个版本可通过 `tag` 标识，在响应中返回自身版本信息便于调试

### test-request.py

- 使用 `requests` 库向 KServe 服务发送 POST 请求
- 解析返回 JSON 中的 `version` 字段以判断请求被哪个模型处理
- 模拟多次请求观察流量分布是否符合预期

## 预期输出示例

运行 `python test-request.py` 后输出可能如下：
```
请求响应来自模型版本: v1
请求响应来自模型版本: v1
请求响应来自模型版本: v2
请求响应来自模型版本: v1
...（共10次）
```

约 70% 请求应返回 v1，30% 返回 v2。

## 常见问题解答

**Q: 为什么无法访问服务？**
A: 确保 Istio IngressGateway 已正确暴露 IP，并且 `SERVICE_HOSTNAME` 设置无误。检查服务状态：`kubectl get inferenceservice`

**Q: 流量分配不准确？**
A: KServe 使用 Istio 的加权路由，小样本下可能存在偏差。增加请求次数（如 100+）后统计更接近设定比例。

**Q: 如何更新流量比例？**
A: 修改 `ab-testing-inferenceservice.yaml` 中的 `traffic[*].percent` 并重新应用即可。

## 扩展学习建议

- 尝试结合 Prometheus 监控各版本模型的延迟与成功率
- 使用 KNative 的自动扩缩容特性优化资源使用
- 实现基于请求头的路由（如用户ID哈希）进行更精细的 A/B 测试
- 探索 KServe 的 Transformer 模式实现预处理逻辑分流

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

```bash
./scripts/apply.sh
```

### 检查状态

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
