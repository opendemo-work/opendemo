# Container 技术栈命名大全

本文件定义了容器技术栈中各类组件、资源、配置的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、容器镜像命名规范

### 1.1 基础镜像命名
```dockerfile
# 官方基础镜像
FROM ubuntu:20.04 AS base-image
FROM alpine:3.15 AS minimal-base
FROM python:3.9-slim AS python-runtime

# 应用特定基础镜像
FROM nginx:1.21-alpine AS web-server-base
FROM postgres:13-alpine AS database-base
FROM redis:6.2-alpine AS cache-base
```

### 1.2 应用镜像命名
```bash
# 镜像仓库地址格式
registry.example.com/namespace/application:tag

# 版本标签规范
myapp:v1.2.3                    # 语义化版本
myapp:latest                   # 最新稳定版
myapp:develop                  # 开发分支版本
myapp:feature-user-auth       # 功能分支版本
myapp:hotfix-security-patch   # 热修复版本

# 构建元数据标签
myapp:build-20231201-1430     # 构建时间戳
myapp:git-a1b2c3d4            # Git提交哈希
myapp:sha256-abc123...        # 镜像内容哈希
```

### 1.3 多阶段构建命名
```dockerfile
# 构建阶段
FROM golang:1.19-alpine AS builder
FROM node:16-alpine AS frontend-builder

# 运行时阶段
FROM alpine:3.15 AS runtime
FROM scratch AS minimal-runtime

# 测试阶段
FROM runtime AS tester
RUN go test ./...

# 最终生产镜像
FROM runtime AS production
```

## 二、容器运行时命名规范

### 2.1 容器实例命名
```bash
# 容器名称格式
${application}-${environment}-${instance-id}
${service}-${version}-${replica-number}

# 具体示例
web-app-prod-001              # Web应用生产实例001
api-service-v2-3              # API服务版本2副本3
database-master-primary       # 数据库主节点
cache-redis-slave-2           # Redis从节点2
```

### 2.2 容器网络命名
```yaml
# Docker网络
networks:
  app-network:           # 应用网络
    driver: bridge
  db-network:            # 数据库网络
    driver: bridge
  monitoring-network:    # 监控网络
    driver: bridge

# 网络别名
services:
  web:
    networks:
      app-network:
        aliases:
          - web.internal     # 内部服务发现名称
          - frontend.local   # 本地开发别名
```

### 2.3 存储卷命名
```yaml
# 数据卷命名
volumes:
  postgres-data:         # PostgreSQL数据卷
    driver: local
  redis-cache:           # Redis缓存卷
    driver: local
  app-logs:              # 应用日志卷
    driver: local
  shared-config:         # 共享配置卷
    driver: local

# 挂载点命名
services:
  app:
    volumes:
      - postgres-data:/var/lib/postgresql/data    # 数据库存储
      - app-logs:/var/log/application             # 应用日志
      - shared-config:/etc/app/config             # 配置文件
```

## 三、编排配置命名规范

### 3.1 Docker Compose服务命名
```yaml
# 服务名称规范
version: '3.8'

services:
  # Web服务层
  nginx-proxy:                    # 反向代理服务
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
      
  web-application:               # Web应用服务
    image: myapp:latest
    depends_on:
      - database
      - cache
      
  api-gateway:                   # API网关服务
    image: kong:latest
    ports:
      - "8000:8000"
      - "8443:8443"

  # 数据服务层
  database-postgres:             # PostgreSQL数据库
    image: postgres:13
    environment:
      POSTGRES_DB: myapp_prod
      POSTGRES_USER: myapp_user
      
  cache-redis:                   # Redis缓存服务
    image: redis:6-alpine
    command: redis-server --appendonly yes
    
  message-queue:                 # 消息队列服务
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  # 监控服务层
  monitoring-prometheus:         # Prometheus监控
    image: prom/prometheus
    ports:
      - "9090:9090"
      
  logging-elasticsearch:         # ELK日志栈
    image: elasticsearch:7.17
    ports:
      - "9200:9200"
      
  tracing-jaeger:                # 分布式追踪
    image: jaegertracing/all-in-one
    ports:
      - "16686:16686"
```

### 3.2 Kubernetes资源配置
```yaml
# Deployment命名
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-deployment        # 应用部署
  namespace: production          # 命名空间
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        version: v1.2.3
        environment: production

---
# Service命名
apiVersion: v1
kind: Service
metadata:
  name: web-app-service          # 服务名称
  namespace: production
spec:
  selector:
    app: web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

---
# ConfigMap命名
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-production    # 配置映射
  namespace: production
data:
  app.properties: |
    server.port=8080
    logging.level=INFO

---
# Secret命名
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials     # 敏感信息
  namespace: production
type: Opaque
data:
  username: base64_encoded_username
  password: base64_encoded_password
```

### 3.3 环境变量命名
```yaml
# 应用配置环境变量
environment:
  # 基础配置
  APP_ENV: production
  APP_DEBUG: "false"
  LOG_LEVEL: INFO
  
  # 数据库连接
  DB_HOST: database-postgres
  DB_PORT: "5432"
  DB_NAME: myapp_production
  DB_USER: myapp_user
  DB_PASSWORD_FILE: /run/secrets/db-password
  
  # 缓存配置
  REDIS_HOST: cache-redis
  REDIS_PORT: "6379"
  REDIS_PASSWORD: ""
  
  # 消息队列
  RABBITMQ_HOST: message-queue
  RABBITMQ_PORT: "5672"
  RABBITMQ_VHOST: /
  
  # 监控配置
  PROMETHEUS_ENDPOINT: http://monitoring-prometheus:9090
  JAEGER_AGENT_HOST: tracing-jaeger
  JAEGER_AGENT_PORT: "6831"
```

## 四、监控告警命名规范

### 4.1 容器健康检查
```yaml
# 健康检查配置
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s

# 自定义健康检查脚本
healthcheck:
  test: ["CMD-SHELL", "/app/scripts/health-check.sh"]
  interval: 15s
  timeout: 5s
  retries: 5
```

### 4.2 资源限制命名
```yaml
# 资源配额
deploy:
  resources:
    limits:
      cpus: '0.5'              # CPU限制
      memory: 512M             # 内存限制
    reservations:
      cpus: '0.25'             # CPU预留
      memory: 256M             # 内存预留

# Kubernetes资源请求
resources:
  requests:
    memory: "256Mi"            # 内存请求
    cpu: "250m"               # CPU请求
  limits:
    memory: "512Mi"            # 内存限制
    cpu: "500m"               # CPU限制
```

### 4.3 日志配置命名
```yaml
# 日志驱动配置
logging:
  driver: json-file
  options:
    max-size: "10m"            # 日志文件最大大小
    max-file: "3"              # 保留日志文件数量
    labels: "production,web"   # 日志标签

# 结构化日志配置
environment:
  LOG_FORMAT: json              # JSON格式日志
  LOG_TIMESTAMP: true           # 包含时间戳
  LOG_LEVEL: INFO               # 日志级别
```

## 五、故障排查命名规范

### 5.1 容器状态检查
```bash
# 容器运行状态
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 容器资源使用
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# 容器网络连接
docker exec container_name netstat -tlnp

# 容器进程信息
docker top container_name

# 容器日志查看
docker logs --tail 100 --timestamps container_name
docker logs --since 1h container_name
```

### 5.2 性能瓶颈诊断
```bash
# CPU性能分析
docker exec container_name top -b -n 1 | head -20
docker exec container_name ps aux --sort=-%cpu | head -10

# 内存使用分析
docker exec container_name free -h
docker exec container_name ps aux --sort=-%mem | head -10

# 磁盘IO监控
docker exec container_name iostat -x 1 5
docker exec container_name du -sh /var/log/*

# 网络性能检查
docker exec container_name ss -tuln
docker exec container_name ping -c 4 external-service
```

### 5.3 存储问题排查
```bash
# 磁盘空间检查
docker system df
docker volume ls -q | xargs -I {} docker volume inspect {}

# 容器磁盘使用
docker exec container_name du -sh /*
docker exec container_name find /tmp -type f -mtime +7 -delete

# 镜像清理
docker images --filter "dangling=true" -q | xargs docker rmi
docker system prune -a --volumes

# 存储驱动问题
docker info | grep -i storage
docker exec container_name df -h
```

## 六、安全合规命名规范

### 6.1 镜像安全扫描
```bash
# 镜像漏洞扫描
docker scan image_name:tag
trivy image --severity HIGH,CRITICAL image_name:tag

# 镜像签名验证
docker trust inspect image_name:tag
cosign verify --key cosign.pub image_name:tag

# 安全基线检查
docker scout cves image_name:tag
anchore-cli image vuln image_name:tag
```

### 6.2 访问控制配置
```yaml
# 用户权限配置
user: "1000:1000"              # 非root用户运行
group_add:
  - "docker"

# 文件权限设置
volumes:
  - type: bind
    source: ./config
    target: /app/config
    read_only: true              # 只读挂载

# SELinux/AppArmor配置
security_opt:
  - label=type:container_t
  - apparmor=profile_name
```

### 6.3 网络安全隔离
```yaml
# 网络隔离配置
networks:
  frontend:
    internal: true               # 内部网络，无外网访问
  backend:
    internal: true
  dmz:
    internal: false              # DMZ网络，允许外网访问

# 端口暴露控制
ports:
  - "127.0.0.1:8080:8080"       # 仅本地访问
  - "0.0.0.0:8443:8443"         # 公开HTTPS端口

# 防火墙规则
cap_add:
  - NET_ADMIN
sysctls:
  - net.ipv4.tcp_syncookies=1
  - net.ipv4.ip_forward=0
```

## 七、备份恢复命名规范

### 7.1 数据备份策略
```bash
# 数据库备份命名
backup_postgres_${DATE}_${TIMESTAMP}.sql.gz
backup_redis_${DATE}_${TIMESTAMP}.rdb
backup_elasticsearch_${DATE}_${TIMESTAMP}.tar.gz

# 配置备份
backup_config_${ENVIRONMENT}_${DATE}.tar.gz
backup_secrets_${ENVIRONMENT}_${DATE}.enc

# 完整系统备份
backup_full_system_${DATE}_${TIMESTAMP}.tar
```

### 7.2 恢复操作命名
```bash
# 恢复脚本命名
restore_database_from_backup.sh
restore_volumes_from_snapshot.sh
rollback_to_previous_version.sh

# 恢复状态标记
RECOVERY_IN_PROGRESS=true
RECOVERY_COMPLETED=false
RECOVERY_FAILED_REASON="Connection timeout"

# 恢复验证
validate_restore_integrity.sh
verify_application_functionality.sh
```

## 八、CI/CD集成命名规范

### 8.1 构建流水线命名
```yaml
# 构建阶段
stages:
  - build-base-image         # 构建基础镜像
  - build-application        # 构建应用镜像
  - security-scan            # 安全扫描
  - deploy-staging           # 部署到测试环境
  - integration-test         # 集成测试
  - deploy-production        # 部署到生产环境

# 构建产物命名
artifacts:
  paths:
    - ${APP_NAME}-${VERSION}-${COMMIT_SHA}.tar.gz
    - ${APP_NAME}-manifest-${VERSION}.yaml
    - security-scan-report-${BUILD_ID}.html
```

### 8.2 部署策略命名
```yaml
# 蓝绿部署
blue_environment:
  tag: blue-${TIMESTAMP}
  active: true

green_environment:
  tag: green-${TIMESTAMP}
  active: false

# 金丝雀发布
canary_deployment:
  replicas: 1
  weight: 10
  
stable_deployment:
  replicas: 9
  weight: 90
```

### 8.3 回滚机制命名
```bash
# 回滚脚本
rollback_to_previous_version.sh
rollback_database_migration.sh
emergency_rollback_procedure.sh

# 回滚触发条件
ROLLBACK_TRIGGER_CPU_THRESHOLD=80
ROLLBACK_TRIGGER_ERROR_RATE=0.05
ROLLBACK_TRIGGER_RESPONSE_TIME=5000

# 回滚验证
post_rollback_validation.sh
service_health_check_after_rollback.sh
```

## 九、最佳实践示例

### 9.1 生产环境Dockerfile模板
```dockerfile
# 多阶段构建生产镜像
FROM python:3.9-slim AS builder

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制源代码
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

# 运行测试
RUN python -m pytest tests/

# 生产阶段
FROM python:3.9-slim AS production

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 复制依赖和应用
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

# 设置权限
RUN chown -R appuser:appuser /app
USER appuser

WORKDIR /app

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动应用
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### 9.2 容器监控脚本
```bash
#!/bin/bash
# container_monitoring.sh - 容器健康监控脚本

CONTAINER_NAME=$1
THRESHOLDS_FILE="/etc/container-thresholds.conf"

# 加载阈值配置
source $THRESHOLDS_FILE

# 检查容器状态
check_container_status() {
    local status=$(docker inspect --format='{{.State.Status}}' $CONTAINER_NAME)
    if [[ "$status" != "running" ]]; then
        echo "CRITICAL: Container $CONTAINER_NAME is not running (status: $status)"
        return 1
    fi
    return 0
}

# 检查资源使用
check_resource_usage() {
    local stats=$(docker stats --no-stream --format "{{.CPUPerc}},{{.MemPerc}}" $CONTAINER_NAME)
    IFS=',' read -r cpu_usage mem_usage <<< "$stats"
    
    cpu_value=${cpu_usage%\%}
    mem_value=${mem_usage%\%}
    
    if (( $(echo "$cpu_value > $CPU_THRESHOLD" | bc -l) )); then
        echo "WARNING: High CPU usage for $CONTAINER_NAME: $cpu_usage%"
    fi
    
    if (( $(echo "$mem_value > $MEMORY_THRESHOLD" | bc -l) )); then
        echo "WARNING: High memory usage for $CONTAINER_NAME: $mem_usage%"
    fi
}

# 检查重启次数
check_restart_count() {
    local restart_count=$(docker inspect --format='{{.RestartCount}}' $CONTAINER_NAME)
    if [[ $restart_count -gt $MAX_RESTARTS ]]; then
        echo "WARNING: Container $CONTAINER_NAME has restarted $restart_count times"
    fi
}

# 主监控循环
main() {
    if ! check_container_status; then
        exit 2
    fi
    
    check_resource_usage
    check_restart_count
    
    echo "OK: Container $CONTAINER_NAME health check passed"
    exit 0
}

main "$@"
```

### 9.3 故障恢复自动化
```yaml
# docker-compose.emergency.yml - 紧急恢复配置
version: '3.8'

services:
  emergency-restore:
    image: backup-manager:latest
    environment:
      - ACTION=RESTORE
      - BACKUP_SOURCE=s3://backups/latest
      - TARGET_ENVIRONMENT=production
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - backup-storage:/backups
    networks:
      - host
      
  health-verifier:
    image: health-checker:latest
    depends_on:
      - emergency-restore
    environment:
      - CHECK_SERVICES=web,database,cache
      - TIMEOUT_SECONDS=300
    command: ["verify-all-services", "--wait-for-ready"]
    
volumes:
  backup-storage:
    external: true
```

---

**注意事项：**
1. 命名应体现层级关系和业务含义
2. 生产环境中优先使用明确的版本标签而非latest
3. 安全相关的配置必须严格控制访问权限
4. 监控告警命名应便于快速定位问题根源
5. 备份恢复流程需要定期演练验证