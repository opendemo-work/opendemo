# 挑战：Go Cobra CLI 工具

## 难度：intermediate | 预计用时：20 分钟 | 推荐工具：Cursor / Claude Code

## 目标

使用 Go + Cobra 库构建一个命令行工具，支持以下子命令：

- `hello` — 打印问候语，支持 `--name` / `-n` 参数指定名字（默认 "World"）
- `version` — 打印版本号和构建时间

## 约束

- 使用 Go 1.19+ 和 Cobra v1.8.0
- 项目结构：`main.go` + `cmd/` 目录（每个子命令一个文件）
- `cmd/` 包中需要 `rootCmd` 作为根命令
- 所有代码注释使用中文

## 项目骨架

```
cobra-demo/
├── main.go          # 入口，调用 cmd.Execute()
├── cmd/
│   ├── root.go      # rootCmd 定义（你需要自己创建）
│   ├── hello.go     # hello 子命令
│   └── version.go   # version 子命令
└── go.mod
```

## 验证

```bash
# 帮助信息
go run main.go
# 应显示可用子命令列表

# hello 命令
go run main.go hello
# 输出：Hello, World!

go run main.go hello --name Alice
# 输出：Hello, Alice!

go run main.go hello -n Bob
# 输出：Hello, Bob!

# version 命令
go run main.go version
# 输出：Version: v1.0.0
#      Build Time: 2023-01-01
```

## 提示（卡住时再看）

<details>
<summary>提示 1：Cobra 命令结构</summary>

每个子命令是一个 `cobra.Command` 结构体，包含 `Use`、`Short`、`Long`、`Run` 字段。在 `init()` 函数中通过 `rootCmd.AddCommand()` 注册。

</details>

<details>
<summary>提示 2：Flag 绑定</summary>

使用 `cmd.Flags().StringVarP(&name, "name", "n", "World", "描述")` 添加带短选项的 flag。

</details>

<details>
<summary>提示 3：关键 Prompt</summary>

"用 Go Cobra 库创建一个 CLI 工具，包含 hello 和 version 两个子命令。hello 命令支持 --name/-n flag 打印问候语，version 命令显示版本号 v1.0.0。项目结构为 main.go + cmd/ 目录。"

</details>

## 对应原 Demo

完成后对比参考实现：`go/go-cobra-cli-cli-tool-demo/`
