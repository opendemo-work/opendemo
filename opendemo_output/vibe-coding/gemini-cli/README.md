# Gemini CLI 案例

## 简介

本案例展示如何在 Kubernetes 集群中部署 Gemini CLI，一个基于 Google Gemini 大模型的 AI 辅助编码命令行工具，用于提升开发效率和代码质量。

## 功能说明

**Gemini CLI**：在 Kubernetes 集群中部署 Gemini CLI 工具，用于 AI 辅助编码、代码生成、智能补全等功能

**难度**：intermediate

**功能覆盖**：
- ✅ AI 代码生成
- ✅ 智能代码补全
- ✅ 代码审查与分析
- ✅ 文档生成
- ✅ 命令行集成
- ✅ 监控与告警

## 配置文件

- `gemini-cli-deployment.yaml` - Gemini CLI 部署配置
- `gemini-cli-service.yaml` - Gemini CLI 服务暴露配置
- `configmap.yaml` - 配置管理
- `secret.yaml` - 密钥管理
- `rbac.yaml` - 权限控制
- `metadata.json` - 案例元数据

## 部署步骤

### 1. 准备工作

- Kubernetes 集群 (v1.23+)
- Helm 3.0+
- Google Cloud 账号
- Gemini API 密钥
- 代码仓库访问凭证

### 2. 部署 Gemini CLI

```bash
# 1. 配置密钥
kubectl create secret generic gemini-cli-secrets \
  --from-literal=gemini-api-key=YOUR_GEMINI_API_KEY \
  --from-literal=github-token=YOUR_GITHUB_TOKEN \
  --namespace gemini-cli-system

# 2. 部署 Gemini CLI
kubectl apply -f rbac.yaml
kubectl apply -f configmap.yaml
kubectl apply -f gemini-cli-deployment.yaml
kubectl apply -f gemini-cli-service.yaml

# 3. 验证部署
kubectl get pods -n gemini-cli-system
kubectl get svc -n gemini-cli-system
```

### 3. 使用 Gemini CLI

```bash
# 获取服务地址
GEMINI_CLI_SERVICE_IP=$(kubectl get svc gemini-cli-service -n gemini-cli-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 设置 Gemini CLI 配置
export GEMINI_API_URL=http://$GEMINI_CLI_SERVICE_IP:8080

# 生成代码
gemini generate "create a function to calculate factorial"

# 代码审查
gemini review ./src

# 智能补全
gemini complete ./src/main.py
```

## 架构说明

### 核心组件

1. **Gemini CLI 服务**：AI 辅助编码服务
2. **代码分析引擎**：代码审查和分析
3. **Gemini 模型推理**：Google Gemini 模型调用和推理
4. **存储服务**：代码和配置存储

### 数据流

1. 用户执行 Gemini CLI 命令 → 发送请求到 Gemini 服务 → Gemini 模型推理 → 返回结果
2. 用户提交代码 → 代码分析 → 生成建议 → 返回结果

## 监控与维护

### 监控指标

- Gemini CLI 服务响应时间
- Gemini 模型推理延迟
- 代码分析成功率
- 资源使用情况

### 日志管理

- Gemini CLI 服务日志
- 代码分析日志
- 模型推理日志
- 错误日志

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| API 密钥错误 | 检查 secret 配置 |
| 资源不足 | 调整部署的资源请求和限制 |
| 代码分析失败 | 检查代码仓库访问权限 |
| 模型推理超时 | 调整模型参数和超时设置 |

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
- [Kubernetes 官方文档](https://kubernetes.io/docs/)

## 许可证

MIT License