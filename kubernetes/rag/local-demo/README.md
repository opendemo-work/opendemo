<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
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
