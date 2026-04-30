package com.opendemo.java.jvm.gc;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ParallelGCExample {

    public static void main(String[] args) throws Exception {
        System.out.println("=== Parallel GC 演示 ===");
        System.out.println("启动参数: -XX:+UseParallelGC -Xms256m -Xmx512m -Xlog:gc*");
        System.out.println();

        demonstrateParallelCollection();
        demonstrateThroughputBenchmark();
        printCharacteristics();
    }

    public static void demonstrateParallelCollection() {
        System.out.println("--- 并行收集演示 ---");

        long startTime = System.currentTimeMillis();

        List<byte[]> holder = new ArrayList<>();
        for (int i = 0; i < 100; i++) {
            holder.add(new byte[256 * 1024]);

            for (int j = 0; j < 50; j++) {
                byte[] temp = new byte[10 * 1024];
            }
        }

        System.gc();

        long duration = System.currentTimeMillis() - startTime;
        System.out.printf("并行收集+分配耗时: %d ms%n", duration);
        System.out.printf("存活对象: %d MB%n", holder.size() / 4);
        System.out.println();
    }

    public static void demonstrateThroughputBenchmark() throws Exception {
        System.out.println("--- 吞吐量基准测试 ---");

        int threadCount = 4;
        int iterationsPerThread = 1000;
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CountDownLatch latch = new CountDownLatch(threadCount);

        long startTime = System.currentTimeMillis();

        for (int t = 0; t < threadCount; t++) {
            executor.submit(() -> {
                try {
                    List<byte[]> local = new ArrayList<>();
                    for (int i = 0; i < iterationsPerThread; i++) {
                        local.add(new byte[1024]);
                        if (local.size() > 100) {
                            local.subList(0, 50).clear();
                        }
                    }
                } finally {
                    latch.countDown();
                }
            });
        }

        latch.await();
        long duration = System.currentTimeMillis() - startTime;

        System.out.printf("线程数: %d%n", threadCount);
        System.out.printf("每线程迭代: %d 次%n", iterationsPerThread);
        System.out.printf("总耗时: %d ms%n", duration);
        System.out.printf("吞吐量: %.0f ops/sec%n",
                (double) threadCount * iterationsPerThread / duration * 1000);

        executor.shutdown();
        System.out.println();
    }

    public static void printCharacteristics() {
        System.out.println("=== Parallel GC 特点 ===");
        System.out.println("优点:");
        System.out.println("  - 多线程并行回收，吞吐量高");
        System.out.println("  - Java 8 默认GC");
        System.out.println("  - 充分利用多核CPU");
        System.out.println();
        System.out.println("缺点:");
        System.out.println("  - STW停顿时间较长");
        System.out.println("  - 停顿时间不可控");
        System.out.println();
        System.out.println("适用场景:");
        System.out.println("  - 批处理应用");
        System.out.println("  - 后台计算任务");
        System.out.println("  - 吞吐量优先的应用");
        System.out.println();
        System.out.println("推荐参数:");
        System.out.println("  -XX:+UseParallelGC -XX:ParallelGCThreads=4");
        System.out.println("  -XX:GCTimeRatio=99 -XX:MaxGCPauseMillis=200");
    }
}
