# Go多阶段Docker构建演示

## 简介
本示例演示了如何使用Go语言结合Docker多阶段构建技术，创建轻量、安全且高效的容器镜像。通过两个具体场景展示不同用途的构建策略。

## 学习目标
- 理解Docker多阶段构建的优势
- 掌握Go程序的静态编译与容器化
- 学会创建生产就绪的最小化镜像
- 避免敏感信息泄露的最佳实践

## 环境要求
- Go 1.20 或更高版本
- Docker 20.10 或更高版本
- 跨平台支持：Windows、Linux、macOS

## 安装依赖步骤
1. 安装Go：访问 https://golang.org/dl/ 下载对应系统的安装包
2. 安装Docker：访问 https://docs.docker.com/get-docker/ 安装Docker Desktop或引擎
3. 验证安装：
   ```bash
   go version
   docker --version
   ```

## 文件说明
- `main.go` - 主应用程序，提供HTTP服务
- `Dockerfile` - 多阶段构建配置文件
- `go.mod` - Go模块依赖声明

## 逐步实操指南

### 步骤1：克隆或创建项目目录
```bash
mkdir go-docker-demo && cd go-docker-demo
```

### 步骤2：初始化Go模块并创建文件
```bash
# 初始化模块（实际已包含在demo中）
go mod init go-docker-demo
```

### 步骤3：构建Docker镜像
```bash
docker build -t go-docker-demo .
```

**预期输出**：
```
[+] Building 10.5s (14/14) DONE
 => ...
 => => writing image sha256:...  
 => => naming to docker.io/library/go-docker-demo
```

### 步骤4：运行容器
```bash
docker run -p 8080:8080 go-docker-demo
```

### 步骤5：测试服务
在另一个终端执行：
```bash
curl http://localhost:8080/hello
```

**预期输出**：
```
Hello from Go in Docker! Built with multi-stage build.
```

## 代码解析

### main.go 关键点
- 使用标准库`net/http`创建轻量HTTP服务器
- `healthz`用于健康检查，符合云原生规范
- 字符串响应包含构建方式信息，验证多阶段构建成功

### Dockerfile 关键点
1. **构建阶段 (builder)**
   - 使用`golang:alpine`作为构建环境
   - 启用CGO_ENABLED=0确保静态编译
   - 只复制必要文件以利用Docker缓存

2. **运行阶段 (final)**
   - 使用`alpine:latest`极小基础镜像
   - 只拷贝编译后的二进制文件
   - 使用非root用户运行提升安全性
   - 暴露8080端口并设置启动命令

## 预期输出示例
启动容器后，访问：
```bash
$ curl http://localhost:8080/hello
Hello from Go in Docker! Built with multi-stage build.

$ curl http://localhost:8080/healthz
OK
```

容器日志显示：
```
2024/01/01 12:00:00 Starting server on :8080
```

## 常见问题解答

**Q: 为什么使用alpine镜像？**
A: Alpine是超小Linux发行版，基础镜像仅~5MB，能显著减小最终镜像体积。

**Q: CGO_ENABLED=0的作用？**
A: 禁用CGO使Go编译为完全静态二进制，不依赖系统glibc，可在任何Linux系统运行。

**Q: 构建时报权限错误？**
A: 确保Docker服务正在运行，并且当前用户有权限访问Docker daemon。

**Q: 如何减小构建时间？**
A: 利用Docker缓存，将`go mod download`放在单独层，仅在go.mod变更时重新下载依赖。

## 扩展学习建议
- 尝试添加Prometheus指标暴露
- 集成gRPC服务替代HTTP
- 使用BuildKit secrets管理敏感信息
- 添加单元测试并在构建阶段运行
- 探索Distroless镜像进一步减小体积