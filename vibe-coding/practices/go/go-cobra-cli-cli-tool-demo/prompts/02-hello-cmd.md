# Prompt 02: 实现 hello 子命令

现在实现 cmd/hello.go：
- Short: "打印问候语"
- Long: "这是一个简单的示例命令，用于展示如何接收用户输入并输出响应"
- 添加 --name/-n flag，默认值 "World"
- Run 函数：fmt.Printf("Hello, %s!\n", name)
- 在 init() 中用 helloCmd.Flags().StringVarP 绑定 flag

---
## 背景
- 工具：Cursor
- 阶段：第 2 轮
- 结果：AI 生成了正确的 hello.go，但用了 PersistentFlags() 而非 Flags()
- 修复：改用 helloCmd.Flags()（Local Flag 而非 Persistent Flag）
