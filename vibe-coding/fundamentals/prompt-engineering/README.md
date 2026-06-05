# Prompt Engineering for Vibe Coding

## 核心原则：Context > Instruction

AI 编码工具的效果 80% 取决于你给的上下文，20% 取决于指令本身。

## 五种高效 Prompt 模式

### 1. 示例驱动（最有效）

```
创建一个 Go HTTP handler，风格参考下面这个：

func GetUserHandler(c *gin.Context) {
    id := c.Param("id")
    user, err := userService.FindByID(id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
        return
    }
    c.JSON(http.StatusOK, user)
}

需求：创建一个 CreateItemHandler，接收 JSON body，验证字段，返回 201
```

**为什么有效**：AI 不需要猜你的代码风格，直接模仿。

### 2. 约束优先

```
用 Python 实现一个 LRU 缓存，约束条件：
- 不使用任何第三方库
- 只用 dict + 双向链表
- 支持 get(key) 和 put(key, value) 两个操作
- 容量满了时淘汰最近最少使用的
- 时间复杂度 O(1)
```

**为什么有效**：约束越具体，AI 不会"自由发挥"到奇怪的方向。

### 3. 分步拆解

```
我要构建一个 CLI 工具，分步实现：

第一步：创建项目骨架
- go mod init task-cli
- 用 Cobra 创建根命令和三个子命令：add, list, done

第二步：数据持久化
- 用 JSON 文件存储任务列表
- 实现 Task struct 和 CRUD 操作

第三步：用户交互
- add 命令接收任务描述
- list 命令格式化输出表格
- done 命令标记完成

现在先做第一步。
```

**为什么有效**：避免 AI 一次生成几百行代码然后你花更多时间调试。

### 4. 错误描述法（调试时用）

```
运行 go test 报错：

    === RUN   TestHandler
    panic: runtime error: invalid memory address or nil pointer dereference
    goroutine 6 [running]:
    main.TestHandler(0xc000082000)

Handler 代码：
[paste code]

测试代码：
[paste test]

分析原因并修复。注意不要改变测试的断言。
```

**为什么有效**：给 AI 完整的错误信息 + 上下文代码，比说"帮我修 bug"有效 10 倍。

### 5. 角色设定

```
你是一个 Go 并发编程专家。我要实现一个 worker pool：
[需求描述]

请给出生产级实现，包括：
- 优雅关闭
- 错误传播
- 可配置的 worker 数量
- 单元测试
```

## 常见反面模式

### ❌ 模糊指令
```
写一个 web 服务器
```
→ AI 会生成一个你可能完全用不上的模板代码。

### ❌ 过度指令
```
写一个函数，变量名叫 handleRequest，参数用 c *gin.Context，
先获取 id，然后调 userService.FindByID，然后判断 err，
如果 err 不等于 nil 返回 404，否则返回 200 和 user 对象
```
→ 你已经在脑中写完了代码，AI 只是打字工具。不如直接写。

### ❌ 无上下文
```
帮我修这个 bug
```
→ AI 需要知道：什么代码、什么错误、你期望什么行为。

## 实战练习

用上面学到的模式完成以下挑战：
- [Go Cobra CLI](../../practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md) — 练习分步拆解模式
- [Python FastAPI](../../practices/python/fastapi-complete-tutorial/CHALLENGE.md) — 练习示例驱动模式
- [Node.js 熔断器](../../practices/nodejs/nodejs-circuit-breaker-demo/CHALLENGE.md) — 练习约束优先模式
