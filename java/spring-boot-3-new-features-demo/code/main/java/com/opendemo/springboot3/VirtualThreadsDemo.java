package com.opendemo.springboot3;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Virtual Threads (虚拟线程) 演示
 *
 * Java 21 引入的 Virtual Threads 是一种轻量级线程，
 * 由 JVM 管理而非操作系统线程，可以大幅减少线程创建的开销。
 *
 * 适用场景:
 * - 高并发 HTTP 请求处理
 * - I/O 密集型任务 (数据库查询、API 调用)
 * - 大量短时任务
 *
 * 注意: CPU 密集型任务不适合使用虚拟线程
 */
public class VirtualThreadsDemo {

    public static void main(String[] args) throws InterruptedException {
        System.out.println("===========================================");
        System.out.println("Virtual Threads 演示开始");
        System.out.println("===========================================\n");

        // 对比测试: 传统线程 vs 虚拟线程
        testTraditionalThreads();
        testVirtualThreads();

        System.out.println("\n===========================================");
        System.out.println("Virtual Threads 演示完成");
        System.out.println("===========================================");
    }

    /**
     * 传统线程池测试
     * 1000 个任务使用 100 个线程
     */
    private static void testTraditionalThreads() throws InterruptedException {
        System.out.println("[传统线程池] 提交 1000 个任务...");

        long startTime = System.currentTimeMillis();

        // 使用传统的固定大小线程池
        try (ExecutorService executor = Executors.newFixedThreadPool(100)) {
            List<Runnable> tasks = new ArrayList<>();

            for (int i = 0; i < 1000; i++) {
                final int taskId = i;
                tasks.add(() -> {
                    try {
                        // 模拟 I/O 操作
                        Thread.sleep(Duration.ofMillis(100));
                        if (taskId % 100 == 0) {
                            System.out.printf("[传统] 任务 %d 完成 (线程: %s)%n",
                                    taskId, Thread.currentThread().getName());
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }

            // 提交所有任务
            for (Runnable task : tasks) {
                executor.submit(task);
            }

            // 等待所有任务完成 (超时 60 秒)
            executor.shutdown();
            executor.awaitTermination(60, TimeUnit.SECONDS);
        }

        long duration = System.currentTimeMillis() - startTime;
        System.out.printf("[传统线程池] 完成时间: %d ms%n%n", duration);
    }

    /**
     * 虚拟线程测试
     * 1000 个任务每个使用一个虚拟线程
     */
    private static void testVirtualThreads() throws InterruptedException {
        System.out.println("[虚拟线程] 提交 1000 个任务...");

        long startTime = System.currentTimeMillis();

        // 使用虚拟线程 per-task 执行器
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Runnable> tasks = new ArrayList<>();

            for (int i = 0; i < 1000; i++) {
                final int taskId = i;
                tasks.add(() -> {
                    try {
                        // 模拟 I/O 操作
                        Thread.sleep(Duration.ofMillis(100));
                        if (taskId % 100 == 0) {
                            System.out.printf("[虚拟] 任务 %d 完成 (线程: %s)%n",
                                    taskId, Thread.currentThread().getName());
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }

            // 提交所有任务
            for (Runnable task : tasks) {
                executor.submit(task);
            }

            // 等待所有任务完成 (超时 60 秒)
            executor.shutdown();
            executor.awaitTermination(60, TimeUnit.SECONDS);
        }

        long duration = System.currentTimeMillis() - startTime;
        System.out.printf("[虚拟线程] 完成时间: %d ms%n%n", duration);
    }
}