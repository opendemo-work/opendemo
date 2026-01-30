# Kubernetes 自定义资源定义（CRD）基础案例

## 什么是 CRD？

自定义资源定义（Custom Resource Definition，简称 CRD）是 Kubernetes API 的扩展机制，允许用户定义自己的资源类型，就像内置的 Pod、Service 等资源一样。

## 本案例包含的内容

- **crd.yaml**: 自定义资源定义，定义了 `App` 资源类型
- **sample-app.yaml**: 示例 App 资源

## 快速开始

### 1. 部署 CRD

```bash
kubectl apply -f crd.yaml
```

### 2. 验证 CRD 已注册

```bash
kubectl get crd apps.example.com
```

### 3. 创建示例 App 资源

```bash
kubectl apply -f sample-app.yaml
```

### 4. 查看创建的 App 资源

```bash
kubectl get apps.example.com
kubectl describe app sample-app
```

### 5. 查看 App 资源的 YAML 配置

```bash
kubectl get app sample-app -o yaml
```

### 6. 更新 App 资源

```bash
kubectl patch app sample-app --type='merge' -p '{"spec":{"replicas":3}}'
```

### 7. 删除 App 资源

```bash
kubectl delete app sample-app
```

## 清理资源

```bash
kubectl delete -f crd.yaml
```

## CRD 的主要组成部分

1. **group**: API 组名，格式为 `example.com`
2. **versions**: API 版本列表，支持多版本并存
3. **scope**: 资源作用域，可选择 `Namespaced`（命名空间级）或 `Cluster`（集群级）
4. **names**: 资源的各种名称形式
5. **schema**: 资源的 JSON Schema 定义，用于验证资源配置

## 工作原理

1. **CRD 注册**: 通过 `kubectl apply -f crd.yaml` 将 CRD 注册到 Kubernetes API Server
2. **API 发现**: Kubernetes API Server 自动创建对应的 API 端点
3. **资源操作**: 用户可以使用标准的 `kubectl` 命令操作自定义资源
4. **验证**: Kubernetes API Server 根据 CRD 中定义的 schema 验证资源配置

## 扩展建议

1. 添加多个 API 版本，实现资源版本转换
2. 为 CRD 添加状态子资源，用于跟踪资源状态
3. 实现自定义控制器，自动处理资源的创建、更新和删除
4. 使用 OpenAPI v3 Schema 定义更复杂的资源结构

## 相关链接

- [Kubernetes CRD 官方文档](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [OpenAPI v3 Schema 参考](https://swagger.io/specification/)
- [Kubernetes API 扩展机制](https://kubernetes.io/docs/concepts/extend-kubernetes/)
