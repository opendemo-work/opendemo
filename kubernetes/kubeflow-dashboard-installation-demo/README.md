# Kubeflow Dashboard 安装与配置演示

## 简介
本演示展示了如何在本地或远程 Kubernetes 集群上安装 Kubeflow Dashboard。Kubeflow 是一个为 Kubernetes 设计的机器学习平台，其核心组件之一是可视化 Dashboard，用于管理实验、训练任务和模型部署。

本项目提供了一个简化但完整的流程，帮助初学者快速搭建 Kubeflow 基础环境并访问其 Web UI。

## 学习目标
- 理解 Kubeflow 的基本架构和 Dashboard 的作用
- 掌握使用 kubectl 和原生清单文件部署 Kubeflow 组件的方法
- 学会通过端口转发访问 Kubeflow Dashboard
- 了解 Istio 在流量管理中的角色

## 环境要求
- 操作系统：Windows / Linux / macOS
- kubectl：v1.24 或更高版本
- Kubernetes 集群（可用 minikube、kind 或云厂商托管集群）
- Helm：v3.9+（用于安装 Istio）
- Internet 连接（用于拉取镜像和清单）

## 安装依赖的详细步骤

### 1. 安装 kubectl
```bash
# macOS
brew install kubectl

# Linux (Ubuntu)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Windows: 下载 https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe
```

### 2. 启动 Kubernetes 集群（以 minikube 为例）
```bash
minikube start --memory=8192 --cpus=4
```

### 3. 安装 Helm
```bash
# macOS
brew install helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 4. 安装 Istio（Kubeflow 所需的服务网格）
```bash
# 下载 Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH="$PWD/bin:$PATH"

# 安装 Istio 默认配置
istioctl install --set profile=demo -y
```

## 文件说明
- `kubeflow-namespace.yaml`: 创建 Kubeflow 所需的命名空间
- `kubeflow-dashboard-deployment.yaml`: 部署 Kubeflow Dashboard 的核心组件
- `kubeflow-service.yaml`: 为 Dashboard 创建服务以便访问

## 逐步实操指南

### 步骤 1: 创建 Kubeflow 命名空间
```bash
kubectl apply -f kubeflow-namespace.yaml
```
**预期输出：**
```bash
namespace/kubeflow created
```

### 步骤 2: 部署 Kubeflow Dashboard 组件
```bash
kubectl apply -f kubeflow-dashboard-deployment.yaml
```
**预期输出：**
```bash
deployment.apps/kubeflow-dashboard created
```

### 步骤 3: 创建服务暴露 Dashboard
```bash
kubectl apply -f kubeflow-service.yaml
```
**预期输出：**
```bash
service/kubeflow-dashboard-svc created
```

### 步骤 4: 启动端口转发以访问 Dashboard
```bash
kubectl port-forward svc/kubeflow-dashboard-svc -n kubeflow 8080:80
```

打开浏览器访问：`http://localhost:8080`

**预期行为：** 浏览器中显示 Kubeflow 登录界面或主页（取决于版本）

## 代码解析

### kubeflow-namespace.yaml
创建名为 `kubeflow` 的命名空间，用于隔离 Kubeflow 相关资源，符合 Kubernetes 最佳实践中的环境隔离原则。

### kubeflow-dashboard-deployment.yaml
部署一个基于官方镜像的 Deployment，运行 Kubeflow Dashboard 前端服务。使用了资源限制和就绪探针，确保稳定性。

### kubeflow-service.yaml
定义 ClusterIP 类型的服务，将 Pod 暴露在集群内部，并通过端口转发供本地访问。这是安全且推荐的开发测试方式。

## 预期输出示例
```bash
$ kubectl get pods -n kubeflow
NAME                                   READY   STATUS    RESTARTS   AGE
kubeflow-dashboard-7b8c6d9f4f-xz2qk    1/1     Running   0          2m

$ kubectl get svc -n kubeflow
NAME                     TYPE        CLUSTER-IP      PORT(S)
kubeflow-dashboard-svc   ClusterIP   10.96.123.45    80/TCP
```

## 常见问题解答

**Q: 访问 localhost:8080 显示连接被拒绝？**
A: 请确认 `port-forward` 命令正在运行，并检查 Pod 是否处于 Running 状态。

**Q: 镜像拉取失败？**
A: 确保网络畅通，或使用国内镜像源替换 `gcr.io/kubeflow-images-public` 为对应镜像仓库。

**Q: 如何在生产环境中暴露服务？**
A: 应使用 Ingress + TLS 配置，而非 port-forward，结合 Istio Gateway 实现安全外部访问。

## 扩展学习建议
- 学习 Kubeflow Pipelines 构建 ML 工作流
- 探索使用 kfctl 或 Manifests 完整部署整个 Kubeflow 平台
- 研究 Istio VirtualService 和 Gateway 配置
- 尝试集成 Prometheus 和 Grafana 监控 ML 任务
- 阅读 Kubeflow 官方文档：https://www.kubeflow.org/docs/