# 🌐 Kubernetes Ingress基础入门实战

> 全面掌握Kubernetes Ingress的核心概念、控制器安装和基础路由配置，从零开始构建外部访问入口

## 📋 案例概述

本案例详细介绍Kubernetes Ingress的基础知识和实践操作，帮助初学者快速理解和掌握Ingress的核心概念和使用方法。

### 🔧 核心技能点

- **Ingress基本概念**: 理解Ingress的作用和工作原理
- **控制器安装**: NGINX Ingress Controller的部署和配置
- **基础路由配置**: 路径路由和主机路由的实现
- **服务暴露**: 通过Ingress暴露内部服务
- **域名配置**: 域名绑定和DNS设置

### 🎯 适用人群

- Kubernetes初学者
- DevOps工程师
- 系统管理员
- 微服务架构学习者

---

## 🚀 快速开始

### 1. 环境准备

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 检查Kubernetes集群状态
kubectl cluster-info
kubectl get nodes

# 创建专用命名空间
kubectl create namespace ingress-demo

# 启用Ingress API（如果尚未启用）
kubectl get ingressclasses
```

### 2. 部署测试应用

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署示例应用
kubectl apply -f sample-apps.yaml -n ingress-demo

# 验证应用部署
kubectl get pods -n ingress-demo
kubectl get services -n ingress-demo
```

---

## 📚 详细教程

### 1. Ingress核心概念

Ingress是Kubernetes中管理外部访问集群服务的API对象，主要功能包括：

#### 1.1 Ingress的作用
- 提供HTTP/HTTPS路由规则
- 实现基于域名和路径的流量分发
- 支持负载均衡和SSL/TLS终结
- 集中管理外部访问策略

#### 1.2 Ingress架构组成

```
外部请求 → Ingress Controller → Ingress规则 → Service → Pod
```

#### 1.3 主要组件说明

- **Ingress**: 定义路由规则的API对象
- **Ingress Controller**: 实际处理请求的控制器（如NGINX、Traefik）
- **IngressClass**: 指定使用的控制器类型

### 2. Ingress Controller安装

#### 2.1 NGINX Ingress Controller安装

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 方法1：使用Helm安装（推荐）
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer

# 方法2：使用YAML安装
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# 验证安装
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

#### 2.2 控制器配置验证

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 检查IngressClass
kubectl get ingressclasses

# 检查控制器状态
kubectl get pods -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 获取外部IP地址
kubectl get svc ingress-nginx-controller -n ingress-nginx
```

### 3. 基础Ingress配置

#### 3.1 简单路径路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-ingress
  namespace: ingress-demo
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /app1
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
      - path: /app2
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
```

#### 3.2 基于主机的路由

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: host-based-ingress
  namespace: ingress-demo
spec:
  ingressClassName: nginx
  rules:
  - host: app1.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
  - host: app2.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
```

#### 3.3 默认后端配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: default-backend-ingress
  namespace: ingress-demo
spec:
  ingressClassName: nginx
  defaultBackend:
    service:
      name: default-service
      port:
        number: 80
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
```

### 4. 部署示例应用

#### 4.1 应用部署配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-deployment
  namespace: ingress-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
      - name: app1
        image: nginx:1.21
        ports:
        - containerPort: 80
        env:
        - name: APP_NAME
          value: "Application 1"
---
apiVersion: v1
kind: Service
metadata:
  name: app1-service
  namespace: ingress-demo
spec:
  selector:
    app: app1
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2-deployment
  namespace: ingress-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app2
  template:
    metadata:
      labels:
        app: app2
    spec:
      containers:
      - name: app2
        image: nginx:1.21
        ports:
        - containerPort: 80
        env:
        - name: APP_NAME
          value: "Application 2"
---
apiVersion: v1
kind: Service
metadata:
  name: app2-service
  namespace: ingress-demo
spec:
  selector:
    app: app2
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

#### 4.2 部署和验证

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 部署应用
kubectl apply -f sample-apps.yaml -n ingress-demo

# 部署Ingress规则
kubectl apply -f ingress-rules.yaml -n ingress-demo

# 验证部署状态
kubectl get pods -n ingress-demo
kubectl get services -n ingress-demo
kubectl get ingress -n ingress-demo
```

### 5. 访问测试

#### 5.1 获取Ingress地址

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 获取LoadBalancer IP
INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# 如果使用NodePort
NODE_PORT=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.spec.ports[0].nodePort}')
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
```

#### 5.2 路径路由测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 测试路径路由
curl http://$INGRESS_IP/app1
curl http://$INGRESS_IP/app2

# 测试默认后端
curl http://$INGRESS_IP/nonexistent-path
```

#### 5.3 主机路由测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 添加hosts记录（本地测试）
echo "$INGRESS_IP app1.example.com" | sudo tee -a /etc/hosts
echo "$INGRESS_IP app2.example.com" | sudo tee -a /etc/hosts

# 测试主机路由
curl -H "Host: app1.example.com" http://$INGRESS_IP
curl -H "Host: app2.example.com" http://$INGRESS_IP
```

---

## 🔧 常用注解配置

### 1. 基础注解

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: annotated-ingress
  namespace: ingress-demo
  annotations:
    # 重写目标路径
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    
    # 请求速率限制
    nginx.ingress.kubernetes.io/rate-limit: "100"
    
    # 连接限制
    nginx.ingress.kubernetes.io/limit-connections: "10"
    
    # 代理缓冲区
    nginx.ingress.kubernetes.io/proxy-buffering: "on"
    
    # 客户端最大体大小
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /app(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
```

### 2. 负载均衡注解

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: loadbalancing-ingress
  namespace: ingress-demo
  annotations:
    # 负载均衡算法
    nginx.ingress.kubernetes.io/upstream-hash-by: "$remote_addr"
    
    # 会话保持
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "route"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

---

## 📊 监控和日志

### 1. 查看Ingress日志

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 查看控制器日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 查看特定Pod日志
kubectl logs -n ingress-nginx <controller-pod-name>

# 实时跟踪日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx -f
```

### 2. 监控指标

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看控制器指标端点
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 10254:10254

# 在浏览器中访问
# http://localhost:10254/metrics
```

### 3. 常用监控命令

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 查看Ingress状态
kubectl describe ingress <ingress-name> -n ingress-demo

# 查看控制器配置
kubectl get configmap nginx-configuration -n ingress-nginx -o yaml

# 检查端点状态
kubectl get endpoints -n ingress-demo
```

---

## ⚠️ 常见问题和解决方案

### 1. Ingress无法访问

**问题现象**: 404 Not Found或连接超时

**排查步骤**:
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 1. 检查Ingress状态
kubectl describe ingress <ingress-name> -n ingress-demo

# 2. 检查控制器Pod状态
kubectl get pods -n ingress-nginx

# 3. 检查服务端点
kubectl get endpoints -n ingress-demo

# 4. 查看控制器日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

### 2. 路径匹配问题

**问题现象**: 路径路由不正确

**解决方案**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fixed-path-ingress
  namespace: ingress-demo
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      # 使用正则表达式匹配路径
      - path: /app(/|$)(.*)
        pathType: ImplementationSpecific  # 更精确的路径匹配
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### 3. 主机名解析问题

**问题现象**: 基于主机名的路由不工作

**解决方案**:
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 检查DNS配置
nslookup app.example.com

# 2. 本地hosts文件配置
echo "<ingress-ip> app.example.com" | sudo tee -a /etc/hosts

# 3. 或者使用curl直接测试
curl -H "Host: app.example.com" http://<ingress-ip>
```

---

## 🧪 实践练习

### 练习1：基础路由配置
部署三个不同的应用，配置基于路径的路由规则，使用户可以通过不同路径访问不同应用。

### 练习2：主机路由实践
配置基于主机名的路由，为不同的域名指向不同的后端服务。

### 练习3：混合路由策略
实现同时包含路径和主机名的复合路由规则。

### 练习4：故障排查演练
故意配置错误的Ingress规则，练习故障诊断和修复技能。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes Ingress官方文档](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [NGINX Ingress Controller文档](https://kubernetes.github.io/ingress-nginx/)

### 相关案例
- [Ingress高级特性](../ingress-advanced/)
- [Ingress安全配置](../ingress-security/)
- [Ingress生产最佳实践](../ingress-production/)

### 进阶主题
- TLS/SSL证书配置
- 路径重写和正则表达式
- 自定义注解和配置
- 多集群Ingress管理

---

## 📋 清理资源

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 删除所有示例资源
kubectl delete namespace ingress-demo

# 删除Ingress Controller（如果需要）
kubectl delete namespace ingress-nginx

# 或单独删除各项资源
kubectl delete ingress --all -n ingress-demo
kubectl delete svc --all -n ingress-demo
kubectl delete deploy --all -n ingress-demo
```

---

> **💡 提示**: Ingress是Kubernetes中非常重要的网络组件，建议先掌握基础概念再学习高级特性。在生产环境中使用时要注意安全配置和监控告警。
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

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
