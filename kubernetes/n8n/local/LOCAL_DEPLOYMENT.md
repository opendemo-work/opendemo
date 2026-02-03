# n8n 本地部署指南

本文档详细介绍如何在 Windows 和 Mac 笔记本上本地部署 n8n 自动化工作流平台，帮助你在个人电脑上快速体验和调试 n8n 工作流。

## 你将学到什么

- **环境准备**：如何在 Windows 与 macOS 上安装 Docker / Node.js，并验证基础运行环境
- **多种部署方式**：掌握 Docker 单容器、Docker Compose、npm 全局安装、Homebrew 安装等多种本地部署路径
- **数据持久化与数据库选择**：理解 SQLite 与 PostgreSQL 的差异及典型配置方式
- **常见问题排查**：学会解决端口占用、容器无法启动、数据丢失、时区与资源不足等实际问题

## 适用场景

- **个人学习 / 试用 n8n**：希望在本机快速启动一个实例，体验工作流编排与运行
- **本地开发与调试**：需要在本地构建和调试工作流，再迁移到 Kubernetes 或其他生产环境
- **培训与演示环境**：在课堂、分享或内部培训中，给学员快速提供可操作的 n8n 环境

## 目录

- [部署方式对比](#部署方式对比)
- [Windows 本地部署](#windows-本地部署)
  - [方式一：Docker 部署（推荐）](#方式一docker-部署推荐)
  - [方式二：npm 直接安装](#方式二npm-直接安装)
- [Mac 本地部署](#mac-本地部署)
  - [方式一：Docker 部署（推荐）](#方式一docker-部署推荐-1)
  - [方式二：npm 直接安装](#方式二npm-直接安装-1)
  - [方式三：Homebrew 安装](#方式三homebrew-安装)
- [数据持久化配置](#数据持久化配置)
- [常见问题排查](#常见问题排查)
- [n8n 工作流案例](#n8n-工作流案例)

---

## 部署方式对比

| 部署方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| Docker | 环境隔离、一键部署、易于升级 | 需要安装 Docker | 推荐方式 |
| npm | 轻量级、直接访问系统资源 | 需要 Node.js 环境 | 开发调试 |
| Homebrew (Mac) | Mac 原生包管理 | 仅限 Mac | Mac 用户 |

---

## Windows 本地部署

### 方式一：Docker 部署（推荐）

#### 前置条件

1. **安装 Docker Desktop**
   - 下载地址：https://www.docker.com/products/docker-desktop/
   - 安装后启动 Docker Desktop
   - 确保 Docker 正常运行：
   ```powershell
   docker --version
   ```

#### 快速启动

```powershell
# 创建数据目录
mkdir C:\n8n-data

# 使用 Docker 启动 n8n
docker run -d --name n8n `
  -p 5678:5678 `
  -v C:\n8n-data:/home/node/.n8n `
  -e GENERIC_TIMEZONE="Asia/Shanghai" `
  -e TZ="Asia/Shanghai" `
  n8nio/n8n
```

#### 使用 Docker Compose（推荐生产环境）

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - GENERIC_TIMEZONE=Asia/Shanghai
      - TZ=Asia/Shanghai
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - N8N_SECURE_COOKIE=false
      - N8N_ENCRYPTION_KEY=your-secret-key-here
      - DB_TYPE=sqlite
      - DB_SQLITE_DATABASE=/home/node/.n8n/database.sqlite
    volumes:
      - n8n_data:/home/node/.n8n

  # 可选：使用 PostgreSQL 作为数据库（生产环境推荐）
  # postgres:
  #   image: postgres:15-alpine
  #   container_name: n8n-postgres
  #   restart: unless-stopped
  #   environment:
  #     - POSTGRES_USER=n8n
  #     - POSTGRES_PASSWORD=n8n_password
  #     - POSTGRES_DB=n8n
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  # postgres_data:
```

启动服务：

```powershell
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f n8n

# 停止
docker-compose down
```

#### 访问 n8n

打开浏览器访问：http://localhost:5678

首次访问需要创建管理员账户。

---

### 方式二：npm 直接安装

#### 前置条件

1. **安装 Node.js**
   - 下载地址：https://nodejs.org/
   - 推荐版本：Node.js 18 LTS 或更高版本
   - 验证安装：
   ```powershell
   node --version
   npm --version
   ```

#### 安装 n8n

```powershell
# 全局安装 n8n
npm install -g n8n

# 验证安装
n8n --version
```

#### 启动 n8n

```powershell
# 基础启动
n8n

# 指定端口启动
n8n --port 5678

# 后台启动（使用 PM2）
npm install -g pm2
pm2 start n8n
pm2 save
pm2 startup
```

#### 设置环境变量（可选）

创建启动脚本 `start-n8n.bat`：

```batch
@echo off
set N8N_HOST=localhost
set N8N_PORT=5678
set N8N_PROTOCOL=http
set GENERIC_TIMEZONE=Asia/Shanghai
set TZ=Asia/Shanghai
set N8N_ENCRYPTION_KEY=your-secret-key-here

n8n start
```

---

## Mac 本地部署

### 方式一：Docker 部署（推荐）

#### 前置条件

1. **安装 Docker Desktop for Mac**
   - 下载地址：https://www.docker.com/products/docker-desktop/
   - 安装后启动 Docker Desktop
   - 验证安装：
   ```bash
   docker --version
   ```

#### 快速启动

```bash
# 创建数据目录
mkdir -p ~/.n8n

# 使用 Docker 启动 n8n
docker run -d --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e GENERIC_TIMEZONE="Asia/Shanghai" \
  -e TZ="Asia/Shanghai" \
  n8nio/n8n
```

#### 使用 Docker Compose（推荐生产环境）

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - GENERIC_TIMEZONE=Asia/Shanghai
      - TZ=Asia/Shanghai
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - N8N_SECURE_COOKIE=false
      - N8N_ENCRYPTION_KEY=your-secret-key-here
      - DB_TYPE=sqlite
      - DB_SQLITE_DATABASE=/home/node/.n8n/database.sqlite
    volumes:
      - n8n_data:/home/node/.n8n

  # 可选：使用 PostgreSQL 作为数据库（生产环境推荐）
  # postgres:
  #   image: postgres:15-alpine
  #   container_name: n8n-postgres
  #   restart: unless-stopped
  #   environment:
  #     - POSTGRES_USER=n8n
  #     - POSTGRES_PASSWORD=n8n_password
  #     - POSTGRES_DB=n8n
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  # postgres_data:
```

启动服务：

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f n8n

# 停止
docker-compose down
```

---

### 方式二：npm 直接安装

#### 前置条件

1. **安装 Node.js**
   - 使用 Homebrew：
   ```bash
   brew install node
   ```
   - 或下载安装包：https://nodejs.org/
   - 验证安装：
   ```bash
   node --version
   npm --version
   ```

#### 安装 n8n

```bash
# 全局安装 n8n
npm install -g n8n

# 验证安装
n8n --version
```

#### 启动 n8n

```bash
# 基础启动
n8n

# 指定端口启动
n8n --port 5678

# 后台启动（使用 PM2）
npm install -g pm2
pm2 start n8n
pm2 save
pm2 startup
```

#### 设置环境变量（可选）

创建启动脚本 `start-n8n.sh`：

```bash
#!/bin/bash
export N8N_HOST=localhost
export N8N_PORT=5678
export N8N_PROTOCOL=http
export GENERIC_TIMEZONE=Asia/Shanghai
export TZ=Asia/Shanghai
export N8N_ENCRYPTION_KEY=your-secret-key-here

n8n start
```

赋予执行权限：

```bash
chmod +x start-n8n.sh
./start-n8n.sh
```

---

### 方式三：Homebrew 安装

```bash
# 添加 n8n tap
brew tap n8n-io/homebrew-n8n

# 安装 n8n
brew install n8n

# 启动 n8n
n8n

# 或作为服务启动
brew services start n8n
```

---

## 数据持久化配置

### SQLite（默认，适用于单机）

无需额外配置，数据默认存储在 `~/.n8n/database.sqlite`。

### PostgreSQL（推荐生产环境）

完整的 Docker Compose 配置：

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: n8n-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=n8n_secure_password
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n"]
      interval: 10s
      timeout: 5s
      retries: 5

  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - GENERIC_TIMEZONE=Asia/Shanghai
      - TZ=Asia/Shanghai
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - N8N_SECURE_COOKIE=false
      - N8N_ENCRYPTION_KEY=your-32-char-secret-key-here!
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n_secure_password
      - DB_POSTGRESDB_DATABASE=n8n
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
  n8n_data:
```

---

## 常见问题排查

### 1. 端口被占用

**问题**：启动时提示端口 5678 已被占用

**解决方案**：

Windows:
```powershell
# 查看端口占用
netstat -ano | findstr :5678

# 终止进程（替换 PID）
taskkill /PID <PID> /F
```

Mac:
```bash
# 查看端口占用
lsof -i :5678

# 终止进程
kill -9 <PID>
```

### 2. Docker 容器无法启动

**问题**：Docker 容器启动失败

**解决方案**：

```bash
# 查看容器日志
docker logs n8n

# 删除并重新创建容器
docker rm -f n8n
docker run -d --name n8n ...
```

### 3. 数据丢失

**问题**：重启后工作流丢失

**解决方案**：确保挂载了数据卷

```bash
# 检查挂载
docker inspect n8n | grep -A 10 Mounts
```

### 4. 时区问题

**问题**：工作流执行时间不正确

**解决方案**：设置时区环境变量

```yaml
environment:
  - GENERIC_TIMEZONE=Asia/Shanghai
  - TZ=Asia/Shanghai
```

### 5. 内存不足

**问题**：n8n 运行缓慢或崩溃

**解决方案**：增加 Docker 内存限制

```yaml
services:
  n8n:
    ...
    deploy:
      resources:
        limits:
          memory: 2G
```

### 6. 无法访问外部服务

**问题**：工作流无法连接外部 API

**解决方案**：

- 检查网络连接
- 确保 Docker 网络配置正确
- 检查防火墙设置

---

## n8n 工作流案例

### 案例 1：定时发送邮件提醒

**场景**：每天早上 9 点发送工作提醒邮件

**工作流配置**：

1. **触发节点**：Schedule Trigger
   - 设置：每天 09:00 执行

2. **邮件节点**：Send Email
   - 配置 SMTP 服务器
   - 设置收件人、主题、内容

```json
{
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "minutesInterval": 60
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [250, 300]
    },
    {
      "parameters": {
        "fromEmail": "noreply@example.com",
        "toEmail": "user@example.com",
        "subject": "Daily Work Reminder",
        "text": "Good morning! Here's your daily work reminder."
      },
      "name": "Send Email",
      "type": "n8n-nodes-base.emailSend",
      "position": [450, 300]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{ "node": "Send Email", "type": "main", "index": 0 }]]
    }
  }
}
```

---

### 案例 2：Webhook 接收数据并存储

**场景**：接收外部系统的 Webhook 数据并保存到数据库

**工作流配置**：

1. **触发节点**：Webhook
   - 路径：`/api/webhook`
   - 方法：POST

2. **处理节点**：Function
   - 数据转换和验证

3. **存储节点**：HTTP Request / Database
   - 保存数据

```json
{
  "nodes": [
    {
      "parameters": {
        "path": "webhook-data",
        "httpMethod": "POST"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "functionCode": "return items.map(item => ({ json: { ...item.json, processedAt: new Date().toISOString() } }));"
      },
      "name": "Process Data",
      "type": "n8n-nodes-base.function",
      "position": [450, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Process Data", "type": "main", "index": 0 }]]
    }
  }
}
```

---

### 案例 3：监控 GitHub 仓库并通知

**场景**：监控 GitHub 仓库的新 Issue 并发送 Slack 通知

**工作流配置**：

1. **触发节点**：GitHub Trigger
   - 事件：Issue 创建

2. **通知节点**：Slack
   - 发送消息到指定频道

---

### 案例 4：自动化数据同步

**场景**：定时从 API 获取数据并同步到数据库

**工作流配置**：

1. **触发节点**：Schedule Trigger
   - 每小时执行一次

2. **数据获取**：HTTP Request
   - GET 请求获取数据

3. **数据处理**：Function
   - 数据转换

4. **数据存储**：Database
   - 批量插入或更新

---

### 案例 5：表单数据处理

**场景**：处理网站表单提交，发送确认邮件并记录到 Google Sheets

**工作流配置**：

1. **触发节点**：Webhook
   - 接收表单数据

2. **邮件节点**：Send Email
   - 发送确认邮件

3. **存储节点**：Google Sheets
   - 记录表单数据

---

## 高级配置

### 启用 HTTPS

使用 Nginx 反向代理启用 HTTPS：

```nginx
server {
    listen 443 ssl;
    server_name n8n.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 启用身份验证

```yaml
environment:
  - N8N_BASIC_AUTH_ACTIVE=true
  - N8N_BASIC_AUTH_USER=admin
  - N8N_BASIC_AUTH_PASSWORD=secure_password
```

### 限制执行超时

```yaml
environment:
  - EXECUTIONS_TIMEOUT=3600
  - EXECUTIONS_TIMEOUT_MAX=7200
```

### 配置邮件服务

```yaml
environment:
  - N8N_EMAIL_MODE=smtp
  - N8N_SMTP_HOST=smtp.gmail.com
  - N8N_SMTP_PORT=587
  - N8N_SMTP_USER=your-email@gmail.com
  - N8N_SMTP_PASS=your-app-password
  - N8N_SMTP_SENDER=noreply@yourdomain.com
```

---

## 相关资源

- [n8n 官方文档](https://docs.n8n.io/)
- [n8n GitHub 仓库](https://github.com/n8n-io/n8n)
- [n8n 社区论坛](https://community.n8n.io/)
- [n8n 工作流模板](https://n8n.io/workflows/)
- [Docker Hub - n8n](https://hub.docker.com/r/n8nio/n8n)

---

## 版本信息

- 文档版本：1.0.0
- 更新日期：2026-01-22
- 支持 n8n 版本：1.0+
- 支持平台：Windows 10/11, macOS 12+
