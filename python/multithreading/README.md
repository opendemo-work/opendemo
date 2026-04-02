# Python Multithreading Demo

Python多线程编程演示项目，展示threading模块、线程同步、线程池等核心概念。

## 技术栈

- Python 3.8+
- threading
- concurrent.futures

## 核心概念

### 创建线程

```python
import threading
import time

def worker(name, delay):
    """工作函数"""
    print(f"线程{name}开始")
    time.sleep(delay)
    print(f"线程{name}结束")

# 创建线程
thread1 = threading.Thread(target=worker, args=("A", 2))
thread2 = threading.Thread(target=worker, args=("B", 1))

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("所有线程完成")
```

### 线程类

```python
import threading

class MyThread(threading.Thread):
    """自定义线程类"""
    
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay
    
    def run(self):
        """线程执行内容"""
        print(f"{self.name}开始")
        import time
        time.sleep(self.delay)
        print(f"{self.name}结束")

# 使用自定义线程
thread = MyThread("自定义线程", 2)
thread.start()
thread.join()
```

### 线程同步 - Lock

```python
import threading

class Counter:
    """线程安全的计数器"""
    
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            # 临界区
            current = self.value
            import time
            time.sleep(0.0001)  # 模拟操作
            self.value = current + 1

counter = Counter()
threads = []

# 创建100个线程
for i in range(100):
    t = threading.Thread(target=counter.increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"最终计数: {counter.value}")  # 100
```

### 线程同步 - RLock

```python
import threading

class RecursiveWorker:
    """递归锁示例"""
    
    def __init__(self):
        self.rlock = threading.RLock()
    
    def outer(self):
        with self.rlock:
            print("外层获取锁")
            self.inner()
    
    def inner(self):
        with self.rlock:
            print("内层获取锁（同一线程可重入）")

worker = RecursiveWorker()
worker.outer()
```

### 线程同步 - Condition

```python
import threading
import time

class ProducerConsumer:
    """生产者消费者模型"""
    
    def __init__(self):
        self.condition = threading.Condition()
        self.items = []
    
    def produce(self, item):
        with self.condition:
            self.items.append(item)
            print(f"生产: {item}")
            self.condition.notify()  # 通知消费者
    
    def consume(self):
        with self.condition:
            while not self.items:
                self.condition.wait()  # 等待生产
            item = self.items.pop(0)
            print(f"消费: {item}")
            return item

pc = ProducerConsumer()

def producer():
    for i in range(5):
        time.sleep(1)
        pc.produce(i)

def consumer():
    for _ in range(5):
        pc.consume()

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join()
t2.join()
```

### 线程池

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    """任务函数"""
    time.sleep(1)
    return n * n

# 使用线程池
with ThreadPoolExecutor(max_workers=5) as executor:
    # 提交单个任务
    future = executor.submit(task, 5)
    result = future.result()
    print(f"结果: {result}")
    
    # 批量提交任务
    results = executor.map(task, range(10))
    print(list(results))
```

## GIL全局解释器锁

```python
import threading
import time

# CPU密集型任务 - 多线程无法加速
def cpu_bound(n):
    count = 0
    for i in range(n):
        count += i
    return count

# IO密集型任务 - 多线程可以加速
def io_bound(n):
    time.sleep(n)
    return n

# 测试
start = time.time()
threads = []
for _ in range(4):
    t = threading.Thread(target=cpu_bound, args=(10000000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"多线程CPU密集型耗时: {time.time() - start}")
```

## 快速开始

```bash
# 运行示例
python threading_basics.py
python thread_synchronization.py
python thread_pool.py
```

## 学习要点

1. GIL对多线程的影响
2. 线程同步机制
3. 线程vs进程的选择
4. 线程安全编程
5. 线程池的使用

## 参考

- [threading文档](https://docs.python.org/3/library/threading.html)
