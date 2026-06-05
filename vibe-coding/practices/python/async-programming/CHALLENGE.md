# 挑战：Python 异步编程

## 难度：intermediate | 预计用时：30 分钟 | 推荐工具：Cursor / Copilot

## 目标

用 Python asyncio 实现一组异步编程示例：

1. **异步基础** — 对比顺序执行 vs 并发执行的耗时差异
2. **协程** — `async def` 定义、`await` 调用、`asyncio.create_task` 创建任务
3. **并发控制** — `asyncio.gather` 和 `asyncio.wait` 的用法区别
4. **超时控制** — `asyncio.wait_for` 和 `asyncio.timeout`（3.11+）
5. **信号量** — 用 `asyncio.Semaphore` 限制并发数量
6. **异步队列** — 生产者-消费者模式的 asyncio.Queue
7. **异常处理** — `gather(return_exceptions=True)` 处理部分任务失败

## 约束

- Python 3.8+（asyncio.timeout 需要 3.11+，用 try/except 兼容）
- 只使用标准库（asyncio、time）
- 所有代码放在一个文件 `async_programming.py` 中
- 每个概念一个 `async def demo_*()` 函数
- 主函数 `async def main()` 依次 await 调用

## 验证

```bash
python code/async_programming.py
```

预期输出要点：
```
1. 异步基础
顺序执行:
  耗时: 0.30秒
并发执行:
  结果: ['Alice done', 'Bob done']
  耗时: 0.20秒  ← 并发更快

3. gather和wait
asyncio.gather:
  结果: ['A: 0.1s', 'B: 0.2s', 'C: 0.15s']
asyncio.wait:
  已完成: 1, 待完成: 2  ← timeout 生效

5. 信号量限制并发
信号量限制(最多2个并发):
  [Task0] 开始
  [Task1] 开始    ← 同时只有 2 个
  [Task0] 完成
  [Task2] 开始

7. 异步异常处理
  任务0: 成功
  任务1: 异常 - 模拟错误
  任务2: 成功
```

## 提示（卡住时再看）

<details>
<summary>提示 1：并发 vs 顺序</summary>

顺序是 `await f()` + `await f()`，并发是 `await asyncio.gather(f(), f())`。对比两者耗时即可。

</details>

<details>
<summary>提示 2：关键 Prompt</summary>

"用 Python asyncio 写一组异步编程 demo：对比顺序 vs 并发执行耗时、协程与 create_task、gather vs wait、wait_for 超时、Semaphore 限流、Queue 生产者消费者、gather 异常处理。每个示例一个 async 函数。"

</details>

## 对应原 Demo

完成后对比参考实现：`python/async-programming/`
