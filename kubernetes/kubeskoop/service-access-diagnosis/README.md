# Kubernetes服务访问诊断Demo

## 简介
本示例演示了在Kubernetes集群中常见的服务访问问题及其诊断方法。通过部署一个简单的Web应用和多个测试Pod，展示如何排查服务发现、网络连通性和DNS解析等问题。

## 学习目标
- 掌握Kubernetes服务访问的基本原理
- 学会使用诊断工具（如curl、nslookup）排查服务连接问题
- 理解Service、Pod和DNS之间的关系
- 掌握kubectl调试命令的实际应用

## 环境要求
- 操作系统：Windows / Linux / macOS
- kubectl v1.20 或更高版本
- 可选：minikube（用于本地运行）
- curl 工具（大多数系统自带）

## 安装依赖步骤
1. 安装kubectl：
   ```bash
   # Linux/macOS
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   chmod +x kubectl
   sudo mv kubectl /usr/local/bin/
   ```

   Windows用户请参考官方文档下载kubectl.exe

2. （可选）安装minikube：
   ```bash
   # Linux/macOS
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```

3. 启动集群（若使用minikube）：
   ```bash
   minikube start
   ```

## 文件说明
- `web-server.yaml`: 部署一个简单的HTTP服务器作为目标服务
- `diagnose-pod.yaml`: 创建用于诊断的临时Pod
- `service-definition.yaml`: 定义ClusterIP类型的服务暴露Web服务器

## 逐步实操指南

### 步骤1: 应用部署
```bash
kubectl apply -f service-definition.yaml
kubectl apply -f web-server.yaml
```

**预期输出**：
```
service/web-service created
deployment.apps/web-server created
```

### 步骤2: 等待Pod就绪
```bash
kubectl get pods -l app=web-server -w
```
等待状态变为`Running`后按Ctrl+C退出。

### 步骤3: 创建诊断Pod
```bash
kubectl apply -f diagnose-pod.yaml
```

**预期输出**：
```
pod/diagnose-pod created
```

### 步骤4: 测试服务连通性
```bash
kubectl exec -it diagnose-pod -- curl http://web-service:8080
```

**预期输出**：
```
Hello, Kubernetes! This is web-server pod.
```

### 步骤5: 模拟并诊断DNS问题（可选）
尝试错误的服务名：
```bash
kubectl exec -it diagnose-pod -- nslookup wrong-service
```
应返回DNS解析失败信息。

## 代码解析

### web-server.yaml
定义了一个轻量级Python HTTP服务器，监听8080端口，并返回简单文本响应。关键点是设置了正确的标签`app: web-server`，以便Service选择器能正确匹配。

### service-definition.yaml
创建ClusterIP类型的Service，将内部流量转发到带有`app=web-server`标签的Pod的8080端口。这是实现服务发现的核心组件。

### diagnose-pod.yaml
使用busybox镜像创建一个包含网络调试工具的Pod。它位于与web-server相同的命名空间，可用于测试服务通信和DNS解析。

## 预期输出示例
```bash
$ kubectl exec -it diagnose-pod -- curl http://web-service:8080
Hello, Kubernetes! This is web-server pod.
```

## 常见问题解答

**Q: curl命令超时？**
A: 检查Pod是否处于Running状态：`kubectl get pods`。确认Service的selector与Pod标签匹配。

**Q: DNS解析失败？**
A: 确保服务名称拼写正确。Kubernetes默认DNS域为`.default.svc.cluster.local`，但同命名空间下可省略。

**Q: 如何从外部访问该服务？**
A: 将Service类型改为NodePort或LoadBalancer，或使用Ingress控制器。

## 扩展学习建议
- 学习使用`kubectl describe service web-service`查看详细事件
- 实践NetworkPolicy限制Pod间通信
- 使用Prometheus和Grafana监控服务健康状况
- 探索Istio等服务网格进行高级流量管理