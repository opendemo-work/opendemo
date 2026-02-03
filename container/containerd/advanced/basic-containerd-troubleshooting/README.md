# Containerd故障排查与应急处理实战

## 1. 案例概述

本案例提供了Containerd容器运行时的故障排查方法和应急解决方案，包括：
- Containerd守护进程故障
- 容器启动失败
- 镜像拉取失败
- 容器网络问题
- 存储驱动问题
- Containerd资源限制问题
- 容器数据丢失
- Containerd升级失败
- CRI接口问题

## 2. 环境准备

- Containerd运行时（v1.6.0+）
- 容器运行环境
- crictl命令行工具
- ctr命令行工具
- 系统管理工具（如systemctl、journalctl、df、free等）
- 网络测试工具（如ping、nc、ip等）

## 3. 常见Containerd故障排查

### 3.1 Containerd守护进程故障

**症状**：
- crictl命令无法执行，提示 "failed to connect to containerd"
- systemctl status containerd显示Containerd服务未运行
- Containerd守护进程日志显示错误信息

**排查步骤**：

1. 检查Containerd服务状态：
   ```bash
   systemctl status containerd
   ```

2. 查看Containerd守护进程日志：
   ```bash
   journalctl -u containerd -f
   ```

3. 检查Containerd配置文件：
   ```bash
   cat /etc/containerd/config.toml
   ```

4. 检查Containerd守护进程端口：
   ```bash
   netstat -tuln | grep 10010
   ```

5. 检查Containerd存储：
   ```bash
   df -h /var/lib/containerd
   ```

**解决方案示例**：

```bash
# 重启Containerd服务
systemctl restart containerd

# 修复Containerd配置错误
vi /etc/containerd/config.toml
systemctl restart containerd

# 重置Containerd配置
containerd config default > /etc/containerd/config.toml
systemctl restart containerd

# 重建Containerd配置
systemctl stop containerd
rm -rf /var/lib/containerd
systemctl start containerd
```

### 3.2 容器启动失败

**症状**：
- crictl run命令执行后容器立即退出
- crictl ps -a显示容器状态为Exited
- crictl logs显示错误信息

**排查步骤**：

1. 查看容器日志：
   ```bash
   crictl logs <container-id>
   ```

2. 检查容器配置：
   ```bash
   crictl inspect <container-id>
   ```

3. 测试容器启动命令：
   ```bash
   crictl run --rm -i -t --runtime=containerd <image-name> sh
   ```

4. 检查容器资源限制：
   ```bash
   crictl stats <container-id>
   ```

5. 检查镜像完整性：
   ```bash
   crictl inspecti <image-name>
   ```

**解决方案示例**：

```bash
# 修复容器配置问题
crictl run --restart always <image-name>

# 增加容器资源限制
crictl run --memory=2g --cpu-shares=1024 <image-name>

# 重建镜像
ctr images pull docker.io/library/nginx:latest

# 修复容器依赖问题
crictl run --mount type=bind,source=/host/path,target=/container/path <image-name>
```

### 3.3 镜像拉取失败

**症状**：
- crictl pull或ctr images pull命令执行失败
- 提示 "image not found" 或 "connection refused"
- 镜像拉取超时

**排查步骤**：

1. 检查Containerd镜像仓库配置：
   ```bash
   cat /etc/containerd/config.toml | grep -A 10 "[plugins.\".io.containerd.grpc.v1.cri\".registry]"
   ```

2. 测试网络连接：
   ```bash
   ping registry-1.docker.io
   curl -I https://registry-1.docker.io
   ```

3. 检查镜像名称和标签：
   ```bash
   crictl images
   ```

4. 检查Containerd认证配置：
   ```bash
   cat /etc/containerd/certs.d/docker.io/hosts.toml
   ```

**解决方案示例**：

```bash
# 修复Containerd镜像仓库配置
cat > /etc/containerd/config.toml << EOF
version = 2
[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    [plugins."io.containerd.grpc.v1.cri".registry]
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["https://docker.mirrors.ustc.edu.cn"]
EOF
systemctl restart containerd

# 登录到镜像仓库
ctr images pull docker.io/library/nginx:latest --user <username>:<password>

# 使用完整的镜像名称
crictl pull docker.io/library/nginx:latest

# 增加拉取超时时间
ctr images pull docker.io/library/nginx:latest --timeout=600s
```

### 3.4 容器网络问题

**症状**：
- 容器无法访问外部网络
- 容器之间无法通信
- CNI插件故障
- DNS解析失败

**排查步骤**：

1. 检查Containerd网络配置：
   ```bash
   cat /etc/containerd/config.toml | grep -A 10 "[plugins.\".io.containerd.grpc.v1.cri\".cni]"
   ```

2. 测试容器网络连接：
   ```bash
   crictl run --rm --name test busybox:latest ping -c 3 8.8.8.8
   ```

3. 检查CNI插件状态：
   ```bash
   ls -la /opt/cni/bin/
   cat /etc/cni/net.d/10-containerd-net.conflist
   ```

4. 检查网络命名空间：
   ```bash
   ip netns list
   ```

**解决方案示例**：

```bash
# 修复CNI插件配置
cat > /etc/cni/net.d/10-containerd-net.conflist << EOF
{
  "cniVersion": "0.4.0",
  "name": "containerd-net",
  "plugins": [
    {
      "type": "bridge",
      "bridge": "cni0",
      "isGateway": true,
      "ipMasq": true,
      "promiscMode": true,
      "ipam": {
        "type": "host-local",
        "ranges": [
          [{"subnet": "10.88.0.0/16"}]
        ],
        "routes": [
          {"dst": "0.0.0.0/0"}
        ]
      }
    },
    {
      "type": "portmap",
      "capabilities": {
        "portMappings": true
      }
    }
  ]
}
EOF
systemctl restart containerd

# 安装CNI插件
git clone https://github.com/containernetworking/plugins.git
cd plugins && make && make install

# 修复网络命名空间
ip link set cni0 up
```

### 3.5 存储驱动问题

**症状**：
- Containerd无法启动，提示存储驱动问题
- 容器启动失败，提示存储相关错误
- 镜像拉取失败，提示存储问题

**排查步骤**：

1. 检查Containerd存储驱动：
   ```bash
   ctr info | grep -A 5 "Storage Driver"
   ```

2. 检查文件系统：
   ```bash
   df -T /var/lib/containerd
   ```

3. 检查存储驱动依赖：
   ```bash
   lsmod | grep overlay
   ```

4. 检查Containerd存储状态：
   ```bash
   ctr snapshots ls
   ```

**解决方案示例**：

```bash
# 切换Containerd存储驱动
cat > /etc/containerd/config.toml << EOF
version = 2
[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    sandbox_image = "registry.k8s.io/pause:3.9"
  [plugins."io.containerd.runtime.v1.linux"]
    runtime = "runc"
  [plugins."io.containerd.snapshotter.v1.overlayfs"]
    root_path = "/var/lib/containerd/io.containerd.snapshotter.v1.overlayfs"
EOF
systemctl stop containerd
rm -rf /var/lib/containerd
systemctl start containerd

# 修复文件系统问题
fsck /dev/sda1

# 检查并加载存储驱动依赖
modprobe overlay
```

### 3.6 Containerd资源限制问题

**症状**：
- 容器被OOM killed
- Containerd无法启动新容器
- 系统资源使用率过高

**排查步骤**：

1. 检查Containerd资源使用情况：
   ```bash
   crictl stats
   ```

2. 检查系统资源使用情况：
   ```bash
   free -h
   df -h
   top
   ```

3. 检查容器资源限制：
   ```bash
   crictl inspect <container-id> | grep -A 10 Resources
   ```

4. 检查Containerd守护进程资源限制：
   ```bash
   cat /etc/systemd/system/containerd.service.d/limits.conf
   ```

**解决方案示例**：

```bash
# 增加系统资源限制
cat > /etc/systemd/system/containerd.service.d/limits.conf << EOF
[Service]
LimitNOFILE=65536
LimitNPROC=65536
EOF
systemctl daemon-reload
systemctl restart containerd

# 设置容器资源限制
crictl run --memory=1g --cpu-shares=1024 <image-name>

# 清理无用资源
ctr images prune
ctr containers rm $(ctr containers ls -q)
ctr snapshots prune
```

### 3.7 容器数据丢失

**症状**：
- 容器重启后数据丢失
- 容器卷挂载数据无法访问
- 容器数据损坏

**排查步骤**：

1. 检查容器数据持久化配置：
   ```bash
   crictl inspect <container-id> | grep -A 20 Mounts
   ```

2. 检查存储卷状态：
   ```bash
   ls -la /var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/
   ```

3. 检查宿主机目录权限：
   ```bash
   ls -la /host/path
   ```

4. 检查容器日志：
   ```bash
   crictl logs <container-id>
   ```

**解决方案示例**：

```bash
# 使用持久化存储
crictl run --mount type=bind,source=/host/path,target=/container/path <image-name>

# 修复卷挂载权限
crictl run --user root --mount type=bind,source=/host/path,target=/container/path <image-name>

# 恢复数据备份
cp -r /backup/path/* /var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/
```

### 3.8 Containerd升级失败

**症状**：
- Containerd升级后无法启动
- 容器无法运行
- crictl命令执行失败

**排查步骤**：

1. 检查Containerd版本：
   ```bash
   containerd --version
   ```

2. 查看Containerd守护进程日志：
   ```bash
   journalctl -u containerd -f
   ```

3. 检查Containerd配置文件：
   ```bash
   cat /etc/containerd/config.toml
   ```

4. 检查系统兼容性：
   ```bash
   uname -a
   ```

**解决方案示例**：

```bash
# 回滚Containerd版本
apt-get install containerd.io=1.6.24-1
rpm -i containerd.io-1.6.24-3.1.el9.x86_64.rpm

# 修复Containerd配置
systemctl stop containerd
mv /etc/containerd/config.toml /etc/containerd/config.toml.bak
containerd config default > /etc/containerd/config.toml
systemctl start containerd

# 清理旧版本数据
systemctl stop containerd
rm -rf /var/lib/containerd
systemctl start containerd

# 重新安装Containerd
apt-get purge containerd.io
dnf remove containerd.io
apt-get install containerd.io
dnf install containerd.io
```

### 3.9 CRI接口问题

**症状**：
- Kubernetes无法连接到Containerd
- kubelet日志显示CRI连接错误
- crictl命令正常但Kubernetes无法使用Containerd

**排查步骤**：

1. 检查Kubelet配置：
   ```bash
   cat /var/lib/kubelet/kubeadm-flags.env
   ```

2. 检查Containerd CRI配置：
   ```bash
   cat /etc/containerd/config.toml | grep -A 20 "[plugins.\".io.containerd.grpc.v1.cri\"]"
   ```

3. 测试CRI接口：
   ```bash
   crictl info
   ```

4. 查看Kubelet日志：
   ```bash
   journalctl -u kubelet -f
   ```

**解决方案示例**：

```bash
# 修复Kubelet CRI配置
cat > /var/lib/kubelet/kubeadm-flags.env << EOF
KUBELET_KUBEADM_ARGS="--container-runtime-endpoint=unix:///run/containerd/containerd.sock --image-service-endpoint=unix:///run/containerd/containerd.sock --pod-infra-container-image=registry.k8s.io/pause:3.9"
EOF
systemctl restart kubelet

# 修复Containerd CRI配置
containerd config default > /etc/containerd/config.toml
systemctl restart containerd

# 检查并修复CRI socket权限
chmod 666 /run/containerd/containerd.sock
```

## 4. 实用工具和命令

### 4.1 Containerd诊断命令

```bash
# 查看Containerd信息
ctr info
crictl info

# 查看Containerd版本
containerd --version

# 查看容器状态
crictl ps -a
ctr containers ls

# 查看容器日志
crictl logs <container-id>

# 查看容器详细信息
crictl inspect <container-id>
ctr containers inspect <container-id>

# 查看容器资源使用情况
crictl stats

# 查看镜像信息
crictl images
ctr images ls

# 查看网络信息
crictl pods

# 查看Containerd存储状态
ctr snapshots ls

# 清理无用资源
ctr images prune
crictl rmi --prune
```

### 4.2 Containerd监控工具

```bash
# 使用cAdvisor监控Containerd
docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:ro --volume=/sys:/sys:ro --volume=/var/lib/containerd/:/var/lib/containerd:ro --publish=8080:8080 --detach=true --name=cadvisor gcr.io/cadvisor/cadvisor:latest

# 使用Prometheus和Grafana监控Containerd
# 参考Prometheus和Grafana部署文档
```

## 5. 故障模拟和练习

### 5.1 模拟Containerd守护进程故障

```bash
# 停止Containerd服务
systemctl stop containerd

# 查看故障状态
crictl ps

# 恢复Containerd服务
systemctl start containerd
```

### 5.2 模拟容器启动失败

```bash
# 创建一个会立即退出的容器
crictl run --rm busybox:latest false

# 查看容器状态
crictl ps -a

# 查看容器日志
crictl logs <container-id>
```

### 5.3 模拟镜像拉取失败

```bash
# 尝试拉取一个不存在的镜像
crictl pull non-existent-image:latest

# 查看错误信息
```

## 6. 最佳实践

1. **监控Containerd服务**：
   - 实施Containerd监控，包括容器状态、资源使用情况、日志等
   - 设置告警规则，及时发现Containerd异常
   - 定期检查Containerd服务状态

2. **合理配置Containerd资源**：
   - 为Containerd守护进程设置适当的资源限制
   - 为容器设置合理的资源请求和限制
   - 避免单个容器占用过多资源

3. **实施数据持久化**：
   - 为所有需要持久化的数据使用卷
   - 定期备份卷数据
   - 使用可靠的存储后端

4. **定期维护Containerd环境**：
   - 定期清理无用的镜像、容器和卷
   - 定期更新Containerd版本
   - 定期检查Containerd配置

5. **确保Containerd安全**：
   - 启用Containerd TLS认证
   - 限制Containerd守护进程访问权限
   - 定期扫描镜像漏洞
   - 实施容器安全最佳实践

6. **建立应急响应流程**：
   - 制定Containerd故障应急响应流程
   - 定期测试应急响应流程
   - 建立Containerd故障恢复机制

## 7. 版本兼容性

| Containerd版本 | 兼容性 |
|---------------|--------|
| v1.6.x        | ✅     |
| v1.7.x        | ✅     |
| v1.8.x        | ✅     |

## 8. 总结

本案例提供了Containerd容器运行时的全面故障排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决各种Containerd故障
- 了解Containerd组件的工作原理和常见问题
- 掌握Containerd资源管理和优化技巧
- 建立Containerd监控和维护策略
- 提高容器环境的整体可靠性和可用性

通过合理的Containerd管理、监控和维护，您将能够确保容器环境始终处于健康状态，为应用提供稳定可靠的运行环境。