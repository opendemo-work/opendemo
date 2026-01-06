# CRD自定义资源定义演示

> 展示如何定义和使用CustomResourceDefinition扩展Kubernetes API，创建自定义资源类型

![Difficulty](https://img.shields.io/badge/难度-初级-green)
![Kubernetes](https://img.shields.io/badge/Kubernetes-≥1.24-blue)
![Status](https://img.shields.io/badge/Status-Ready-success)

---

## 📋 功能概述

本Demo演示Kubernetes CRD（CustomResourceDefinition）的完整使用流程，帮助您理解如何扩展Kubernetes API并创建自定义资源类型。

**核心功能**：
- ✅ CRD定义与注册 - 使用OpenAPI v3规范定义资源Schema
- ✅ 自定义资源CRUD操作 - 创建、查询、更新、删除自定义资源
- ✅ Schema验证机制 - 字段类型验证、取值范围限制
- ✅ 自定义输出列 - kubectl命令的个性化展示
- ✅ 子资源支持 - Status独立更新、Scale扩缩容

**适用场景**：
- 构建Kubernetes原生应用
- 实现声明式API管理
- 扩展Kubernetes资源模型
- 开发Kubernetes Operator基础

**学习目标**：
- 掌握CRD定义语法和规范
- 理解OpenAPI Schema验证机制
- 熟悉自定义资源生命周期管理
- 了解Kubernetes API扩展原理

---

## 🔧 前置要求

| 类别 | 要求 | 说明 |
|------|------|------|
| **Kubernetes集群** | v1.24+ | 本地minikube或云端集群均可 |
| **kubectl** | v1.24+ | Kubernetes命令行工具 |
| **权限** | cluster-admin | 创建CRD需要集群管理员权限 |
| **操作系统** | Linux/macOS/Windows | 支持bash脚本的环境 |

**环境准备**：

```bash
# 检查kubectl版本
kubectl version --client

# 检查集群连接
kubectl cluster-info

# 验证权限（需要能查看CRD）
kubectl get crd
```

---

## 🚀 快速开始

### 步骤1：部署CRD定义

**目标**：向Kubernetes集群注册`AppDeployment`自定义资源类型

**执行命令**：
```bash
# 方式1：使用脚本自动部署
bash scripts/deploy.sh

# 方式2：手动部署
kubectl apply -f manifests/crd-definition.yaml
```

**预期输出**：
```
customresourcedefinition.apiextensions.k8s.io/appdeployments.demo.opendemo.io created
```

**验证方法**：
```bash
# 查看CRD列表
kubectl get crd appdeployments.demo.opendemo.io

# 输出示例：
# NAME                                 CREATED AT
# appdeployments.demo.opendemo.io     2026-01-06T07:00:00Z

# 检查API资源
kubectl api-resources | grep appdeployment

# 输出示例：
# appdeployments     appdep    demo.opendemo.io/v1    true    AppDeployment
```

### 步骤2：创建自定义资源

**目标**：创建AppDeployment资源实例，验证CRD功能

**执行命令**：
```bash
kubectl apply -f manifests/cr-example.yaml
```

**预期输出**：
```
appdeployment.demo.opendemo.io/nginx-app created
appdeployment.demo.opendemo.io/nodejs-api created
appdeployment.demo.opendemo.io/minimal-app created
```

**验证方法**：
```bash
# 查看资源列表
kubectl get appdeployments

# 输出示例：
# NAME          REPLICAS   READY   PHASE   AGE
# nginx-app     3          <none>          10s
# nodejs-api    2          <none>          10s
# minimal-app   1          <none>          10s

# 使用简写查询
kubectl get appdep

# 查看详细信息
kubectl describe appdeployment nginx-app
```

### 步骤3：操作自定义资源

**目标**：演示资源的查询、更新、删除操作

**查询资源详情**：
```bash
# 查看YAML格式
kubectl get appdeployment nginx-app -o yaml

# 查看JSON格式
kubectl get appdeployment nginx-app -o json

# 显示扩展列信息
kubectl get appdeployments -o wide
```

**更新资源配置**：
```bash
# 方式1：直接编辑
kubectl edit appdeployment nginx-app

# 方式2：使用patch更新
kubectl patch appdeployment nginx-app -p '{"spec":{"replicas":5}}' --type=merge

# 方式3：使用scale命令（因为启用了scale子资源）
kubectl scale appdeployment nginx-app --replicas=4

# 验证更新
kubectl get appdeployment nginx-app -o jsonpath='{.spec.replicas}'
```

**删除资源**：
```bash
# 删除单个资源
kubectl delete appdeployment nginx-app

# 删除所有资源
kubectl delete appdeployments --all

# 验证删除
kubectl get appdeployments
```

### 步骤4：运行自动化测试

**目标**：执行完整的5层验证测试

**执行命令**：
```bash
bash scripts/test.sh
```

**测试内容**：
- L1: 文件完整性检查
- L2: YAML语法验证
- L3: API兼容性测试
- L4: 功能可用性测试
- L5: 清理完整性验证

---

## 📖 详细步骤

### 1. CRD定义文件解析

CRD定义文件位于`manifests/crd-definition.yaml`，关键字段说明：

```yaml
apiVersion: apiextensions.k8s.io/v1  # CRD API版本
kind: CustomResourceDefinition        # 资源类型

spec:
  group: demo.opendemo.io             # API组名
  scope: Namespaced                   # 命名空间级别资源
  
  names:
    plural: appdeployments            # 复数形式（URL使用）
    singular: appdeployment           # 单数形式
    kind: AppDeployment               # Kind名称
    shortNames: [appdep]              # 简写

  versions:
  - name: v1                          # 版本号
    served: true                      # 提供服务
    storage: true                     # 存储版本
    
    schema:                           # OpenAPI Schema定义
      openAPIV3Schema:
        properties:
          spec:                       # 期望状态
            required: [replicas, image, port]
            properties:
              replicas:                # 副本数
                type: integer
                minimum: 1
                maximum: 10
              image:                   # 镜像名称
                type: string
                pattern: '^[a-zA-Z0-9\.\-\/\:]+$'
              port:                    # 端口号
                type: integer
                minimum: 1
                maximum: 65535
```

**Schema验证规则**：
- **类型验证**：integer、string、object、array
- **范围限制**：minimum、maximum
- **格式验证**：pattern（正则表达式）
- **必填字段**：required数组
- **默认值**：default字段

### 2. 自定义输出列配置

CRD的`additionalPrinterColumns`定义了kubectl输出格式：

```yaml
additionalPrinterColumns:
- name: Replicas        # 列名称
  type: integer         # 数据类型
  jsonPath: .spec.replicas  # 数据路径
- name: Phase
  type: string
  jsonPath: .status.phase
- name: Age
  type: date
  jsonPath: .metadata.creationTimestamp
```

**输出效果**：
```
NAME        REPLICAS   READY   PHASE   AGE
nginx-app   3          2       Running 5m
```

### 3. 子资源支持

**Status子资源**：
```yaml
subresources:
  status: {}  # 启用独立的status更新
```

好处：
- Status更新不会触发spec的validation
- 可以区分用户意图和实际状态
- Operator可以独立更新status

**Scale子资源**：
```yaml
subresources:
  scale:
    specReplicasPath: .spec.replicas
    statusReplicasPath: .status.readyReplicas
```

支持的操作：
```bash
# 使用kubectl scale命令
kubectl scale appdeployment nginx-app --replicas=5

# 使用HPA自动扩缩容（需要Operator支持）
kubectl autoscale appdeployment nginx-app --min=2 --max=10
```

### 4. 版本管理策略

**单版本示例**（当前Demo）：
```yaml
versions:
- name: v1
  served: true
  storage: true
```

**多版本共存**（生产环境建议）：
```yaml
versions:
- name: v2         # 新版本
  served: true
  storage: true    # 存储版本
- name: v1         # 旧版本
  served: true     # 仍提供服务
  storage: false   # 不再用于存储
  deprecated: true # 标记为废弃
```

### 5. 实际应用场景

**场景1：应用部署管理**
```yaml
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: production-api
spec:
  replicas: 5
  image: myapp:v2.1.0
  port: 8080
  resources:
    cpu: "1"
    memory: "1Gi"
```

**场景2：微服务配置**
```yaml
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: user-service
spec:
  replicas: 3
  image: user-svc:latest
  port: 3000
```

---

## ✅ 测试验证

### 功能正确性测试

**测试1：资源创建**
```bash
kubectl apply -f manifests/cr-example.yaml
kubectl get appdeployments
# 验证：3个资源成功创建
```

**测试2：Schema验证（边界值）**
```bash
# 测试最小值
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-min
spec:
  replicas: 1
  image: nginx:latest
  port: 1
' | kubectl apply -f -
# 验证：成功创建

# 测试超出范围（应失败）
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-invalid
spec:
  replicas: 100
  image: nginx:latest
  port: 80
' | kubectl apply -f -
# 验证：报错 "spec.replicas: Invalid value: 100: spec.replicas in body should be less than or equal to 10"
```

**测试3：字段验证**
```bash
# 测试非法镜像名（应失败）
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-bad-image
spec:
  replicas: 1
  image: "invalid image name"
  port: 80
' | kubectl apply -f -
# 验证：报错 pattern不匹配
```

### 错误处理测试

**错误1：缺少必填字段**
```bash
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-missing
spec:
  replicas: 1
  # 缺少image和port字段
' | kubectl apply -f -
# 预期：ValidationError - missing required field
```

**错误2：类型错误**
```bash
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-type-error
spec:
  replicas: "three"  # 应该是integer
  image: nginx:latest
  port: 80
' | kubectl apply -f -
# 预期：ValidationError - invalid type
```

### 清理验证

```bash
# 执行清理
bash scripts/cleanup.sh

# 验证1：资源实例已删除
kubectl get appdeployments
# 输出：No resources found

# 验证2：CRD已删除
kubectl get crd appdeployments.demo.opendemo.io
# 输出：Error from server (NotFound)

# 验证3：API不再注册
kubectl api-resources | grep appdeployment
# 输出：无结果
```

---

## 🎓 进阶使用

### 1. 与Operator结合

CRD定义了"声明式API"，Operator实现"控制逻辑"：

```
CRD            →    定义资源结构
Custom Resource →    用户期望状态
Operator        →    实现期望状态
```

参考本项目的Operator Demo：`operator-controller-demo`

### 2. Admission Webhook集成

通过Webhook实现复杂验证逻辑：

```yaml
spec:
  conversion:  # 版本转换Webhook
    strategy: Webhook
    webhook:
      clientConfig:
        service:
          name: conversion-webhook
          namespace: default
```

### 3. 生产环境注意事项

**版本管理**：
- 始终保持一个storage版本
- 逐步废弃旧版本
- 提供版本转换机制

**性能优化**：
- 合理设置字段默认值
- 避免过于复杂的Schema
- 使用索引优化查询

**安全考虑**：
- 限制CRD创建权限
- 使用RBAC控制资源访问
- 避免在CRD中存储敏感信息

### 4. 与原生资源集成

**OwnerReference关联**：
```yaml
metadata:
  ownerReferences:
  - apiVersion: demo.opendemo.io/v1
    kind: AppDeployment
    name: nginx-app
    uid: <uid>
    controller: true
```

**Label选择器**：
```yaml
spec:
  selector:
    matchLabels:
      app.kubernetes.io/managed-by: appdeployment-controller
```

---

## 🔍 故障排查

| 现象 | 可能原因 | 解决方法 |
|------|----------|----------|
| **CRD创建失败** | API版本不兼容 | 检查集群版本：`kubectl version`，确保≥1.16 |
| **资源无法创建** | Schema验证失败 | 查看错误详情：`kubectl apply -f file.yaml -v=8` |
| **CRD未就绪** | Webhook配置错误 | 检查Webhook服务：`kubectl get validatingwebhookconfigurations` |
| **资源删除卡住** | Finalizer未清理 | 手动移除Finalizer：`kubectl patch ... --type=merge -p '{"metadata":{"finalizers":null}}'` |
| **版本冲突** | 多版本配置错误 | 确保只有一个storage版本：`kubectl get crd ... -o yaml \| grep storage` |
| **权限不足** | 缺少CRD权限 | 使用cluster-admin角色或添加CRD权限 |

**查看详细错误**：
```bash
# 查看CRD状态
kubectl describe crd appdeployments.demo.opendemo.io

# 查看资源事件
kubectl describe appdeployment <name>

# 查看API服务器日志
kubectl logs -n kube-system <kube-apiserver-pod>
```

**常见错误示例**：

错误1：Schema格式错误
```
Error: ValidationError(CustomResourceDefinition.spec.versions[0].schema.openAPIV3Schema): 
invalid type for io.k8s.apiextensions-apiserver.pkg.apis.apiextensions.v1.JSONSchemaProps: 
got "map", expected "string"
```
解决：检查YAML缩进和字段类型

错误2：CRD名称冲突
```
Error from server (Conflict): customresourcedefinitions.apiextensions.k8s.io 
"appdeployments.demo.opendemo.io" already exists
```
解决：删除已存在的CRD或使用不同的group/plural

---

## 🧹 清理资源

### 完整清理步骤

**方式1：使用清理脚本**
```bash
bash scripts/cleanup.sh
```

**方式2：手动清理**
```bash
# 步骤1：删除所有自定义资源实例
kubectl delete appdeployments --all

# 步骤2：删除CRD定义
kubectl delete crd appdeployments.demo.opendemo.io

# 步骤3：验证清理完成
kubectl get appdeployments
kubectl get crd appdeployments.demo.opendemo.io
```

### 清理验证

```bash
# 检查是否有残留资源
kubectl get appdeployments --all-namespaces

# 检查CRD是否完全删除
kubectl api-resources | grep appdeployment

# 如果有finalizer阻塞删除
kubectl patch crd appdeployments.demo.opendemo.io \
  -p '{"metadata":{"finalizers":[]}}' --type=merge
```

---

## 📚 参考资料

### 官方文档
- [Kubernetes CRD官方文档](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [OpenAPI v3 Schema规范](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.0.md#schemaObject)
- [API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

### 相关教程
- [Kubernetes API扩展机制](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/)
- [自定义资源最佳实践](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

### 社区资源
- [kubebuilder - Operator开发框架](https://book.kubebuilder.io/)
- [Operator SDK](https://sdk.operatorframework.io/)
- [Awesome Operators](https://github.com/operator-framework/awesome-operators)

### 本项目相关
- [Operator控制器开发Demo](../operator-controller-demo/) - 下一步学习
- [KubeSkoop网络诊断](../../kubeskoop/) - 生产级CRD示例

---

## 💡 提示

- ✅ CRD只是定义资源结构，不包含业务逻辑
- ✅ 需要Operator或控制器才能实现自动化管理
- ✅ Schema验证在API服务器层面执行，非常高效
- ✅ 合理使用defaulting和validation减少用户配置负担
- ✅ Status子资源是Operator模式的核心设计

---

**Created**: 2026-01-06  
**Version**: 1.0.0  
**License**: MIT
# CRD自定义资源定义演示

> 展示如何定义和使用CustomResourceDefinition扩展Kubernetes API，创建自定义资源类型

![Difficulty](https://img.shields.io/badge/难度-初级-green)
![Kubernetes](https://img.shields.io/badge/Kubernetes-≥1.24-blue)
![Status](https://img.shields.io/badge/Status-Ready-success)

---

## 📋 功能概述

本Demo演示Kubernetes CRD（CustomResourceDefinition）的完整使用流程，帮助您理解如何扩展Kubernetes API并创建自定义资源类型。

**核心功能**：
- ✅ CRD定义与注册 - 使用OpenAPI v3规范定义资源Schema
- ✅ 自定义资源CRUD操作 - 创建、查询、更新、删除自定义资源
- ✅ Schema验证机制 - 字段类型验证、取值范围限制
- ✅ 自定义输出列 - kubectl命令的个性化展示
- ✅ 子资源支持 - Status独立更新、Scale扩缩容

**适用场景**：
- 构建Kubernetes原生应用
- 实现声明式API管理
- 扩展Kubernetes资源模型
- 开发Kubernetes Operator基础

**学习目标**：
- 掌握CRD定义语法和规范
- 理解OpenAPI Schema验证机制
- 熟悉自定义资源生命周期管理
- 了解Kubernetes API扩展原理

---

## 🔧 前置要求

| 类别 | 要求 | 说明 |
|------|------|------|
| **Kubernetes集群** | v1.24+ | 本地minikube或云端集群均可 |
| **kubectl** | v1.24+ | Kubernetes命令行工具 |
| **权限** | cluster-admin | 创建CRD需要集群管理员权限 |
| **操作系统** | Linux/macOS/Windows | 支持bash脚本的环境 |

**环境准备**：

```bash
# 检查kubectl版本
kubectl version --client

# 检查集群连接
kubectl cluster-info

# 验证权限（需要能查看CRD）
kubectl get crd
```

---

## 🚀 快速开始

### 步骤1：部署CRD定义

**目标**：向Kubernetes集群注册`AppDeployment`自定义资源类型

**执行命令**：
```bash
# 方式1：使用脚本自动部署
bash scripts/deploy.sh

# 方式2：手动部署
kubectl apply -f manifests/crd-definition.yaml
```

**预期输出**：
```
customresourcedefinition.apiextensions.k8s.io/appdeployments.demo.opendemo.io created
```

**验证方法**：
```bash
# 查看CRD列表
kubectl get crd appdeployments.demo.opendemo.io

# 输出示例：
# NAME                                 CREATED AT
# appdeployments.demo.opendemo.io     2026-01-06T07:00:00Z

# 检查API资源
kubectl api-resources | grep appdeployment

# 输出示例：
# appdeployments     appdep    demo.opendemo.io/v1    true    AppDeployment
```

### 步骤2：创建自定义资源

**目标**：创建AppDeployment资源实例，验证CRD功能

**执行命令**：
```bash
kubectl apply -f manifests/cr-example.yaml
```

**预期输出**：
```
appdeployment.demo.opendemo.io/nginx-app created
appdeployment.demo.opendemo.io/nodejs-api created
appdeployment.demo.opendemo.io/minimal-app created
```

**验证方法**：
```bash
# 查看资源列表
kubectl get appdeployments

# 输出示例：
# NAME          REPLICAS   READY   PHASE   AGE
# nginx-app     3          <none>          10s
# nodejs-api    2          <none>          10s
# minimal-app   1          <none>          10s

# 使用简写查询
kubectl get appdep

# 查看详细信息
kubectl describe appdeployment nginx-app
```

### 步骤3：操作自定义资源

**目标**：演示资源的查询、更新、删除操作

**查询资源详情**：
```bash
# 查看YAML格式
kubectl get appdeployment nginx-app -o yaml

# 查看JSON格式
kubectl get appdeployment nginx-app -o json

# 显示扩展列信息
kubectl get appdeployments -o wide
```

**更新资源配置**：
```bash
# 方式1：直接编辑
kubectl edit appdeployment nginx-app

# 方式2：使用patch更新
kubectl patch appdeployment nginx-app -p '{"spec":{"replicas":5}}' --type=merge

# 方式3：使用scale命令（因为启用了scale子资源）
kubectl scale appdeployment nginx-app --replicas=4

# 验证更新
kubectl get appdeployment nginx-app -o jsonpath='{.spec.replicas}'
```

**删除资源**：
```bash
# 删除单个资源
kubectl delete appdeployment nginx-app

# 删除所有资源
kubectl delete appdeployments --all

# 验证删除
kubectl get appdeployments
```

### 步骤4：运行自动化测试

**目标**：执行完整的5层验证测试

**执行命令**：
```bash
bash scripts/test.sh
```

**测试内容**：
- L1: 文件完整性检查
- L2: YAML语法验证
- L3: API兼容性测试
- L4: 功能可用性测试
- L5: 清理完整性验证

---

## 📖 详细步骤

### 1. CRD定义文件解析

CRD定义文件位于`manifests/crd-definition.yaml`，关键字段说明：

```yaml
apiVersion: apiextensions.k8s.io/v1  # CRD API版本
kind: CustomResourceDefinition        # 资源类型

spec:
  group: demo.opendemo.io             # API组名
  scope: Namespaced                   # 命名空间级别资源
  
  names:
    plural: appdeployments            # 复数形式（URL使用）
    singular: appdeployment           # 单数形式
    kind: AppDeployment               # Kind名称
    shortNames: [appdep]              # 简写

  versions:
  - name: v1                          # 版本号
    served: true                      # 提供服务
    storage: true                     # 存储版本
    
    schema:                           # OpenAPI Schema定义
      openAPIV3Schema:
        properties:
          spec:                       # 期望状态
            required: [replicas, image, port]
            properties:
              replicas:                # 副本数
                type: integer
                minimum: 1
                maximum: 10
              image:                   # 镜像名称
                type: string
                pattern: '^[a-zA-Z0-9\.\-\/\:]+$'
              port:                    # 端口号
                type: integer
                minimum: 1
                maximum: 65535
```

**Schema验证规则**：
- **类型验证**：integer、string、object、array
- **范围限制**：minimum、maximum
- **格式验证**：pattern（正则表达式）
- **必填字段**：required数组
- **默认值**：default字段

### 2. 自定义输出列配置

CRD的`additionalPrinterColumns`定义了kubectl输出格式：

```yaml
additionalPrinterColumns:
- name: Replicas        # 列名称
  type: integer         # 数据类型
  jsonPath: .spec.replicas  # 数据路径
- name: Phase
  type: string
  jsonPath: .status.phase
- name: Age
  type: date
  jsonPath: .metadata.creationTimestamp
```

**输出效果**：
```
NAME        REPLICAS   READY   PHASE   AGE
nginx-app   3          2       Running 5m
```

### 3. 子资源支持

**Status子资源**：
```yaml
subresources:
  status: {}  # 启用独立的status更新
```

好处：
- Status更新不会触发spec的validation
- 可以区分用户意图和实际状态
- Operator可以独立更新status

**Scale子资源**：
```yaml
subresources:
  scale:
    specReplicasPath: .spec.replicas
    statusReplicasPath: .status.readyReplicas
```

支持的操作：
```bash
# 使用kubectl scale命令
kubectl scale appdeployment nginx-app --replicas=5

# 使用HPA自动扩缩容（需要Operator支持）
kubectl autoscale appdeployment nginx-app --min=2 --max=10
```

### 4. 版本管理策略

**单版本示例**（当前Demo）：
```yaml
versions:
- name: v1
  served: true
  storage: true
```

**多版本共存**（生产环境建议）：
```yaml
versions:
- name: v2         # 新版本
  served: true
  storage: true    # 存储版本
- name: v1         # 旧版本
  served: true     # 仍提供服务
  storage: false   # 不再用于存储
  deprecated: true # 标记为废弃
```

### 5. 实际应用场景

**场景1：应用部署管理**
```yaml
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: production-api
spec:
  replicas: 5
  image: myapp:v2.1.0
  port: 8080
  resources:
    cpu: "1"
    memory: "1Gi"
```

**场景2：微服务配置**
```yaml
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: user-service
spec:
  replicas: 3
  image: user-svc:latest
  port: 3000
```

---

## ✅ 测试验证

### 功能正确性测试

**测试1：资源创建**
```bash
kubectl apply -f manifests/cr-example.yaml
kubectl get appdeployments
# 验证：3个资源成功创建
```

**测试2：Schema验证（边界值）**
```bash
# 测试最小值
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-min
spec:
  replicas: 1
  image: nginx:latest
  port: 1
' | kubectl apply -f -
# 验证：成功创建

# 测试超出范围（应失败）
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-invalid
spec:
  replicas: 100
  image: nginx:latest
  port: 80
' | kubectl apply -f -
# 验证：报错 "spec.replicas: Invalid value: 100: spec.replicas in body should be less than or equal to 10"
```

**测试3：字段验证**
```bash
# 测试非法镜像名（应失败）
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-bad-image
spec:
  replicas: 1
  image: "invalid image name"
  port: 80
' | kubectl apply -f -
# 验证：报错 pattern不匹配
```

### 错误处理测试

**错误1：缺少必填字段**
```bash
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-missing
spec:
  replicas: 1
  # 缺少image和port字段
' | kubectl apply -f -
# 预期：ValidationError - missing required field
```

**错误2：类型错误**
```bash
echo '
apiVersion: demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-type-error
spec:
  replicas: "three"  # 应该是integer
  image: nginx:latest
  port: 80
' | kubectl apply -f -
# 预期：ValidationError - invalid type
```

### 清理验证

```bash
# 执行清理
bash scripts/cleanup.sh

# 验证1：资源实例已删除
kubectl get appdeployments
# 输出：No resources found

# 验证2：CRD已删除
kubectl get crd appdeployments.demo.opendemo.io
# 输出：Error from server (NotFound)

# 验证3：API不再注册
kubectl api-resources | grep appdeployment
# 输出：无结果
```

---

## 🎓 进阶使用

### 1. 与Operator结合

CRD定义了"声明式API"，Operator实现"控制逻辑"：

```
CRD            →    定义资源结构
Custom Resource →    用户期望状态
Operator        →    实现期望状态
```

参考本项目的Operator Demo：`operator-controller-demo`

### 2. Admission Webhook集成

通过Webhook实现复杂验证逻辑：

```yaml
spec:
  conversion:  # 版本转换Webhook
    strategy: Webhook
    webhook:
      clientConfig:
        service:
          name: conversion-webhook
          namespace: default
```

### 3. 生产环境注意事项

**版本管理**：
- 始终保持一个storage版本
- 逐步废弃旧版本
- 提供版本转换机制

**性能优化**：
- 合理设置字段默认值
- 避免过于复杂的Schema
- 使用索引优化查询

**安全考虑**：
- 限制CRD创建权限
- 使用RBAC控制资源访问
- 避免在CRD中存储敏感信息

### 4. 与原生资源集成

**OwnerReference关联**：
```yaml
metadata:
  ownerReferences:
  - apiVersion: demo.opendemo.io/v1
    kind: AppDeployment
    name: nginx-app
    uid: <uid>
    controller: true
```

**Label选择器**：
```yaml
spec:
  selector:
    matchLabels:
      app.kubernetes.io/managed-by: appdeployment-controller
```

---

## 🔍 故障排查

| 现象 | 可能原因 | 解决方法 |
|------|----------|----------|
| **CRD创建失败** | API版本不兼容 | 检查集群版本：`kubectl version`，确保≥1.16 |
| **资源无法创建** | Schema验证失败 | 查看错误详情：`kubectl apply -f file.yaml -v=8` |
| **CRD未就绪** | Webhook配置错误 | 检查Webhook服务：`kubectl get validatingwebhookconfigurations` |
| **资源删除卡住** | Finalizer未清理 | 手动移除Finalizer：`kubectl patch ... --type=merge -p '{"metadata":{"finalizers":null}}'` |
| **版本冲突** | 多版本配置错误 | 确保只有一个storage版本：`kubectl get crd ... -o yaml \| grep storage` |
| **权限不足** | 缺少CRD权限 | 使用cluster-admin角色或添加CRD权限 |

**查看详细错误**：
```bash
# 查看CRD状态
kubectl describe crd appdeployments.demo.opendemo.io

# 查看资源事件
kubectl describe appdeployment <name>

# 查看API服务器日志
kubectl logs -n kube-system <kube-apiserver-pod>
```

**常见错误示例**：

错误1：Schema格式错误
```
Error: ValidationError(CustomResourceDefinition.spec.versions[0].schema.openAPIV3Schema): 
invalid type for io.k8s.apiextensions-apiserver.pkg.apis.apiextensions.v1.JSONSchemaProps: 
got "map", expected "string"
```
解决：检查YAML缩进和字段类型

错误2：CRD名称冲突
```
Error from server (Conflict): customresourcedefinitions.apiextensions.k8s.io 
"appdeployments.demo.opendemo.io" already exists
```
解决：删除已存在的CRD或使用不同的group/plural

---

## 🧹 清理资源

### 完整清理步骤

**方式1：使用清理脚本**
```bash
bash scripts/cleanup.sh
```

**方式2：手动清理**
```bash
# 步骤1：删除所有自定义资源实例
kubectl delete appdeployments --all

# 步骤2：删除CRD定义
kubectl delete crd appdeployments.demo.opendemo.io

# 步骤3：验证清理完成
kubectl get appdeployments
kubectl get crd appdeployments.demo.opendemo.io
```

### 清理验证

```bash
# 检查是否有残留资源
kubectl get appdeployments --all-namespaces

# 检查CRD是否完全删除
kubectl api-resources | grep appdeployment

# 如果有finalizer阻塞删除
kubectl patch crd appdeployments.demo.opendemo.io \
  -p '{"metadata":{"finalizers":[]}}' --type=merge
```

---

## 📚 参考资料

### 官方文档
- [Kubernetes CRD官方文档](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [OpenAPI v3 Schema规范](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.0.md#schemaObject)
- [API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

### 相关教程
- [Kubernetes API扩展机制](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/)
- [自定义资源最佳实践](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

### 社区资源
- [kubebuilder - Operator开发框架](https://book.kubebuilder.io/)
- [Operator SDK](https://sdk.operatorframework.io/)
- [Awesome Operators](https://github.com/operator-framework/awesome-operators)

### 本项目相关
- [Operator控制器开发Demo](../operator-controller-demo/) - 下一步学习
- [KubeSkoop网络诊断](../../kubeskoop/) - 生产级CRD示例

---

## 💡 提示

- ✅ CRD只是定义资源结构，不包含业务逻辑
- ✅ 需要Operator或控制器才能实现自动化管理
- ✅ Schema验证在API服务器层面执行，非常高效
- ✅ 合理使用defaulting和validation减少用户配置负担
- ✅ Status子资源是Operator模式的核心设计

---

**Created**: 2026-01-06  
**Version**: 1.0.0  
**License**: MIT
