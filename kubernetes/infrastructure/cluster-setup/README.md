# 🏗️ Kubernetes集群搭建和初始化实战

> 全面掌握Kubernetes集群的部署、初始化和配置管理，从单节点开发环境到生产级高可用集群的完整搭建指南

## 📋 案例概述

本案例详细介绍Kubernetes集群的完整搭建流程和初始化配置，帮助用户从零开始构建稳定可靠的Kubernetes基础设施。

### 🔧 核心技能点

- **集群规划**: 节点角色划分、网络规划、硬件要求
- **单节点部署**: kubeadm单节点集群快速搭建
- **多节点集群**: 多Master多Worker节点高可用部署
- **初始化配置**: 网络插件、存储配置、系统优化
- **集群验证**: 健康检查、功能测试、性能基准
- **安全管理**: 证书管理、访问控制、安全加固

### 🎯 适用人群

- Kubernetes系统管理员
- DevOps工程师
- 云平台架构师
- 基础设施运维人员

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 检查系统要求
uname -a
cat /etc/os-release
free -h
df -h

# 关闭防火墙和SELinux
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo setenforce 0

# 禁用swap
sudo swapoff -a
sudo sed -i '/swap/d' /etc/fstab

# 加载内核模块
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
overlay
EOF
sudo modprobe br_netfilter overlay

# 配置内核参数
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
sudo sysctl --system
```

### 2. 安装容器运行时

```bash
# 安装containerd
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

sudo yum install -y containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl enable containerd
sudo systemctl start containerd
```

### 3. 安装kubeadm工具

```bash
sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

---

## 📚 详细教程

### 1. 单节点集群搭建

#### 1.1 初始化Master节点

```bash
# 初始化集群
sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --apiserver-advertise-address=192.168.1.100 \
  --cri-socket=/run/containerd/containerd.sock

# 配置kubectl
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 部署网络插件
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

#### 1.2 Worker节点加入

```bash
# 在Worker节点上执行（由kubeadm init输出提供）
sudo kubeadm join 192.168.1.100:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. 高可用集群搭建

#### 2.1 架构设计

```
负载均衡器 (VIP: 192.168.1.200)
├── Master Node 1 (192.168.1.101)
├── Master Node 2 (192.168.1.102)
└── Master Node 3 (192.168.1.103)

Worker Nodes:
├── Worker Node 1 (192.168.1.111)
├── Worker Node 2 (192.168.1.112)
└── Worker Node 3 (192.168.1.113)
```

#### 2.2 负载均衡器配置

```bash
# 安装HAProxy
sudo yum install -y haproxy

# HAProxy配置
cat <<EOF | sudo tee /etc/haproxy/haproxy.cfg
global
    log         127.0.0.1 local2
    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon

defaults
    mode                    tcp
    log                     global
    option                  tcplog
    option                  dontlognull
    option                  redispatch
    retries                 3
    timeout connect         10s
    timeout client          1m
    timeout server          1m

frontend kubernetes-frontend
    bind *:6443
    default_backend kubernetes-backend

backend kubernetes-backend
    balance roundrobin
    server master1 192.168.1.101:6443 check
    server master2 192.168.1.102:6443 check
    server master3 192.168.1.103:6443 check
EOF

sudo systemctl enable haproxy
sudo systemctl start haproxy
```

#### 2.3 Master节点初始化

```bash
# 第一个Master节点
sudo kubeadm init \
  --control-plane-endpoint "192.168.1.200:6443" \
  --upload-certs \
  --pod-network-cidr=10.244.0.0/16 \
  --cri-socket=/run/containerd/containerd.sock

# 其他Master节点
sudo kubeadm join 192.168.1.200:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  --control-plane \
  --certificate-key yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

### 3. 网络插件配置

#### 3.1 Calico网络插件

```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
    - blockSize: 26
      cidr: 10.244.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()
```

#### 3.2 Cilium网络插件

```bash
# 安装Cilium CLI
curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-amd64.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-amd64.tar.gz /usr/local/bin
rm cilium-linux-amd64.tar.gz{,.sha256sum}

# 安装Cilium
cilium install \
  --version 1.14.0 \
  --helm-set ipam.mode=kubernetes \
  --helm-set kubeProxyReplacement=true
```

### 4. 存储基础设施配置

#### 4.1 本地存储配置

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv-1
spec:
  capacity:
    storage: 100Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /mnt/disks/ssd1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - worker-node-1
```

#### 4.2 NFS存储配置

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 1Ti
  accessModes:
    - ReadWriteMany
  nfs:
    server: 192.168.1.50
    path: "/nfs/shared"
  mountOptions:
    - vers=4.1
```

### 5. 监控和日志基础设施

#### 5.1 Prometheus监控栈

```bash
# 添加监控命名空间
kubectl create namespace monitoring

# 部署Prometheus Operator
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml

# 部署kube-prometheus-stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.adminPassword=admin123
```

#### 5.2 EFK日志栈

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: logging
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elasticsearch
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
        env:
        - name: discovery.type
          value: single-node
        ports:
        - containerPort: 9200
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### 6. 私有镜像仓库配置

#### 6.1 Harbor部署

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: harbor
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: harbor-core
  namespace: harbor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: harbor-core
  template:
    metadata:
      labels:
        app: harbor-core
    spec:
      containers:
      - name: core
        image: goharbor/harbor-core:v2.8.0
        ports:
        - containerPort: 8080
        env:
        - name: CORE_SECRET
          valueFrom:
            secretKeyRef:
              name: harbor-core-secret
              key: secret
```

---

## 🔧 实践操作

### 1. 集群健康检查

```bash
# 检查节点状态
kubectl get nodes

# 检查系统组件
kubectl get pods -n kube-system

# 检查集群信息
kubectl cluster-info

# 运行基准测试
kubectl run nginx-test --image=nginx --replicas=3
kubectl get pods -l run=nginx-test
```

### 2. 网络连通性测试

```bash
# 部署测试Pod
kubectl run debug-pod --image=busybox --rm -it -- sh

# 测试DNS解析
nslookup kubernetes.default

# 测试跨节点通信
ping <other-pod-ip>
```

### 3. 存储功能验证

```bash
# 创建测试PVC
kubectl apply -f test-pvc.yaml

# 部署使用PVC的应用
kubectl apply -f test-app.yaml

# 验证数据持久性
kubectl exec -it test-pod -- touch /data/test-file
kubectl delete pod test-pod
kubectl apply -f test-app.yaml
kubectl exec -it test-pod -- ls /data/
```

---

## 📊 监控和维护

### 1. 集群状态监控

```bash
# 查看集群组件状态
kubectl get componentstatuses

# 监控节点资源使用
kubectl top nodes

# 查看集群事件
kubectl get events --sort-by='.lastTimestamp'
```

### 2. 日志收集

```bash
# 查看系统组件日志
kubectl logs -n kube-system <component-pod>

# 查看节点日志
journalctl -u kubelet -f

# 收集集群诊断信息
kubectl cluster-info dump > cluster-dump.log
```

---

## ⚠️ 常见问题和解决方案

### 1. 节点NotReady状态

**问题现象**: 节点状态显示为NotReady

**可能原因**:
- 网络插件未正确安装
- kubelet服务异常
- 证书过期
- 资源不足

**解决步骤**:
```bash
# 1. 检查节点详细状态
kubectl describe node <node-name>

# 2. 检查kubelet服务
systemctl status kubelet
journalctl -u kubelet -f

# 3. 重新安装网络插件
kubectl apply -f <network-plugin.yaml>

# 4. 检查证书状态
openssl x509 -in /var/lib/kubelet/pki/kubelet.crt -text
```

### 2. Pod无法调度

**问题现象**: Pod长时间处于Pending状态

**解决步骤**:
```bash
# 1. 检查Pod事件
kubectl describe pod <pod-name>

# 2. 检查节点资源
kubectl describe nodes

# 3. 检查污点和容忍度
kubectl get nodes -o jsonpath='{.items[*].spec.taints}'
```

### 3. 网络插件故障

**问题现象**: Pod间无法通信或DNS解析失败

**解决步骤**:
```bash
# 1. 检查网络插件Pod状态
kubectl get pods -n kube-system | grep <network-plugin>

# 2. 查看网络插件日志
kubectl logs -n kube-system <network-plugin-pod>

# 3. 重新部署网络插件
kubectl delete -f <network-plugin.yaml>
kubectl apply -f <network-plugin.yaml>
```

---

## 🧪 实践练习

### 练习1：单节点集群搭建
按照教程步骤搭建单节点Kubernetes集群，验证基本功能。

### 练习2：高可用集群部署
配置三节点高可用集群，测试故障转移能力。

### 练习3：网络插件对比
分别部署Calico和Flannel，比较性能差异。

### 练习4：存储基础设施
配置本地存储和NFS存储，验证持久化功能。

---

## 📚 扩展阅读

### 官方文档
- [Kubernetes安装指南](https://kubernetes.io/docs/setup/)
- [kubeadm文档](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)
- [集群网络](https://kubernetes.io/docs/concepts/cluster-administration/networking/)

### 相关案例
- [RBAC权限管理](../rbac-auth/)
- [监控日志基础设施](../monitoring-logging/)
- [备份灾备恢复](../backup-disaster/)

### 进阶主题
- 多云集群管理
- 边缘计算部署
- 安全加固配置
- 性能调优优化

---

## 📋 清理资源

```bash
# 重置节点
sudo kubeadm reset -f

# 清理网络配置
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X
sudo ipvsadm --clear

# 删除配置文件
rm -rf $HOME/.kube/
sudo rm -rf /etc/cni/net.d
sudo rm -rf /var/lib/etcd
```

---

> **💡 提示**: 集群搭建是Kubernetes运维的基础，建议在测试环境中充分练习后再部署生产环境。注意保留好集群配置和证书备份。