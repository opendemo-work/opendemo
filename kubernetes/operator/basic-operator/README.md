# Kubernetes Operator 模式基础案例

## 什么是 Kubernetes Operator？

Kubernetes Operator 是一种软件扩展，用于管理 Kubernetes 应用程序，它利用自定义资源定义（CRD）和控制器来实现自动化操作。

## 本案例包含的内容

- **crd.yaml**: 自定义资源定义，定义了 `Demo` 资源类型
- **rbac.yaml**: RBAC 权限配置，授权 Operator 访问 Kubernetes API
- **operator-deployment.yaml**: Operator 控制器的 Deployment
- **sample-demo.yaml**: 示例 Demo 资源

## 快速开始

### 1. 部署 CRD

```bash
kubectl apply -f crd.yaml
```

### 2. 部署 RBAC 权限

```bash
kubectl apply -f rbac.yaml
```

### 3. 部署 Operator 控制器

```bash
kubectl apply -f operator-deployment.yaml
```

### 4. 检查 Operator 状态

```bash
kubectl get pods -l app=demo-operator
```

### 5. 创建示例 Demo 资源

```bash
kubectl apply -f sample-demo.yaml
```

### 6. 查看创建的 Demo 资源

```bash
kubectl get demos.example.com
```

## 清理资源

```bash
kubectl delete -f sample-demo.yaml
kubectl delete -f operator-deployment.yaml
kubectl delete -f rbac.yaml
kubectl delete -f crd.yaml
```

## 工作原理

1. **CRD 注册**: 首先注册自定义资源定义，让 Kubernetes 认识 `Demo` 资源类型
2. **RBAC 授权**: 为 Operator 控制器提供访问 Kubernetes API 的权限
3. **控制器部署**: 部署 Operator 控制器，它会监听 `Demo` 资源的变化
4. **资源创建**: 当创建 `Demo` 资源时，控制器会根据资源的 `spec` 执行相应的操作

## 扩展建议

1. 替换 Operator 控制器的镜像，使用真正的控制器实现
2. 扩展 CRD 的 schema，添加更多字段
3. 实现复杂的业务逻辑，如自动扩缩容、滚动更新等

## 相关链接

- [Kubernetes Operator 官方文档](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [Operator SDK](https://sdk.operatorframework.io/)
- [Kubebuilder](https://book.kubebuilder.io/)
