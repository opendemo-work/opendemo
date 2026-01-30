# RAG 平台案例

## 简介

本案例展示如何在 Kubernetes 集群中部署一个完整的 RAG (Retrieval-Augmented Generation) 平台，用于增强大语言模型的知识检索能力。

## 功能说明

**RAG 平台**：在 Kubernetes 集群中部署完整的 RAG 系统，包括文档检索、向量存储、模型推理等组件

**难度**：intermediate

**功能覆盖**：
- ✅ 文档管理与索引
- ✅ 向量存储
- ✅ 检索增强生成
- ✅ 知识库管理
- ✅ API 接口
- ✅ 监控与告警

## 配置文件

- `manifests/rag-deployment.yaml` - RAG 平台部署配置
- `manifests/rag-service.yaml` - RAG 平台服务暴露配置
- `manifests/configmap.yaml` - 配置管理
- `manifests/secret.yaml` - 密钥管理
- `manifests/rbac.yaml` - 权限控制
- `meta/metadata.json` - 案例元数据（CLI / 工具使用）

## 部署步骤

### 1. 准备工作

- Kubernetes 集群 (v1.23+)
- Helm 3.0+
- 适当的 GPU 资源（推荐）
- 向量数据库（如 Pinecone、Milvus 等）API 密钥
- 大语言模型 API 密钥

### 2. 部署 RAG 平台

```bash
# 1. 配置密钥
kubectl create secret generic rag-platform-secrets \
  --from-literal=llm-api-key=YOUR_LLM_API_KEY \
  --from-literal=vector-db-api-key=YOUR_VECTOR_DB_API_KEY \
  --namespace rag-system

# 2. 部署 RAG 平台（一次性应用所有清单）
kubectl apply -f manifests/

# 3. 验证部署
kubectl get pods -n rag-system
kubectl get svc -n rag-system
```

### 3. 访问 RAG 平台

```bash
# 获取服务地址
RAG_SERVICE_IP=$(kubectl get svc rag-platform-service -n rag-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 测试 API
curl -X GET http://$RAG_SERVICE_IP:8080/api/v1/health

# 上传文档
curl -X POST http://$RAG_SERVICE_IP:8080/api/v1/documents \
  -H "Content-Type: application/json" \
  -d '{"name": "example.pdf", "url": "https://example.com/example.pdf"}'

# 发送查询
curl -X POST http://$RAG_SERVICE_IP:8080/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?"}'
```

## 架构说明

### 核心组件

1. **RAG 服务**：处理用户查询，协调检索和生成过程
2. **文档处理器**：负责文档解析、分块和向量化
3. **向量存储**：存储文档向量表示，支持相似度搜索
4. **大语言模型**：基于检索结果生成回答
5. **API 网关**：提供 RESTful API 接口

### 数据流

1. 用户上传文档 → 文档处理器 → 向量化 → 向量存储
2. 用户发送查询 → RAG 服务 → 向量存储检索 → 大语言模型生成 → 返回结果

## 监控与维护

### 监控指标

- RAG 服务响应时间
- 文档处理成功率
- 检索准确率
- 生成质量
- 资源使用情况

### 日志管理

- RAG 服务日志
- 文档处理日志
- 检索日志
- 错误日志

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| API 密钥错误 | 检查 secret 配置 |
| 资源不足 | 调整部署的资源请求和限制 |
| 检索结果不准确 | 优化向量存储配置和检索参数 |
| 生成质量差 | 调整大语言模型参数和提示模板 |

## 版本兼容性

- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

## 相关资源

- [RAG 技术文档](https://arxiv.org/abs/2005.11401)
- [LangChain](https://www.langchain.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Pinecone](https://www.pinecone.io/)
- [Milvus](https://milvus.io/)
- [Kubernetes 官方文档](https://kubernetes.io/docs/)

## 许可证

MIT License