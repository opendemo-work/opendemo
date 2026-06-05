# 挑战：Go Docker SDK 容器管理

## 难度：advanced | 预计用时：35 分钟 | 推荐工具：Claude Code

## 目标

使用 Go Docker SDK 编程管理容器生命周期：

1. 创建一个 nginx:alpine 容器（名称 `demo-nginx-container`）
2. 启动容器
3. 等待 2 秒观察
4. 停止容器
5. 删除容器
6. 额外：实现一个 `list_containers.go` 列出当前运行中的容器

## 约束

- Go 1.19+，Docker SDK v24.0.7
- 必须有 Docker Engine 运行在本地
- 容器暴露 80 端口
- 使用 `client.NewClientWithOpts(client.FromEnv)` 创建客户端
- 所有 `error` 必须处理（不能忽略）
- 代码注释使用中文
- 每个步骤打印 emoji 状态提示（🚀 ✅ 🗑️ 🎉）

## 验证

```bash
# 确保 Docker 正在运行
docker ps

# 运行主程序
go run main.go
# 预期输出：
# 🚀 开始容器管理演示...
# ✅ 成功创建容器：cf8a5b2c3d...
# ✅ 容器已启动
# ✅ 容器已停止
# 🗑️ 容器已删除
# 🎉 演示完成！

# 运行容器列表
go run list_containers.go
# 输出当前运行中的容器 ID、镜像、命令
```

## 提示（卡住时再看）

<details>
<summary>提示 1：容器创建</summary>

使用 `cli.ContainerCreate()`，需要配置 `container.Config`（Image、Cmd、ExposedPorts）。

</details>

<details>
<summary>提示 2：+incompatible 标记</summary>

Docker SDK for Go 使用 `v24.0.7+incompatible`，在 go get 时需要带上这个标记。

</details>

<details>
<summary>提示 3：关键 Prompt</summary>

"用 Go Docker SDK 实现容器生命周期管理：创建 nginx:alpine 容器→启动→等待 2 秒→停止→删除。每步打印中文状态提示。使用 client.FromEnv 创建客户端。"

</details>

## 前置要求

- Docker Desktop 或 Docker Engine 正在运行
- Linux 用户确保当前用户在 `docker` 组中

## 对应原 Demo

完成后对比参考实现：`go/go-dockersdkgo-container-management/`
