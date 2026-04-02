# Containerd and CRI

Containerd容器运行时与CRI接口演示，深入理解Kubernetes底层容器管理。

## 容器运行时演进

```
演进历程:
Docker (2013) → containerd (2016) → CRI-O (2017)
     │                │                 │
     ▼                ▼                 ▼
  完整平台        轻量运行时        K8s专用
  开发友好        生产稳定          精简高效
```

## Containerd架构

```
containerd架构:
┌─────────────────────────────────────────────────────┐
│                    Client (ctr)                     │
└────────────────────────┬────────────────────────────┘
                         │ gRPC
┌────────────────────────┼────────────────────────────┐
│  containerd daemon     ▼                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Images    │  │  Runtime    │  │   Snapshots │  │
│  │  (镜像管理)  │  │   (runc)    │  │   (存储)     │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Content   │  │  Metadata   │  │    Tasks    │  │
│  │  (内容寻址)  │  │   (元数据)   │  │   (任务管理) │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 安装Containerd

```bash
# Ubuntu/Debian
sudo apt install containerd

# 或使用官方包
wget https://github.com/containerd/containerd/releases/download/v1.7.0/containerd-1.7.0-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local containerd-1.7.0-linux-amd64.tar.gz

# 安装runc
sudo apt install runc

# 启动服务
sudo systemctl start containerd
sudo systemctl enable containerd
```

## 基本操作

```bash
# 拉取镜像
sudo ctr images pull docker.io/library/nginx:latest

# 列出镜像
sudo ctr images list

# 运行容器
sudo ctr run --rm -t docker.io/library/nginx:latest webserver

# 列出容器
sudo ctr containers list

# 执行任务
sudo ctr tasks exec --exec-id shell webserver /bin/sh

# 停止容器
sudo ctr tasks kill -9 webserver
sudo ctr containers delete webserver
```

## CRI插件配置

```toml
# /etc/containerd/config.toml
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.k8s.io/pause:3.9"
  
[plugins."io.containerd.grpc.v1.cri".containerd]
  default_runtime_name = "runc"
  
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  runtime_type = "io.containerd.runc.v2"
  
[plugins."io.containerd.grpc.v1.cri".cni]
  bin_dir = "/opt/cni/bin"
  conf_dir = "/etc/cni/net.d"

# 私有镜像仓库
[plugins."io.containerd.grpc.v1.cri".registry.mirrors."harbor.example.com"]
  endpoint = ["https://harbor.example.com"]
```

## 与Kubernetes集成

```bash
# K8s使用containerd
kubectl get nodes -o wide
# 查看运行时
kubectl get nodes -o jsonpath='{.items[0].status.nodeInfo.containerRuntimeVersion}'

# crictl工具
sudo crictl --runtime-endpoint unix:///run/containerd/containerd.sock images
sudo crictl pods
sudo crictl ps
```

## nerdctl工具

```bash
# 安装nerdctl
wget https://github.com/containerd/nerdctl/releases/download/v1.5.0/nerdctl-1.5.0-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local/bin nerdctl-1.5.0-linux-amd64.tar.gz

# Docker兼容命令
nerdctl run -d -p 80:80 --name nginx nginx:latest
nerdctl ps
nerdctl exec -it nginx /bin/sh
nerdctl logs nginx
nerdctl stop nginx
nerdctl rm nginx

# 构建镜像
nerdctl build -t myapp:latest .
```
