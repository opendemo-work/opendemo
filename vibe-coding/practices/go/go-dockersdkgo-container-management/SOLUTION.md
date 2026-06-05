# 解决过程：Go Docker SDK 容器管理

## 使用的工具：Claude Code

---

### 第 1 轮：项目初始化 + 客户端创建

**Prompt：**
> 用 Go Docker SDK 创建一个容器生命周期管理工具。go module 名 docker-demo。
>
> 先写 main.go 的框架：
> - 创建 Docker 客户端（client.FromEnv）
> - defer 关闭客户端
> - 打印 "🚀 开始容器管理演示..."

**AI 生成：** 正确的框架代码。

---

### 第 2 轮：容器创建

**Prompt：**
> 添加容器创建逻辑：
> - 使用 nginx:alpine 镜像
> - 容器名 "demo-nginx-container"
> - 暴露 80/tcp 端口
> - 打印 "✅ 成功创建容器：<ID 前 12 位>"

**AI 生成：** 正确使用 `cli.ContainerCreate()`。

**问题：** AI 忘记处理 `ExposedPorts`，只配置了 `Cmd`。

**修复：** "加上 ExposedPorts: map[string]struct{}{'80/tcp': {}}"。

---

### 第 3 轮：启动 → 停止 → 删除

**Prompt：**
> 添加启动、停止、删除的完整流程：
> - 启动后打印 "✅ 容器已启动"
> - 等待 2 秒（time.Sleep）
> - 停止后打印 "✅ 容器已停止"
> - 强制删除后打印 "🗑️ 容器已删除"
> - 最后打印 "🎉 演示完成！"

**AI 生成：** 正确使用 `ContainerStart`、`ContainerStop`、`ContainerRemove`。

---

### 第 4 轮：list_containers.go

**Prompt：**
> 创建 list_containers.go，列出当前运行中的容器：
> - 使用 ContainerList(All: false) 只查运行中
> - 打印 ID（前 8 位）、Image、Command

**问题：** 两个文件都有 `func main()`，不能同时编译。

**修复：** "把 list_containers.go 的 main 改为 ListRunningContainers()，然后在单独目录或者运行时指定：`go run list_containers.go`（不包含 main.go）"。实际方案：保持两个独立 main，运行时分开执行。

---

### 第 5 轮：验证

```bash
# 确保 Docker 在运行
docker info

go run main.go
# 🚀 开始容器管理演示...
# ✅ 成功创建容器：cf8a5b2c3d12
# ✅ 容器已启动
# ✅ 容器已停止
# 🗑️ 容器已删除
# 🎉 演示完成！

go run list_containers.go
# 📦 当前运行中的容器：...
```

**结果：** 全部通过 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 5 轮 |
| 实际用时 | ~20 分钟 |
| AI 犯错次数 | 2（遗漏 ExposedPorts、多 main 冲突） |
| 人工干预 | 补充端口配置、解决编译冲突 |

### 关键技巧
- **Docker SDK API 和 CLI 命令对应** — `ContainerCreate` = `docker create`，`ContainerStart` = `docker start`
- **container.Config vs HostConfig** — Config 是容器内部配置（镜像、命令、环境变量），HostConfig 是主机侧配置（端口映射、卷挂载）
- **+incompatible 标记** — Docker SDK 还没有完全迁移到 Go module，需要特殊处理

### 常见坑
- Docker daemon 未运行 — 所有操作报 "Cannot connect to Docker daemon"
- 多文件多 main — Go 不允许同一个 package 有多个 main 函数
- 容器名称冲突 — 如果上次没有清理，同名的容器已存在会报错
- `ContainerStop` 的第二个参数 — 传 `nil` 使用默认超时
