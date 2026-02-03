#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python多线程编程演示
展示threading模块、线程同步、线程池等
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import queue


def demo_thread_basics():
    """线程基础"""
    print("=" * 50)
    print("1. 线程基础")
    print("=" * 50)
    
    def worker(name, delay):
        print(f"  [{name}] 开始工作")
        time.sleep(delay)
        print(f"  [{name}] 完成工作")
    
    # 创建线程
    t1 = threading.Thread(target=worker, args=("Thread-1", 0.2))
    t2 = threading.Thread(target=worker, args=("Thread-2", 0.1))
    
    print("启动线程:")
    t1.start()
    t2.start()
    
    # 等待线程完成
    t1.join()
    t2.join()
    print("所有线程完成")
    
    # 使用类创建线程
    class MyThread(threading.Thread):
        def __init__(self, name, value):
            super().__init__()
            self.name = name
            self.value = value
            self.result = None
        
        def run(self):
            self.result = self.value ** 2
    
    print("\n类方式创建线程:")
    threads = [MyThread(f"T{i}", i) for i in range(1, 4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        print(f"  {t.name}: {t.value}^2 = {t.result}")


def demo_thread_sync():
    """线程同步"""
    print("\n" + "=" * 50)
    print("2. 线程同步 - Lock")
    print("=" * 50)
    
    # 不使用锁的问题
    counter_unsafe = 0
    
    def increment_unsafe():
        global counter_unsafe
        for _ in range(100000):
            counter_unsafe += 1
    
    threads = [threading.Thread(target=increment_unsafe) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"无锁结果(应为200000): {counter_unsafe}")
    
    # 使用锁
    counter_safe = 0
    lock = threading.Lock()
    
    def increment_safe():
        global counter_safe
        for _ in range(100000):
            with lock:
                counter_safe += 1
    
    threads = [threading.Thread(target=increment_safe) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"有锁结果(应为200000): {counter_safe}")


def demo_rlock():
    """可重入锁"""
    print("\n" + "=" * 50)
    print("3. 可重入锁 RLock")
    print("=" * 50)
    
    rlock = threading.RLock()
    
    def recursive_function(n, lock):
        with lock:
            if n > 0:
                print(f"  递归层级: {n}")
                recursive_function(n - 1, lock)
    
    print("RLock允许同一线程多次获取:")
    recursive_function(3, rlock)
    print("  递归完成")


def demo_condition():
    """条件变量"""
    print("\n" + "=" * 50)
    print("4. 条件变量 Condition")
    print("=" * 50)
    
    condition = threading.Condition()
    items = []
    
    def producer():
        for i in range(3):
            time.sleep(0.1)
            with condition:
                items.append(i)
                print(f"  生产: {i}")
                condition.notify()
    
    def consumer():
        for _ in range(3):
            with condition:
                while not items:
                    condition.wait()
                item = items.pop(0)
                print(f"  消费: {item}")
    
    print("生产者-消费者模式:")
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t2.start()
    t1.start()
    t1.join()
    t2.join()


def demo_semaphore():
    """信号量"""
    print("\n" + "=" * 50)
    print("5. 信号量 Semaphore")
    print("=" * 50)
    
    # 限制并发数
    semaphore = threading.Semaphore(2)  # 最多2个线程同时执行
    
    def limited_worker(name):
        with semaphore:
            print(f"  [{name}] 获取信号量, 开始工作")
            time.sleep(0.2)
            print(f"  [{name}] 释放信号量, 完成工作")
    
    print("信号量限制并发(最多2个同时):")
    threads = [threading.Thread(target=limited_worker, args=(f"W{i}",)) 
               for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def demo_thread_pool():
    """线程池"""
    print("\n" + "=" * 50)
    print("6. 线程池 ThreadPoolExecutor")
    print("=" * 50)
    
    def task(n):
        time.sleep(0.1)
        return n * n
    
    print("使用线程池执行任务:")
    with ThreadPoolExecutor(max_workers=3) as executor:
        # submit提交单个任务
        future = executor.submit(task, 5)
        print(f"  submit(5): {future.result()}")
        
        # map批量执行
        results = list(executor.map(task, range(1, 6)))
        print(f"  map(1-5): {results}")


def demo_thread_queue():
    """线程安全队列"""
    print("\n" + "=" * 50)
    print("7. 线程安全队列")
    print("=" * 50)
    
    q = queue.Queue(maxsize=5)
    
    def producer():
        for i in range(5):
            q.put(i)
            print(f"  生产: {i}")
            time.sleep(0.05)
        q.put(None)  # 结束信号
    
    def consumer():
        while True:
            item = q.get()
            if item is None:
                break
            print(f"  消费: {item}")
            q.task_done()
    
    print("队列生产消费:")
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def demo_thread_local():
    """线程本地存储"""
    print("\n" + "=" * 50)
    print("8. 线程本地存储")
    print("=" * 50)
    
    local_data = threading.local()
    
    def worker(name):
        local_data.name = name
        local_data.value = len(name)
        time.sleep(0.1)
        print(f"  线程 {name}: local_data.value = {local_data.value}")
    
    print("每个线程有独立的本地数据:")
    threads = [threading.Thread(target=worker, args=(f"Thread-{i}",)) 
               for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    demo_thread_basics()
    demo_thread_sync()
    demo_rlock()
    demo_condition()
    demo_semaphore()
    demo_thread_pool()
    demo_thread_queue()
    demo_thread_local()
    print("\n[OK] 多线程编程演示完成!")
