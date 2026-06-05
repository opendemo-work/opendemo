# 多轮对话迭代技巧

## 核心理念：Vibe Coding 不是一次生成，而是持续对话

AI 生成的第一版代码几乎不可能是最终版本。Vibe Coding 的真正技能是**知道如何迭代**。

## 四种迭代策略

### 策略一：骨架 → 填充

**第一轮**：生成整体结构
```
创建一个 Go 项目，包含以下模块：
- cmd/ 目录：CLI 子命令
- internal/service/：业务逻辑
- internal/repository/：数据访问
- main.go：入口

先只生成文件结构和接口定义，不要写实现。
```

**第二轮**：逐个填充
```
现在实现 internal/service/user_service.go，包含 CreateUser 和 GetUser 方法。
使用 internal/repository 包的接口。
```

**适用场景**：从零创建新项目。

### 策略二：需求 → 实现 → 打磨

**第一轮**：粗略实现
```
用 Gin 写一个 REST API，支持用户 CRUD。
```

**第二轮**：补充细节
```
给所有 handler 加上：
- 请求参数验证（字段长度、格式）
- 统一错误响应格式 {"error": "...", "code": 400}
- JWT 认证中间件
```

**第三轮**：边界处理
```
现在处理边界情况：
- 重复用户名返回 409
- 不存在的资源返回 404
- 数据库错误返回 500 并记录日志
```

**适用场景**：功能开发。

### 策略三：测试驱动

**第一轮**：写测试
```
为 Worker Pool 写测试用例：
1. 正常提交和执行任务
2. worker 数量为 0 时报错
3. 优雅关闭时等待进行中的任务
4. context 取消时立即返回
```

**第二轮**：让 AI 通过测试
```
实现 Worker Pool 让上面的测试全部通过。
运行 go test 查看结果。
```

**第三轮**：根据失败修正
```
测试 3 失败了：优雅关闭时直接 return 了，没有等待。
修复：用 WaitGroup 等待所有 worker 完成。
```

**适用场景**：逻辑复杂的模块。

### 策略四：模仿 → 理解 → 创造

**第一轮**：给 AI 一个参考实现
```
这是一个 Python 装饰器的例子：

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper

参考这个模式，实现一个 retry 装饰器：
- 最多重试 3 次
- 指数退避（1s, 2s, 4s）
- 只重试特定的异常类型
```

**适用场景**：学习新技术或模式。

## 迭代中的常见陷阱

### 1. 对话退化
AI 的回答质量随对话轮次下降。**解决方法**：超过 5 轮后，重新开始对话，把当前代码状态作为上下文重新输入。

### 2. 越改越差
每次迭代没有比上一版更好。**解决方法**：每轮迭代前明确"这一轮要改什么"，改完立即验证，不行就回退。

### 3. 迷失方向
AI 开始添加你不需要的功能。**解决方法**：明确说"不要添加额外功能，只修复当前问题"。

## 实战练习

- [Go Cobra CLI](../../practices/go/go-cobra-cli-cli-tool-demo/CHALLENGE.md) — 体验骨架→填充策略
- [Python 异步编程](../../practices/python/async-programming/CHALLENGE.md) — 体验测试驱动策略
- [Go gRPC](../../practices/go/go-grpc-protobuf-go-demo/CHALLENGE.md) — 体验需求→实现→打磨策略
