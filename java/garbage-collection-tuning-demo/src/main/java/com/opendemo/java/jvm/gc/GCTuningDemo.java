package com.opendemo.java.jvm.gc;

import java.lang.management.GarbageCollectorMXBean;
import java.lang.management.ManagementFactory;
import java.util.ArrayList;
import java.util.List;

public class GCTuningDemo {

    public static void main(String[] args) {
        demonstrateTuningStrategies();
        runGCBenchmark("Young GC密集型", createYoungGCWorkload());
        runGCBenchmark("Old GC密集型", createOldGCWorkload());
        runGCBenchmark("混合型", createMixedWorkload());
        printTuningRecommendations();
    }

    public static void demonstrateTuningStrategies() {
        System.out.println("=== GC调优策略 ===");
        System.out.println();
        System.out.println("策略一：吞吐量优先");
        System.out.println("  -XX:+UseParallelGC");
        System.out.println("  -XX:GCTimeRatio=99");
        System.out.println("  -XX:MaxGCPauseMillis=200");
        System.out.println();
        System.out.println("策略二：延迟优先");
        System.out.println("  -XX:+UseG1GC");
        System.out.println("  -XX:MaxGCPauseMillis=50");
        System.out.println();
        System.out.println("策略三：超低延迟");
        System.out.println("  -XX:+UseZGC");
        System.out.println("  -Xms4g -Xmx4g");
        System.out.println();
    }

    public static void runGCBenchmark(String name, Runnable workload) {
        System.out.println("=== " + name + " 基准测试 ===");

        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        long gcCountBefore = getTotalGCCount(gcBeans);
        long gcTimeBefore = getTotalGCTime(gcBeans);

        long startTime = System.nanoTime();
        workload.run();
        long duration = (System.nanoTime() - startTime) / 1_000_000;

        long gcCountAfter = getTotalGCCount(gcBeans);
        long gcTimeAfter = getTotalGCTime(gcBeans);

        System.out.printf("  执行时间: %d ms%n", duration);
        System.out.printf("  GC次数: %d%n", gcCountAfter - gcCountBefore);
        System.out.printf("  GC时间: %d ms%n", gcTimeAfter - gcTimeBefore);
        System.out.printf("  GC占比: %.1f%%%n",
                duration > 0 ? (double)(gcTimeAfter - gcTimeBefore) / duration * 100 : 0);
        System.out.println();
    }

    private static Runnable createYoungGCWorkload() {
        return () -> {
            for (int i = 0; i < 10000; i++) {
                byte[] temp = new byte[1024];
                String s = "temp-" + i;
            }
        };
    }

    private static Runnable createOldGCWorkload() {
        return () -> {
            List<byte[]> holder = new ArrayList<>();
            for (int i = 0; i < 5000; i++) {
                holder.add(new byte[512]);
            }
        };
    }

    private static Runnable createMixedWorkload() {
        return () -> {
            List<byte[]> holder = new ArrayList<>();
            for (int i = 0; i < 5000; i++) {
                byte[] temp = new byte[512];
                if (i % 50 == 0) {
                    holder.add(new byte[2048]);
                }
                if (holder.size() > 100) {
                    holder.subList(0, 20).clear();
                }
            }
        };
    }

    public static void printTuningRecommendations() {
        System.out.println("=== 调优建议 ===");
        System.out.println();
        System.out.println("1. 确定调优目标:");
        System.out.println("   - 吞吐量优先 → Parallel GC");
        System.out.println("   - 延迟优先   → G1 GC / ZGC");
        System.out.println("   - 内存占用   → Serial GC");
        System.out.println();
        System.out.println("2. 监控GC指标:");
        System.out.println("   - GC停顿时间 < 200ms");
        System.out.println("   - Full GC频率 < 1次/小时");
        System.out.println("   - GC占比 < 5%");
        System.out.println();
        System.out.println("3. 常见调优参数:");
        System.out.println("   -Xms = -Xmx          避免堆扩容");
        System.out.println("   -XX:MaxGCPauseMillis  目标停顿时间");
        System.out.println("   -XX:GCTimeRatio       GC时间占比目标");
        System.out.println("   -XX:+DisableExplicitGC 禁止System.gc()");
    }

    private static long getTotalGCCount(List<GarbageCollectorMXBean> gcBeans) {
        return gcBeans.stream().mapToLong(GarbageCollectorMXBean::getCollectionCount).sum();
    }

    private static long getTotalGCTime(List<GarbageCollectorMXBean> gcBeans) {
        return gcBeans.stream().mapToLong(GarbageCollectorMXBean::getCollectionTime).sum();
    }
}
