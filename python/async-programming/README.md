# Python Async Programming Demo

Python异步编程演示项目，全面展示async/await、asyncio、异步IO等核心概念。

## 技术栈

- Python 3.7+
- asyncio
- async/await

## 核心概念

### 异步函数

```python
import asyncio

async def say_hello():
    """异步函数"""
    print("Hello")
    await asyncio.sleep(1)  # 模拟IO操作
    print("World")

# 运行异步函数
asyncio.run(say_hello())
```

### 并发执行

```python
async def task(name, delay):
    """模拟异步任务"""
    print(f"任务{name}开始")
    await asyncio.sleep(delay)
    print(f"任务{name}完成")
    return f"结果{name}"

async def main():
    # 并发执行多个任务
    tasks = [
        task("A", 2),
        task("B", 1),
        task("C", 3)
    ]
    results = await asyncio.gather(*tasks)
    print(results)  # ['结果A', '结果B', '结果C']

asyncio.run(main())
```

### 异步迭代器

```python
class AsyncRange:
    """异步迭代器"""
    
    def __init__(self, n):
        self.n = n
        self.i = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)  # 模拟异步操作
        i = self.i
        self.i += 1
        return i

async def main():
    async for i in AsyncRange(5):
        print(i)

asyncio.run(main())
```

### 异步上下文管理器

```python
class AsyncConnection:
    """异步连接上下文管理器"""
    
    async def __aenter__(self):
        print("建立连接...")
        await asyncio.sleep(1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("关闭连接...")
        await asyncio.sleep(0.5)
    
    async def fetch(self):
        await asyncio.sleep(0.5)
        return "数据"

async def main():
    async with AsyncConnection() as conn:
        data = await conn.fetch()
        print(data)

asyncio.run(main())
```

### 事件循环

```python
import asyncio

# 获取事件循环
loop = asyncio.get_event_loop()

# 创建任务
task = loop.create_task(say_hello())

# 运行直到完成
loop.run_until_complete(task)

# 关闭循环
loop.close()
```

## 实际应用

### 异步HTTP请求

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    """异步获取URL"""
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        'https://api.github.com',
        'https://httpbin.org/get',
        'https://jsonplaceholder.typicode.com/posts/1'
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for url, result in zip(urls, results):
            print(f"{url}: {len(result)} bytes")

asyncio.run(main())
```

### 异步数据库操作

```python
import asyncio
import aiomysql

async def test_mysql():
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test'
    )
    
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM users")
        result = await cur.fetchall()
        print(result)
    
    conn.close()

asyncio.run(test_mysql())
```

## 快速开始

```bash
# 安装依赖
pip install aiohttp aiomysql

# 运行示例
python async_basics.py
python async_http.py

# 运行测试
python -m pytest test_async.py -v
```

## 性能对比

```python
import time
import asyncio

# 同步版本
def sync_tasks():
    for i in range(3):
        time.sleep(1)
        print(f"同步任务{i}")

# 异步版本
async def async_tasks():
    await asyncio.gather(*[
        asyncio.sleep(1) for _ in range(3)
    ])

# 同步执行时间: 3秒
# 异步执行时间: 1秒
```

## 学习要点

1. 异步编程与同步编程的区别
2. 事件循环的工作原理
3. async/await语法
4. Task和Future对象
5. 并发与并行的区别
6. 异步编程最佳实践

## 参考

- [Python asyncio文档](https://docs.python.org/3/library/asyncio.html)
- 《Fluent Python》
