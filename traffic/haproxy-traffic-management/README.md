# HAProxy 流量管理演示

## 🎯 概述

本演示展示了如何使用HAProxy进行高级流量管理，包括基于路径、域名、Header的路由规则，以及蓝绿部署和金丝雀发布策略。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: HAProxy 2.4+
- **适用场景**: 微服务流量管理、灰度发布、A/B测试
- **难度等级**: 🔴 高级

### 技术栈
```yaml
components:
  - haproxy: "2.4"
  - alpine: "3.15"
  - docker: "20.10+"
  - docker-compose: "1.29+"

features:
  - path-based routing
  - header-based routing
  - blue-green deployment
  - canary release
  - rate limiting
```

## 🚀 快速开始

### 环境准备
```bash
# 系统要求
- Linux/macOS系统
- Docker和Docker Compose
- 至少2GB内存

# 克隆项目
git clone <repo-url>
cd infrastructure/haproxy-traffic-management

# 启动演示环境
docker-compose up -d
```

### 验证部署
```bash
# 检查HAProxy状态
docker-compose exec haproxy echo "show stat" | socat stdio /var/run/haproxy.sock

# 测试基本路由
curl -H "Host: api.example.com" http://localhost:8080/version
```

## 📁 项目结构

```
haproxy-traffic-management/
├── docker-compose.yml              # Docker编排文件
├── haproxy/                        # HAProxy配置目录
│   ├── haproxy.cfg                # 主配置文件
│   ├── errors/                    # 自定义错误页面
│   │   ├── 400.http
│   │   ├── 403.http
│   │   └── 503.http
│   └── ssl/                       # SSL证书目录
├── backend-services/               # 后端服务目录
│   ├── api-v1/                    # API v1服务
│   ├── api-v2/                    # API v2服务
│   └── web-app/                   # Web应用服务
├── scripts/                       # 脚本目录
│   ├── deploy-blue-green.sh      # 蓝绿部署脚本
│   ├── canary-release.sh         # 金丝雀发布脚本
│   └── traffic-shift.sh          # 流量切换脚本
├── tests/                         # 测试目录
│   ├── integration-tests.sh      # 集成测试
│   └── performance-tests.sh      # 性能测试
└── README.md                     # 本文件
```

## 🔧 核心功能演示

### 1. 基于路径的路由
```haproxy
# haproxy.cfg 路径路由配置
frontend http_front
    bind *:80
    mode http
    
    # API路由
    acl is_api path_beg /api/
    use_backend api_backend if is_api
    
    # Web路由
    acl is_web path_beg /web/
    use_backend web_backend if is_web
    
    # 默认后端
    default_backend default_backend

backend api_backend
    balance roundrobin
    server api-v1 api-v1:8080 check
    server api-v2 api-v2:8080 check

backend web_backend
    balance roundrobin
    server web-app web-app:80 check
```

### 2. Header-based路由
```haproxy
# 基于Header的路由规则
frontend http_front
    bind *:80
    mode http
    
    # 根据User-Agent路由
    acl is_mobile hdr_sub(User-Agent) -i mobile
    use_backend mobile_backend if is_mobile
    
    # 根据自定义Header路由
    acl is_internal hdr(X-Internal-Access) -i true
    use_backend internal_backend if is_internal
    
    default_backend public_backend
```

### 3. 蓝绿部署
```bash
#!/bin/bash
# scripts/deploy-blue-green.sh

BLUE_ENV="blue"
GREEN_ENV="green"
ACTIVE_ENV=$(cat /tmp/active_env)

# 部署新版本到非活跃环境
if [ "$ACTIVE_ENV" = "blue" ]; then
    TARGET_ENV=$GREEN_ENV
    OLD_ENV=$BLUE_ENV
else
    TARGET_ENV=$BLUE_ENV
    OLD_ENV=$GREEN_ENV
fi

echo "Deploying to $TARGET_ENV environment..."

# 更新目标环境
docker-compose up -d ${TARGET_ENV}-service

# 健康检查
sleep 30
if curl -f http://localhost:${TARGET_ENV}_port/health; then
    echo "Health check passed, switching traffic..."
    
    # 切换流量
    sed -i "s/use_backend ${OLD_ENV}_backend/use_backend ${TARGET_ENV}_backend/" haproxy/haproxy.cfg
    docker-compose exec haproxy haproxy -f /usr/local/etc/haproxy/haproxy.cfg -c
    docker-compose exec haproxy kill -HUP 1
    
    # 更新活跃环境标记
    echo $TARGET_ENV > /tmp/active_env
    echo "Deployment completed successfully!"
else
    echo "Health check failed, rollback..."
    docker-compose stop ${TARGET_ENV}-service
    exit 1
fi
```

## 📊 使用示例

### 基本路由测试
```bash
# 测试API路由
curl -H "Host: api.example.com" http://localhost:8080/api/users
curl -H "Host: api.example.com" http://localhost:8080/api/products

# 测试Web路由
curl -H "Host: www.example.com" http://localhost:8080/web/dashboard
curl -H "Host: www.example.com" http://localhost:8080/web/profile

# 测试移动设备路由
curl -H "User-Agent: Mobile Safari" http://localhost:8080/
```

### 金丝雀发布测试
```bash
#!/bin/bash
# 测试金丝雀发布

# 发送100个请求，观察流量分配
for i in {1..100}; do
    response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:8080/)
    echo "Request $i: Status $response"
    sleep 0.1
done

# 查看HAProxy统计
echo "HAProxy Statistics:"
curl -s http://localhost:8080/admin/stats | grep -E "(v1|v2)"
```

## ⚙️ 高级配置

### 速率限制
```haproxy
# 全局速率限制
frontend http_front
    bind *:80
    mode http
    
    # 每个IP每分钟最多100个请求
    stick-table type ip size 1m expire 1m store http_req_rate(60s)
    http-request track-sc0 src
    http-request deny if { sc0_http_req_rate gt 100 }
    
    # API端点特殊限制
    acl is_api path_beg /api/
    stick-table type ip size 1m expire 1m store http_req_rate(60s)
    http-request track-sc1 src if is_api
    http-request deny if is_api { sc1_http_req_rate gt 50 }
```

### SSL终止和重定向
```haproxy
frontend https_front
    bind *:443 ssl crt /etc/haproxy/ssl/cert.pem
    mode http
    option httplog
    
    # 强制HTTPS重定向
    redirect scheme https code 301 if !{ ssl_fc }
    
    # HSTS头部
    rspadd Strict-Transport-Security:\ max-age=31536000;\ includeSubDomains;\ preload
```

## 🔍 监控和日志

### HAProxy统计页面
```haproxy
# 启用统计页面
listen stats
    bind *:8404
    mode http
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST
    stats auth admin:password
```

### 访问日志配置
```haproxy
# 详细的访问日志
capture request header Host len 32
capture request header User-Agent len 64
capture request header X-Forwarded-For len 15
capture response header Content-Length len 10

log stdout format raw daemon info
```

## 🔒 安全配置

### 访问控制
```haproxy
# IP白名单
acl allowed_ips src 192.168.1.0/24 10.0.0.0/8
acl internal_endpoint path_beg /internal/
http-request deny if internal_endpoint !allowed_ips

# HTTP方法限制
acl is_read_only_method method GET HEAD OPTIONS
acl is_admin_path path_beg /admin/
http-request deny if is_admin_path !is_read_only_method
```

## 🧪 测试验证

### 自动化测试脚本
```bash
#!/bin/bash
# tests/integration-tests.sh

echo "Running HAProxy Traffic Management Tests..."

# 测试1: 基本路由功能
test_basic_routing() {
    echo "Testing basic routing..."
    response=$(curl -s -H "Host: api.example.com" http://localhost:8080/api/health)
    if [[ $response == *"healthy"* ]]; then
        echo "✓ Basic routing test passed"
    else
        echo "✗ Basic routing test failed"
        return 1
    fi
}

# 测试2: 负载均衡
test_load_balancing() {
    echo "Testing load balancing..."
    v1_count=0
    v2_count=0
    
    for i in {1..20}; do
        response=$(curl -s http://localhost:8080/api/version)
        if [[ $response == *"v1"* ]]; then
            ((v1_count++))
        elif [[ $response == *"v2"* ]]; then
            ((v2_count++))
        fi
    done
    
    # 验证负载相对均衡
    if [ $v1_count -gt 5 ] && [ $v2_count -gt 5 ]; then
        echo "✓ Load balancing test passed (v1:$v1_count, v2:$v2_count)"
    else
        echo "✗ Load balancing test failed"
        return 1
    fi
}

# 运行所有测试
test_basic_routing
test_load_balancing

echo "All tests completed!"
```

## 📈 性能优化

### 内核参数调优
```bash
# /etc/sysctl.conf 优化配置
net.core.somaxconn = 65535
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 5000
```

### HAProxy性能配置
```haproxy
global
    maxconn 10000
    tune.ssl.default-dh-param 2048
    tune.bufsize 16384
    nbproc 2
    cpu-map 1 0
    cpu-map 2 1

defaults
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option redispatch
    retries 3
```

## 🚀 生产部署

### Kubernetes部署配置
```yaml
# k8s/haproxy-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: haproxy-lb
spec:
  replicas: 3
  selector:
    matchLabels:
      app: haproxy
  template:
    metadata:
      labels:
        app: haproxy
    spec:
      containers:
      - name: haproxy
        image: haproxy:2.4
        ports:
        - containerPort: 80
        - containerPort: 443
        volumeMounts:
        - name: config-volume
          mountPath: /usr/local/etc/haproxy
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: config-volume
        configMap:
          name: haproxy-config
```

## 📚 相关资源

### 官方文档
- [HAProxy官方文档](https://www.haproxy.org/#docs)
- [HAProxy配置手册](https://cbonte.github.io/haproxy-dconv/)

### 学习资源
- 《HAProxy实战指南》
- 微服务网关架构最佳实践

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境
```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up

# 运行测试
./tests/run-all-tests.sh

# 重新加载配置
docker-compose exec haproxy haproxy -f /usr/local/etc/haproxy/haproxy.cfg -c
docker-compose exec haproxy kill -HUP 1
```

## 📄 许可证

本项目采用 MIT 许可证

---
*最后更新: 2026年2月3日*