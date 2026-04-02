# Docker Integration Demo

Docker容器化部署演示项目，演示Spring Boot应用的Docker化部署。

## 技术栈

- Spring Boot 2.7
- Docker
- Docker Compose
- Nginx
- Redis
- Prometheus + Grafana

## 项目结构

```
docker-integration-demo/
├── src/main/java/com/example/demo/
│   └── DockerDemoApplication.java         # 应用入口
├── Dockerfile                             # Docker镜像构建
├── docker-compose.yml                     # 多服务编排
├── nginx.conf                             # Nginx配置
├── prometheus.yml                         # Prometheus配置
├── pom.xml
└── README.md
```

## Dockerfile详解

### 多阶段构建

```dockerfile
# 第一阶段：构建
FROM eclipse-temurin:11-jdk-alpine AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# 第二阶段：运行
FROM eclipse-temurin:11-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

优势：
- 构建和运行环境分离
- 最终镜像更小（只包含JRE和jar包）
- 安全性更高（不包含编译工具）

### 安全最佳实践

```dockerfile
# 使用非root用户
RUN addgroup -S spring && adduser -S spring -G spring
USER spring

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --quiet --tries=1 --spider \
    http://localhost:8080/actuator/health || exit 1
```

## Docker Compose服务

### 应用服务

```yaml
app:
  build:
    context: .
    dockerfile: Dockerfile
  ports:
    - "8080:8080"
  environment:
    - SPRING_PROFILES_ACTIVE=docker
    - JAVA_OPTS=-Xmx512m -Xms256m
```

### Nginx反向代理

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

### Redis缓存

```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - redis-data:/data
  command: redis-server --appendonly yes
```

### 监控栈

```yaml
prometheus:
  image: prom/prometheus:latest
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
```

## 快速开始

### 1. 构建镜像

```bash
# 构建应用镜像
docker build -t docker-demo:latest .

# 查看镜像
docker images | grep docker-demo
```

### 2. 运行容器

```bash
# 运行单个容器
docker run -d -p 8080:8080 --name docker-demo docker-demo:latest

# 查看日志
docker logs -f docker-demo

# 停止容器
docker stop docker-demo

# 删除容器
docker rm docker-demo
```

### 3. 使用Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app

# 停止所有服务
docker-compose down

# 停止并删除卷
docker-compose down -v
```

### 4. 访问服务

| 服务 | URL |
|------|-----|
| 应用 | http://localhost:8080 |
| Nginx | http://localhost |
| Redis | localhost:6379 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 (admin/admin) |

## Docker命令速查

### 镜像管理

```bash
# 查看镜像
docker images

# 删除镜像
docker rmi <image-id>

# 清理悬空镜像
docker image prune
```

### 容器管理

```bash
# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 停止容器
docker stop <container-id>

# 启动容器
docker start <container-id>

# 重启容器
docker restart <container-id>

# 删除容器
docker rm <container-id>

# 强制删除运行中的容器
docker rm -f <container-id>

# 进入容器
docker exec -it <container-id> /bin/sh

# 查看容器日志
docker logs <container-id>
docker logs -f <container-id>  # 持续跟踪
```

### 网络管理

```bash
# 查看网络
docker network ls

# 创建网络
docker network create my-network

# 查看网络详情
docker network inspect my-network
```

### 卷管理

```bash
# 查看卷
docker volume ls

# 创建卷
docker volume create my-volume

# 删除卷
docker volume rm my-volume
```

## 生产环境部署

### 镜像仓库

```bash
# 登录镜像仓库
docker login registry.example.com

# 标记镜像
docker tag docker-demo:latest registry.example.com/docker-demo:1.0.0

# 推送镜像
docker push registry.example.com/docker-demo:1.0.0

# 拉取镜像
docker pull registry.example.com/docker-demo:1.0.0
```

### 滚动更新

```bash
# 使用Docker Compose滚动更新
docker-compose pull
docker-compose up -d --no-deps --build app
```

### 资源限制

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 故障排查

### 容器无法启动

```bash
# 查看容器日志
docker logs <container-id>

# 检查容器详情
docker inspect <container-id>

# 检查退出状态码
docker inspect <container-id> --format='{{.State.ExitCode}}'
```

### 网络问题

```bash
# 测试容器间网络
docker exec -it <container-id> ping <target-ip>

# 查看容器IP
docker inspect <container-id> --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

## 学习要点

1. Docker基础概念（镜像、容器、网络、卷）
2. Dockerfile编写和多阶段构建
3. Docker Compose服务编排
4. 容器安全最佳实践
5. 生产环境部署策略
6. 监控和日志收集
