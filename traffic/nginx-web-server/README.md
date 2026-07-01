# NGINX Web 服务器演示 - 静态资源托管

> 使用 NGINX 作为静态 Web 服务器，演示静态资源托管、目录索引、Gzip 压缩、访问日志配置和缓存策略。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 使用 NGINX 托管静态网站
- ✅ 配置 Gzip 压缩减少传输体积
- ✅ 配置访问日志和错误日志
- ✅ 理解 location 匹配规则和优先级
- ✅ 为静态资源配置浏览器缓存

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    NGINX Web 服务器架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   浏览器 ──▶ NGINX :80 ──▶ 静态文件目录                          │
│                                /usr/share/nginx/html            │
│                                                                 │
│              ┌─────────────────────────────┐                   │
│              │ index.html / style.css      │                   │
│              │ app.js / images/            │                   │
│              │ 404.html / favicon.ico      │                   │
│              └─────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Docker | >= 20.10 | 运行 NGINX 容器 |
| Docker Compose | >= 1.29 | 编排服务 |

### 启动服务

```bash
cd traffic/nginx-web-server
./scripts/start.sh
sleep 3
./scripts/check.sh
```

### 访问网站

```bash
curl -s http://localhost/
```

浏览器访问 http://localhost 可查看静态页面。

---

## 📖 核心概念

### 1. root 与 alias

- **root**：将 URL 路径附加到根目录后查找文件
- **alias**：将 location 匹配部分替换为指定路径

```nginx
location /static/ {
    root /var/www;          # 实际路径 /var/www/static/file.css
}

location /static/ {
    alias /var/www/static/; # 实际路径 /var/www/static/file.css
}
```

### 2. location 匹配规则

| 修饰符 | 含义 |
|--------|------|
| `=` | 精确匹配 |
| `^~` | 前缀匹配，匹配到后不再检查正则 |
| `~` | 区分大小写的正则匹配 |
| `~*` | 不区分大小写的正则匹配 |
| 无 | 普通前缀匹配 |

### 3. Gzip 压缩

减少文本类资源的传输体积：

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml;
```

### 4. 浏览器缓存

通过 `expires` 和 `Cache-Control` 控制静态资源缓存：

```nginx
location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## 💻 代码示例

### 完整 NGINX 配置

```nginx
# configs/nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # 默认字符编码
    charset utf-8;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        application/json
        application/javascript
        text/xml
        application/xml;

    # 日志
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # 静态资源缓存
    location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # 首页
    location = / {
        try_files $uri $uri/ /index.html;
    }

    # 404 页面
    error_page 404 /404.html;

    # 禁止访问隐藏文件
    location ~ /\\. {
        deny all;
    }
}
```

### 示例 HTML

```html
<!-- html/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>OpenDemo NGINX Web Server</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Hello from NGINX!</h1>
    <p>这是一个由 NGINX 托管的静态网站示例。</p>
</body>
</html>
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `configs/nginx.conf` | NGINX 主配置 |
| `html/index.html` | 网站首页 |
| `html/style.css` | 样式文件 |
| `docker-compose.yml` | 服务编排 |

---

## 🧪 验证测试

```bash
# 访问首页
curl -s http://localhost/

# 检查 Gzip 压缩是否生效
curl -s -H "Accept-Encoding: gzip" -I http://localhost/style.css

# 检查缓存头
curl -s -I http://localhost/style.css

# 查看访问日志
docker exec nginx-web-server tail -n 20 /var/log/nginx/access.log
```

---

## 📊 运行结果

```bash
$ curl -s http://localhost/
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>OpenDemo NGINX Web Server</title>
    ...
</html>
```

---

## 🐛 常见问题

### Q1：静态文件 404？

**A**：检查 `root` 路径和 `location` 匹配是否正确，确认文件已挂载到容器内。

### Q2：Gzip 没有生效？

**A**：确认请求头包含 `Accept-Encoding: gzip`，且文件大小超过 `gzip_min_length`。

### Q3：中文显示乱码？

**A**：在 NGINX 配置中添加 `charset utf-8;`。

---

## 📚 扩展学习

- [NGINX 反向代理](../nginx-reverse-proxy/)
- [NGINX 负载均衡](../nginx-load-balancing/)
- [NGINX 官方文档](https://nginx.org/en/docs/beginners_guide.html)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
