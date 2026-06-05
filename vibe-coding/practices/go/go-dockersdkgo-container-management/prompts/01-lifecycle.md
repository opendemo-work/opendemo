# Prompt 01: Docker 客户端 + 容器生命周期

用 Go Docker SDK 实现容器生命周期管理：

先写 main.go 框架：
- 创建 Docker 客户端（client.FromEnv）
- defer 关闭客户端
- 打印 "🚀 开始容器管理演示..."

然后添加完整流程：
- 创建 nginx:alpine 容器（名称 demo-nginx-container，暴露 80 端口）
- 启动容器
- 等待 2 秒
- 停止容器
- 强制删除容器

每步打印 emoji 状态：✅ 成功 🗑️ 删除 🎉 完成

---
## 背景
- 工具：Claude Code
- 阶段：第 1-3 轮
- 结果：AI 忘记处理 ExposedPorts，修复后正确
