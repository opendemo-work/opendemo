# Packet Capture Demo - Kubernetes 网络抓包实战

## 简介
本演示展示如何在 Kubernetes 集群中通过 Sidecar 模式安全地进行网络数据包捕获，用于故障排查和流量分析。避免直接在主应用容器中安装调试工具，遵循最小权限原则。

## 学习目标
- 掌握 Kubernetes 中使用 Sidecar 进行网络诊断的方法
- 理解共享网络命名空间的原理与配置
- 学会使用 tcpdump 在生产环境中安全抓包
- 实践容器化调试工具的最佳实践

## 环境要求
- kubectl >= 1.20
- Docker >= 20.10
- 可选：Minikube >= 1.25（本地测试）
- 操作系统：Windows / Linux / macOS

## 安装依赖步骤

### 1. 安装 kubectl
```bash
# Linux/macOS
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://dl.k8s.io/release/$(Invoke-RestMethod -Uri https://dl.k8s.io/release/stable.txt)/bin/windows/amd64/kubectl.exe" -OutFile kubectl.exe
```

### 2. 安装 Docker
访问 https://www.docker.com/products/docker-desktop 下载对应平台版本

### 3. 启动集群（如使用 Minikube）
```bash
minikube start --driver=docker
```

## 文件说明
- `pod-with-tcpdump-sidecar.yaml`：主应用与 tcpdump Sidecar 的 Pod 定义
- `capture-packets.sh`：自动化抓包脚本
- `verify-capture.sh`：验证抓包结果脚本

## 逐步实操指南

### 步骤 1: 创建带有 tcpdump Sidecar 的 Pod
```bash
kubectl apply -f pod-with-tcpdump-sidecar.yaml
```

**预期输出：**
```
pod/packet-capture-demo created
```

### 步骤 2: 等待 Pod 就绪
```bash
kubectl get pods -w
```
等待状态变为 `Running` 后按 Ctrl+C 退出

### 步骤 3: 执行网络抓包
```bash
./capture-packets.sh
```

**预期输出：**
```
capturing packets on eth0...
10 packets captured
Saved to capture.pcap
```

### 步骤 4: 查看抓包结果
```bash
./verify-capture.sh
```

**预期输出：**
```
Reading from capture.pcap
IP 172.17.0.10.45678 > 172.17.0.11.80: Flags [S], seq ...
... (显示数据包内容)
```

### 步骤 5: 清理资源
```bash
kubectl delete -f pod-with-tcpdump-sidecar.yaml
```

## 代码解析

### pod-with-tcpdump-sidecar.yaml 关键点
- `shareProcessNamespace: true`：允许容器间信号通信
- `hostNetwork: false`：使用 Pod 网络而非主机网络（更安全）
- `securityContext.privileged: false`：避免特权模式，提升安全性
- `emptyDir` 卷用于容器间共享抓包文件

### capture-packets.sh 脚本逻辑
- 使用 `kubectl exec` 进入 sidecar 容器
- 运行 tcpdump 抓取指定数量的数据包
- 保存到共享卷供后续分析

## 预期输出示例
```bash
$ ./capture-packets.sh 
capturing packets on eth0...
reading from file -, link-type EN10MB (Ethernet)
10 packets captured
12 packets received by filter
0 packets dropped by kernel
Saved to capture.pcap
```

## 常见问题解答

**Q: 抓包时提示 permission denied？**
A: 确保 tcpdump 镜像已正确构建并推送到镜像仓库，或使用本地镜像：`minikube image load your-image:tag`

**Q: 为什么看不到任何流量？**
A: 主容器需要产生网络流量。可修改 nginx 配置或添加 curl 循环测试。

**Q: 如何抓取特定端口的流量？**
A: 修改 capture-packets.sh 中的 tcpdump 命令，例如：`tcpdump -i eth0 -c 10 port 80 -w /captures/capture.pcap`

## 扩展学习建议
- 结合 NetworkPolicy 限制抓包范围
- 使用 eBPF 工具（如 cilium monitor）替代传统抓包
- 将抓包功能封装为 Kubernetes Job 资源
- 集成到 CI/CD 流水线中用于自动化网络测试