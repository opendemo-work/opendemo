#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python多进程编程演示
展示multiprocessing模块、进程池、进程间通信等
"""
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import os
import time


def worker_function(name, delay):
    """工作函数"""
    pid = os.getpid()
    print(f"  [{name}] PID={pid} 开始工作")
    time.sleep(delay)
    print(f"  [{name}] PID={pid} 完成工作")
    return f"{name} done"


def demo_process_basics():
    """进程基础"""
    print("=" * 50)
    print("1. 进程基础")
    print("=" * 50)
    
    print(f"主进程 PID: {os.getpid()}")
    
    # 创建进程
    p1 = mp.Process(target=worker_function, args=("Process-1", 0.2))
    p2 = mp.Process(target=worker_function, args=("Process-2", 0.1))
    
    print("\n启动进程:")
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    print("所有进程完成")


def square(x):
    """计算平方"""
    return x * x


def demo_process_pool():
    """进程池"""
    print("\n" + "=" * 50)
    print("2. 进程池 Pool")
    print("=" * 50)
    
    numbers = list(range(1, 11))
    
    # 使用Pool
    with mp.Pool(processes=4) as pool:
        # map - 阻塞方式
        results = pool.map(square, numbers)
        print(f"pool.map结果: {results}")
        
        # apply_async - 异步方式
        async_result = pool.apply_async(square, (10,))
        print(f"apply_async结果: {async_result.get()}")


def demo_process_pool_executor():
    """ProcessPoolExecutor"""
    print("\n" + "=" * 50)
    print("3. ProcessPoolExecutor")
    print("=" * 50)
    
    def compute_heavy(n):
        """模拟计算密集型任务"""
        return sum(i*i for i in range(n))
    
    numbers = [100000, 200000, 300000, 400000]
    
    print("使用ProcessPoolExecutor:")
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(compute_heavy, numbers))
        for n, r in zip(numbers, results):
            print(f"  compute_heavy({n}): {r}")


def producer(q, items):
    """生产者进程"""
    for item in items:
        q.put(item)
        print(f"  生产: {item}")
    q.put(None)  # 结束信号


def consumer(q):
    """消费者进程"""
    while True:
        item = q.get()
        if item is None:
            break
        print(f"  消费: {item}")


def demo_queue_communication():
    """队列通信"""
    print("\n" + "=" * 50)
    print("4. 进程间通信 - Queue")
    print("=" * 50)
    
    q = mp.Queue()
    items = [1, 2, 3, 4, 5]
    
    print("生产者-消费者模式:")
    p1 = mp.Process(target=producer, args=(q, items))
    p2 = mp.Process(target=consumer, args=(q,))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def sender(conn, messages):
    """发送方"""
    for msg in messages:
        conn.send(msg)
        print(f"  发送: {msg}")
    conn.send(None)
    conn.close()


def receiver(conn):
    """接收方"""
    while True:
        msg = conn.recv()
        if msg is None:
            break
        print(f"  接收: {msg}")
    conn.close()


def demo_pipe_communication():
    """管道通信"""
    print("\n" + "=" * 50)
    print("5. 进程间通信 - Pipe")
    print("=" * 50)
    
    parent_conn, child_conn = mp.Pipe()
    messages = ["Hello", "World", "Python"]
    
    print("管道通信:")
    p1 = mp.Process(target=sender, args=(parent_conn, messages))
    p2 = mp.Process(target=receiver, args=(child_conn,))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def increment_shared(shared_value, lock, count):
    """增加共享值"""
    for _ in range(count):
        with lock:
            shared_value.value += 1


def demo_shared_memory():
    """共享内存"""
    print("\n" + "=" * 50)
    print("6. 共享内存 - Value和Array")
    print("=" * 50)
    
    # 共享值
    shared_counter = mp.Value('i', 0)  # 'i' = integer
    lock = mp.Lock()
    
    processes = [
        mp.Process(target=increment_shared, args=(shared_counter, lock, 10000))
        for _ in range(4)
    ]
    
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    
    print(f"共享计数器(应为40000): {shared_counter.value}")
    
    # 共享数组
    shared_array = mp.Array('d', [0.0, 0.0, 0.0])  # 'd' = double
    print(f"共享数组: {list(shared_array)}")


def demo_manager():
    """Manager共享复杂对象"""
    print("\n" + "=" * 50)
    print("7. Manager共享复杂对象")
    print("=" * 50)
    
    def worker(d, l, key, value):
        d[key] = value
        l.append(value)
    
    with mp.Manager() as manager:
        shared_dict = manager.dict()
        shared_list = manager.list()
        
        processes = [
            mp.Process(target=worker, args=(shared_dict, shared_list, f"key{i}", i))
            for i in range(3)
        ]
        
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        
        print(f"共享字典: {dict(shared_dict)}")
        print(f"共享列表: {list(shared_list)}")


if __name__ == "__main__":
    # Windows需要在 if __name__ == "__main__" 中运行多进程
    demo_process_basics()
    demo_process_pool()
    demo_process_pool_executor()
    demo_queue_communication()
    demo_pipe_communication()
    demo_shared_memory()
    demo_manager()
    print("\n[OK] 多进程编程演示完成!")
