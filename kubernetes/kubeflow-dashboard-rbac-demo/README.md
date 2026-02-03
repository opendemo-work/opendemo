# Kubeflow Dashboard RBAC 权限配置演示

## 简介
本演示展示了如何在 Kubernetes 集群中为 Kubeflow Dashboard 配置基于角色的访问控制（RBAC），包括创建自定义角色、绑定用户到角色以及验证权限效果。通过本示例，您将学习如何安全地管理对 Kubeflow 的访问。

## 学习目标
- 理解 Kubernetes RBAC 核心概念（Role、RoleBinding、ServiceAccount）
- 掌握为 Kubeflow Dashboard 配置最小权限原则的方法
- 实践不同粒度的权限控制策略

## 环境要求
- kubectl v1.20 或更高版本
- 访问启用了 Kubeflow 的 Kubernetes 集群（推荐 v1.20+）
- 具备 cluster-admin 权限以创建 RBAC 资源

## 安装依赖的详细步骤
1. 安装 kubectl：https://kubernetes.io/docs/tasks/tools/install-kubectl/
2. 配置 kubeconfig 指向您的 Kubeflow 集群
3. 确保 Kubeflow 已部署并运行（建议使用 Kubeflow 1.7+）

## 文件说明
- `kf-user-role.yaml`：定义允许访问 Kubeflow Central Dashboard 的基本角色
- `kf-admin-rolebinding.yaml`：将管理员角色绑定到特定 ServiceAccount
- `kf-viewer-role.yaml`：只读角色，适用于普通用户

## 逐步实操指南

### 步骤 1: 应用只读角色
```bash
kubectl apply -f kf-viewer-role.yaml
```

**预期输出:**
```
role.rbac.authorization.k8s.io/kubeflow-viewer created
```

### 步骤 2: 创建用户服务账户
```bash
kubectl create serviceaccount alice -n kubeflow
```

**预期输出:**
```
serviceaccount/alice created
```

### 步骤 3: 绑定用户到只读角色
```bash
kubectl apply -f kf-user-role.yaml
```

**预期输出:**
```
rolebinding.rbac.authorization.k8s.io/alice-kubeflow-viewer created
```

### 步骤 4: 验证权限
查看当前用户可访问的资源：
```bash
kubectl auth can-i --as=system:serviceaccount:kubeflow:alice get pods -n kubeflow
```

**预期输出:**
```
yes
```

尝试写操作（应被拒绝）：
```bash
kubectl auth can-i --as=system:serviceaccount:kubeflow:alice delete pods -n kubeflow
```

**预期输出:**
```
no
```

## 代码解析

### `kf-viewer-role.yaml`
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: kubeflow
  name: kubeflow-viewer
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch"]
```

此角色授予对 Pods、Services 和 ConfigMaps 的只读权限，符合最小权限原则。

### `kf-user-role.yaml`
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: alice-kubeflow-viewer
  namespace: kubeflow
roleRef:
  kind: Role
  name: kubeflow-viewer
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: alice
  namespace: kubeflow
```

将名为 alice 的 ServiceAccount 绑定到 kubeflow-viewer 角色，实现权限分配。

## 预期输出示例
```bash
$ kubectl get rolebindings -n kubeflow alice-kubeflow-viewer
NAME                     ROLE                   AGE
alice-kubeflow-viewer    Role/kubeflow-viewer   5m
```

## 常见问题解答

**Q: 为什么使用 ServiceAccount 而不是用户？**
A: Kubernetes RBAC 主要设计用于服务账户；实际用户通常通过 OIDC 映射到 service account。

**Q: 如何授予更多权限？**
A: 修改 Role 中的 `resources` 和 `verbs` 字段，或创建新的 Role 并绑定。

**Q: 权限未生效？**
A: 检查命名空间是否正确，确保 Kubeflow 使用的是命名空间本地角色而非集群角色。

## 扩展学习建议
- 学习 ClusterRole 和 ClusterRoleBinding 的使用场景
- 探索 Kubeflow 多用户隔离架构
- 实现基于团队的命名空间隔离策略
- 集成外部身份提供商（如 Dex、Okta）