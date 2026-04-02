# Docker vs VM

Docker容器与传统虚拟机的对比分析，展示架构差异、性能特点和应用场景。

## 架构对比

### 传统虚拟机
```
传统虚拟机架构:
┌─────────────────────────────────────────────┐
│ App A │ App B │ App C │ App D              │
├─────────────────────────────────────────────┤
│  Guest OS   │  Guest OS   │  Guest OS      │
├─────────────┼─────────────┼─────────────────┤
│  Hypervisor (VMware/ESXi/KVM)               │
├─────────────────────────────────────────────┤
│              Host OS                        │
├─────────────────────────────────────────────┤
│              Hardware                       │
└─────────────────────────────────────────────┘

特点:
- 完整操作系统隔离
- 重量级 (GB级)
- 启动分钟级
- 硬件级隔离
```

### Docker容器
```
容器架构:
┌─────────────────────────────────────────────┐
│ App A │ App B │ App C │ App D              │
├─────────────────────────────────────────────┤
│ Bin/Lib │ Bin/Lib │ Bin/Lib │ Bin/Lib       │
├─────────────────────────────────────────────┤
│         Docker Engine                        │
├─────────────────────────────────────────────┤
│              Host OS                        │
├─────────────────────────────────────────────┤
│              Hardware                       │
└─────────────────────────────────────────────┘

特点:
- 共享宿主机内核
- 轻量级 (MB级)
- 启动秒级
- 进程级隔离
```

## 启动时间对比

```
启动时间:
VM:  [██████████████] 60-120秒
    完整OS启动 + 应用初始化

Container:
    [██] 1-5秒
    进程启动 + 应用初始化

Serverless:
    [█] <100ms (热启动)
    直接运行代码
```

## 资源占用对比

| 资源 | 虚拟机 | Docker容器 | 比例 |
|------|--------|-----------|------|
| 磁盘 | 10-20GB | 100-500MB | 1:50 |
| 内存 | 2-4GB | 50-200MB | 1:20 |
| CPU开销 | 10-20% | 接近原生 | 1:0.1 |
| 启动时间 | 60-120s | 1-5s | 60:1 |

## 隔离性对比

```
隔离层次:

VM:                         Container:
┌──────────┐                ┌──────────┐
│  Process │                │  Process │
├──────────┤                ├──────────┤
│  Filesys │                │ Namespace│
├──────────┤                ├──────────┤
│  Network │                │ Cgroups  │
├──────────┤                ├──────────┤
│  Kernel  │                │ Seccomp  │
├──────────┤                ├──────────┤
│ Hardware │                │ Host Kernel
├──────────┤                ├──────────┤
│ Physical │                │ Hardware │
└──────────┘                └──────────┘

VM: 硬件级隔离              Container: 操作系统级隔离
    最安全                        轻量高效
```

## 性能测试对比

### CPU性能
```bash
# 测试命令
docker run --rm -it alpine sh -c 'time for i in $(seq 1 1000000); do : ; done'
# 在VM中运行相同测试

# 结果:
# 原生Linux: 2.1s
# Docker:    2.2s (99%)
# VM:        2.8s (75%)
```

### I/O性能
```bash
# 磁盘I/O测试
docker run --rm -v $(pwd):/data alpine sh -c 'dd if=/dev/zero of=/data/test bs=1M count=1000'

# 结果:
# 原生:    500 MB/s
# Docker:  480 MB/s (96%)
# VM:      350 MB/s (70%)
```

### 网络性能
```bash
# 网络吞吐量测试
iperf3 -c <target>

# 结果:
# 原生:    10 Gbps
# Docker (bridge):  8.5 Gbps (85%)
# Docker (host):    9.8 Gbps (98%)
# VM (virtio):      7.0 Gbps (70%)
```

## 使用场景对比

### 选择虚拟机的场景
```
┌─────────────────────────────────────┐
│ ✓ 运行不同操作系统 (Windows/Linux)  │
│ ✓ 强隔离要求 (多租户安全)            │
│ ✓ 需要完整内核访问                   │
│ ✓ 遗留应用兼容性                     │
│ ✓ 硬件直通需求 (GPU/FPGA)            │
└─────────────────────────────────────┘
```

### 选择容器的场景
```
┌─────────────────────────────────────┐
│ ✓ 微服务架构                         │
│ ✓ CI/CD流水线                        │
│ ✓ 快速弹性伸缩                       │
│ ✓ 开发环境一致性                     │
│ ✓ 云原生应用部署                     │
│ ✓ 资源效率优先                       │
└─────────────────────────────────────┘
```

## 安全性对比

### 攻击面分析
```
VM攻击面:                    Container攻击面:
┌──────────────────┐         ┌──────────────────┐
│ 应用漏洞          │         │ 应用漏洞          │
├──────────────────┤         ├──────────────────┤
│ 容器运行时漏洞    │         │ 容器运行时漏洞    │
├──────────────────┤         ├──────────────────┤
│ 共享内核漏洞      │  X      │ Hypervisor漏洞   │
├──────────────────┤         ├──────────────────┤
│ Host Kernel      │         │ Host OS          │
├──────────────────┤         ├──────────────────┤
│ Host OS          │         │ Hardware         │
├──────────────────┤         └──────────────────┘
│ Hardware         │
└──────────────────┘

VM: 多层防御        Container: 依赖单一内核
```

### 安全最佳实践
```bash
# Docker安全选项
docker run \
  --read-only \                    # 只读文件系统
  --security-opt=no-new-privileges \ # 禁止提权
  --cap-drop=ALL \                 # 移除所有能力
  --cap-add=NET_BIND_SERVICE \     # 仅添加必要能力
  --memory=512m \                  # 内存限制
  --cpus=1 \                       # CPU限制
  --pids-limit=100 \               # 进程数限制
  myapp
```

## 编排能力对比

### VM编排
```yaml
# Terraform示例
resource "vsphere_virtual_machine" "vm" {
  name             = "web-server"
  resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
  datastore_id     = data.vsphere_datastore.datastore.id
  
  num_cpus = 2
  memory   = 4096
  
  disk {
    label            = "disk0"
    size             = 50
    thin_provisioned = true
  }
  
  network_interface {
    network_id = data.vsphere_network.network.id
  }
}
```

### 容器编排
```yaml
# Kubernetes示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

## 混合部署模式

```
现代架构趋势:
┌─────────────────────────────────────────────────┐
│              Kubernetes Cluster                  │
│  ┌─────────────────────────────────────────┐   │
│  │  Pod A  │  Pod B  │  Pod C            │   │
│  │ (微服务)│ (微服务)│ (微服务)          │   │
│  └─────────────────────────────────────────┘   │
├─────────────────────────────────────────────────┤
│              Docker Engine                       │
├─────────────────────────────────────────────────┤
│              Host Linux OS                       │
├─────────────────────────────────────────────────┤
│  VM: ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│      │ Worker1 │  │ Worker2 │  │ Worker3 │    │
│      └─────────┘  └─────────┘  └─────────┘    │
├─────────────────────────────────────────────────┤
│              Hypervisor (KVM/vSphere)            │
├─────────────────────────────────────────────────┤
│              Physical Hardware                   │
└─────────────────────────────────────────────────┘

容器在VM中运行，结合两者优势
```

## 学习要点

1. 架构差异和设计哲学
2. 性能和资源效率对比
3. 隔离性和安全性权衡
4. 适用场景选择
5. 混合部署策略
