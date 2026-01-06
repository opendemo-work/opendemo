# CRD故障排查指南

## 常见问题分类

### 1. CRD创建问题

#### 问题：CRD创建失败 - API版本不支持

**现象**：
```
error: unable to recognize "crd-definition.yaml": 
no matches for kind "CustomResourceDefinition" in version "apiextensions.k8s.io/v1beta1"
```

**原因**：Kubernetes 1.22+移除了v1beta1 API版本

**解决方法**：
```yaml
# 将apiVersion更新为v1
apiVersion: apiextensions.k8s.io/v1  # ✅ 正确
# apiVersion: apiextensions.k8s.io/v1beta1  # ❌ 已废弃
```

#### 问题：CRD名称格式错误

**现象**：
```
The CustomResourceDefinition "appdeployments" is invalid: 
metadata.name: Invalid value: "appdeployments": must be spec.names.plural+"."+spec.group
```

**原因**：CRD name必须是`<plural>.<group>`格式

**解决方法**：
```yaml
metadata:
  name: appdeployments.demo.opendemo.io  # ✅ 正确格式
  # name: appdeployments  # ❌ 错误格式
```

### 2. Schema验证问题

#### 问题：资源创建被拒绝 - 字段验证失败

**现象**：
```
The AppDeployment "test" is invalid: 
spec.replicas: Invalid value: 100: spec.replicas in body should be less than or equal to 10
```

**原因**：字段值超出Schema定义的范围

**解决方法**：
检查并修正字段值，确保符合CRD定义的验证规则：
```yaml
spec:
  replicas: 5  # ✅ 在1-10范围内
  # replicas: 100  # ❌ 超出范围
```

#### 问题：缺少必填字段

**现象**：
```
error validating data: ValidationError(AppDeployment.spec): 
missing required field "image" in demo.opendemo.io/v1.AppDeployment.spec
```

**解决方法**：
```yaml
spec:
  replicas: 1
  image: nginx:latest  # ✅ 添加必填字段
  port: 80
```

### 3. CRD更新问题

#### 问题：CRD无法更新 - 存储版本冲突

**现象**：
```
The CustomResourceDefinition "appdeployments.demo.opendemo.io" is invalid: 
status.storedVersions[0]: Invalid value: "v1beta1": must appear in spec.versions
```

**原因**：尝试移除已使用的存储版本

**解决方法**：
1. 确保新版本设置为storage版本
2. 迁移现有资源到新版本
3. 删除旧版本

```bash
# 查看当前存储版本
kubectl get crd appdeployments.demo.opendemo.io \
  -o jsonpath='{.status.storedVersions}'
```

### 4. 资源删除问题

#### 问题：资源删除卡住（Terminating状态）

**现象**：
```bash
$ kubectl get appdeployments
NAME        AGE
test-app    5m    # 状态一直是Terminating
```

**原因**：Finalizer未被正确清理

**解决方法**：
```bash
# 方式1：手动移除finalizer
kubectl patch appdeployment test-app \
  -p '{"metadata":{"finalizers":null}}' --type=merge

# 方式2：强制删除
kubectl delete appdeployment test-app --grace-period=0 --force
```

#### 问题：CRD无法删除

**现象**：
```
customresourcedefinition.apiextensions.k8s.io 
"appdeployments.demo.opendemo.io" deleted
# 但仍然存在
```

**原因**：存在该CRD的资源实例

**解决方法**：
```bash
# 步骤1：先删除所有资源实例
kubectl delete appdeployments --all --all-namespaces

# 步骤2：再删除CRD
kubectl delete crd appdeployments.demo.opendemo.io
```

### 5. 权限问题

#### 问题：没有权限创建CRD

**现象**：
```
Error from server (Forbidden): error when creating "crd-definition.yaml": 
customresourcedefinitions.apiextensions.k8s.io is forbidden: 
User "developer" cannot create resource "customresourcedefinitions"
```

**解决方法**：
需要cluster-admin角色或特定的CRD权限：
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: crd-manager
rules:
- apiGroups: ["apiextensions.k8s.io"]
  resources: ["customresourcedefinitions"]
  verbs: ["create", "get", "list", "delete"]
```

## 调试技巧

### 1. 查看详细错误信息

```bash
# 使用-v=8获取详细日志
kubectl apply -f crd-definition.yaml -v=8

# 查看CRD状态
kubectl describe crd appdeployments.demo.opendemo.io

# 查看资源事件
kubectl describe appdeployment test-app
```

### 2. 验证Schema

```bash
# 使用dry-run测试
kubectl apply --dry-run=client -f cr-example.yaml

# 使用server-side dry-run
kubectl apply --dry-run=server -f cr-example.yaml
```

### 3. 检查API可用性

```bash
# 查看CRD是否就绪
kubectl get crd appdeployments.demo.opendemo.io \
  -o jsonpath='{.status.conditions[?(@.type=="Established")].status}'

# 输出应该是：True

# 查看API资源列表
kubectl api-resources | grep appdeployment
```

### 4. 分析API服务器日志

```bash
# 查看kube-apiserver日志
kubectl logs -n kube-system <kube-apiserver-pod> | grep appdeployment
```

## 预防措施

### 1. Schema设计阶段

- ✅ 使用`kubectl apply --dry-run`测试
- ✅ 编写完整的validation规则
- ✅ 为字段添加description
- ✅ 合理设置默认值

### 2. CRD部署阶段

- ✅ 先在测试环境验证
- ✅ 检查Kubernetes版本兼容性
- ✅ 备份现有CRD配置
- ✅ 准备回滚方案

### 3. 资源使用阶段

- ✅ 监控资源创建失败率
- ✅ 设置资源配额限制
- ✅ 定期清理无用资源
- ✅ 记录重要操作日志

## 应急处理流程

### 场景1：CRD配置错误导致无法创建资源

```bash
# 1. 查看错误详情
kubectl describe crd appdeployments.demo.opendemo.io

# 2. 导出当前配置
kubectl get crd appdeployments.demo.opendemo.io -o yaml > backup.yaml

# 3. 修复配置
vi crd-definition.yaml

# 4. 更新CRD
kubectl apply -f crd-definition.yaml
```

### 场景2：大量资源无法删除

```bash
# 1. 列出所有资源
kubectl get appdeployments --all-namespaces

# 2. 批量移除finalizer
kubectl get appdeployments --all-namespaces -o name | \
  xargs -I {} kubectl patch {} \
  -p '{"metadata":{"finalizers":null}}' --type=merge

# 3. 强制删除
kubectl delete appdeployments --all --all-namespaces --grace-period=0 --force
```

## 联系支持

如果遇到无法解决的问题：
1. 查看Kubernetes官方文档
2. 搜索GitHub Issues
3. 在Kubernetes Slack频道提问
4. 提交Bug报告（附带完整日志）

## 参考资料

- [Kubernetes CRD故障排除](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#troubleshooting)
- [API扩展问题排查](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#common-mistakes)
