# Kubeflow Notebook服务器创建与配置

## 概述

本Demo演示如何在Kubeflow平台中创建和配置Jupyter Notebook服务器。Kubeflow Notebooks提供了基于Kubernetes的Web开发环境，支持数据科学家和机器学习工程师进行交互式开发。

**所属组件**: Kubeflow Notebooks  
**难度级别**: beginner  
**核心功能**: Notebook服务器创建、资源配置、镜像选择

## 前置条件

### 环境要求
- Kubernetes集群：v1.26或更高版本
- Kubeflow平台：v1.8或更高版本
- kubectl：已配置并能访问集群
- 集群资源：至少2个CPU核心，4GB内存

### 存储要求
- 已配置StorageClass用于Notebook持久化存储
- 支持ReadWriteOnce访问模式的PV

### 权限要求
- 有权限在目标命名空间创建Notebook资源
- 有权限创建PVC

## 资源清单说明

### manifests/notebook.yaml
定义Notebook CRD资源，包含：
- Notebook名称和命名空间
- 容器镜像配置
- 资源请求和限制
- 持久化卷配置
- 网络和服务配置

## 部署步骤

### 1. 创建命名空间（如果不存在）

```bash
kubectl create namespace kubeflow-user-example-com
```

### 2. 应用Notebook配置

应用Notebook资源定义：

```bash
kubectl apply -f manifests/notebook.yaml
```

### 3. 等待Notebook就绪

等待Notebook Pod启动完成：

```bash
kubectl wait --for=condition=ready pod -l notebook-name=jupyter-notebook -n kubeflow-user-example-com --timeout=300s
```

## 验证和测试

### 1. 检查Notebook状态

查看Notebook资源状态：

```bash
kubectl get notebook -n kubeflow-user-example-com
```

**预期输出**：
```
NAME               AGE   READY
jupyter-notebook   2m    True
```

### 2. 检查Pod状态

查看Notebook Pod：

```bash
kubectl get pods -n kubeflow-user-example-com -l notebook-name=jupyter-notebook
```

**预期输出**：
```
NAME                                READY   STATUS    RESTARTS   AGE
jupyter-notebook-0                  1/1     Running   0          2m
```

### 3. 检查Service

查看Notebook Service：

```bash
kubectl get svc -n kubeflow-user-example-com -l notebook-name=jupyter-notebook
```

### 4. 访问Notebook

#### 方式一：通过Kubeflow Dashboard

1. 登录Kubeflow Dashboard
2. 进入Notebooks页面
3. 找到创建的Notebook
4. 点击"CONNECT"按钮访问Jupyter

#### 方式二：Port-Forward直接访问

```bash
kubectl port-forward -n kubeflow-user-example-com svc/jupyter-notebook-service 8888:80
```

在浏览器访问：`http://localhost:8888`

### 5. 验证Notebook功能

在Jupyter中创建新Notebook，测试基本功能：

```python
# 测试Python环境
import sys
print(f"Python version: {sys.version}")

# 测试常用库
import numpy as np
import pandas as pd
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
```

## 监控和日志

### 查看Notebook日志

```bash
kubectl logs -n kubeflow-user-example-com -l notebook-name=jupyter-notebook --tail=50 -f
```

### 查看Notebook事件

```bash
kubectl get events -n kubeflow-user-example-com --sort-by='.lastTimestamp' | grep jupyter-notebook
```

### 检查资源使用

查看Notebook Pod的资源使用情况：

```bash
kubectl top pod -n kubeflow-user-example-com -l notebook-name=jupyter-notebook
```

## 故障排查

### 问题1：Notebook无法启动

**症状**：Pod处于Pending或ImagePullBackOff状态

**排查步骤**：
1. 检查镜像是否可访问
2. 验证资源配额是否足够
3. 检查PVC是否成功绑定

```bash
kubectl describe notebook jupyter-notebook -n kubeflow-user-example-com
kubectl describe pod -n kubeflow-user-example-com -l notebook-name=jupyter-notebook
```

### 问题2：无法访问Jupyter界面

**症状**：浏览器无法打开或连接超时

**排查步骤**：
1. 确认Service已创建
2. 检查Port-Forward是否正常
3. 验证网络策略配置

```bash
kubectl get svc -n kubeflow-user-example-com
kubectl describe svc jupyter-notebook-service -n kubeflow-user-example-com
```

### 问题3：持久化数据丢失

**症状**：重启后数据丢失

**排查步骤**：
1. 检查PVC状态
2. 验证卷挂载配置
3. 确认StorageClass配置

```bash
kubectl get pvc -n kubeflow-user-example-com
kubectl describe pvc workspace-jupyter-notebook -n kubeflow-user-example-com
```

## 清理步骤

### 删除Notebook

```bash
kubectl delete -f manifests/notebook.yaml
```

### 删除持久化卷（可选）

如果需要删除数据：

```bash
kubectl delete pvc workspace-jupyter-notebook -n kubeflow-user-example-com
```

### 删除命名空间（可选）

```bash
kubectl delete namespace kubeflow-user-example-com
```

## 扩展参考

### 官方文档
- [Kubeflow Notebooks官方文档](https://www.kubeflow.org/docs/components/notebooks/)
- [Jupyter Notebook文档](https://jupyter-notebook.readthedocs.io/)

### 进阶配置
- 使用自定义Docker镜像
- 配置GPU资源
- 集成数据卷和外部存储
- 配置Notebook Server扩展
- 多用户环境配置

### 关联Demo
- [Notebook自定义镜像使用] - 使用自定义容器镜像
- [Notebook GPU资源分配] - 配置GPU资源支持
- [Notebook持久化存储] - 数据卷挂载和持久化配置
- [Pipeline Python组件开发] - 在Notebook中开发Pipeline组件

## 最佳实践

1. **镜像选择**
   - 使用官方提供的稳定镜像
   - 根据需求选择合适的基础镜像（minimal/scipy/tensorflow/pytorch）
   - 定期更新镜像版本

2. **资源配置**
   - 根据工作负载设置合理的CPU和内存限制
   - 预留足够的磁盘空间
   - 考虑使用GPU时的资源分配

3. **数据管理**
   - 重要数据使用持久化卷存储
   - 定期备份工作成果
   - 使用版本控制管理代码

4. **安全建议**
   - 使用命名空间隔离不同用户
   - 配置适当的RBAC权限
   - 定期更新Notebook镜像
   - 避免在Notebook中存储敏感信息

## 版本说明

本Demo基于以下版本测试：
- Kubernetes: v1.26+
- Kubeflow: v1.8+
- Jupyter Notebook Server: 以Kubeflow提供的镜像版本为准
