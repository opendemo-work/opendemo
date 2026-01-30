# Amazon Agent 案例

## 简介

本目录包含Amazon在AI Agent领域的实践案例，展示如何在Kubernetes环境中部署和管理基于Amazon技术栈的AI Agent系统。

## 案例列表

### 1. Bedrock 大模型 Agent 部署

**功能说明**：在Kubernetes集群中部署基于Amazon Bedrock的AI Agent服务

**难度**：intermediate

**功能覆盖**：
- ✅ Bedrock大模型部署
- ✅ Agent服务架构设计
- ✅ 多模态能力集成
- ✅ 知识库对接
- ✅ 权限管理与安全控制
- ✅ 监控与可观测性

**配置文件**：
- `bedrock-agent-deployment.yaml` - Bedrock Agent服务部署配置
- `bedrock-agent-service.yaml` - Bedrock Agent服务暴露配置
- `configmap.yaml` - 配置管理
- `secret.yaml` - 密钥管理
- `rbac.yaml` - 权限控制

## 部署步骤

### 1. 准备工作

- Kubernetes集群 (v1.23+)
- Helm 3.0+
- Amazon Bedrock API密钥
- 适当的GPU资源（推荐）

### 2. 部署Bedrock Agent

```bash
# 1. 配置密钥
kubectl create secret generic bedrock-agent-secrets \
  --from-literal=api-key=YOUR_BEDROCK_API_KEY \
  --namespace agent-system

# 2. 部署Agent服务
kubectl apply -f bedrock-agent-deployment.yaml
kubectl apply -f bedrock-agent-service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f rbac.yaml

# 3. 验证部署
kubectl get pods -n agent-system
kubectl get svc -n agent-system
```

### 3. 访问Agent服务

```bash
# 获取服务地址
AGENT_SERVICE_IP=$(kubectl get svc bedrock-agent-service -n agent-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 测试API
curl -X POST http://$AGENT_SERVICE_IP:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，我是开发者"}'
```

## 监控与维护

### 监控指标

- Agent服务响应时间
- 模型推理延迟
- API调用成功率
- 资源使用情况

### 日志管理

- Agent服务日志
- 模型调用日志
- 错误日志

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| API密钥错误 | 检查secret配置 |
| 资源不足 | 调整部署的资源请求和限制 |
| 网络连接失败 | 检查网络策略和防火墙规则 |

## 版本兼容性

- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

## 相关资源

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon AWS AI](https://aws.amazon.com/ai/)
- [Kubernetes官方文档](https://kubernetes.io/docs/)

## 许可证

MIT License