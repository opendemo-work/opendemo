# 解决过程：Python 异步编程

## 使用的工具：Copilot Chat

---

### 第 1 轮：异步基础 + 协程

**Prompt：**
> 用 Python asyncio 实现两组函数：
> 1. demo_async_basics() — 定义 async def say_hello(name, delay)，先顺序 await 两次（0.2s + 0.1s），再 gather 并发。打印耗时对比。
> 2. demo_coroutine() — 演示直接 await 和 create_task 的区别

**AI 生成：** 正确。耗时对比清晰展示了并发优势。

---

### 第 2 轮：gather vs wait + 超时

**Prompt：**
> 添加两个函数：
> 1. demo_gather_and_wait() — 用 gather 并发 3 个任务，用 wait 加 timeout=0.12 演示部分完成
> 2. demo_timeout() — wait_for 超时控制，asyncio.timeout 上下文管理器（3.11+）

**AI 生成：** 正确。`asyncio.wait` 的 `done, pending` 返回值处理正确。

**问题：** `asyncio.timeout` 在 Python 3.10 下不存在。

**修复：** "在 demo_timeout 中把 asyncio.timeout 部分注释说明需要 3.11+，或用 try/except AttributeError 包裹"。

---

### 第 3 轮：信号量 + 队列 + 异常处理

**Prompt：**
> 添加三个函数：
> 1. demo_semaphore() — Semaphore(2) 限制并发，4 个任务竞争，打印开始/完成
> 2. demo_queue() — asyncio.Queue 生产者-消费者，生产 5 个数字
> 3. demo_exception_handling() — gather(return_exceptions=True) 处理部分任务失败

**AI 生成：** 基本正确。

**问题：** 队列的消费者没有正确的退出条件，会无限等待。

**修复：** "消费者收到 item >= 4 时 break 退出循环，因为生产者最多生产 0-4"。

---

### 第 4 轮：验证

```bash
python code/async_programming.py
```

**结果：** 全部 7 个 demo 输出正确 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 4 轮 |
| 实际用时 | ~18 分钟 |
| AI 犯错次数 | 2（Python 版本兼容、消费者退出条件） |
| 人工干预 | 版本注释、退出条件 |

### 关键技巧
- **asyncio.gather vs asyncio.wait** — gather 简单但不够灵活，wait 支持超时和 FIRST_COMPLETED
- **return_exceptions=True** — 默认情况下 gather 中一个异常会取消所有任务，设置后异常作为结果返回
- **Semaphore 控制并发** — 比手动管理 worker 数量更优雅

### 常见坑
- `asyncio.run()` 只能调用一次 — 不能在已有事件循环中嵌套调用
- `asyncio.timeout` 是 3.11+ 新增 — 低版本用 `asyncio.wait_for`
- Queue 消费者需要退出条件 — 否则会永远阻塞在 `queue.get()`
- `create_task` 后必须 await — 否则任务被创建但从未等待完成
