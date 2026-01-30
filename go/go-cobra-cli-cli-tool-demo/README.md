# Cobra CLI 工具开发演示

本项目是一个使用 Go 语言和 Cobra 库构建命令行工具的完整示例。通过这个 Demo，你将学习如何创建结构清晰、可扩展的 CLI 应用。

## 学习目标

- 理解 Cobra 的基本架构（Command 和 Args）
- 掌握子命令的定义与注册方式
- 学会使用 Persistent 和 Local Flags
- 实践 Go CLI 项目的标准目录结构

## 环境要求

- Go 1.19 或更高版本
- 操作系统：Windows、Linux、macOS（均支持）
- 终端工具（如 bash、zsh、PowerShell）

## 安装依赖的详细步骤

1. 确保已安装 Go：
   ```bash
   go version
   # 预期输出：go version go1.19.x linux/amd64 （或对应平台）
   ```

2. 初始化 Go 模块并添加 Cobra 依赖：
   ```bash
   go mod init cobra-demo
   go get github.com/spf13/cobra@v1.8.0
   ```

## 文件说明

- `main.go`：程序入口，初始化根命令
- `cmd/hello.go`：实现 `hello` 子命令
- `cmd/version.go`：实现 `version` 子命令，展示版本信息

## 逐步实操指南

### 步骤 1：创建项目结构

```bash
mkdir -p cobra-demo/cmd
cd cobra-demo
```

### 步骤 2：复制代码文件

将 `main.go`、`cmd/hello.go`、`cmd/version.go` 复制到对应路径。

### 步骤 3：运行程序

```bash
go run main.go
# 输出帮助信息
```

### 步骤 4：尝试子命令

```bash
# 运行 hello 命令
go run main.go hello
# 预期输出：Hello, World!

# 使用 --name 参数
go run main.go hello --name Alice
# 预期输出：Hello, Alice!

# 查看版本
go run main.go version
# 预期输出：Version: v1.0.0\nBuild Time: 2023-01-01\n```

## 代码解析

### main.go

- 导入 `cobra/cmd` 包并调用 `Execute()` 启动 CLI
- 是标准的 Cobra 项目入口点

### cmd/hello.go

- 定义 `helloCmd` 命令对象，设置 `Run` 函数处理逻辑
- 使用 `StringVarP` 添加本地标志 `--name`，支持短选项 `-n`
- 展示如何从命令上下文中读取用户输入

### cmd/version.go

- 展示静态数据输出命令
- 版本信息可通过编译时注入（如 ldflags），此处为简化硬编码

## 预期输出示例

```bash
$ go run main.go hello --name Bob
Hello, Bob!

$ go run main.go version
Version: v1.0.0
Build Time: 2023-01-01
```

## 常见问题解答

**Q: 运行时报错 `cannot find package "github.com/spf13/cobra"`？**
A: 请确认是否执行了 `go get github.com/spf13/cobra`，并检查 `go.mod` 是否包含该依赖。

**Q: 如何添加新的子命令？**
A: 在 `cmd/` 目录下新建 `.go` 文件，定义 `*cobra.Command` 并在 `init()` 中通过 `rootCmd.AddCommand()` 注册。

**Q: 如何跨平台编译？**
A: 使用 `GOOS=windows GOARCH=amd64 go build` 等命令交叉编译。

## 扩展学习建议

- 学习使用 Viper 集成配置文件支持
- 尝试 Cobra 生成器 `cobra-cli init` 自动生成项目骨架
- 添加单元测试覆盖命令逻辑
- 实现命令自动补全功能（bash/zsh）
