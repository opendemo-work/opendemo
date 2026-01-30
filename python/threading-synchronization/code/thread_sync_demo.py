#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 线程同步完整示例
演示各种线程同步原语和并发控制
"""

import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager


# ============ 1. Lock 互斥锁 ============
print("=" * 50)
print("1. Lock 互斥锁")
print("=" * 50)

class BankAccount:
    """使用锁保护的银行账户"""
    
    def __init__(self, balance: int = 0):
        self.balance = balance
        self._lock = threading.Lock()
    
    def deposit(self, amount: int):
        with self._lock:
            current = self.balance
            time.sleep(0.001)  # 模拟处理时间
            self.balance = current + amount
    
    def withdraw(self, amount: int) -> bool:
        with self._lock:
            if self.balance >= amount:
                current = self.balance
                time.sleep(0.001)
                self.balance = current - amount
                return True
            return False

# 测试
account = BankAccount(1000)

def do_transactions():
    for _ in range(100):
        account.deposit(10)
        account.withdraw(10)

threads = [threading.Thread(target=do_transactions) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"最终余额: {account.balance} (应为1000)")


# ============ 2. RLock 可重入锁 ============
print("\n" + "=" * 50)
print("2. RLock 可重入锁")
print("=" * 50)

class Counter:
    """可重入锁允许同一线程多次获取"""
    
    def __init__(self):
        self.value = 0
        self._lock = threading.RLock()
    
    def increment(self):
        with self._lock:
            self.value += 1
    
    def add(self, n: int):
        with self._lock:
            for _ in range(n):
                self.increment()  # 可重入,不会死锁

counter = Counter()
counter.add(10)
print(f"计数器值: {counter.value}")


# ============ 3. Condition 条件变量 ============
print("\n" + "=" * 50)
print("3. Condition 条件变量")
print("=" * 50)

class BoundedBuffer:
    """有界缓冲区 - 生产者消费者模式"""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = []
        self.condition = threading.Condition()
    
    def put(self, item):
        with self.condition:
            while len(self.buffer) >= self.capacity:
                self.condition.wait()
            self.buffer.append(item)
            print(f"  生产: {item}, 缓冲区大小: {len(self.buffer)}")
            self.condition.notify_all()
    
    def get(self):
        with self.condition:
            while len(self.buffer) == 0:
                self.condition.wait()
            item = self.buffer.pop(0)
            print(f"  消费: {item}, 缓冲区大小: {len(self.buffer)}")
            self.condition.notify_all()
            return item

buffer = BoundedBuffer(capacity=3)

def producer():
    for i in range(5):
        buffer.put(f"item-{i}")
        time.sleep(0.05)

def consumer():
    for _ in range(5):
        buffer.get()
        time.sleep(0.1)

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()


# ============ 4. Semaphore 信号量 ============
print("\n" + "=" * 50)
print("4. Semaphore 信号量")
print("=" * 50)

class ConnectionPool:
    """使用信号量限制并发连接数"""
    
    def __init__(self, max_connections: int):
        self.semaphore = threading.Semaphore(max_connections)
        self.active_connections = 0
        self._lock = threading.Lock()
    
    @contextmanager
    def connection(self):
        self.semaphore.acquire()
        with self._lock:
            self.active_connections += 1
            conn_id = self.active_connections
        try:
            yield f"Connection-{conn_id}"
        finally:
            with self._lock:
                self.active_connections -= 1
            self.semaphore.release()

pool = ConnectionPool(max_connections=3)

def use_connection(task_id: int):
    with pool.connection() as conn:
        print(f"  任务{task_id} 使用 {conn}")
        time.sleep(0.1)

threads = [threading.Thread(target=use_connection, args=(i,)) for i in range(6)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("所有连接已释放")


# ============ 5. Event 事件 ============
print("\n" + "=" * 50)
print("5. Event 事件")
print("=" * 50)

start_event = threading.Event()

def worker(worker_id: int):
    print(f"  Worker-{worker_id} 等待启动信号...")
    start_event.wait()
    print(f"  Worker-{worker_id} 开始工作!")

workers = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for w in workers:
    w.start()

time.sleep(0.5)
print("发送启动信号!")
start_event.set()

for w in workers:
    w.join()


# ============ 6. Barrier 屏障 ============
print("\n" + "=" * 50)
print("6. Barrier 屏障")
print("=" * 50)

barrier = threading.Barrier(3)

def phase_worker(worker_id: int):
    print(f"  Worker-{worker_id} 阶段1完成")
    barrier.wait()  # 等待所有线程到达
    print(f"  Worker-{worker_id} 阶段2开始")

workers = [threading.Thread(target=phase_worker, args=(i,)) for i in range(3)]
for w in workers:
    w.start()
for w in workers:
    w.join()


# ============ 7. Queue 线程安全队列 ============
print("\n" + "=" * 50)
print("7. Queue 线程安全队列")
print("=" * 50)

task_queue = queue.Queue(maxsize=10)
results = []

def producer_queue():
    for i in range(5):
        task_queue.put(f"task-{i}")
        print(f"  生产任务: task-{i}")
        time.sleep(0.05)
    task_queue.put(None)  # 结束信号

def consumer_queue():
    while True:
        task = task_queue.get()
        if task is None:
            break
        print(f"  处理任务: {task}")
        results.append(f"done-{task}")
        task_queue.task_done()

producer_t = threading.Thread(target=producer_queue)
consumer_t = threading.Thread(target=consumer_queue)

producer_t.start()
consumer_t.start()
producer_t.join()
consumer_t.join()

print(f"结果: {results}")


# ============ 8. ThreadPoolExecutor ============
print("\n" + "=" * 50)
print("8. ThreadPoolExecutor 线程池")
print("=" * 50)

def process_item(item: int) -> int:
    time.sleep(0.1)
    return item * 2

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_item, i) for i in range(5)]
    
    results = []
    for future in futures:
        result = future.result()
        results.append(result)
        print(f"  完成: {result}")

print(f"所有结果: {results}")


# ============ 9. 读写锁模拟 ============
print("\n" + "=" * 50)
print("9. 读写锁模拟")
print("=" * 50)

class ReadWriteLock:
    """读写锁: 多读单写"""
    
    def __init__(self):
        self._readers = 0
        self._readers_lock = threading.Lock()
        self._writers_lock = threading.Lock()
    
    @contextmanager
    def read_lock(self):
        with self._readers_lock:
            self._readers += 1
            if self._readers == 1:
                self._writers_lock.acquire()
        try:
            yield
        finally:
            with self._readers_lock:
                self._readers -= 1
                if self._readers == 0:
                    self._writers_lock.release()
    
    @contextmanager
    def write_lock(self):
        self._writers_lock.acquire()
        try:
            yield
        finally:
            self._writers_lock.release()

class SharedData:
    def __init__(self):
        self.data = {"value": 0}
        self.rw_lock = ReadWriteLock()
    
    def read(self):
        with self.rw_lock.read_lock():
            return self.data["value"]
    
    def write(self, value):
        with self.rw_lock.write_lock():
            self.data["value"] = value

shared = SharedData()

def reader(reader_id):
    for _ in range(3):
        value = shared.read()
        print(f"  读者{reader_id} 读取: {value}")
        time.sleep(0.05)

def writer(value):
    time.sleep(0.1)
    shared.write(value)
    print(f"  写者 写入: {value}")

threads = [
    threading.Thread(target=reader, args=(1,)),
    threading.Thread(target=reader, args=(2,)),
    threading.Thread(target=writer, args=(42,)),
]

for t in threads:
    t.start()
for t in threads:
    t.join()


# ============ 10. 线程本地存储 ============
print("\n" + "=" * 50)
print("10. 线程本地存储 (Thread Local)")
print("=" * 50)

thread_local = threading.local()

def worker_local(worker_id: int):
    # 每个线程有自己的副本
    thread_local.id = worker_id
    thread_local.data = f"data-{worker_id}"
    time.sleep(0.1)
    print(f"  线程 {thread_local.id}: {thread_local.data}")

threads = [threading.Thread(target=worker_local, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()


# ============ 总结 ============
print("\n" + "=" * 50)
print("线程同步总结")
print("=" * 50)
print("""
同步原语:
- Lock: 基本互斥锁
- RLock: 可重入锁
- Condition: 条件变量
- Semaphore: 信号量
- Event: 事件通知
- Barrier: 屏障同步

高级工具:
- Queue: 线程安全队列
- ThreadPoolExecutor: 线程池

最佳实践:
1. 优先使用 with 语句
2. 避免过度同步
3. 注意死锁风险
4. 使用 Queue 代替共享变量
5. 考虑使用线程池
""")
