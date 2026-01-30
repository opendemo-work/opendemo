#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python异步编程演示
展示asyncio、async/await、并发任务等
"""
import asyncio
import time


async def demo_async_basics():
    """异步基础"""
    print("=" * 50)
    print("1. 异步基础")
    print("=" * 50)
    
    async def say_hello(name, delay):
        await asyncio.sleep(delay)
        print(f"  Hello, {name}!")
        return f"{name} done"
    
    print("顺序执行:")
    start = time.time()
    await say_hello("Alice", 0.2)
    await say_hello("Bob", 0.1)
    print(f"  耗时: {time.time() - start:.2f}秒")
    
    print("\n并发执行:")
    start = time.time()
    results = await asyncio.gather(
        say_hello("Alice", 0.2),
        say_hello("Bob", 0.1)
    )
    print(f"  结果: {results}")
    print(f"  耗时: {time.time() - start:.2f}秒")


async def demo_coroutine():
    """协程"""
    print("\n" + "=" * 50)
    print("2. 协程定义与调用")
    print("=" * 50)
    
    async def fetch_data(url, delay):
        print(f"  开始获取: {url}")
        await asyncio.sleep(delay)
        return f"Data from {url}"
    
    # 直接await
    result = await fetch_data("http://example.com", 0.1)
    print(f"  结果: {result}")
    
    # 创建任务
    task = asyncio.create_task(fetch_data("http://test.com", 0.1))
    print(f"  任务状态: {task.done()}")
    result = await task
    print(f"  任务完成: {result}")


async def demo_gather_and_wait():
    """并发控制"""
    print("\n" + "=" * 50)
    print("3. gather和wait")
    print("=" * 50)
    
    async def task(name, delay):
        await asyncio.sleep(delay)
        return f"{name}: {delay}s"
    
    # gather - 并发执行多个协程
    print("asyncio.gather:")
    results = await asyncio.gather(
        task("A", 0.1),
        task("B", 0.2),
        task("C", 0.15)
    )
    print(f"  结果: {results}")
    
    # wait - 更细粒度控制
    print("\nasyncio.wait:")
    tasks = {
        asyncio.create_task(task("X", 0.1)),
        asyncio.create_task(task("Y", 0.2)),
        asyncio.create_task(task("Z", 0.15))
    }
    done, pending = await asyncio.wait(tasks, timeout=0.12)
    print(f"  已完成: {len(done)}, 待完成: {len(pending)}")
    
    # 等待剩余任务
    if pending:
        await asyncio.wait(pending)


async def demo_timeout():
    """超时控制"""
    print("\n" + "=" * 50)
    print("4. 超时控制")
    print("=" * 50)
    
    async def slow_operation():
        await asyncio.sleep(1)
        return "完成"
    
    # wait_for 超时
    print("asyncio.wait_for:")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=0.1)
        print(f"  结果: {result}")
    except asyncio.TimeoutError:
        print("  超时!")
    
    # timeout 上下文管理器 (Python 3.11+)
    print("\nasyncio.timeout (3.11+):")
    try:
        async with asyncio.timeout(0.1):
            await slow_operation()
    except asyncio.TimeoutError:
        print("  超时!")


async def demo_semaphore():
    """信号量限制并发"""
    print("\n" + "=" * 50)
    print("5. 信号量限制并发")
    print("=" * 50)
    
    sem = asyncio.Semaphore(2)  # 最多2个并发
    
    async def limited_task(name):
        async with sem:
            print(f"  [{name}] 开始")
            await asyncio.sleep(0.1)
            print(f"  [{name}] 完成")
    
    print("信号量限制(最多2个并发):")
    await asyncio.gather(*[limited_task(f"Task{i}") for i in range(4)])


async def demo_queue():
    """异步队列"""
    print("\n" + "=" * 50)
    print("6. 异步队列")
    print("=" * 50)
    
    queue = asyncio.Queue(maxsize=5)
    
    async def producer(q):
        for i in range(5):
            await q.put(i)
            print(f"  生产: {i}")
            await asyncio.sleep(0.05)
    
    async def consumer(q):
        while True:
            item = await q.get()
            print(f"  消费: {item}")
            q.task_done()
            if item >= 4:
                break
    
    print("生产者-消费者:")
    await asyncio.gather(producer(queue), consumer(queue))


async def demo_exception_handling():
    """异步异常处理"""
    print("\n" + "=" * 50)
    print("7. 异步异常处理")
    print("=" * 50)
    
    async def may_fail(should_fail):
        if should_fail:
            raise ValueError("模拟错误")
        return "成功"
    
    # gather中的异常
    print("gather异常处理 (return_exceptions=True):")
    results = await asyncio.gather(
        may_fail(False),
        may_fail(True),
        may_fail(False),
        return_exceptions=True
    )
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  任务{i}: 异常 - {result}")
        else:
            print(f"  任务{i}: {result}")


async def main():
    """主函数"""
    await demo_async_basics()
    await demo_coroutine()
    await demo_gather_and_wait()
    await demo_timeout()
    await demo_semaphore()
    await demo_queue()
    await demo_exception_handling()
    print("\n[OK] 异步编程演示完成!")


if __name__ == "__main__":
    asyncio.run(main())
