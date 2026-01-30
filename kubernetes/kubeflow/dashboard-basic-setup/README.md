# Kubeflow Dashboard基础安装与配置

## 概述

本Demo演示如何安装和配置Kubeflow Central Dashboard，这是Kubeflow平台的统一访问入口和管理界面。Dashboard提供了Web界面来访问和管理Kubeflow的各个组件。

**所属组件**: Kubeflow Central Dashboard  
**难度级别**: beginner  
**核心功能**: Dashboard安装、部署配置、访问设置

## 前置条件

### 环境要求
- Kubernetes集群：v1.26或更高版本
- kubectl：已配置并能访问集群
- 集群资源：至少2个CPU核心，4GB内存
- 存储：支持动态PV provisioning

### Kubeflow要求
- Kubeflow平台：v1.8或更高版本
- 已安装kustomize工具（v3.2.0+）

### 权限要求
- 集群管理员权限或足够的RBAC权限创建Namespace、Deployment等资源

## 资源清单说明

### manifests/namespace.yaml
创建kubeflow命名空间，用于部署Dashboard相关资源。

### manifests/dashboard-deployment.yaml  
Dashboard的Deployment配置，定义Dashboard容器的运行参数。

### manifests/dashboard-service.yaml
Dashboard的Service配置，暴露Dashboard服务端口。

### manifests/dashboard-configmap.yaml
Dashboard配置文件，包含UI配置选项。

## 部署步骤

### 1. 创建命名空间

首先创建专用的Kubeflow命名空间：

```bash
kubectl create namespace kubeflow
```

### 2. 应用Dashboard配置

应用Dashboard的ConfigMap配置：

```bash
kubectl apply -f manifests/dashboard-configmap.yaml -n kubeflow
```

### 3. 部署Dashboard

部署Dashboard Deployment和Service：

```bash
kubectl apply -f manifests/dashboard-deployment.yaml -n kubeflow
kubectl apply -f manifests/dashboard-service.yaml -n kubeflow
```

### 4. 等待部署完成

检查Pod状态，等待Dashboard Pod运行：

```bash
kubectl wait --for=condition=ready pod -l app=dashboard -n kubeflow --timeout=300s
```

## 验证和测试

### 1. 检查部署状态

查看Dashboard Pod状态：

```bash
kubectl get pods -n kubeflow -l app=dashboard
```

**预期输出**：
```
NAME                         READY   STATUS    RESTARTS   AGE
dashboard-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

### 2. 检查Service

查看Dashboard Service：

```bash
kubectl get svc -n kubeflow -l app=dashboard
```

**预期输出**：
```
NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
dashboard   ClusterIP   10.xxx.xxx.xxx   <none>        8080/TCP   2m
```

### 3. 访问Dashboard

#### 方式一：使用Port-Forward

最简单的访问方式，适合测试和开发：

```bash
kubectl port-forward -n kubeflow svc/dashboard 8080:8080
```

然后在浏览器访问：`http://localhost:8080`

#### 方式二：使用NodePort（可选）

如果需要外部访问，可以修改Service类型为NodePort：

```bash
kubectl patch svc dashboard -n kubeflow -p '{"spec":{"type":"NodePort"}}'
```

获取NodePort端口：

```bash
kubectl get svc dashboard -n kubeflow -o jsonpath='{.spec.ports[0].nodePort}'
```

#### 方式三：使用Ingress（生产推荐）

生产环境建议配置Ingress进行访问控制和HTTPS加密。

## 监控和日志

### 查看Dashboard日志

```bash
kubectl logs -n kubeflow -l app=dashboard --tail=100 -f
```

### 查看Dashboard事件

```bash
kubectl get events -n kubeflow --sort-by='.lastTimestamp' | grep dashboard
```

### 常见日志信息

- `Starting dashboard server on port 8080` - Dashboard成功启动
- `Connected to backend services` - 后端服务连接成功

## 故障排查

### 问题1：Pod无法启动

**症状**：Pod状态为Pending或CrashLoopBackOff

**排查步骤**：
1. 查看Pod详情：`kubectl describe pod -n kubeflow -l app=dashboard`
2. 查看事件：检查是否有资源不足或镜像拉取失败
3. 查看日志：`kubectl logs -n kubeflow -l app=dashboard`

**常见原因**：
- 镜像拉取失败：检查网络和镜像仓库访问
- 资源不足：增加节点资源或调整资源请求

### 问题2：无法访问Dashboard

**症状**：浏览器无法连接或连接超时

**排查步骤**：
1. 确认Service存在：`kubectl get svc -n kubeflow dashboard`
2. 确认Port-Forward正在运行
3. 检查防火墙规则
4. 验证Dashboard Pod日志无错误

## 清理步骤

### 删除Dashboard资源

```bash
kubectl delete -f manifests/dashboard-service.yaml -n kubeflow
kubectl delete -f manifests/dashboard-deployment.yaml -n kubeflow
kubectl delete -f manifests/dashboard-configmap.yaml -n kubeflow
```

### 删除命名空间（可选）

如果要完全清理：

```bash
kubectl delete namespace kubeflow
```

**注意**：删除命名空间会删除其中的所有资源，请谨慎操作。

## 扩展参考

### 官方文档
- [Kubeflow Dashboard官方文档](https://www.kubeflow.org/docs/components/central-dash/overview/)
- [Kubeflow安装指南](https://www.kubeflow.org/docs/started/getting-started/)

### 进阶配置
- 配置HTTPS访问和证书
- 集成企业身份认证（LDAP/OAuth）
- 自定义Dashboard主题和Logo
- 配置多租户隔离

### 关联Demo
- [Dashboard RBAC权限配置] - 多用户和命名空间权限管理
- [Notebook服务器创建] - 从Dashboard创建Jupyter Notebook
- [Pipeline管理] - 通过Dashboard管理ML Pipeline

## 最佳实践

1. **生产环境部署**
   - 使用Ingress配置HTTPS访问
   - 启用身份认证和授权
   - 配置资源限制和请求
   - 启用高可用部署（多副本）

2. **安全建议**
   - 定期更新Dashboard镜像版本
   - 配置Network Policy限制流量
   - 启用审计日志
   - 使用Secret管理敏感配置

3. **性能优化**
   - 根据负载调整副本数
   - 配置HPA自动扩缩容
   - 优化后端服务连接池
   - 启用缓存机制

## 版本说明

本Demo基于以下版本测试：
- Kubernetes: v1.26+
- Kubeflow: v1.8+
- Dashboard版本: 以官方发布版本为准

不同版本可能存在配置差异，请参考对应版本的官方文档。
