# 🔐 Kubernetes RBAC权限管理和认证授权实战

> 深入学习Kubernetes RBAC权限控制系统：用户认证、角色授权、访问控制等企业级安全配置实践

## 📋 案例概述

本案例详细介绍Kubernetes RBAC权限管理和认证授权的完整配置方法，帮助企业构建安全可靠的访问控制体系。

### 🔧 核心技能点

- **RBAC基础概念**: Role、ClusterRole、RoleBinding、ClusterRoleBinding
- **用户认证配置**: 证书认证、Token认证、LDAP集成
- **权限精细控制**: 命名空间级别和集群级别权限管理
- **服务账户管理**: SA创建、Token管理和权限绑定
- **审计日志配置**: 访问审计、安全监控、合规检查
- **安全最佳实践**: 最小权限原则、权限审查、安全加固

### 🎯 适用人群

- Kubernetes安全管理员
- 系统架构师
- DevOps安全工程师
- 合规审计人员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查RBAC是否启用
kubectl api-versions | grep rbac

# 创建测试命名空间
kubectl create namespace rbac-demo

# 验证当前用户权限
kubectl auth can-i get pods --all-namespaces
```

### 2. 基础RBAC配置

```bash
# 创建测试用户证书
openssl genrsa -out user.key 2048
openssl req -new -key user.key -out user.csr -subj "/CN=test-user/O=example-org"
openssl x509 -req -in user.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out user.crt -days 365
```

---

## 📚 详细教程

### 1. RBAC核心概念

#### 1.1 Role和ClusterRole

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: rbac-demo
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]
```

#### 1.2 RoleBinding和ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: rbac-demo
subjects:
- kind: User
  name: test-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-cluster-pods
subjects:
- kind: User
  name: admin-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 2. 用户认证配置

#### 2.1 证书认证用户

```bash
# 创建用户私钥
openssl genrsa -out developer.key 2048

# 创建证书签名请求
cat > developer-csr.yaml <<EOF
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: developer-request
spec:
  request: $(cat developer.csr | base64 | tr -d '\n')
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
EOF

# 提交CSR并批准
kubectl apply -f developer-csr.yaml
kubectl certificate approve developer-request

# 获取签发的证书
kubectl get csr developer-request -o jsonpath='{.status.certificate}' | base64 --decode > developer.crt
```

#### 2.2 ServiceAccount认证

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: rbac-demo
---
apiVersion: v1
kind: Secret
metadata:
  name: app-service-account-token
  namespace: rbac-demo
  annotations:
    kubernetes.io/service-account.name: app-service-account
type: kubernetes.io/service-account-token
```

### 3. 权限精细控制

#### 3.1 命名空间级别权限

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: production-operator
rules:
- apiGroups: [""]
  resources: ["pods", "services", "deployments"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"]
- apiGroups: [""]
  resources: ["pods/exec"]
  verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: production-team-access
  namespace: production
subjects:
- kind: User
  name: dev-team-member
  apiGroup: rbac.authorization.k8s.io
- kind: Group
  name: dev-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: production-operator
  apiGroup: rbac.authorization.k8s.io
```

#### 3.2 资源配额和限制

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: rbac-demo
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
    persistentvolumeclaims: "4"
    services.loadbalancers: "1"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
  namespace: rbac-demo
spec:
  limits:
  - default:
      memory: 512Mi
    defaultRequest:
      memory: 256Mi
    type: Container
```

### 4. 高级RBAC配置

#### 4.1 条件访问控制

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: conditional-access
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
  resourceNames: ["critical-app-*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: restricted-access
subjects:
- kind: User
  name: junior-developer
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: conditional-access
  apiGroup: rbac.authorization.k8s.io
```

#### 4.2 动态权限管理

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: dynamic-permissions
rules:
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
  # 只能访问带有特定标签的资源
  resourceNames: []
```

### 5. 审计和监控

#### 5.1 审计策略配置

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets"]
  verbs: ["get", "list", "watch"]
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods"]
  verbs: ["create", "update", "delete"]
- level: None
  users: ["system:serviceaccount:kube-system:*"]
```

#### 5.2 审计日志分析

```bash
# 查看审计日志
kubectl logs -n kube-system <audit-pod> -f

# 分析特定用户的操作
grep "user.username=test-user" /var/log/kubernetes/audit.log

# 统计高频操作
awk '/"verb":"(create|update|delete)"/ {print $0}' /var/log/kubernetes/audit.log | wc -l
```

---

## 🔧 实践操作

### 1. RBAC权限测试

```bash
# 1. 创建测试用户和角色
kubectl apply -f rbac-test.yaml

# 2. 验证权限
kubectl auth can-i get pods --as=test-user -n rbac-demo
kubectl auth can-i delete pods --as=test-user -n rbac-demo

# 3. 测试实际操作
kubectl run test-pod --image=nginx --as=test-user -n rbac-demo
kubectl delete pod test-pod --as=test-user -n rbac-demo
```

### 2. 权限审查脚本

```bash
#!/bin/bash
# rbac-audit.sh

NAMESPACE=${1:-default}

echo "=== RBAC权限审计报告 ==="
echo "命名空间: $NAMESPACE"
echo "生成时间: $(date)"
echo ""

echo "1. 角色列表:"
kubectl get roles,clusterroles -n $NAMESPACE

echo -e "\n2. 角色绑定列表:"
kubectl get rolebindings,clusterrolebindings -n $NAMESPACE

echo -e "\n3. 服务账户列表:"
kubectl get serviceaccounts -n $NAMESPACE

echo -e "\n4. 权限详情:"
for role in $(kubectl get roles -n $NAMESPACE -o name); do
  echo "Role: $role"
  kubectl describe $role -n $NAMESPACE
  echo "---"
done
```

### 3. 安全扫描工具

```bash
# 使用kubeaudit检查RBAC配置
kubeaudit all -n rbac-demo

# 检查过度宽松的权限
kubectl get clusterrolebindings -o json | jq '.items[] | select(.roleRef.name=="cluster-admin")'

# 查找匿名访问配置
kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[].name=="system:anonymous")'
```

---

## 📊 监控和告警

### 1. 权限变更监控

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rbac-monitoring
  namespace: monitoring
data:
  rbac-alerts.yaml: |
    groups:
    - name: rbac.alerts
      rules:
      - alert: UnauthorizedAccessAttempt
        expr: increase(audit_event_total{verb=~"create|update|delete", response_status=~"4.."}[5m]) > 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "检测到未授权访问尝试"
          description: "{{ $labels.user.username }} 尝试执行 {{ $labels.verb }} 操作被拒绝"
```

### 2. 权限使用统计

```bash
# 统计各用户操作频率
kubectl get events --field-selector reason=Forbidden -o json | \
  jq -r '.items[].involvedObject | "\(.kind):\(.name) by \(.username)"' | \
  sort | uniq -c | sort -nr

# 分析权限使用模式
kubectl get rolebindings --all-namespaces -o json | \
  jq -r '.items[].subjects[].name' | \
  sort | uniq -c | sort -nr
```

---

## ⚠️ 常见问题和解决方案

### 1. 权限不足错误

**问题现象**: Forbidden错误或权限被拒绝

**解决步骤**:
```bash
# 1. 检查用户权限
kubectl auth can-i <verb> <resource> --as=<user> -n <namespace>

# 2. 查看详细错误信息
kubectl describe <resource> <name> -n <namespace>

# 3. 检查RoleBinding配置
kubectl get rolebindings -n <namespace> -o yaml

# 4. 验证用户认证
kubectl config view --raw -o jsonpath='{.users[?(@.name=="<user>")].user.client-certificate-data}' | base64 -d | openssl x509 -text
```

### 2. 服务账户权限问题

**问题现象**: Pod无法访问API Server

**解决步骤**:
```bash
# 1. 检查SA Token
kubectl get secret $(kubectl get sa <sa-name> -n <namespace> -o jsonpath='{.secrets[0].name}') -n <namespace> -o jsonpath='{.data.token}' | base64 -d

# 2. 验证SA权限
kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<namespace>:<sa-name>

# 3. 检查Pod配置
kubectl describe pod <pod-name> -n <namespace>
```

### 3. RBAC配置复杂度过高

**问题现象**: 权限配置难以维护和理解

**解决步骤**:
```bash
# 1. 使用工具可视化权限关系
kubectl tree rolebinding -n <namespace>

# 2. 定期审查和清理权限
./rbac-cleanup.sh

# 3. 建立权限申请和审批流程
# 实施最小权限原则
```

---

## 🧪 实践练习

### 练习1：基础权限配置
为开发团队创建只读权限的角色和绑定。

### 练习2：生产环境权限管理
配置多层级权限管理体系，区分开发、测试、生产环境。

### 练习3：安全审计实践
实施完整的RBAC审计和监控体系。

### 练习4：权限优化演练
定期审查和优化现有权限配置，消除过度授权。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [认证和授权](https://kubernetes.io/docs/reference/access-authn-authz/)
- [审计策略](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/)

### 相关案例
- [集群搭建](../cluster-setup/)
- [安全加固](../security-hardening/)
- [合规检查](../compliance-audit/)

### 进阶主题
- 多租户权限管理
- 动态权限分配
- 零信任安全模型
- 细粒度访问控制

---

## 📋 清理资源

```bash
# 删除测试资源
kubectl delete namespace rbac-demo

# 删除测试用户
kubectl delete certificateSigningRequest developer-request

# 清理配置文件
rm -f developer.key developer.csr developer.crt

# 重置RBAC配置
kubectl delete rolebindings,clusterrolebindings --all
kubectl delete roles,clusterroles --all
```

---

> **💡 提示**: RBAC权限管理是Kubernetes安全的核心，建议遵循最小权限原则，定期审查权限配置，建立完善的审计和监控体系。