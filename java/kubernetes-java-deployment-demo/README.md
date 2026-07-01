<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Kubernetes Java 应用部署演示

## 项目简介

本项目是一个 Spring Boot 应用在 Kubernetes（K8s）上的完整部署演示。项目包含应用代码、Dockerfile、Kubernetes 资源清单（Namespace、Deployment、Service、ConfigMap、Ingress）以及健康检查接口。

通过本项目，你将掌握 Spring Boot 应用的容器化构建、Kubernetes 核心资源对象的配置、滚动更新策略、健康检查机制、配置管理以及 Ingress 路由等核心概念。

---

## 目录

1. [Kubernetes 基本概念](#1-kubernetes-基本概念)
2. [Docker 容器化](#2-docker-容器化)
3. [Kubernetes Deployment](#3-kubernetes-deployment)
4. [Service 与服务发现](#4-service-与服务发现)
5. [ConfigMap 配置管理](#5-configmap-配置管理)
6. [Ingress 路由](#6-ingress-路由)
7. [健康检查机制](#7-健康检查机制)
8. [项目代码结构说明](#8-项目代码结构说明)
9. [快速开始](#9-快速开始)
10. [常见问题](#10-常见问题)
11. [参考资料](#11-参考资料)

---

## 1. Kubernetes 基本概念

### 核心架构

```
┌───────────────────────────────────────────────────┐
│                  Kubernetes Cluster                │
│  ┌──────────────────────────────────────────────┐ │
│  │              Master Node                      │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │ │
│  │  │ API Server│ │Scheduler │ │ Controller   │ │ │
│  │  │          │ │          │ │ Manager      │ │ │
│  │  └──────────┘ └──────────┘ └──────────────┘ │ │
│  └──────────────────────────────────────────────┘ │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │   Worker Node 1  │  │   Worker Node 2      │   │
│  │ ┌───┐ ┌───┐     │  │ ┌───┐ ┌───┐         │   │
│  │ │Pod│ │Pod│     │  │ │Pod│ │Pod│         │   │
│  │ └───┘ └───┘     │  │ └───┘ └───┘         │   │
│  │ ┌─────────────┐ │  │ ┌─────────────┐     │   │
│  │ │  kubelet    │ │  │ │  kubelet    │     │   │
│  │ └─────────────┘ │  │ └─────────────┘     │   │
│  └──────────────────┘  └──────────────────────┘   │
└───────────────────────────────────────────────────┘
```

### 核心资源对象

| 资源 | 缩写 | 说明 |
|------|------|------|
| **Pod** | po | 最小调度单元，包含一个或多个容器 |
| **Deployment** | deploy | 管理 Pod 副本集，支持滚动更新 |
| **Service** | svc | 为 Pod 提供稳定的访问入口 |
| **ConfigMap** | cm | 存储非敏感配置数据 |
| **Secret** | - | 存储敏感数据（密码、密钥等） |
| **Ingress** | ing | HTTP 路由规则，外部流量入口 |
| **Namespace** | ns | 资源隔离的逻辑分区 |
| **Node** | no | 集群中的工作节点 |

---

## 2. Docker 容器化

### Dockerfile 详解

本项目的 `Dockerfile`：

```dockerfile
FROM eclipse-temurin:11-jre-alpine    # 使用轻量级 JRE 基础镜像
WORKDIR /app                          # 设置工作目录
COPY target/*.jar app.jar             # 复制 JAR 包
EXPOSE 8080                           # 声明端口
ENTRYPOINT ["java", "-jar", "app.jar"] # 启动命令
```

### 镜像构建最佳实践

| 实践 | 说明 |
|------|------|
| 使用 JRE 而非 JDK | 减小镜像体积（约 100MB vs 400MB） |
| 使用 Alpine 基础镜像 | 基于 musl libc，体积更小 |
| 多阶段构建 | 编译阶段使用 JDK，运行阶段使用 JRE |
| `.dockerignore` | 排除不需要的文件 |
| 非 root 用户 | 安全最佳实践 |

### 构建与推送

```bash
# 构建镜像
docker build -t kubernetes-demo:1.0.0 .

# 本地测试
docker run -p 8080:8080 kubernetes-demo:1.0.0

# 推送到仓库
docker tag kubernetes-demo:1.0.0 registry.example.com/kubernetes-demo:1.0.0
docker push registry.example.com/kubernetes-demo:1.0.0
```

---

## 3. Kubernetes Deployment

### Deployment 配置详解

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-demo
  namespace: kubernetes-demo
spec:
  replicas: 3                          # Pod 副本数量
  selector:
    matchLabels:
      app: kubernetes-demo
  strategy:
    type: RollingUpdate                # 滚动更新策略
    rollingUpdate:
      maxSurge: 1                      # 最多超出副本数 1 个
      maxUnavailable: 0                # 不允许不可用
```

### 滚动更新（Rolling Update）

```
版本 v1:  [Pod1-v1] [Pod2-v1] [Pod3-v1]
                ↓ 更新开始
版本过渡: [Pod1-v1] [Pod2-v1] [Pod3-v1] [Pod4-v2]   (maxSurge=1)
                ↓ 继续更新
版本过渡: [Pod1-v1] [Pod2-v2] [Pod3-v2] [Pod4-v2]
                ↓ 更新完成
版本 v2:  [Pod1-v2] [Pod2-v2] [Pod3-v2]
```

### 资源限制

```yaml
resources:
  requests:                            # 最小保证资源
    memory: "256Mi"
    cpu: "200m"                        # 200 millicores = 0.2 CPU
  limits:                              # 最大允许资源
    memory: "512Mi"
    cpu: "500m"
```

| 参数 | 说明 |
|------|------|
| `requests.memory` | Pod 调度时保证的最小内存 |
| `requests.cpu` | Pod 调度时保证的最小 CPU |
| `limits.memory` | 超过此值容器会被 OOM Kill |
| `limits.cpu` | 超过此值 CPU 会被限流 |

### 常用命令

```bash
# 查看 Deployment
kubectl get deploy -n kubernetes-demo

# 查看 Pod
kubectl get pods -n kubernetes-demo

# 查看滚动更新状态
kubectl rollout status deploy/kubernetes-demo -n kubernetes-demo

# 回滚到上一版本
kubectl rollout undo deploy/kubernetes-demo -n kubernetes-demo

# 扩缩容
kubectl scale deploy/kubernetes-demo --replicas=5 -n kubernetes-demo
```

---

## 4. Service 与服务发现

### Service 类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `ClusterIP` | 集群内部 IP（默认） | 内部服务通信 |
| `NodePort` | 在节点上开放端口 | 开发/测试环境 |
| `LoadBalancer` | 云厂商负载均衡器 | 生产环境（云上） |
| `ExternalName` | CNAME 映射 | 引用外部服务 |

### 本项目 Service 配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-demo-service
spec:
  type: ClusterIP
  selector:
    app: kubernetes-demo              # 匹配 Pod 标签
  ports:
    - name: http
      port: 80                        # Service 端口
      targetPort: 8080                # Pod 容器端口
```

### 服务发现机制

```
同命名空间内访问:
  http://kubernetes-demo-service/

跨命名空间访问:
  http://kubernetes-demo-service.kubernetes-demo.svc.cluster.local
       └── 服务名 ──────┘└── 命名空间 ──┘└── 集群域名 ──┘
```

---

## 5. ConfigMap 配置管理

### ConfigMap 详解

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubernetes-demo-config
  namespace: kubernetes-demo
data:
  welcome-message: "欢迎使用Kubernetes部署演示（来自ConfigMap）"
  log-level: "INFO"
  max-connections: "200"
```

### 使用方式

#### 作为环境变量

```yaml
env:
  - name: WELCOME_MESSAGE
    valueFrom:
      configMapKeyRef:
        name: kubernetes-demo-config
        key: welcome-message
```

#### 挂载为文件

```yaml
volumes:
  - name: config-volume
    configMap:
      name: kubernetes-demo-config
volumeMounts:
  - name: config-volume
    mountPath: /config
```

### ConfigMap vs Secret

| 特性 | ConfigMap | Secret |
|------|-----------|--------|
| 数据类型 | 明文配置 | Base64 编码 |
| 存储大小 | 1MB | 1MB |
| 适用数据 | 非敏感配置 | 密码、密钥、证书 |
| 访问控制 | RBAC | RBAC + 更严格的策略 |

---

## 6. Ingress 路由

### Ingress 配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kubernetes-demo-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: kubernetes-demo.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: kubernetes-demo-service
                port:
                  number: 80
```

### 请求流转

```
客户端请求
    ↓
Ingress Controller (Nginx)
    ↓ 路由匹配: kubernetes-demo.local → kubernetes-demo-service:80
Service (ClusterIP)
    ↓ 选择器匹配: app=kubernetes-demo
Pod (targetPort: 8080)
    ↓
Spring Boot Application
```

### 常用 Ingress 注解

| 注解 | 说明 |
|------|------|
| `nginx.ingress.kubernetes.io/ssl-redirect` | SSL 重定向 |
| `nginx.ingress.kubernetes.io/rewrite-target` | URL 重写 |
| `nginx.ingress.kubernetes.io/proxy-body-size` | 请求体大小限制 |
| `nginx.ingress.kubernetes.io/cors-allow-origin` | CORS 配置 |
| `nginx.ingress.kubernetes.io/rate-limit` | 限流配置 |

---

## 7. 健康检查机制

### 三种探针类型

| 探针 | 说明 | 用途 |
|------|------|------|
| **livenessProbe** | 存活探针 | 检测容器是否运行，失败则重启容器 |
| **readinessProbe** | 就绪探针 | 检测是否可接收流量，失败则从 Service 摘除 |
| **startupProbe** | 启动探针 | 检测应用是否启动完成，成功后才执行其他探针 |

### 探针配置

```yaml
livenessProbe:
  httpGet:
    path: /liveness          # 存活检查路径
    port: 8080
  initialDelaySeconds: 30    # 容器启动后 30 秒开始检查
  periodSeconds: 10          # 每 10 秒检查一次
  timeoutSeconds: 5          # 超时时间 5 秒
  failureThreshold: 3        # 连续失败 3 次则判定为不健康

readinessProbe:
  httpGet:
    path: /readiness         # 就绪检查路径
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

### 本项目的健康端点

| 端点 | 路径 | 对应探针 |
|------|------|---------|
| 健康检查 | `/health` | 综合健康状态 |
| 存活探针 | `/liveness` | livenessProbe |
| 就绪探针 | `/readiness` | readinessProbe |
| 应用信息 | `/info` | - |
| 配置信息 | `/config` | - |

---

## 8. 项目代码结构说明

### 应用层

- **KubernetesDemoApplication.java**：Spring Boot 启动类
- **HealthController.java**：健康检查端点，提供 liveness/readiness 探针
- **InfoController.java**：应用信息端点，展示 JVM 和 K8s 环境信息
- **KubernetesConfig.java**：K8s 环境配置，读取 Pod 元数据和 ConfigMap 配置

### Kubernetes 资源

| 文件 | 资源 | 功能 |
|------|------|------|
| `k8s/namespace.yaml` | Namespace | 命名空间隔离 |
| `k8s/deployment.yaml` | Deployment | 应用部署管理 |
| `k8s/service.yaml` | Service | 服务发现与负载均衡 |
| `k8s/configmap.yaml` | ConfigMap | 外部化配置 |
| `k8s/ingress.yaml` | Ingress | HTTP 路由入口 |

### 构建文件

- **Dockerfile**：容器镜像构建脚本
- **pom.xml**：Maven 构建配置（Spring Boot）

---

## 9. 快速开始

### 前置条件

- JDK 11+
- Maven 3.6+
- Docker
- Kubernetes 集群（minikube 或云上集群）
- kubectl 命令行工具

### 本地开发

```bash
cd java/kubernetes-java-deployment-demo

# 编译项目
mvn clean compile

# 运行测试
mvn test

# 本地运行
mvn spring-boot:run

# 测试端点
curl http://localhost:8080/health
curl http://localhost:8080/info
```

### Docker 构建

```bash
# 打包
mvn clean package -DskipTests

# 构建镜像
docker build -t kubernetes-demo:1.0.0 .

# 本地测试
docker run -p 8080:8080 kubernetes-demo:1.0.0
```

### Kubernetes 部署

```bash
# 创建命名空间
kubectl apply -f k8s/namespace.yaml

# 创建 ConfigMap
kubectl apply -f k8s/configmap.yaml

# 部署应用
kubectl apply -f k8s/deployment.yaml

# 创建 Service
kubectl apply -f k8s/service.yaml

# 创建 Ingress
kubectl apply -f k8s/ingress.yaml

# 查看部署状态
kubectl get all -n kubernetes-demo

# 查看应用日志
kubectl logs -f deploy/kubernetes-demo -n kubernetes-demo

# 端口转发测试
kubectl port-forward svc/kubernetes-demo-service 8080:80 -n kubernetes-demo
```

### 一键部署

```bash
kubectl apply -f k8s/
```

### 清理资源

```bash
kubectl delete -f k8s/
```

---

## 10. 常见问题

### Q1: Pod 一直处于 ImagePullBackOff 状态？

镜像名称或标签不正确，或者镜像仓库需要认证。检查 Deployment 中的 `image` 字段。

### Q2: 如何查看 Pod 日志？

```bash
kubectl logs <pod-name> -n kubernetes-demo
kubectl logs -f deploy/kubernetes-demo -n kubernetes-demo   # 实时跟踪
```

### Q3: 如何进入容器调试？

```bash
kubectl exec -it <pod-name> -n kubernetes-demo -- /bin/sh
```

### Q4: 如何查看 ConfigMap 是否生效？

```bash
kubectl get configmap kubernetes-demo-config -n kubernetes-demo -o yaml
kubectl describe pod <pod-name> -n kubernetes-demo
```

### Q5: 如何在 minikube 中测试？

```bash
minikube start
eval $(minikube docker-env)
docker build -t kubernetes-demo:1.0.0 .
kubectl apply -f k8s/
minikube tunnel
```

---

## 11. 参考资料

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Spring Boot Docker](https://spring.io/guides/topicals/spring-boot-docker/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
