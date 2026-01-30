# Kubernetes Grafana 监控可视化基础案例

## 什么是 Grafana？

Grafana 是一个开源的监控可视化平台，支持多种数据源，能够将数据转化为美观、可交互的仪表盘。

## 本案例包含的内容

- **grafana-config.yaml**: 创建命名空间和数据源配置
- **grafana-deployment.yaml**: Grafana Deployment 和 Service

## 前置条件

本案例需要与 Prometheus 集成，确保已部署 Prometheus 实例。

## 快速开始

### 1. 部署 Grafana 配置

```bash
kubectl apply -f grafana-config.yaml
```

### 2. 部署 Grafana 实例

```bash
kubectl apply -f grafana-deployment.yaml
```

### 3. 验证 Grafana 部署

```bash
# 检查 Pod 状态
kubectl get pods -n grafana

# 检查 Service 状态
kubectl get svc -n grafana
```

### 4. 访问 Grafana UI

#### 4.1 使用 NodePort 访问

```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Grafana UI
echo "http://$NODE_IP:30030"
```

#### 4.2 使用 Port Forward 访问

```bash
kubectl port-forward svc/grafana 3000:3000 -n grafana
```

然后访问：http://localhost:3000

### 5. 登录 Grafana

- **用户名**: admin
- **密码**: admin

## 基本使用

### 1. 查看数据源

登录后，点击左侧菜单栏的 **Configuration** > **Data Sources**，可以看到已配置的 Prometheus 数据源。

### 2. 导入仪表盘

Grafana 支持导入现成的仪表盘模板，以下是一些常用的 Kubernetes 仪表盘：

#### 2.1 导入 Kubernetes 节点仪表盘

1. 点击左侧菜单栏的 **+** > **Import**
2. 输入仪表盘 ID: **1860**（Kubernetes Node Exporter Full）
3. 选择 Prometheus 数据源
4. 点击 **Import**

#### 2.2 导入 Kubernetes Pod 仪表盘

1. 点击左侧菜单栏的 **+** > **Import**
2. 输入仪表盘 ID: **6417**（Kubernetes Pod Resources）
3. 选择 Prometheus 数据源
4. 点击 **Import**

#### 2.3 导入 Kubernetes 集群仪表盘

1. 点击左侧菜单栏的 **+** > **Import**
2. 输入仪表盘 ID: **12970**（Kubernetes Cluster）
3. 选择 Prometheus 数据源
4. 点击 **Import**

### 3. 创建自定义仪表盘

1. 点击左侧菜单栏的 **+** > **Dashboard**
2. 点击 **Add a new panel**
3. 在查询编辑器中输入 PromQL 查询，例如：
   ```
   sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, namespace)
   ```
4. 点击 **Apply** 保存面板
5. 点击右上角的 **Save Dashboard** 保存仪表盘

## 常用仪表盘推荐

| 仪表盘名称 | 仪表盘 ID | 描述 |
|-----------|-----------|------|
| Kubernetes Node Exporter Full | 1860 | 完整的节点监控仪表盘 |
| Kubernetes Pod Resources | 6417 | Pod 资源监控仪表盘 |
| Kubernetes Cluster | 12970 | 集群概览仪表盘 |
| Prometheus 2.0 Overview | 3662 | Prometheus 自身监控仪表盘 |
| Grafana Metrics | 240 | Grafana 自身监控仪表盘 |

## 清理资源

```bash
kubectl delete -f grafana-deployment.yaml
kubectl delete -f grafana-config.yaml
```

## 扩展建议

1. **添加持久化存储**: 将 Grafana 的存储从 emptyDir 改为 PersistentVolumeClaim
2. **配置 HTTPS**: 为 Grafana 启用 HTTPS
3. **添加告警**: 配置 Grafana Alerting
4. **使用 LDAP 认证**: 集成企业 LDAP 认证
5. **配置自动备份**: 定期备份 Grafana 配置和仪表盘

## 相关链接

- [Grafana 官方文档](https://grafana.com/docs/)
- [Grafana 仪表盘市场](https://grafana.com/grafana/dashboards/)
- [Prometheus 官方文档](https://prometheus.io/docs/introduction/overview/)
- [Kubernetes 监控最佳实践](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/)
