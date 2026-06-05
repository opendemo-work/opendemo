# 解决过程：Go Cobra CLI 工具

## 使用的工具：Cursor（Cmd+K 行内编辑）

---

### 第 1 轮：创建项目骨架

**Prompt：**
> 创建一个 Go 项目，使用 Cobra 库构建 CLI 工具。项目结构：
> - main.go：调用 cmd.Execute()
> - cmd/root.go：定义 rootCmd（无特殊功能，只做子命令容器）
> - cmd/hello.go：hello 子命令，支持 --name/-n flag
> - cmd/version.go：version 子命令，显示版本号 v1.0.0
>
> 先只生成文件结构和 rootCmd，不要写子命令实现。

**AI 生成：** main.go + cmd/root.go，go.mod 已初始化。

**评价：** 骨架正确，但 rootCmd 的 Short/Long 描述是英文。需要补充中文。

---

### 第 2 轮：实现 hello 子命令

**Prompt：**
> 现在实现 cmd/hello.go：
> - Short: "打印问候语"
> - Long: "这是一个简单的示例命令，用于展示如何接收用户输入并输出响应"
> - 添加 --name/-n flag，默认值 "World"
> - Run 函数：fmt.Printf("Hello, %s!\n", name)
> - 在 init() 中用 helloCmd.Flags().StringVarP 绑定 flag

**AI 生成：** 完整的 hello.go，逻辑正确。

**问题：** AI 生成的 flag 绑定用了 `PersistentFlags()` 而不是 `Flags()`。Local flag 应该用 `Flags()`。

**修复：** 指出 "改用 helloCmd.Flags() 而不是 helloCmd.PersistentFlags()，因为这是 hello 命令专属的 flag"。

**学习点：** PersistentFlags 会被子命令继承，Local Flags 只在当前命令可用。对于 hello 的 --name，应该用 Local。

---

### 第 3 轮：实现 version 子命令

**Prompt：**
> 实现 cmd/version.go：
> - Short: "打印版本信息"
> - 输出 Version: v1.0.0 和 Build Time: 2023-01-01
> - 在 init() 中注册到 rootCmd

**AI 生成：** 正确实现。

---

### 第 4 轮：验证

**Prompt：**
> 运行以下命令验证：
> go run main.go hello
> go run main.go hello --name Alice
> go run main.go version

**结果：** 全部通过 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 4 轮 |
| 实际用时 | ~12 分钟 |
| AI 犯错次数 | 1（PersistentFlags vs Flags） |
| 人工干预 | 提醒 flag 类型 |

### 关键技巧
- **先骨架后填充** — 分步生成比一次生成全部代码质量更高
- **了解 Cobra 的 flag 类型** — Persistent vs Local 是常见坑
- **验证每一步** — 每写完一个子命令就运行验证

### 常见坑
- `init()` 函数不能忘记写，否则子命令不会注册
- `StringVarP` 的参数顺序：`&变量, "长选项", "短选项", 默认值, "描述"`
- rootCmd 不能和 main package 同名，否则 import 会冲突
