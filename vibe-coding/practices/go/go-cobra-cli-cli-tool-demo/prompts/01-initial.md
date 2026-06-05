# Prompt 01: 创建项目骨架

创建一个 Go 项目，使用 Cobra 库构建 CLI 工具。项目结构：
- main.go：调用 cmd.Execute()
- cmd/root.go：定义 rootCmd（无特殊功能，只做子命令容器）
- cmd/hello.go：hello 子命令，支持 --name/-n flag
- cmd/version.go：version 子命令，显示版本号 v1.0.0

先只生成文件结构和 rootCmd，不要写子命令实现。

---
## 背景
- 工具：Cursor（Cmd+K 行内编辑）
- 阶段：第 1 轮
- 结果：骨架正确，rootCmd 描述需改为中文
