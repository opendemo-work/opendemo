package com.opendemo.java.concurrent;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.*;

public class ExecutorServiceDemo {

    public static void main(String[] args) throws Exception {
        demonstrateFixedThreadPool();
        demonstrateCachedThreadPool();
        demonstrateScheduledThreadPool();
        demonstrateFuture();
        demonstrateCompletableFuture();
        printThreadPoolGuide();
    }

    public static void demonstrateFixedThreadPool() throws Exception {
        System.out.println("=== FixedThreadPool 固定线程池 ===");

        ExecutorService executor = Executors.newFixedThreadPool(3);
        CountDownLatch latch = new CountDownLatch(5);

        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.printf("  [%s] 任务%d执行%n",
                        Thread.currentThread().getName(), taskId);
                latch.countDown();
            });
        }

        latch.await();
        executor.shutdown();
        System.out.println("  特点: 固定线程数，适合CPU密集型任务");
        System.out.println("  线程数 = CPU核心数 (Runtime.getRuntime().availableProcessors())");
        System.out.println();
    }

    public static void demonstrateCachedThreadPool() throws Exception {
        System.out.println("=== CachedThreadPool 缓存线程池 ===");

        ExecutorService executor = Executors.newCachedThreadPool();
        CountDownLatch latch = new CountDownLatch(10);

        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.printf("  [%s] 短任务%d%n",
                        Thread.currentThread().getName(), taskId);
                latch.countDown();
            });
        }

        latch.await();
        executor.shutdown();
        System.out.println("  特点: 按需创建线程，空闲60秒回收");
        System.out.println("  适合: 大量短时异步任务");
        System.out.println("  风险: 可能创建大量线程导致OOM");
        System.out.println();
    }

    public static void demonstrateScheduledThreadPool() throws Exception {
        System.out.println("=== ScheduledThreadPool 定时线程池 ===");

        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);

        scheduler.schedule(() -> System.out.println("  延迟1秒执行的任务"), 1, TimeUnit.SECONDS);

        ScheduledFuture<?> future = scheduler.scheduleAtFixedRate(
                () -> System.out.println("  每500ms执行一次"),
                0, 500, TimeUnit.MILLISECONDS);

        Thread.sleep(2000);
        future.cancel(false);
        scheduler.shutdown();
        System.out.println("  特点: 支持延迟和定时执行");
        System.out.println();
    }

    public static void demonstrateFuture() throws Exception {
        System.out.println("=== Future 异步计算 ===");

        ExecutorService executor = Executors.newFixedThreadPool(2);

        Future<String> future1 = executor.submit(() -> {
            Thread.sleep(500);
            return "任务1完成";
        });

        Future<String> future2 = executor.submit(() -> {
            Thread.sleep(300);
            return "任务2完成";
        });

        System.out.printf("  任务1是否完成: %s%n", future1.isDone());
        System.out.printf("  任务2结果: %s%n", future2.get());
        System.out.printf("  任务1结果: %s%n", future1.get());

        executor.shutdown();
        System.out.println("  Future局限: 无法手动完成、链式调用、组合多个Future");
        System.out.println();
    }

    public static void demonstrateCompletableFuture() throws Exception {
        System.out.println("=== CompletableFuture 异步编排 ===");

        CompletableFuture<String> future = CompletableFuture
                .supplyAsync(() -> {
                    return "Hello";
                })
                .thenApply(s -> s + " World")
                .thenApply(String::toUpperCase);

        System.out.printf("  链式结果: %s%n", future.get());

        CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "数据A");
        CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "数据B");

        CompletableFuture<String> combined = f1.thenCombine(f2, (a, b) -> a + " + " + b);
        System.out.printf("  合并结果: %s%n", combined.get());

        List<String> results = Arrays.asList("task1", "task2", "task3")
                .stream()
                .map(name -> CompletableFuture.supplyAsync(() -> name + "-done"))
                .collect(Collectors.toList())
                .stream()
                .map(CompletableFuture::join)
                .collect(Collectors.toList());
        System.out.printf("  并行流结果: %s%n", results);

        System.out.println("  特点: 链式调用、异常处理、组合编排");
        System.out.println();
    }

    public static void printThreadPoolGuide() {
        System.out.println("=== 线程池选择指南 ===");
        System.out.println("  CPU密集型: 线程数 = CPU核心数 + 1");
        System.out.println("  IO密集型:  线程数 = CPU核心数 * 2");
        System.out.println("  混合型:    根据任务比例调整");
        System.out.println();
        System.out.println("  推荐: 使用ThreadPoolExecutor自定义线程池");
        System.out.println("  避免: 使用Executors（阿里Java规范）");
        System.out.println("  原因: FixedThreadPool队列无上限; CachedThreadPool线程数无上限");
    }

    static class Collectors {
        static <T> java.util.stream.Collector<CompletableFuture<T>, ?, List<T>> toList() {
            return java.util.stream.Collectors.collectingAndThen(
                    java.util.stream.Collectors.toList(),
                    list -> {
                        List<T> result = new java.util.ArrayList<>();
                        for (CompletableFuture<T> f : list) {
                            try { result.add(f.get()); } catch (Exception e) { throw new RuntimeException(e); }
                        }
                        return result;
                    }
            );
        }
    }
}
