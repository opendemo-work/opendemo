# Kubernetes EFK 日志管理基础案例

## 什么是 EFK？

EFK 是 Elasticsearch、Fluentd 和 Kibana 的组合，用于 Kubernetes 集群的日志管理解决方案：

- **Elasticsearch**: 分布式搜索引擎，用于存储和索引日志数据
- **Fluentd**: 日志收集和转发工具，用于从 Kubernetes 集群收集日志
- **Kibana**: 数据可视化平台，用于查询和分析 Elasticsearch 中的日志

## 本案例包含的内容

- **elasticsearch.yaml**: Elasticsearch 部署配置
- **fluentd.yaml**: Fluentd DaemonSet 配置
- **kibana.yaml**: Kibana 部署配置

## 快速开始

### 1. 部署 Elasticsearch

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f elasticsearch.yaml
```

### 2. 验证 Elasticsearch 部署

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查 Elasticsearch Pod 状态
kubectl get pods -n efk -l app=elasticsearch

# 等待 Elasticsearch 就绪
kubectl wait --for=condition=ready pod -l app=elasticsearch -n efk --timeout=300s
```

### 3. 部署 Fluentd

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f fluentd.yaml
```

### 4. 验证 Fluentd 部署

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查 Fluentd Pod 状态
kubectl get pods -n efk -l app=fluentd
```

### 5. 部署 Kibana

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f kibana.yaml
```

### 6. 验证 Kibana 部署

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查 Kibana Pod 状态
kubectl get pods -n efk -l app=kibana

# 等待 Kibana 就绪
kubectl wait --for=condition=ready pod -l app=kibana -n efk --timeout=300s
```

### 7. 访问 Kibana UI

#### 7.1 使用 NodePort 访问

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Kibana UI
echo "http://$NODE_IP:30061"
```

#### 7.2 使用 Port Forward 访问

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl port-forward svc/kibana 5601:5601 -n efk
```

然后访问：http://localhost:5601

## 基本使用

### 1. 配置 Kibana 索引模式

首次登录 Kibana 后，需要配置索引模式：

1. 点击左侧菜单栏的 **Management** > **Stack Management** > **Data** > **Index Patterns**
2. 点击 **Create index pattern**
3. 输入索引模式名称：`kubernetes-*`
4. 选择时间字段：`@timestamp`
5. 点击 **Create index pattern**

### 2. 查看日志

1. 点击左侧菜单栏的 **Analytics** > **Discover**
2. 选择刚刚创建的索引模式 `kubernetes-*`
3. 你可以看到 Kubernetes 集群中的日志数据
4. 使用搜索栏和过滤器可以查询特定的日志

### 3. 创建可视化

1. 点击左侧菜单栏的 **Analytics** > **Visualize Library**
2. 点击 **Create visualization**
3. 选择可视化类型，例如 **Line**、**Bar** 或 **Pie**
4. 配置数据源和查询条件
5. 点击 **Save** 保存可视化

### 4. 创建仪表盘

1. 点击左侧菜单栏的 **Analytics** > **Dashboard**
2. 点击 **Create dashboard**
3. 点击 **Add** 添加之前创建的可视化
4. 调整布局和配置
5. 点击 **Save** 保存仪表盘

## 日志查询示例

### 1. 查询特定 Pod 的日志

```
kubernetes.pod_name: "my-pod"
```

### 2. 查询特定命名空间的日志

```
kubernetes.namespace_name: "default"
```

### 3. 查询特定容器的日志

```
kubernetes.container_name: "nginx"
```

### 4. 查询包含特定关键词的日志

```
message: "error" OR message: "warning"
```

### 5. 查询特定时间段的日志

使用 Kibana 界面上的时间选择器，或者在查询中指定时间范围：

```
@timestamp > "2024-01-20T00:00:00.000Z" AND @timestamp < "2024-01-21T00:00:00.000Z"
```

## 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
kubectl delete -f kibana.yaml
kubectl delete -f fluentd.yaml
kubectl delete -f elasticsearch.yaml
```

## 扩展建议

1. **添加持久化存储**: 为 Elasticsearch 添加持久化存储
2. **配置高可用性**: 扩展 Elasticsearch 集群到多个节点
3. **添加安全配置**: 为 EFK 堆栈配置 TLS 和认证
4. **配置日志保留策略**: 为 Elasticsearch 配置索引生命周期管理
5. **添加日志过滤**: 配置 Fluentd 过滤不必要的日志

## 相关链接

- [EFK 官方文档](https://www.elastic.co/guide/en/elastic-stack-overview/current/index.html)
- [Fluentd 官方文档](https://docs.fluentd.org/)
- [Kibana 官方文档](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Kubernetes 日志管理最佳实践](https://kubernetes.io/docs/concepts/cluster-administration/logging/)

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
