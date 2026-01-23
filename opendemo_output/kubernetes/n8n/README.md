# basic-n8n：n8n 自动化平台（本地 + Kubernetes）

## 简介

本案例展示如何在本地环境和 Kubernetes 集群中部署 n8n，一个强大的开源自动化工具，用于创建工作流和自动化任务，并通过一套统一的示例帮助你从入门到实战。

### 你将学到什么

- **部署实践**：如何在 Windows/Mac 上本地运行 n8n，以及在 Kubernetes 集群中以生产方案部署
- **工作流设计**：通过完整的案例集，掌握 Webhook、定时任务、数据处理、外部服务集成等常见场景
- **运维与监控**：了解健康检查、日志与监控配置，形成可观察性的基础实践

## 功能说明

**n8n 工作流平台**：部署完整的 n8n 系统，用于创建和管理自动化工作流

**难度**：intermediate

**功能覆盖**：
- ✅ 工作流创建与管理
- ✅ 节点集成（400+ 集成节点）
- ✅ 触发器配置（Webhook、定时、事件驱动）
- ✅ 数据处理与转换
- ✅ API 接口
- ✅ 监控与告警
- ✅ 自定义代码执行

## 学习路径

1. **本地快速体验**：先按照 `LOCAL_DEPLOYMENT.md` 在自己的 Windows/Mac 环境中启动一个 n8n 实例，熟悉基本界面和概念。
2. **练习基础工作流**：参考 `WORKFLOW_EXAMPLES.md` 中的基础案例（定时任务、Webhook、HTTP 请求），在本地实例上反复实践。
3. **进阶自动化与数据处理**：继续尝试自动化与数据处理类案例，逐步组合多个节点完成真实业务流程。
4. **迁移到 Kubernetes**：当你对 n8n 使用较为熟悉后，按照本 `README.md` 中的 Kubernetes 部署章节，将 n8n 迁移到集群环境运行。
5. **完善监控与运维**：结合配置文件中的健康检查与 Prometheus 抓取配置，为 n8n 实例增加可观察性与告警能力。

## 部署方式

本案例提供两种部署方式：

| 部署方式 | 适用场景 | 文档 |
|---------|---------|------|
| **本地部署** | 个人学习、开发测试、小团队使用 | [LOCAL_DEPLOYMENT.md](local/LOCAL_DEPLOYMENT.md) |
| **Kubernetes 部署** | 生产环境、高可用、企业级部署 | 本文档 |

---

## 文件导航

- **README.md**：本文件，提供 n8n 案例的整体介绍，重点讲解 Kubernetes 部署与架构说明。
- **local/LOCAL_DEPLOYMENT.md**：本地部署实战手册，详细覆盖 Windows/Mac（Docker、npm、Homebrew 等多种方式）。
- **workflows/WORKFLOW_EXAMPLES.md**：工作流案例库，按基础、自动化、数据处理、高级四大类组织，所有案例可以在本地或 Kubernetes 环境中复现。
- **manifests/n8n-deployment.yaml / manifests/n8n-service.yaml**：n8n 在 Kubernetes 中的核心 Deployment 与 Service 定义，用于实际部署到集群。
- **manifests/configmap.yaml / manifests/secret.yaml / manifests/rbac.yaml**：配置、密钥和 RBAC 权限清单，为生产级部署提供配置与安全基础。
- **meta/metadata.json**：demo 元数据描述，供 CLI / 管理工具识别和展示，不参与实际部署。

## 本地部署（Windows/Mac）

> **详细文档请参考**：[LOCAL_DEPLOYMENT.md](local/LOCAL_DEPLOYMENT.md)

### 快速开始（Docker 方式）

**Windows PowerShell**：
```powershell
mkdir C:\n8n-data
docker run -d --name n8n -p 5678:5678 -v C:\n8n-data:/home/node/.n8n n8nio/n8n
```

**Mac/Linux**：
```bash
mkdir -p ~/.n8n
docker run -d --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

启动后访问：http://localhost:5678

### 其他安装方式

- **npm 安装**：`npm install -g n8n && n8n`
- **Homebrew (Mac)**：`brew install n8n && n8n`

---

## Kubernetes 部署

### 配置文件

- `manifests/n8n-deployment.yaml` - n8n 部署配置
- `manifests/n8n-service.yaml` - n8n 服务暴露配置
- `manifests/configmap.yaml` - 配置管理
- `manifests/secret.yaml` - 密钥管理
- `manifests/rbac.yaml` - 权限控制
- `metadata.json` - 案例元数据

### 1. 准备工作

- Kubernetes 集群 (v1.23+)
- Helm 3.0+
- 持久存储 (PV/PVC)
- 域名（可选，用于 Ingress 配置）

### 2. 部署 n8n

```bash
# 1. 配置密钥
kubectl create secret generic n8n-secrets \
  --from-literal=n8n-encryption-key=YOUR_ENCRYPTION_KEY \
  --from-literal=postgres-password=YOUR_POSTGRES_PASSWORD \
  --namespace n8n-system

# 2. 部署 n8n（一次性应用所有清单）
kubectl apply -f manifests/

# 3. 验证部署
kubectl get pods -n n8n-system
kubectl get svc -n n8n-system
```

### 3. 访问 n8n

```bash
# 获取服务地址
N8N_SERVICE_IP=$(kubectl get svc n8n-service -n n8n-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 访问 n8n 界面
echo "n8n 界面地址: http://$N8N_SERVICE_IP:5678"

# 测试 API
curl -X GET http://$N8N_SERVICE_IP:5678/api/v1/workflows
```

## 架构说明

### 核心组件

1. **n8n 核心**：工作流引擎和 Web 界面
2. **数据库**：存储工作流、执行历史等数据
3. **队列**：管理任务执行
4. **存储**：保存文件和数据

### 数据流

1. 用户创建工作流 → 保存到数据库
2. 触发器触发 → 执行工作流 → 处理数据 → 保存执行结果

## 监控与维护

### 监控指标

- n8n 服务响应时间
- 工作流执行成功率
- 队列长度
- 资源使用情况

### 日志管理

- n8n 服务日志
- 工作流执行日志
- 错误日志

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 数据库连接失败 | 检查数据库配置和网络连接 |
| 工作流执行失败 | 检查工作流配置和节点设置 |
| 资源不足 | 调整部署的资源请求和限制 |
| 持久存储问题 | 检查 PVC 配置和存储提供商 |

## 版本兼容性

- Kubernetes v1.23.x+ 完全兼容
- Kubernetes v1.24.x+ 完全兼容
- Kubernetes v1.25.x+ 完全兼容
- Kubernetes v1.26.x+ 完全兼容
- Kubernetes v1.27.x+ 完全兼容
- Kubernetes v1.28.x+ 完全兼容
- Kubernetes v1.29.x+ 完全兼容

---

## n8n 工作流案例

### 案例 1：定时发送邮件提醒

**场景**：每天早上 9 点发送工作提醒邮件

**配置步骤**：
1. 添加 **Schedule Trigger** 节点，设置每天 09:00 执行
2. 添加 **Send Email** 节点，配置 SMTP 和邮件内容
3. 连接节点并激活工作流

### 案例 2：Webhook 接收并处理数据

**场景**：接收外部系统的 Webhook 数据并处理

**配置步骤**：
1. 添加 **Webhook** 节点，设置 HTTP 方法为 POST
2. 添加 **Function** 节点进行数据转换
3. 添加目标节点（如数据库、API 等）

### 案例 3：监控 GitHub 仓库

**场景**：监控 GitHub 仓库的新 Issue 并发送通知

**配置步骤**：
1. 添加 **GitHub Trigger** 节点，选择 Issue 事件
2. 添加 **Slack/Email** 节点发送通知
3. 配置 GitHub 凭据并激活

### 案例 4：自动化数据同步

**场景**：定时从 API 获取数据并同步到数据库

**配置步骤**：
1. 添加 **Schedule Trigger** 节点，设置执行间隔
2. 添加 **HTTP Request** 节点获取数据
3. 添加 **Function** 节点处理数据
4. 添加 **Database** 节点存储数据

### 案例 5：表单数据处理

**场景**：处理网站表单提交，发送确认邮件并记录

**配置步骤**：
1. 添加 **Webhook** 节点接收表单数据
2. 添加 **Send Email** 节点发送确认邮件
3. 添加 **Google Sheets** 节点记录数据

> **更多工作流案例**：请参考 [WORKFLOW_EXAMPLES.md](WORKFLOW_EXAMPLES.md) 中的详细案例配置

---

## 相关资源

- [n8n 官方文档](https://docs.n8n.io/)
- [n8n GitHub 仓库](https://github.com/n8n-io/n8n)
- [n8n 工作流模板](https://n8n.io/workflows/)
- [n8n 社区论坛](https://community.n8n.io/)
- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [本地部署指南](local/LOCAL_DEPLOYMENT.md)
- [工作流案例集](workflows/WORKFLOW_EXAMPLES.md)

## 许可证

MIT License
