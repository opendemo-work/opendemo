# Amazon MCP 案例

## 简介

本目录包含Amazon在MCP (Model Control Plane)领域的实践案例，展示如何在Kubernetes环境中部署和管理基于Amazon技术栈的MCP系统。

## 案例列表

### 1. Bedrock 大模型 MCP 部署

**功能说明**：在Kubernetes集群中部署基于Amazon Bedrock大模型的MCP系统

**难度**：intermediate

**功能覆盖**：
- ✅ 模型生命周期管理
- ✅ 模型版本控制
- ✅ 模型部署与扩缩容
- ✅ 模型监控与告警
- ✅ 模型访问控制
- ✅ 多模型支持

**配置文件**：
- `bedrock-mcp-deployment.yaml` - Bedrock MCP服务部署配置
- `bedrock-mcp-service.yaml` - Bedrock MCP服务暴露配置
- `configmap.yaml` - 配置管理
- `secret.yaml` - 密钥管理
- `rbac.yaml` - 权限控制

## 部署步骤

### 1. 准备工作

- Kubernetes集群 (v1.23+)
- Helm 3.0+
- Amazon Bedrock API密钥
- 适当的GPU资源（推荐）
- AWS账号和凭证

### 2. 部署Bedrock MCP

```bash
# 1. 配置密钥
kubectl create secret generic bedrock-mcp-secrets \
  --from-literal=aws-access-key=YOUR_AWS_ACCESS_KEY \
  --from-literal=aws-secret-key=YOUR_AWS_SECRET_KEY \
  --namespace mcp-system

# 2. 部署MCP服务
kubectl apply -f bedrock-mcp-deployment.yaml
kubectl apply -f bedrock-mcp-service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f rbac.yaml

# 3. 验证部署
kubectl get pods -n mcp-system
kubectl get svc -n mcp-system
```

### 3. 访问MCP服务

```bash
# 获取服务地址
MCP_SERVICE_IP=$(kubectl get svc bedrock-mcp-service -n mcp-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 测试API
curl -X GET http://$MCP_SERVICE_IP:8080/api/v1/models
```

## 监控与维护

### 监控指标

- MCP服务响应时间
- 模型推理延迟
- 模型调用成功率
- 资源使用情况
- 模型健康状态

### 日志管理

- MCP服务日志
- 模型调用日志
- 错误日志
- 审计日志

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| API密钥错误 | 检查secret配置 |
| 资源不足 | 调整部署的资源请求和限制 |
| 网络连接失败 | 检查网络策略和防火墙规则 |
| 模型部署失败 | 检查模型配置和依赖 |

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
- [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
- [Amazon EKS](https://aws.amazon.com/eks/)
- [Kubernetes官方文档](https://kubernetes.io/docs/)

## 许可证

MIT License