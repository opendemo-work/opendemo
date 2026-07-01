<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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
   🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
   > ⚠️ 生产安全提示：
   > - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
   > - 注意检查依赖版本、端口占用和目标资源配置。
   > - 生产环境执行前请经过变更评审和备份确认。
   ```bash
   minikube start
   ```

## 文件说明
- `pod-diagnosis.yaml`: 包含两个Pod定义，一个运行nginx服务器，另一个用于诊断的busybox客户端
- `test-connectivity.sh`: 一个脚本，自动执行连通性测试

## 逐步实操指南

### 步骤1: 应用YAML文件创建Pod
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl apply -f pod-diagnosis.yaml
```
**预期输出:**
```
pod/nginx-server created
pod/diagnosis-client created
```

### 步骤2: 检查Pod状态
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
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
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl exec diagnosis-client -- wget -qO- http://nginx-server
```
**预期输出:** 应显示Nginx的欢迎页面HTML内容

### 步骤4: 测试ICMP连通性（ping）
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
kubectl exec diagnosis-client -- ping -c 3 nginx-server
```
**预期输出:** 显示三次成功的ping响应

### 步骤5: 清理资源
🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
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
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

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


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*
