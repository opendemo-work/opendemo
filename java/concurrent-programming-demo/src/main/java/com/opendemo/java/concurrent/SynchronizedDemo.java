package com.opendemo.java.concurrent;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class SynchronizedDemo {

    private static int sharedCounter = 0;
    private static final Object lock = new Object();
    private static final ReentrantLock reentrantLock = new ReentrantLock();
    private static int lockCounter = 0;

    public static void main(String[] args) throws Exception {
        demonstrateSynchronizedBlock();
        demonstrateReentrantLock();
        demonstrateReadWriteLock();
        demonstrateLockComparison();
    }

    public static void demonstrateSynchronizedBlock() throws Exception {
        System.out.println("=== synchronized 同步块 ===");
        sharedCounter = 0;

        int threadCount = 10;
        int incrementsPerThread = 1000;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    synchronized (lock) {
                        sharedCounter++;
                    }
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        System.out.printf("  synchronized结果: %d (期望: %d) ✓%n",
                sharedCounter, threadCount * incrementsPerThread);
        System.out.println();
    }

    public static void demonstrateReentrantLock() throws Exception {
        System.out.println("=== ReentrantLock 可重入锁 ===");
        lockCounter = 0;

        int threadCount = 10;
        int incrementsPerThread = 1000;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    reentrantLock.lock();
                    try {
                        lockCounter++;
                    } finally {
                        reentrantLock.unlock();
                    }
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        System.out.printf("  ReentrantLock结果: %d (期望: %d) ✓%n",
                lockCounter, threadCount * incrementsPerThread);

        System.out.println("  ReentrantLock特性:");
        System.out.println("    - 可中断: lockInterruptibly()");
        System.out.println("    - 可超时: tryLock(timeout, unit)");
        System.out.println("    - 公平锁: new ReentrantLock(true)");
        System.out.println("    - 条件变量: newCondition()");
        System.out.println();
    }

    public static void demonstrateReadWriteLock() throws Exception {
        System.out.println("=== ReentrantReadWriteLock 读写锁 ===");

        ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
        ReentrantReadWriteLock.ReadLock readLock = rwLock.readLock();
        ReentrantReadWriteLock.WriteLock writeLock = rwLock.writeLock();

        int[] data = {0};
        int readers = 5;
        int writers = 2;
        CountDownLatch latch = new CountDownLatch(readers + writers);

        for (int i = 0; i < writers; i++) {
            final int writerId = i;
            new Thread(() -> {
                writeLock.lock();
                try {
                    data[0]++;
                    System.out.printf("  [写者%d] 写入数据: %d%n", writerId, data[0]);
                } finally {
                    writeLock.unlock();
                }
                latch.countDown();
            }).start();
        }

        for (int i = 0; i < readers; i++) {
            final int readerId = i;
            new Thread(() -> {
                readLock.lock();
                try {
                    System.out.printf("  [读者%d] 读取数据: %d%n", readerId, data[0]);
                } finally {
                    readLock.unlock();
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        System.out.println("  读写锁特点: 多个读者可同时读，写者独占");
        System.out.println();
    }

    public static void demonstrateLockComparison() {
        System.out.println("=== synchronized vs ReentrantLock ===");
        System.out.println("┌─────────────┬──────────────┬──────────────┐");
        System.out.println("│ 特性        │ synchronized │ ReentrantLock│");
        System.out.println("├─────────────┼──────────────┼──────────────┤");
        System.out.println("│ 实现方式    │ JVM内置      │ API层面      │");
        System.out.println("│ 锁释放      │ 自动         │ 手动unlock   │");
        System.out.println("│ 可中断      │ 不可         │ 可以         │");
        System.out.println("│ 超时获取    │ 不支持       │ tryLock      │");
        System.out.println("│ 公平性      │ 非公平       │ 可选         │");
        System.out.println("│ 条件变量    │ wait/notify  │ Condition    │");
        System.out.println("│ 可重入      │ 是           │ 是           │");
        System.out.println("└─────────────┴──────────────┴──────────────┘");
    }
}
