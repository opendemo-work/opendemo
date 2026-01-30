# RegFlow 基础演示

## 概述

RegFlow 是一个 Kubernetes 原生的容器镜像注册表工作流引擎。它专门用于管理和自动化容器镜像注册表相关的任务，如镜像扫描、标记、迁移和生命周期管理。

## 架构

RegFlow 采用 Kubernetes CRD（Custom Resource Definition）实现，与 Kubernetes 生态系统无缝集成。主要组件包括：

- **RegFlow Controller**：监听并处理 RegFlow 自定义资源
- **Registry Adapters**：连接各种容器镜像注册表服务
- **Workflow Engine**：执行注册表工作流任务

## 快速开始

### 安装 RegFlow

```bash
# 添加 RegFlow Helm 仓库
helm repo add regflow https://charts.regflow.io

# 更新仓库
helm repo update

# 安装 RegFlow
helm install regflow regflow/regflow \
  --namespace regflow-system \
  --create-namespace
```

### 部署示例工作流

```bash
# 应用示例工作流定义
kubectl apply -f regflow-sample-workflow.yaml

# 检查工作流状态
kubectl get regflowworkflows
```

### 查看工作流详情

```bash
# 获取特定工作流的详细信息
kubectl describe regflowworkflow sample-regflow-workflow

# 查看工作流日志
kubectl logs -l app=regflow-controller
```

## 示例配置

### 基础工作流定义

```yaml
apiVersion: regflow.k8s.io/v1alpha1
kind: RegistryWorkflow
metadata:
  name: sample-regflow-workflow
spec:
  tasks:
    - name: scan-images
      image: registry-scanner:latest
      command: ["/bin/sh"]
      args: ["-c", "scan-registry --repo=my-registry.com/my-app --output=results.json"]
    - name: validate-images
      image: validator:latest
      command: ["/bin/sh"]
      args: ["-c", "validate --config=config.yaml --input=results.json"]
    - name: tag-images
      image: tagger:latest
      command: ["/bin/sh"]
      args: ["-c", "tag --source=validated.json --tags=stable,latest"]
  triggers:
    - type: schedule
      cron: "0 2 * * *"
    - type: webhook
      endpoint: /webhooks/registry-updates
```

## 使用场景

1. **自动镜像扫描**：定期扫描注册表中的镜像，检查安全漏洞
2. **镜像生命周期管理**：自动清理过期镜像，管理镜像标签
3. **跨注册表同步**：在多个注册表之间同步镜像
4. **合规性检查**：验证镜像是否符合组织的安全策略

## 最佳实践

- 使用命名空间隔离不同的 RegFlow 实例
- 定期备份 RegFlow 配置和工作流定义
- 监控 RegFlow 控制器的性能指标
- 使用 RBAC 控制对 RegFlow 资源的访问权限

## 故障排除

### 工作流未启动

检查 RegFlow 控制器是否正在运行：

```bash
kubectl get pods -n regflow-system
```

### 任务执行失败

查看具体的错误日志：

```bash
kubectl describe regflowworkflow <workflow-name>
```

## 扩展阅读

- [RegFlow 官方文档](https://docs.regflow.io)
- [Kubernetes CRD 指南](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [容器镜像最佳实践](https://cloud.google.com/architecture/best-practices-for-operating-containers#container_image_best_practices)