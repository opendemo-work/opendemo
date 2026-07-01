# Kubernetes RBAC 基础案例

## 什么是 RBAC？

基于角色的访问控制（Role-Based Access Control，简称 RBAC）是 Kubernetes 中用于管理资源访问权限的机制。它允许管理员通过定义角色和角色绑定来精确控制谁可以访问哪些资源。

## 本案例包含的内容

- **rbac.yaml**: RBAC 配置文件，包含：
  - ServiceAccount: 用于运行 Pod 的身份
  - Role: 命名空间级别的权限定义
  - RoleBinding: 将 Role 绑定到 ServiceAccount
  - ClusterRole: 集群级别的权限定义
  - ClusterRoleBinding: 将 ClusterRole 绑定到 ServiceAccount

## 快速开始

### 1. 部署 RBAC 配置

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f rbac.yaml
```

### 2. 验证资源创建

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
kubectl get serviceaccount demo-sa
kubectl get role demo-role
kubectl get rolebinding demo-rolebinding
kubectl get clusterrole demo-clusterrole
kubectl get clusterrolebinding demo-clusterrolebinding
```

### 3. 测试 RBAC 权限

使用 ServiceAccount 运行一个测试 Pod，验证其权限：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl run test-pod --image=bitnami/kubectl:latest --serviceaccount=demo-sa --restart=Never -- sleep 3600
```

### 4. 验证权限生效

#### 4.1 验证允许的操作

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 验证可以查看 pods
kubectl exec -it test-pod -- kubectl get pods

# 验证可以查看 services
kubectl exec -it test-pod -- kubectl get services

# 验证可以查看 pod logs
kubectl exec -it test-pod -- kubectl logs -l app=not-exist 2>/dev/null || echo "No logs found (expected)"

# 验证可以查看 nodes（集群级别权限）
kubectl exec -it test-pod -- kubectl get nodes

# 验证可以查看 namespaces（集群级别权限）
kubectl exec -it test-pod -- kubectl get namespaces
```

#### 4.2 验证禁止的操作

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 验证不能创建 pods（应该失败）
kubectl exec -it test-pod -- kubectl run test-pod-2 --image=nginx:latest 2>&1 | grep -i forbidden

# 验证不能删除 services（应该失败）
kubectl exec -it test-pod -- kubectl delete service kubernetes 2>&1 | grep -i forbidden
```

### 5. 清理测试资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
kubectl delete pod test-pod
```

## 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
kubectl delete -f rbac.yaml
```

## RBAC 的主要组成部分

1. **ServiceAccount**: 用于标识 Pod 或用户的身份
2. **Role**: 定义命名空间级别的权限集合
3. **RoleBinding**: 将 Role 绑定到一个或多个主体（ServiceAccount、User、Group）
4. **ClusterRole**: 定义集群级别的权限集合
5. **ClusterRoleBinding**: 将 ClusterRole 绑定到一个或多个主体

## 权限规则格式

```yaml
rules:
- apiGroups: ["<api-group>"]  # 空字符串代表核心 API 组
  resources: ["<resource>"]   # 资源名称，如 pods, services
  verbs: ["<verb>"]           # 操作动词，如 get, list, create, delete
```

## 常用动词

- **只读**: get, list, watch
- **写入**: create, update, patch
- **删除**: delete
- **全部权限**: *

## 最佳实践

1. **遵循最小权限原则**: 只授予必需的权限
2. **使用命名空间级别的 Role**: 优先使用 Role 而非 ClusterRole
3. **使用 ServiceAccount**: 为每个应用创建专用的 ServiceAccount
4. **定期审查权限**: 定期检查和更新 RBAC 配置
5. **使用工具管理**: 考虑使用工具如 `kubectl auth can-i` 测试权限

## 相关链接

- [Kubernetes RBAC 官方文档](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [kubectl auth can-i 命令](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#auth)
- [RBAC 最佳实践](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)

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
