package com.opendemo.java.concurrent;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.CountDownLatch;

public class AtomicVariableDemo {

    private static int unsafeCounter = 0;
    private static final AtomicInteger atomicCounter = new AtomicInteger(0);
    private static final AtomicLong atomicLong = new AtomicLong(0);

    public static void main(String[] args) throws Exception {
        demonstrateUnsafeCounter();
        demonstrateAtomicInteger();
        demonstrateAtomicLong();
        demonstrateAtomicReference();
        demonstrateCAS();
        printAtomicGuide();
    }

    public static void demonstrateUnsafeCounter() throws Exception {
        System.out.println("=== 非线程安全计数器（演示竞态条件） ===");
        unsafeCounter = 0;

        int threadCount = 10;
        int incrementsPerThread = 10000;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    unsafeCounter++;
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        int expected = threadCount * incrementsPerThread;
        System.out.printf("  非安全结果: %d (期望: %d, 差异: %d)%n",
                unsafeCounter, expected, expected - unsafeCounter);
        System.out.println("  ++操作不是原子的: 读取→加1→写回（三步操作）");
        System.out.println();
    }

    public static void demonstrateAtomicInteger() throws Exception {
        System.out.println("=== AtomicInteger 原子整数 ===");
        atomicCounter.set(0);

        int threadCount = 10;
        int incrementsPerThread = 10000;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    atomicCounter.incrementAndGet();
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        int expected = threadCount * incrementsPerThread;
        System.out.printf("  AtomicInteger结果: %d (期望: %d) ✓%n",
                atomicCounter.get(), expected);

        atomicCounter.set(0);
        System.out.printf("  getAndIncrement(): %d%n", atomicCounter.getAndIncrement());
        System.out.printf("  incrementAndGet(): %d%n", atomicCounter.incrementAndGet());
        System.out.printf("  getAndAdd(10): %d%n", atomicCounter.getAndAdd(10));
        System.out.printf("  当前值: %d%n", atomicCounter.get());
        System.out.println();
    }

    public static void demonstrateAtomicLong() throws Exception {
        System.out.println("=== AtomicLong 原子长整型 ===");
        atomicLong.set(0);

        int threadCount = 10;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < 10000; j++) {
                    atomicLong.addAndGet(1);
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        System.out.printf("  AtomicLong结果: %d (期望: %d) ✓%n",
                atomicLong.get(), 100000L);
        System.out.println("  适用场景: 计数器、统计累加");
        System.out.println();
    }

    public static void demonstrateAtomicReference() {
        System.out.println("=== AtomicReference 原子引用 ===");

        AtomicReference<String> ref = new AtomicReference<>("初始值");
        System.out.printf("  初始值: %s%n", ref.get());

        ref.set("新值");
        System.out.printf("  set后: %s%n", ref.get());

        boolean swapped = ref.compareAndSet("新值", "CAS更新值");
        System.out.printf("  CAS(新值→CAS更新值): 成功=%b, 当前=%s%n", swapped, ref.get());

        swapped = ref.compareAndSet("旧值", "不会成功");
        System.out.printf("  CAS(旧值→不会成功): 成功=%b, 当前=%s%n", swapped, ref.get());

        System.out.println("  适用场景: 无锁数据结构、状态管理");
        System.out.println();
    }

    public static void demonstrateCAS() {
        System.out.println("=== CAS (Compare And Swap) 机制 ===");

        AtomicInteger ai = new AtomicInteger(10);

        System.out.println("CAS原理:");
        System.out.println("  1. 读取当前值 V");
        System.out.println("  2. 比较V与期望值E");
        System.out.println("  3. 如果 V==E，则将V设为新值N");
        System.out.println("  4. 如果 V!=E，返回false，重试");
        System.out.println();

        boolean success = ai.compareAndSet(10, 20);
        System.out.printf("  CAS(10→20): success=%b, value=%d%n", success, ai.get());

        success = ai.compareAndSet(10, 30);
        System.out.printf("  CAS(10→30): success=%b, value=%d%n", success, ai.get());
        System.out.println();
    }

    public static void printAtomicGuide() {
        System.out.println("=== 原子类选择指南 ===");
        System.out.println("┌────────────────────┬──────────────────────┐");
        System.out.println("│ 原子类             │ 用途                 │");
        System.out.println("├────────────────────┼──────────────────────┤");
        System.out.println("│ AtomicInteger      │ 整型计数器           │");
        System.out.println("│ AtomicLong         │ 长整型计数器         │");
        System.out.println("│ AtomicBoolean      │ 布尔标志             │");
        System.out.println("│ AtomicReference    │ 引用类型原子更新     │");
        System.out.println("│ AtomicStampedRef   │ 带版本号的引用(CAS)  │");
        System.out.println("│ LongAdder          │ 高并发累加(优于ALong) │");
        System.out.println("│ LongAccumulator    │ 自定义累加函数       │");
        System.out.println("└────────────────────┴──────────────────────┘");
    }
}
