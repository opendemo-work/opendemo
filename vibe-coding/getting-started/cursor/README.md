# Cursor IDE 快速上手

## 什么是 Cursor

Cursor 是基于 VS Code 的 AI-first 编辑器，内置代码补全、多文件编辑、代码库对话等功能。适合 Vibe Coding 的主力工具。

## 安装

1. 下载：https://cursor.com
2. 安装后登录（支持 GitHub / Google）
3. 首次打开会提示导入 VS Code 扩展和设置

## 核心 Vibe Coding 功能

### Cmd+K：行内编辑
选中代码，按 `Cmd+K`（Mac）或 `Ctrl+K`（Windows），用自然语言描述要做的修改：
```
把这个函数改成支持并发，用 goroutine 实现
```

### Cmd+L：代码对话
按 `Cmd+L` 打开聊天面板，可以针对选中代码提问：
```
这段代码有什么潜在的性能问题？
```

### @引用：上下文注入
在对话中使用 `@` 引用不同上下文：
- `@Files` — 引用项目中的文件
- `@Codebase` — 让 AI 搜索整个代码库
- `@Web` — 联网搜索最新文档
- `@Docs` — 引用已索引的官方文档

### Composer（Cmd+I）：多文件编辑
最强大的功能——一次 prompt 修改多个文件：
```
给这个项目添加用户认证功能：
1. 在 main.py 中添加 JWT 中间件
2. 创建 auth.py 模块
3. 更新 requirements.txt 添加依赖
```

## Vibe Coding 最佳实践

1. **先写需求，再让 AI 实现** — 用注释或 markdown 描述你要什么，再让 Cursor 填充代码
2. **小步迭代** — 不要一次让 AI 写 500 行，拆成 3-4 步逐步构建
3. **用 @Codebase 让 AI 理解项目** — 新文件时先 `@Codebase` 让 AI 了解已有代码风格
4. **Review 每次 AI 改动** — Cursor 的 diff 视图很清晰，别盲目接受

## 配置建议

在 `.cursorrules` 文件中写入项目约定：
```
本项目使用中文注释，英文变量名
Go 代码使用 gofmt 格式化
测试文件放在 tests/ 目录
```

## 对应 OpenDemo 练习

- 入门：[Go Cobra CLI](../practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md)
- 进阶：[Node.js 闭包](../practices/nodejs/nodejs-closures-demo/CHALLENGE.md)
- 高级：[Go gRPC](../practices/go/go-grpc-protobuf-go-demo/CHALLENGE.md)
