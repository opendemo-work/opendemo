# Nginx Web服务器演示

## 🎯 概述

本演示展示了Nginx作为高性能Web服务器的核心功能，包括静态文件服务、反向代理、负载均衡、SSL终止和缓存优化等高级特性。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: Nginx 1.20+
- **适用场景**: Web服务、反向代理、负载均衡、静态资源服务
- **难度等级**: 🟡 中级

### 技术栈
```yaml
components:
  - nginx: "1.20"
  - alpine: "3.15"
  - docker: "20.10+"
  - letsencrypt: "latest"

features:
  - static file serving
  - reverse proxy
  - load balancing
  - ssl termination
  - http caching
  - gzip compression
```

## 🚀 快速开始

### 环境准备
```bash
# 克隆项目并进入目录
cd infrastructure/nginx-web-server

# 启动演示环境
docker-compose up -d

# 验证服务状态
curl -I http://localhost:8080
```

## 🔧 核心功能

### 1. 高性能静态文件服务
```nginx
server {
    listen 80;
    server_name example.com;
    
    # 静态文件根目录
    root /var/www/html;
    index index.html index.htm;
    
    # 静态文件优化
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

### 2. 反向代理配置
```nginx
upstream backend {
    server app1:3000 weight=3;
    server app2:3000 weight=2;
    server app3:3000 backup;
}

server {
    listen 80;
    server_name api.example.com;
    
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### 3. SSL/TLS配置
```nginx
server {
    listen 443 ssl http2;
    server_name secure.example.com;
    
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # SSL安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

## 📊 性能优化

### 缓存配置
```nginx
# HTTP缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g 
                 inactive=60m use_temp_path=off;

server {
    location /api/data/ {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_lock on;
    }
}
```

## 🧪 测试验证

### 性能测试脚本
```bash
#!/bin/bash
# 测试Nginx性能

echo "Testing Nginx Performance..."

# 基准测试
ab -n 1000 -c 10 http://localhost:8080/

# 静态文件测试
ab -n 1000 -c 50 http://localhost:8080/static/image.jpg

# API代理测试
ab -n 500 -c 20 http://localhost:8080/api/users

echo "Performance tests completed!"
```

---
*最后更新: 2026年2月3日*