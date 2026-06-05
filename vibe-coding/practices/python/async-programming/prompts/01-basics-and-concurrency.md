# Prompt 01: 异步基础 + 协程 + 并发控制

用 Python asyncio 实现三组函数：

demo_async_basics()：
- async def say_hello(name, delay)，await asyncio.sleep(delay)
- 先顺序执行两次（0.2s + 0.1s），打印耗时
- 再 gather 并发执行，打印耗时对比

demo_coroutine()：
- 演示直接 await 和 create_task 的区别

demo_gather_and_wait()：
- gather 并发 3 个任务
- wait 加 timeout=0.12 演示部分完成

---
## 背景
- 工具：Copilot Chat
- 阶段：第 1-2 轮
- 结果：正确。asyncio.timeout 需要 Python 3.11+
