# 🐳 Container 命令行速查表 (container-cli.md)

> 容器技术必备的命令行参考手册，涵盖Docker、Containerd、runc等核心容器工具，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [Docker管理](#docker管理)
- [Containerd管理](#containerd管理)
- [runc管理](#runc管理)
- [镜像管理](#镜像管理)
- [容器网络](#容器网络)
- [容器存储](#容器存储)
- [容器安全](#容器安全)
- [容器编排](#容器编排)
- [容器监控](#容器监控)
- [容器调试](#容器调试)
- [容器优化](#容器优化)
- [容器部署](#容器部署)
- [容器注册表](#容器注册表)
- [最佳实践](#最佳实践)

---

## Docker管理

### 基础容器操作
```bash
# 运行容器
docker run -d --name my-container nginx:latest
docker run -it --rm ubuntu:20.04 bash

# 查看容器状态
docker ps
docker ps -a  # 包含停止的容器
docker stats  # 实时资源使用

# 启动/停止容器
docker start container_name
docker stop container_name
docker restart container_name

# 进入容器
docker exec -it container_name bash
docker attach container_name

# 删除容器
docker rm container_name
docker rm -f container_name  # 强制删除运行中的容器
```

### 容器生命周期管理
```bash
# 查看容器详细信息
docker inspect container_name
docker logs container_name
docker logs -f container_name  # 实时查看日志

# 容器资源限制
docker run -d --name limited-container \
    --memory=512m \
    --cpus=0.5 \
    --restart=unless-stopped \
    nginx:latest

# 容器健康检查
docker run -d --name health-container \
    --health-cmd="curl -f http://localhost/ || exit 1" \
    --health-interval=30s \
    --health-timeout=10s \
    --health-retries=3 \
    nginx:latest
```

### Docker Compose
```bash
# 启动服务
docker-compose up -d
docker-compose up -d service_name

# 查看状态
docker-compose ps
docker-compose logs
docker-compose logs service_name

# 管理服务
docker-compose start
docker-compose stop
docker-compose restart
docker-compose down

# 构建镜像
docker-compose build
docker-compose build --no-cache
```

---

## Containerd管理

### 基础操作
```bash
# 查看容器列表
ctr containers ls

# 创建容器
ctr container create docker.io/library/nginx:latest my-nginx

# 启动容器
ctr task start my-nginx

# 停止容器
ctr task kill my-nginx

# 删除容器
ctr container delete my-nginx

# 查看任务状态
ctr task ls
```

### 镜像管理
```bash
# 拉取镜像
ctr images pull docker.io/library/ubuntu:20.04

# 查看镜像列表
ctr images ls

# 删除镜像
ctr images rm docker.io/library/ubuntu:20.04

# 导出镜像
ctr images export ubuntu.tar docker.io/library/ubuntu:20.04

# 导入镜像
ctr images import ubuntu.tar
```

### 命名空间管理
```bash
# 查看命名空间
ctr namespaces ls

# 创建命名空间
ctr namespaces create my-namespace

# 在指定命名空间操作
ctr -n my-namespace containers ls
```

---

## runc管理

### 容器运行时操作
```bash
# 创建容器配置
mkdir /containers/my-container
cd /containers/my-container

# 生成配置文件
runc spec

# 修改配置文件config.json
# 设置容器根文件系统、挂载点、资源限制等

# 运行容器
runc run my-container

# 后台运行容器
runc run -d my-container

# 进入运行中的容器
runc exec my-container bash
```

### 容器状态管理
```bash
# 查看容器状态
runc state my-container

# 暂停/恢复容器
runc pause my-container
runc resume my-container

# 杀死容器
runc kill my-container SIGTERM

# 删除容器
runc delete my-container
```

---

## 镜像管理

### Docker镜像操作
```bash
# 拉取镜像
docker pull nginx:latest
docker pull ubuntu:20.04

# 查看本地镜像
docker images
docker image ls

# 构建镜像
docker build -t my-app:v1.0 .
docker build -t registry.example.com/my-app:v1.0 .

# 推送镜像
docker push my-app:v1.0
docker push registry.example.com/my-app:v1.0

# 删除镜像
docker rmi image_name:tag
docker image rm image_id

# 镜像标签管理
docker tag source_image:tag target_image:tag
```

### 镜像优化
```dockerfile
# 多阶段构建示例
FROM golang:1.19-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
CMD ["./main"]

# 最小化镜像层数
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### 镜像安全扫描
```bash
# Docker Scout
docker scout cves image_name:tag

# Trivy扫描
trivy image nginx:latest
trivy fs /path/to/project

# Clair扫描
clair-scanner nginx:latest
```

---

## 容器网络

### Docker网络管理
```bash
# 查看网络
docker network ls

# 创建网络
docker network create my-network
docker network create --driver bridge my-bridge-net
docker network create --driver overlay my-overlay-net

# 连接容器到网络
docker network connect my-network container_name
docker run --network my-network --name container2 nginx

# 断开网络连接
docker network disconnect my-network container_name

# 查看网络详情
docker network inspect my-network
```

### 网络模式
```bash
# 桥接模式
docker run --network bridge nginx

# 主机模式
docker run --network host nginx

# 无网络模式
docker run --network none nginx

# 自定义网络
docker run --network my-custom-net nginx
```

### 端口映射
```bash
# 端口映射
docker run -p 8080:80 nginx
docker run -p 127.0.0.1:8080:80 nginx

# 多端口映射
docker run -p 80:80 -p 443:443 nginx
```

---

## 容器存储

### 数据卷管理
```bash
# 创建数据卷
docker volume create my-volume

# 查看数据卷
docker volume ls
docker volume inspect my-volume

# 使用数据卷
docker run -v my-volume:/data nginx
docker run -v /host/path:/container/path nginx

# 删除数据卷
docker volume rm my-volume
docker volume prune  # 清理未使用的卷
```

### 绑定挂载
```bash
# 绑定挂载
docker run -v /host/path:/container/path:ro nginx
docker run -v $(pwd)/data:/app/data nginx

# tmpfs挂载
docker run --tmpfs /tmp:rw,noexec,nosuid,size=100m nginx
```

### 存储驱动
```bash
# 查看存储驱动
docker info | grep "Storage Driver"

# Overlay2配置
# /etc/docker/daemon.json
{
    "storage-driver": "overlay2",
    "storage-opts": [
        "overlay2.override_kernel_check=true"
    ]
}
```

---

## 容器安全

### 安全配置
```bash
# 用户权限控制
docker run --user 1000:1000 nginx

# 只读文件系统
docker run --read-only nginx

# 能力限制
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx

# seccomp配置
docker run --security-opt seccomp=profile.json nginx

# SELinux/AppArmor
docker run --security-opt label=type:container_t nginx
```

### 安全扫描
```bash
# 镜像漏洞扫描
docker scan nginx:latest
anchore-cli image add nginx:latest

# 运行时安全监控
falco -r /etc/falco/falco_rules.yaml
```

### 密钥管理
```bash
# Docker Secrets
echo "my-secret-password" | docker secret create db_password -
docker service create --secret db_password nginx

# 环境变量注入
docker run -e DB_PASSWORD=mysecretpassword nginx
```

---

## 容器编排

### Docker Swarm
```bash
# 初始化Swarm
docker swarm init --advertise-addr 192.168.1.100

# 查看节点
docker node ls

# 创建服务
docker service create --name web --replicas 3 nginx:latest

# 服务管理
docker service ls
docker service ps web
docker service scale web=5
docker service update --image nginx:1.21 web

# 删除服务
docker service rm web
```

### Kubernetes集成
```bash
# Minikube操作
minikube start
minikube status
minikube dashboard

# kubectl与Docker集成
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs pod_name
```

---

## 容器监控

### 资源监控
```bash
# Docker内置监控
docker stats
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# cAdvisor监控
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  gcr.io/cadvisor/cadvisor:latest
```

### 日志管理
```bash
# 日志驱动配置
docker run --log-driver=json-file --log-opt max-size=10m nginx

# 查看日志
docker logs container_name
docker logs --since 1h container_name
docker logs --tail 100 container_name

# 日志轮转
# /etc/docker/daemon.json
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}
```

### 性能分析
```bash
# 容器性能分析
docker exec container_name top
docker exec container_name ps aux

# 系统调用跟踪
docker exec container_name strace -p 1

# 网络监控
docker exec container_name netstat -tuln
docker exec container_name ss -tuln
```

---

## 容器调试

### 调试工具
```bash
# 进入容器调试
docker exec -it container_name bash
docker exec -it container_name sh

# 安装调试工具
docker exec container_name apt-get update
docker exec container_name apt-get install -y procps net-tools dnsutils

# 复制文件
docker cp container_name:/path/file ./local_file
docker cp ./local_file container_name:/path/file
```

### 故障诊断
```bash
# 检查容器状态
docker inspect container_name | jq '.[].State'

# 查看容器事件
docker events --filter container=container_name

# 检查网络连通性
docker exec container_name ping google.com
docker exec container_name curl http://service:port

# 检查资源限制
docker inspect container_name | jq '.[].HostConfig'
```

### 容器取证
```bash
# 导出容器文件系统
docker export container_name > container.tar

# 查看容器变更
docker diff container_name

# 提交容器为镜像
docker commit container_name new_image:tag
```

---

## 容器优化

### 性能优化
```bash
# 资源限制优化
docker run \
    --memory=1g \
    --memory-swap=2g \
    --cpus=1.5 \
    --cpu-shares=512 \
    nginx

# 网络优化
docker run --network host nginx  # 减少网络开销

# 存储优化
docker run --tmpfs /tmp:rw,noexec,nosuid,size=100m nginx
```

### 镜像优化
```dockerfile
# 使用轻量基础镜像
FROM alpine:latest
# 或
FROM gcr.io/distroless/static:nonroot

# 多阶段构建
FROM golang:1.19-alpine AS builder
# 构建步骤
FROM alpine:latest
# 运行时只需要二进制文件
```

### 启动优化
```bash
# 健康检查优化
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# 预热容器
docker run --init nginx  # 使用tini作为init系统
```

---

## 容器部署

### CI/CD集成
```yaml
# GitHub Actions示例
name: Docker Build and Push
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: registry.example.com/my-app:${{ github.sha }}
```

### 部署策略
```bash
# 滚动更新
docker service update --image nginx:1.21 web

# 蓝绿部署
docker service create --name web-blue nginx:v1
docker service create --name web-green nginx:v2
docker service update --replicas 0 web-blue

# 金丝雀部署
docker service create --name web-stable nginx:v1
docker service create --name web-canary --replicas 1 nginx:v2
```

### 配置管理
```bash
# 环境变量
docker run -e ENV=production -e DB_HOST=mysql nginx

# 配置文件挂载
docker run -v ./config/nginx.conf:/etc/nginx/nginx.conf nginx

# Docker Configs
echo "server_tokens off;" | docker config create nginx-config -
docker service create --config nginx-config nginx
```

---

## 容器注册表

### 私有注册表
```bash
# 启动私有注册表
docker run -d -p 5000:5000 --name registry registry:2

# 推送镜像到私有注册表
docker tag nginx:latest localhost:5000/nginx:latest
docker push localhost:5000/nginx:latest

# 从私有注册表拉取
docker pull localhost:5000/nginx:latest
```

### 注册表认证
```bash
# Docker Hub认证
docker login
docker logout

# 私有注册表认证
docker login registry.example.com

# 配置认证信息
# ~/.docker/config.json
{
    "auths": {
        "registry.example.com": {
            "auth": "base64-encoded-credentials"
        }
    }
}
```

### 镜像签名
```bash
# Docker Content Trust
export DOCKER_CONTENT_TRUST=1
docker push registry.example.com/my-app:v1.0

# Cosign签名
cosign sign registry.example.com/my-app:v1.0
cosign verify registry.example.com/my-app:v1.0
```

---

## 最佳实践

### 安全最佳实践
```bash
# 镜像安全
- 使用官方基础镜像
- 定期更新基础镜像
- 运行漏洞扫描
- 启用内容信任

# 运行时安全
- 以非root用户运行
- 限制容器能力
- 启用seccomp/AppArmor
- 配置资源限制

# 网络安全
- 使用用户定义网络
- 限制端口暴露
- 启用网络策略
```

### 性能最佳实践
```bash
# 镜像优化
- 使用多阶段构建
- 最小化镜像层数
- 清理构建依赖
- 使用.dockerignore

# 资源管理
- 设置合理的资源限制
- 启用健康检查
- 配置自动重启策略
- 监控资源使用

# 网络优化
- 使用host网络模式（适当场景）
- 优化DNS配置
- 减少网络跳数
```

### 运维最佳实践
```bash
# 标签规范
docker build -t my-app:v1.2.3-$(date +%Y%m%d) .

# 日志管理
- 配置日志轮转
- 使用结构化日志
- 集中日志收集
- 设置日志级别

# 监控告警
- 设置资源使用阈值
- 配置容器健康检查
- 建立故障恢复机制
- 定期备份重要数据
```

---