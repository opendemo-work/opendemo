package com.opendemo.java.profiling;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadInfo;
import java.lang.management.ThreadMXBean;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class CpuProfilingDemo {

    public static void main(String[] args) throws Exception {
        demonstrateCpuTimeMeasurement();
        demonstrateThreadCpuTime();
        demonstrateDeadlockDetection();
        demonstrateCpuIntensiveProfiling();
    }

    public static void demonstrateCpuTimeMeasurement() {
        System.out.println("=== CPU时间测量 ===");

        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();

        if (!threadBean.isCurrentThreadCpuTimeSupported()) {
            System.out.println("当前JVM不支持CPU时间测量");
            return;
        }

        if (!threadBean.isThreadCpuTimeEnabled()) {
            threadBean.setThreadCpuTimeEnabled(true);
        }

        long cpuTimeBefore = threadBean.getCurrentThreadCpuTime();
        long userTimeBefore = threadBean.getCurrentThreadUserTime();

        long sum = 0;
        for (long i = 0; i < 100_000_000L; i++) {
            sum += i;
        }

        long cpuTimeAfter = threadBean.getCurrentThreadCpuTime();
        long userTimeAfter = threadBean.getCurrentThreadUserTime();

        System.out.printf("计算结果: %d (防止优化)%n", sum);
        System.out.printf("CPU时间: %.3f ms%n", (cpuTimeAfter - cpuTimeBefore) / 1_000_000.0);
        System.out.printf("用户时间: %.3f ms%n", (userTimeAfter - userTimeBefore) / 1_000_000.0);
        System.out.printf("系统时间: %.3f ms%n",
                (cpuTimeAfter - cpuTimeBefore - (userTimeAfter - userTimeBefore)) / 1_000_000.0);
        System.out.println();
    }

    public static void demonstrateThreadCpuTime() throws Exception {
        System.out.println("=== 多线程CPU时间分析 ===");

        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        if (!threadBean.isThreadCpuTimeSupported()) {
            System.out.println("当前JVM不支持CPU时间测量");
            return;
        }
        threadBean.setThreadCpuTimeEnabled(true);

        Runnable cpuTask = () -> {
            long sum = 0;
            for (long i = 0; i < 50_000_000L; i++) {
                sum += i;
            }
            System.out.printf("  [%s] 计算完成: sum=%d%n",
                    Thread.currentThread().getName(), sum);
        };

        Runnable ioTask = () -> {
            try {
                Thread.sleep(200);
                System.out.printf("  [%s] IO模拟完成%n", Thread.currentThread().getName());
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        };

        Thread cpuThread = new Thread(cpuTask, "CPU-Thread");
        Thread ioThread = new Thread(ioTask, "IO-Thread");

        cpuThread.start();
        ioThread.start();

        while (cpuThread.isAlive() || ioThread.isAlive()) {
            long cpuTime = threadBean.getThreadCpuTime(cpuThread.getId());
            long ioTime = threadBean.getThreadCpuTime(ioThread.getId());

            System.out.printf("  CPU线程时间: %.2fms | IO线程时间: %.2fms%n",
                    cpuTime / 1_000_000.0, ioTime / 1_000_000.0);

            Thread.sleep(50);
        }

        cpuThread.join();
        ioThread.join();

        System.out.println("  CPU密集型线程的CPU时间远高于IO密集型线程");
        System.out.println();
    }

    public static void demonstrateDeadlockDetection() {
        System.out.println("=== 死锁检测 ===");

        Object lock1 = new Object();
        Object lock2 = new Object();

        Thread thread1 = new Thread(() -> {
            synchronized (lock1) {
                try { Thread.sleep(50); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                synchronized (lock2) {
                    System.out.println("线程1获取两把锁");
                }
            }
        }, "Deadlock-Thread-1");

        Thread thread2 = new Thread(() -> {
            synchronized (lock2) {
                try { Thread.sleep(50); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                synchronized (lock1) {
                    System.out.println("线程2获取两把锁");
                }
            }
        }, "Deadlock-Thread-2");

        thread1.start();
        thread2.start();

        try { Thread.sleep(200); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        long[] deadlockedThreads = threadBean.findDeadlockedThreads();

        if (deadlockedThreads != null && deadlockedThreads.length > 0) {
            System.out.printf("  检测到 %d 个死锁线程!%n", deadlockedThreads.length);
            ThreadInfo[] infos = threadBean.getThreadInfo(deadlockedThreads);
            for (ThreadInfo info : infos) {
                System.out.printf("  死锁线程: %s (状态: %s)%n", info.getThreadName(), info.getThreadState());
                System.out.printf("    等待锁: %s%n", info.getLockName());
                System.out.printf("    持有锁: %s%n", info.getLockOwnerName());
            }
        } else {
            System.out.println("  未检测到死锁");
        }

        thread1.interrupt();
        thread2.interrupt();

        System.out.println("  死锁检测方法: threadBean.findDeadlockedThreads()");
        System.out.println("  预防措施: 按固定顺序获取锁，使用tryLock(timeout)");
        System.out.println();
    }

    public static void demonstrateCpuIntensiveProfiling() throws Exception {
        System.out.println("=== CPU密集型任务分析 ===");

        int iterations = 10;
        long[] durations = new long[iterations];

        for (int i = 0; i < iterations; i++) {
            long start = System.nanoTime();
            fibonacci(30);
            durations[i] = System.nanoTime() - start;
        }

        for (int i = 0; i < iterations; i++) {
            System.out.printf("  第%d次: %.3f ms%n", i + 1, durations[i] / 1_000_000.0);
        }

        double avgFirst5 = 0, avgLast5 = 0;
        for (int i = 0; i < 5; i++) avgFirst5 += durations[i];
        for (int i = 5; i < 10; i++) avgLast5 += durations[i];
        avgFirst5 /= 5;
        avgLast5 /= 5;

        System.out.printf("  前5次平均: %.3f ms%n", avgFirst5 / 1_000_000.0);
        System.out.printf("  后5次平均: %.3f ms%n", avgLast5 / 1_000_000.0);
        System.out.printf("  JIT优化加速: %.2fx%n", avgFirst5 / avgLast5);
    }

    private static long fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}
