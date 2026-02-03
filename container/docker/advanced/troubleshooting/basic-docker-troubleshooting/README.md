# Docker故障排查与应急处理实战

## 1. 案例概述

本案例提供了Docker容器引擎的故障排查方法和应急解决方案，包括：
- Docker守护进程故障
- 容器启动失败
- 镜像拉取失败
- 容器网络问题
- 存储驱动问题
- Docker资源限制问题
- 容器数据丢失
- Docker升级失败
- Docker镜像构建问题

## 2. 环境准备

- Docker引擎（v20.10.0+）
- 容器运行环境
- Docker命令行工具
- 系统管理工具（如systemctl、journalctl、df、free等）
- 网络测试工具（如ping、nc、ip等）

## 3. 常见Docker故障排查

### 3.1 Docker守护进程故障

**症状**：
- Docker命令无法执行，提示 "Cannot connect to the Docker daemon"
- systemctl status docker显示Docker服务未运行
- Docker守护进程日志显示错误信息

**排查步骤**：

1. 检查Docker服务状态：
   ```bash
   systemctl status docker
   ```

2. 查看Docker守护进程日志：
   ```bash
   journalctl -u docker -f
   ```

3. 检查Docker配置文件：
   ```bash
   cat /etc/docker/daemon.json
   ```

4. 检查Docker守护进程端口：
   ```bash
   netstat -tuln | grep 2375
   netstat -tuln | grep 2376
   ```

5. 检查Docker存储：
   ```bash
   df -h /var/lib/docker
   ```

**解决方案示例**：

```bash
# 重启Docker服务
systemctl restart docker

# 修复Docker配置错误
vi /etc/docker/daemon.json
systemctl restart docker

# 清理Docker存储
docker system prune -f

# 重建Docker配置
systemctl stop docker
rm -rf /var/lib/docker
systemctl start docker
```

### 3.2 容器启动失败

**症状**：
- docker run命令执行后容器立即退出
- docker ps -a显示容器状态为Exited
- docker logs显示错误信息

**排查步骤**：

1. 查看容器日志：
   ```bash
   docker logs <container-id>
   ```

2. 检查容器配置：
   ```bash
   docker inspect <container-id>
   ```

3. 测试容器启动命令：
   ```bash
   docker run --rm -it <image-name> bash
   ```

4. 检查容器资源限制：
   ```bash
   docker stats <container-id>
   ```

5. 检查镜像完整性：
   ```bash
   docker image inspect <image-name>
   ```

**解决方案示例**：

```bash
# 修复容器配置问题
docker run --restart always <image-name>

# 增加容器资源限制
docker run -m 2g --cpus=2 <image-name>

# 重建镜像
docker build -t <image-name> .

# 修复容器依赖问题
docker run --volume /host/path:/container/path <image-name>
```

### 3.3 镜像拉取失败

**症状**：
- docker pull命令执行失败
- 提示 "image not found" 或 "connection refused"
- 镜像拉取超时

**排查步骤**：

1. 检查Docker镜像仓库连接：
   ```bash
   docker info
   ```

2. 测试网络连接：
   ```bash
   ping registry-1.docker.io
   curl -I https://registry-1.docker.io
   ```

3. 检查镜像名称和标签：
   ```bash
   docker search <image-name>
   ```

4. 检查Docker镜像仓库配置：
   ```bash
   cat /etc/docker/daemon.json | grep registry
   ```

5. 检查Docker认证配置：
   ```bash
   cat ~/.docker/config.json
   ```

**解决方案示例**：

```bash
# 修复Docker镜像仓库配置
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
EOF
systemctl restart docker

# 登录到镜像仓库
docker login docker.io

# 使用完整的镜像名称
docker pull docker.io/library/nginx:latest

# 增加拉取超时时间
docker pull --timeout=600 <image-name>
```

### 3.4 容器网络问题

**症状**：
- 容器无法访问外部网络
- 容器之间无法通信
- 端口映射无法访问
- DNS解析失败

**排查步骤**：

1. 检查Docker网络配置：
   ```bash
   docker network ls
   docker network inspect bridge
   ```

2. 测试容器网络连接：
   ```bash
   docker run --rm busybox ping -c 3 8.8.8.8
   docker run --rm busybox nslookup google.com
   ```

3. 检查端口映射：
   ```bash
   docker port <container-id>
   netstat -tuln | grep <port>
   ```

4. 检查iptables规则：
   ```bash
   iptables -L DOCKER -n
   ```

5. 检查DNS配置：
   ```bash
   cat /etc/docker/daemon.json | grep dns
   ```

**解决方案示例**：

```bash
# 修复Docker DNS配置
cat > /etc/docker/daemon.json << EOF
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
EOF
systemctl restart docker

# 修复容器网络
docker network prune

# 检查并修复iptables规则
iptables -F DOCKER
iptables -F DOCKER-ISOLATION-STAGE-1
iptables -F DOCKER-ISOLATION-STAGE-2
systemctl restart docker

# 使用自定义网络
docker network create my-network
docker run --network my-network <image-name>
```

### 3.5 存储驱动问题

**症状**：
- Docker无法启动，提示存储驱动问题
- 容器启动失败，提示存储相关错误
- Docker镜像构建失败，提示存储问题

**排查步骤**：

1. 检查Docker存储驱动：
   ```bash
   docker info | grep Storage
   ```

2. 检查文件系统：
   ```bash
   df -T /var/lib/docker
   ```

3. 检查存储驱动依赖：
   ```bash
   lsmod | grep overlay
   lsmod | grep aufs
   ```

4. 检查Docker存储状态：
   ```bash
   docker system df
   ```

5. 检查存储驱动配置：
   ```bash
   cat /etc/docker/daemon.json | grep storage-driver
   ```

**解决方案示例**：

```bash
# 切换Docker存储驱动
cat > /etc/docker/daemon.json << EOF
{
  "storage-driver": "overlay2"
}
EOF
systemctl stop docker
rm -rf /var/lib/docker
systemctl start docker

# 修复文件系统问题
fsck /dev/sda1

# 清理Docker存储
docker system prune -f --volumes

# 检查并加载存储驱动依赖
modprobe overlay
```

### 3.6 Docker资源限制问题

**症状**：
- 容器被OOM killed
- Docker无法启动新容器
- 系统资源使用率过高

**排查步骤**：

1. 检查Docker资源使用情况：
   ```bash
   docker stats
   docker system df
   ```

2. 检查系统资源使用情况：
   ```bash
   free -h
   df -h
   top
   ```

3. 检查容器资源限制：
   ```bash
   docker inspect <container-id> | grep -A 10 Resources
   ```

4. 检查Docker守护进程资源限制：
   ```bash
   cat /etc/systemd/system/docker.service.d/limits.conf
   ```

**解决方案示例**：

```bash
# 增加系统资源限制
cat > /etc/systemd/system/docker.service.d/limits.conf << EOF
[Service]
LimitNOFILE=65536
LimitNPROC=65536
EOF
systemctl daemon-reload
systemctl restart docker

# 设置容器资源限制
docker run -m 1g --cpus=1 <image-name>

# 清理无用资源
docker system prune -f --volumes

# 增加Docker存储空间
export DOCKER_DATA_ROOT=/new/path
systemctl stop docker
rsync -a /var/lib/docker/ $DOCKER_DATA_ROOT/
cat > /etc/docker/daemon.json << EOF
{
  "data-root": "$DOCKER_DATA_ROOT"
}
EOF
systemctl start docker
```

### 3.7 容器数据丢失

**症状**：
- 容器重启后数据丢失
- 卷挂载数据无法访问
- 容器数据损坏

**排查步骤**：

1. 检查容器数据持久化配置：
   ```bash
   docker inspect <container-id> | grep -A 20 Mounts
   ```

2. 检查卷状态：
   ```bash
   docker volume ls
   docker volume inspect <volume-name>
   ```

3. 检查宿主机目录权限：
   ```bash
   ls -la /host/path
   ```

4. 检查容器日志：
   ```bash
   docker logs <container-id>
   ```

**解决方案示例**：

```bash
# 使用命名卷持久化数据
docker volume create my-volume
docker run --volume my-volume:/data <image-name>

# 修复卷挂载权限
docker run --user root --volume /host/path:/container/path <image-name>

# 恢复数据备份
docker run --volume /backup/path:/data <image-name> restore

# 使用数据卷容器
docker run --name data-container <image-name>
docker run --volumes-from data-container <image-name>
```

### 3.8 Docker升级失败

**症状**：
- Docker升级后无法启动
- 容器无法运行
- Docker命令执行失败

**排查步骤**：

1. 检查Docker版本：
   ```bash
   docker version
   ```

2. 查看Docker守护进程日志：
   ```bash
   journalctl -u docker -f
   ```

3. 检查Docker配置文件：
   ```bash
   cat /etc/docker/daemon.json
   ```

4. 检查系统兼容性：
   ```bash
   uname -a
   ```

**解决方案示例**：

```bash
# 回滚Docker版本
apt-get install docker-ce=5:20.10.24~3-0~ubuntu-jammy
dnf install docker-ce-20.10.24-3.el9

# 修复Docker配置
systemctl stop docker
mv /etc/docker/daemon.json /etc/docker/daemon.json.bak
systemctl start docker

# 清理旧版本数据
docker system prune -f

# 重新安装Docker
systemctl stop docker
apt-get purge docker-ce docker-ce-cli containerd.io
dnf remove docker-ce docker-ce-cli containerd.io
rm -rf /var/lib/docker
apt-get install docker-ce docker-ce-cli containerd.io
dnf install docker-ce docker-ce-cli containerd.io
```

### 3.9 Docker镜像构建问题

**症状**：
- docker build命令执行失败
- 构建过程中出现错误
- 镜像构建超时

**排查步骤**：

1. 检查Dockerfile语法：
   ```bash
   docker build --no-cache -t <image-name> .
   ```

2. 查看构建日志：
   ```bash
   docker build -t <image-name> .
   ```

3. 检查基础镜像可用性：
   ```bash
   docker pull <base-image-name>
   ```

4. 检查构建上下文：
   ```bash
   ls -la .dockerignore
   ```

**解决方案示例**：

```bash
# 修复Dockerfile语法错误
vi Dockerfile
docker build -t <image-name> .

# 使用更稳定的基础镜像
docker pull ubuntu:22.04
docker build -t <image-name> .

# 优化构建上下文
cat > .dockerignore << EOF
node_modules/
.git/
*.log
EOF
docker build -t <image-name> .

# 增加构建超时时间
docker build --timeout=600 -t <image-name> .
```

## 4. 实用工具和命令

### 4.1 Docker诊断命令

```bash
# 查看Docker信息
docker info

# 查看Docker版本
docker version

# 查看容器状态
docker ps -a

# 查看容器日志
docker logs <container-id>

# 查看容器详细信息
docker inspect <container-id>

# 查看容器资源使用情况
docker stats

# 查看卷信息
docker volume ls

# 查看网络信息
docker network ls

# 查看Docker系统资源使用情况
docker system df

# 清理无用资源
docker system prune -f

# 清理所有资源
docker system prune -f --volumes
```

### 4.2 Docker监控工具

```bash
# 使用cAdvisor监控Docker
docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:ro --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=8080:8080 --detach=true --name=cadvisor gcr.io/cadvisor/cadvisor:latest

# 使用Prometheus和Grafana监控Docker
# 参考Prometheus和Grafana部署文档
```

## 5. 故障模拟和练习

### 5.1 模拟Docker守护进程故障

```bash
# 停止Docker服务
systemctl stop docker

# 查看故障状态
docker ps

# 恢复Docker服务
systemctl start docker
```

### 5.2 模拟容器启动失败

```bash
# 创建一个会立即退出的容器
docker run --rm busybox false

# 查看容器状态
docker ps -a

# 查看容器日志
docker logs <container-id>
```

### 5.3 模拟镜像拉取失败

```bash
# 尝试拉取一个不存在的镜像
docker pull non-existent-image:latest

# 查看错误信息
```

## 6. 最佳实践

1. **监控Docker服务**：
   - 实施Docker监控，包括容器状态、资源使用情况、日志等
   - 设置告警规则，及时发现Docker异常
   - 定期检查Docker服务状态

2. **合理配置Docker资源**：
   - 为Docker守护进程设置适当的资源限制
   - 为容器设置合理的资源请求和限制
   - 避免单个容器占用过多资源

3. **实施数据持久化**：
   - 为所有需要持久化的数据使用卷
   - 定期备份卷数据
   - 使用可靠的存储后端

4. **定期维护Docker环境**：
   - 定期清理无用的镜像、容器和卷
   - 定期更新Docker版本
   - 定期检查Docker配置

5. **确保Docker安全**：
   - 启用Docker TLS认证
   - 限制Docker守护进程访问权限
   - 定期扫描镜像漏洞
   - 实施容器安全最佳实践

6. **建立应急响应流程**：
   - 制定Docker故障应急响应流程
   - 定期测试应急响应流程
   - 建立Docker故障恢复机制

## 7. 版本兼容性

| Docker版本 | 兼容性 |
|------------|--------|
| v20.10.x   | ✅     |
| v23.0.x    | ✅     |
| v24.0.x    | ✅     |

## 8. 总结

本案例提供了Docker容器引擎的全面故障排查方法和解决方案，通过学习本案例，您可以：
- 快速定位和解决各种Docker故障
- 了解Docker组件的工作原理和常见问题
- 掌握Docker资源管理和优化技巧
- 建立Docker监控和维护策略
- 提高容器环境的整体可靠性和可用性

通过合理的Docker管理、监控和维护，您将能够确保容器环境始终处于健康状态，为应用提供稳定可靠的运行环境。