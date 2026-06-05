# 用 AI 做代码审查

## 核心理念：AI 是不知疲倦的 Reviewer

AI Code Review 的优势：
- 不会因为累了就跳过审查
- 不受人际关系影响，直接指出问题
- 可以瞬间审查整个 PR 的上下文

## 三种 AI Review 模式

### 模式一：增量审查（PR Review）

```
审查以下 PR 变更，重点关注：
1. 安全问题（SQL 注入、XSS、敏感信息泄露）
2. 并发安全（数据竞争、死锁风险）
3. 错误处理（遗漏的 error check、吞错误）
4. 性能问题（N+1 查询、不必要的内存分配）

变更内容：
[git diff 输出]

相关上下文：
[被修改文件的其他部分]
```

### 模式二：全量审查（新代码）

```
审查以下完整模块，按以下维度打分（1-5）并给出具体建议：

1. 代码可读性
2. 函数职责划分
3. 错误处理完整性
4. 测试覆盖率预估
5. 潜在 Bug

代码：
[paste]
```

### 模式三：特定关注点审查

```
这段代码将用于生产环境，请重点审查：

1. 所有外部输入是否做了验证？
2. 所有错误是否正确传播？没有吞错误？
3. 资源（连接、文件句柄）是否正确释放？
4. 日志是否包含足够的调试信息？
5. 是否有硬编码的配置（端口、密码、URL）？

代码：
[paste]
```

## AI Review 的 Prompt 技巧

### 指定严重程度
```
按严重程度分类反馈：
- 🔴 必须修复：会导致 bug 或安全问题
- 🟡 建议修改：影响可维护性或性能
- 🟢 可选优化：代码风格改进
```

### 限定范围
```
只审查错误处理相关的代码，不要评论代码风格和命名。
```

### 要求给出修复建议
```
每个问题必须附带修复建议，给出修改后的代码片段。
不要只说"这里有问题"，要说"改成这样："。
```

## 用 Cursor/Claude Code 做 Review 的快捷方式

### Cursor
选中代码 → `Cmd+L` → 输入 `/review`

### Claude Code
```
> 审查最近一次 git commit 的变更，指出潜在问题
```

### GitHub Copilot
在 PR 页面使用 Copilot Review 功能，自动审查所有变更。

## 常见被忽略的问题（让 AI 重点检查）

1. **`defer` 在循环中使用**（Go）— defer 在函数退出时执行，不是循环结束时
2. **goroutine 泄漏** — 启动的 goroutine 永远不会退出
3. **context 传播缺失** — 创建了 context 但没有传递给下游
4. **错误被覆盖** — `err = doB()` 覆盖了之前 `err = doA()` 的错误
5. **map 并发读写** — 多个 goroutine 同时操作 map 没有 sync
6. **time.After 在 select 中泄漏** — 每次 case 都创建新 timer

## 实战练习

完成以下挑战后，用 AI Review 自己写的代码：
- [Node.js 闭包](../../practices/nodejs/nodejs-closures-demo/CHALLENGE.md)
- [Go Gin Web](../../practices/go/go-ginwebdemo-web-framework-intro/CHALLENGE.md)
- [Python 异步编程](../../practices/python/async-programming/CHALLENGE.md)
