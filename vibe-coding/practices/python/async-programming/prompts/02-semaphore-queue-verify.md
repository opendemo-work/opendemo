# Prompt 02: 信号量 + 队列 + 异常 + 验证

添加三个函数：

demo_semaphore()：Semaphore(2) 限制并发，4 个任务竞争，打印开始/完成

demo_queue()：asyncio.Queue 生产者-消费者，生产 5 个数字，消费者收到 >=4 时退出

demo_exception_handling()：gather(return_exceptions=True) 处理部分任务失败

运行 python code/async_programming.py 验证全部 7 个 demo。

---
## 背景
- 工具：Copilot Chat
- 阶段：第 3-4 轮
- 结果：消费者缺少退出条件，修复后正确
