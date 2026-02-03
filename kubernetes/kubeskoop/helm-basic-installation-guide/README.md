# Helm基础安装与使用演示

## 简介
本演示项目旨在帮助初学者理解如何在Kubernetes集群中安装、配置并使用Helm——Kubernetes的包管理工具。通过本指南，您将学会如何使用Helm快速部署应用、管理Chart以及升级和回滚版本。

## 学习目标
- 理解Helm的基本概念（Chart、Release、Repository）
- 掌握Helm的安装与初始化
- 能够使用Helm部署、升级和删除应用
- 了解如何自定义Chart值

## 环境要求
- 操作系统：Windows / Linux / macOS
- minikube >= 1.25（用于本地Kubernetes集群）
- kubectl >= 1.20
- Helm >= 3.8

> 提示：所有工具均支持跨平台，建议使用最新稳定版。

## 安装依赖的详细步骤

### 1. 安装 minikube 和 kubectl

#### macOS (使用 Homebrew)
```bash
brew install minikube kubectl
```

#### Linux (使用官方二进制)
```bash
# 下载 kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# 安装 minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

#### Windows (使用 Chocolatey)
```powershell
choco install minikube kubectl
```

### 2. 启动本地 Kubernetes 集群
```bash
minikube start
```

预期输出：
```
😄  minikube v1.xx.x on Microsoft Windows ...
✨  Automatically selected the docker driver
👍  Starting control plane node minikube in cluster minikube
...
🏄  Done! kubectl is now configured to use "minikube" cluster.
```

## 文件说明
- `chart-example/`: 一个简单的Nginx Helm Chart示例
- `values.yaml`: 自定义配置文件
- `dependency`: 项目依赖声明

## 逐步实操指南

### 步骤1：验证环境
```bash
kubectl version --short
helm version
```

**预期输出**：显示客户端版本信息，无错误。

### 步骤2：创建一个简单的 Helm Chart
```bash
helm create chart-example
```

> 这将生成一个名为 `chart-example` 的标准目录结构。

### 步骤3：修改 values.yaml 以简化部署
编辑 `chart-example/values.yaml`，将 `replicaCount` 改为 1，并确保 `image.repository` 为 `nginx`。

### 步骤4：部署应用
```bash
helm install my-nginx ./chart-example
```

**预期输出**：
```
NAME: my-nginx
LAST DEPLOYED: Mon Apr  1 10:00:00 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

### 步骤5：查看部署状态
```bash
helm list
kubectl get pods
```

### 步骤6：升级 Release
修改 `chart-example/values.yaml` 中的 `service.type` 为 `NodePort`，然后执行：
```bash
helm upgrade my-nginx ./chart-example
```

### 步骤7：查看历史与回滚
```bash
helm history my-nginx
helm rollback my-nginx 1
```

### 步骤8：卸载 Release
```bash
helm uninstall my-nginx
```

## 代码解析

### chart-example/values.yaml
```yaml
replicaCount: 1
image:
  repository: nginx
  tag: "latest"
service:
  type: ClusterIP
  port: 80
```

- `replicaCount`: 控制Pod副本数量
- `image.repository`: 指定容器镜像
- `service.type`: 定义服务暴露方式

这些值可在 `templates/` 中被Go模板引擎引用，实现动态渲染。

## 预期输出示例
```bash
$ helm list
NAME       NAMESPACE  REVISION   STATUS     CHART             APP VERSION
my-nginx   default    2          deployed chart-example-v0.1.0 1.16.0
```

## 常见问题解答

**Q: Helm 安装时报错 'cannot connect to Tiller'?**
A: Helm 3 已移除 Tiller 组件，确保你使用的是 Helm 3+ 版本。

**Q: 如何查看 Helm 渲染后的 YAML？**
A: 使用命令 `helm template ./chart-example` 或 `helm install --dry-run --debug my-nginx ./chart-example`

**Q: 如何添加公共仓库？**
A: `helm repo add stable https://charts.helm.sh/stable`（注意：stable 已归档，可尝试 bitnami）

## 扩展学习建议
- 学习如何创建自己的 Helm Chart 并发布到私有仓库
- 探索 Helm Hooks 的使用场景
- 尝试使用 Helmfile 管理多环境部署
- 阅读官方文档：https://helm.sh/docs/