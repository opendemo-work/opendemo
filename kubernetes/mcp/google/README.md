# 谷歌 MCP 案例

## 简介

本目录包含谷歌在 MCP (Model Control Plane) 领域的实践案例，展示如何在 Kubernetes 环境中部署和管理基于谷歌技术栈的 MCP 系统。

## 案例列表

### 1. Gemini 大模型 MCP 部署

**功能说明**：在 Kubernetes 集群中部署基于谷歌 Gemini 大模型的 MCP 系统

**难度**：intermediate

**功能覆盖**：
- ✅ 模型生命周期管理
- ✅ 模型版本控制
- ✅ 模型部署与扩缩容
- ✅ 模型监控与告警
- ✅ 模型访问控制
- ✅ 多模型支持

**配置文件**：
- `gemini-mcp-deployment.yaml` - Gemini MCP 服务部署配置
- `gemini-mcp-service.yaml` - Gemini MCP 服务暴露配置
- `configmap.yaml` - 配置管理
- `secret.yaml` - 密钥管理
- `rbac.yaml` - 权限控制

## 部署步骤

### 1. 准备工作

- Kubernetes 集群 (v1.23+)
- Helm 3.0+
- Gemini API 密钥
- 适当的 GPU 资源（推荐）
- Google Cloud 账号

### 2. 部署 Gemini MCP

```bash
# 1. 配置密钥
kubectl create secret generic gemini-mcp-secrets \
  --from-literal=api-key=YOUR_GEMINI_API_KEY \
  --namespace mcp-system

# 2. 部署 MCP 服务
kubectl apply -f gemini-mcp-deployment.yaml
kubectl apply -f gemini-mcp-service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f rbac.yaml

# 3. 验证部署
kubectl get pods -n mcp-system
kubectl get svc -n mcp-system
```

### 3. 访问 MCP 服务

```bash
# 获取服务地址
MCP_SERVICE_IP=$(kubectl get svc gemini-mcp-service -n mcp-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 测试 API
curl -X GET http://$MCP_SERVICE_IP:8080/api/v1/models
```

## 监控与维护

### 监控指标

- MCP 服务响应时间
- 模型推理延迟
- 模型调用成功率
- 资源使用情况
- 模型健康状态

### 日志管理

- MCP 服务日志
- 模型调用日志
- 错误日志
- 审计日志

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| API 密钥错误 | 检查 secret 配置 |
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

- [Google Gemini](https://gemini.google.com/)
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai)
- [Google Cloud Native](https://cloud.google.com/kubernetes-engine)
- [Kubernetes 官方文档](https://kubernetes.io/docs/)

## 许可证

MIT License