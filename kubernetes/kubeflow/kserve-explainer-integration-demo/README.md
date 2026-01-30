# KServe 模型解释器集成 Demo

## 简介
本演示展示了如何在 Kubernetes 上使用 KServe 集成模型解释器（Explainer），为机器学习模型提供预测结果的可解释性。通过此 Demo，用户可以部署一个支持解释功能的推理服务，并调用 `/explain` 接口获取预测背后的特征重要性。

## 学习目标
- 理解 KServe 中 Explainer 的工作原理
- 掌握如何配置 InferenceService 资源以启用模型解释
- 学会调用解释接口并解析响应
- 实践 KServe 最佳实践：分离推理与解释、使用标准 CRD

## 环境要求
- Python 3.9 或更高版本
- Kubernetes 集群（v1.25+）
- kubectl 已配置并连接到集群
- Istio v1.18+（已安装并启用）
- KServe v0.11.0 已安装
- Helm（可选，用于安装 KServe）

## 安装依赖步骤

1. **安装 KServe**（若未安装）：
```bash
# 添加 KServe Helm 仓库
helm repo add kserve https://kserve.github.io/kserve/
helm repo update

# 安装 KServe 控制器
helm install kserve kserve/kserve --version=0.11.0 -n kserve --create-namespace
```

2. **验证安装**：
```bash
kubectl get pods -n kserve
# 应看到 kserve-controller-manager 正在运行
```

3. **安装示例模型依赖（本地）**：
```bash
pip install numpy seldon-core alibi
```

## 文件说明
- `inferenceservice-explainer.yaml`：定义带有解释器的 KServe InferenceService
- `input-sample.json`：用于发送请求的输入数据样本

## 逐步实操指南

### 第一步：部署 InferenceService
```bash
kubectl apply -f inferenceservice-explainer.yaml -n kserve-test
```

> 如果命名空间不存在，先创建：
> ```bash
> kubectl create namespace kserve-test
> ```

**预期输出**：
```bash
inferenceservice.serving.kserve.io/boston-explainer created
```

### 第二步：等待服务就绪
```bash
kubectl wait --for=condition=Ready inferenceservice/boston-explainer -n kserve-test --timeout=600s
```

**预期输出**：
```bash
inferenceservice.serving.kserve.io/boston-explainer condition met
```

### 第三步：获取入口网关地址
```bash
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export SERVICE_HOSTNAME=$(kubectl get inferenceservice boston-explainer -n kserve-test -o jsonpath='{.status.url}' | cut -d '/' -f 3)
```

### 第四步：发送解释请求
```bash
curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${INGRESS_HOST}/v2/models/boston-explainer/explain -d @input-sample.json
```

## 代码解析

### `inferenceservice-explainer.yaml`
- 使用 `explainer` 字段声明解释器配置
- 采用 `AlibiAnchorsTabular` 解释算法，适用于表格数据
- 模型使用预训练的 sklearn 回归模型（Boston 房价）
- 所有路径指向公开可用的模型/解释器存储位置（模拟实际部署）

### `input-sample.json`
- 包含符合模型输入格式的特征向量
- `instances` 字段传递原始数据
- KServe 自动将请求路由至解释器容器

## 预期输出示例
```json
{
  "explanation": {
    "anchor": ["RM > 6.5", "LSTAT <= 10"],
    "precision": 0.92,
    "coverage": 0.75
  }
}
```
表示：当 RM > 6.5 且 LSTAT <= 10 时，该预测锚点具有 92% 准确率和 75% 覆盖率。

## 常见问题解答

**Q: 请求返回 404？**
A: 检查 `SERVICE_HOSTNAME` 是否正确，确认 InferenceService 处于 Ready 状态。

**Q: 解释器启动失败？**
A: 确认镜像路径是否可达，或更换为本地构建的解释器镜像。

**Q: 如何自定义解释算法？**
A: 修改 `explainer.type` 为 `alibi-anchor-image` 或 `alibi-lime-tabular`，并调整参数。

## 扩展学习建议
- 尝试集成 SHAP 解释器
- 在图像分类模型中应用 Anchors 解释
- 使用 KFServing SDK 编程式生成 InferenceService YAML
- 结合 Prometheus 监控解释请求延迟