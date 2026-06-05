# Prompt 02: 容器列表 + 验证

创建 list_containers.go，列出当前运行中的容器：
- 使用 ContainerList(All: false) 只查运行中
- 打印 ID（前 8 位）、Image、Command

验证：
go run main.go  # 完整生命周期
go run list_containers.go  # 查看运行中容器

---
## 背景
- 工具：Claude Code
- 阶段：第 4-5 轮
- 结果：两个文件都有 func main() 导致编译冲突，需分开运行
