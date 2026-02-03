# Pod连通性诊断演示

## 简介
本演示展示了在Kubernetes集群中如何诊断Pod之间的网络连接问题。通过创建不同的Pod并测试它们之间的通信，学习者可以掌握基本的网络故障排查技巧。

## 学习目标
- 理解Kubernetes中Pod间通信的基本原理
- 学会使用`kubectl exec`命令执行远程命令
- 掌握使用`curl`和`ping`进行网络连通性测试的方法
- 能够识别常见的网络配置错误

## 环境要求
- 操作系统：Windows、Linux或macOS
- 已安装`kubectl`命令行工具（版本1.20及以上）
- 可选：已安装`minikube`用于本地测试

## 安装依赖的详细步骤
1. 安装`kubectl`：
   - 访问 https://kubernetes.io/docs/tasks/tools/install-kubectl/ 获取安装指南
2. （可选）安装`minikube`：
   - 访问 https://minikube.sigs.k8s.io/docs/start/ 获取安装指南
3. 启动集群（如果使用minikube）：
   ```bash
   minikube start
   ```

## 文件说明
- `pod-diagnosis.yaml`: 包含两个Pod定义，一个运行nginx服务器，另一个用于诊断的busybox客户端
- `test-connectivity.sh`: 一个脚本，自动执行连通性测试

## 逐步实操指南

### 步骤1: 应用YAML文件创建Pod
```bash
kubectl apply -f pod-diagnosis.yaml
```
**预期输出:**
```
pod/nginx-server created
pod/diagnosis-client created
```

### 步骤2: 检查Pod状态
```bash
kubectl get pods -o wide
```
**预期输出:**
```
NAME              READY   STATUS    RESTARTS   AGE   IP             NODE       NOMINATED NODE
nginx-server     1/1     Running   0          10s   172.17.0.2     minikube   <none>
diagnosis-client 1/1     Running   0          10s   172.17.0.3     minikube   <none>
```

### 步骤3: 测试从诊断客户端到Nginx服务器的HTTP连接
```bash
kubectl exec diagnosis-client -- wget -qO- http://nginx-server
```
**预期输出:** 应显示Nginx的欢迎页面HTML内容

### 步骤4: 测试ICMP连通性（ping）
```bash
kubectl exec diagnosis-client -- ping -c 3 nginx-server
```
**预期输出:** 显示三次成功的ping响应

### 步骤5: 清理资源
```bash
kubectl delete -f pod-diagnosis.yaml
```
**预期输出:**
```
pod "nginx-server" deleted
pod "diagnosis-client" deleted
```

## 代码解析

### pod-diagnosis.yaml
- 定义了两个Pod：
  - `nginx-server`: 运行标准Nginx镜像，监听80端口
  - `diagnosis-client`: 使用busybox镜像，预装了网络诊断工具如wget和ping
- 使用默认网络命名空间，允许Pod间通过服务名或IP直接通信

### test-connectivity.sh
- 自动化执行常用的连通性测试命令
- 包括HTTP请求和ICMP探测

## 预期输出示例
当所有测试成功时，你应该看到：
- `kubectl get pods` 显示两个Pod都处于Running状态
- `wget` 命令返回Nginx的HTML响应
- `ping` 命令显示来自目标Pod的回复包

## 常见问题解答

**Q: 如果ping不通怎么办？**
A: 大多数容器镜像默认不启用ICMP响应。建议优先使用`wget`或`curl`测试应用层连通性。

**Q: 报错找不到命令如wget或ping？**
A: 确保你使用的镜像是`radial/busyboxplus:curl`这类包含网络工具的镜像，而不是基础busybox镜像。

**Q: 如何跨命名空间测试连通性？**
A: 需要使用完整的服务DNS名称：`<service>.<namespace>.svc.cluster.local`

## 扩展学习建议
- 学习使用Kubernetes Services暴露Pod
- 探索NetworkPolicy实现网络隔离
- 使用`kubectl port-forward`调试本地访问问题
- 尝试使用Istio等服务网格进行高级流量控制