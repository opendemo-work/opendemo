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

```bash
kubectl apply -f rbac.yaml
```

### 2. 验证资源创建

```bash
kubectl get serviceaccount demo-sa
kubectl get role demo-role
kubectl get rolebinding demo-rolebinding
kubectl get clusterrole demo-clusterrole
kubectl get clusterrolebinding demo-clusterrolebinding
```

### 3. 测试 RBAC 权限

使用 ServiceAccount 运行一个测试 Pod，验证其权限：

```bash
kubectl run test-pod --image=bitnami/kubectl:latest --serviceaccount=demo-sa --restart=Never -- sleep 3600
```

### 4. 验证权限生效

#### 4.1 验证允许的操作

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

```bash
# 验证不能创建 pods（应该失败）
kubectl exec -it test-pod -- kubectl run test-pod-2 --image=nginx:latest 2>&1 | grep -i forbidden

# 验证不能删除 services（应该失败）
kubectl exec -it test-pod -- kubectl delete service kubernetes 2>&1 | grep -i forbidden
```

### 5. 清理测试资源

```bash
kubectl delete pod test-pod
```

## 清理资源

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
