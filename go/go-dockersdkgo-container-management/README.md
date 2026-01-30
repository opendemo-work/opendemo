# Docker SDK 容器操作管理 Go 示例

## 简介
本项目演示如何使用 Go 语言结合 Docker SDK（官方客户端）对本地 Docker 引擎进行编程化容器管理，包括创建、启动、停止和删除容器。适合 DevOps 工具开发、自动化部署系统学习。

## 学习目标
- 掌握 Go 中调用 Docker Engine API 的基本方法
- 理解容器生命周期管理的编程模型
- 学会使用官方 Docker SDK for Go 进行资源操作
- 提升对容器化基础设施自动化的理解

## 环境要求
- Go 1.19 或更高版本
- Docker Engine 正在运行（本地或可通过 Unix socket 访问）
- 操作系统：Windows / Linux / macOS（支持 Docker Desktop）

## 安装依赖步骤

1. 安装 Go（若未安装）
   ```bash
   # 建议从官网 https://golang.org/dl/ 下载安装
   go version  # 验证安装
   ```

2. 初始化 Go 模块
   ```bash
   mkdir docker-demo && cd docker-demo
   go mod init docker-demo
   ```

3. 添加 Docker SDK 依赖
   ```bash
   go get github.com/docker/docker@v24.0.7+incompatible
   ```

## 文件说明
- `main.go`：主程序，展示容器的创建、启动、查看状态、停止与删除
- `list_containers.go`：列出当前所有正在运行的容器
- `go.mod`：Go 模块依赖声明文件

## 逐步实操指南

### 步骤 1：创建并编辑 main.go
```bash
cat > main.go <<EOF
[将下方 main.go 内容粘贴至此]
EOF
```

### 步骤 2：创建 list_containers.go
```bash
cat > list_containers.go <<EOF
[将下方 list_containers.go 内容粘贴至此]
EOF
```

### 步骤 3：运行程序
```bash
go run main.go
```

#### 预期输出（部分示例）：
```
✅ 成功创建容器：cf8a5b2c3d...
✅ 容器已启动
📊 容器 stats 流已开启（5秒后继续）...
✅ 容器已停止
🗑️ 容器已删除
```

### 步骤 4：查看运行中的容器（可选）
```bash
go run list_containers.go
```

预期输出：
```
📦 当前运行中的容器：
- ID: a1b2c3d4, Image: nginx, Command: nginx -g 'daemon off;'
```

## 代码解析

### main.go 关键段解释
- `client.NewClientWithOpts(client.FromEnv)`：从环境变量（如 DOCKER_HOST）创建客户端，默认连接本地 Docker daemon
- `client.ContainerCreate()`：定义并创建容器，指定镜像、命令、网络等配置
- `client.ContainerStart()`：异步启动容器
- `client.ContainerWait()`：阻塞等待容器退出，可用于监控生命周期
- `client.ContainerRemove()`：删除容器，`RemoveOptions` 可强制删除

### list_containers.go
使用 `client.ContainerList()` 获取所有运行中容器，并打印基础信息，展示资源查询能力。

## 预期输出示例
```
🚀 开始容器管理演示...
✅ 成功创建容器：ab7c8d9e0f12
✅ 容器已启动
📊 正在获取容器实时数据流...
✅ 容器已停止
🗑️ 容器已删除
🎉 演示完成！
```

## 常见问题解答

**Q: 报错 `Cannot connect to the Docker daemon`？**
A: 请确保 Docker Desktop 或 dockerd 正在运行。Linux 用户可尝试 `sudo systemctl start docker`。

**Q: Windows 上权限错误？**
A: 确保你的用户属于 `docker-users` 组，或以管理员身份运行终端。

**Q: 如何连接远程 Docker？**
A: 设置 `DOCKER_HOST=tcp://<ip>:2375` 环境变量（需远程 Docker 启用 TCP 接口）。

**Q: 为什么使用 v24.0.7+incompatible？**
A: Docker SDK for Go 尚未完全模块化，需使用 +incompatible 标志兼容旧版本。

## 扩展学习建议
- 使用 `ContainerExecAttach` 在运行容器中执行命令
- 监听 Docker 事件流（Events API）
- 构建镜像并通过 API 推送
- 结合 Cobra 实现 CLI 工具
- 集成到 CI/CD 系统中实现部署自动化