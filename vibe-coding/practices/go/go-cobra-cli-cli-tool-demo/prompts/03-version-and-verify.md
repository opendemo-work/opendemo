# Prompt 03: 实现 version 子命令 + 验证

实现 cmd/version.go：
- Short: "打印版本信息"
- 输出 Version: v1.0.0 和 Build Time: 2023-01-01
- 在 init() 中注册到 rootCmd

然后运行验证：
go run main.go hello
go run main.go hello --name Alice
go run main.go version

---
## 背景
- 工具：Cursor
- 阶段：第 3-4 轮
- 结果：全部通过
