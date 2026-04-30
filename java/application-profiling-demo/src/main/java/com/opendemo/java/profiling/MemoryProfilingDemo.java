package com.opendemo.java.profiling;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryPoolMXBean;
import java.lang.management.MemoryUsage;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MemoryProfilingDemo {

    public static void main(String[] args) {
        demonstrateHeapProfiling();
        demonstrateAllocationRate();
        demonstrateMemoryFootprint();
        demonstrateGCImpact();
        printMemoryProfilingGuide();
    }

    public static void demonstrateHeapProfiling() {
        System.out.println("=== 堆内存分析 ===");

        MemoryMXBean memBean = ManagementFactory.getMemoryMXBean();
        MemoryUsage heapUsage = memBean.getHeapMemoryUsage();

        System.out.printf("堆初始: %d MB%n", heapUsage.getInit() / (1024 * 1024));
        System.out.printf("堆已用: %d MB%n", heapUsage.getUsed() / (1024 * 1024));
        System.out.printf("堆已提交: %d MB%n", heapUsage.getCommitted() / (1024 * 1024));
        System.out.printf("堆最大: %d MB%n", heapUsage.getMax() / (1024 * 1024));

        double usagePercent = (double) heapUsage.getUsed() / heapUsage.getMax() * 100;
        System.out.printf("堆使用率: %.1f%%%n", usagePercent);

        MemoryUsage nonHeapUsage = memBean.getNonHeapMemoryUsage();
        System.out.printf("非堆已用: %d MB%n", nonHeapUsage.getUsed() / (1024 * 1024));
        System.out.println();
    }

    public static void demonstrateAllocationRate() {
        System.out.println("=== 内存分配速率 ===");

        Runtime runtime = Runtime.getRuntime();

        long usedBefore = runtime.totalMemory() - runtime.freeMemory();
        long startTime = System.nanoTime();

        List<byte[]> objects = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            objects.add(new byte[1024]);
        }

        long duration = System.nanoTime() - startTime;
        long usedAfter = runtime.totalMemory() - runtime.freeMemory();

        long allocatedBytes = usedAfter - usedBefore;
        double allocRateMBps = (allocatedBytes / (1024.0 * 1024.0)) / (duration / 1_000_000_000.0);

        System.out.printf("分配对象数: 1000 (各1KB)%n");
        System.out.printf("分配内存: %d KB%n", allocatedBytes / 1024);
        System.out.printf("分配耗时: %.3f ms%n", duration / 1_000_000.0);
        System.out.printf("分配速率: %.1f MB/s%n", allocRateMBps);
        System.out.println();
    }

    public static void demonstrateMemoryFootprint() {
        System.out.println("=== 不同数据结构内存占用对比 ===");

        Runtime runtime = Runtime.getRuntime();

        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        long baseline = runtime.totalMemory() - runtime.freeMemory();

        int count = 100_000;

        List<Integer> arrayList = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            arrayList.add(Integer.valueOf(i));
        }

        long afterArrayList = runtime.totalMemory() - runtime.freeMemory();
        long arrayListBytes = afterArrayList - baseline;

        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        long baseline2 = runtime.totalMemory() - runtime.freeMemory();

        int[] primitiveArray = new int[count];
        for (int i = 0; i < count; i++) {
            primitiveArray[i] = i;
        }

        long afterPrimitive = runtime.totalMemory() - runtime.freeMemory();
        long primitiveBytes = afterPrimitive - baseline2;

        System.out.printf("100,000个Integer (ArrayList): ~%d KB%n", arrayListBytes / 1024);
        System.out.printf("100,000个int (原始数组):     ~%d KB%n", primitiveBytes / 1024);
        System.out.printf("装箱开销: ~%.1fx%n", (double) arrayListBytes / primitiveBytes);

        System.out.println();
        System.out.println("结论: 使用原始类型数组比包装类型集合节省大量内存");
        System.out.println();
    }

    public static void demonstrateGCImpact() {
        System.out.println("=== GC对性能的影响 ===");

        long startNoGC = System.nanoTime();
        long sum = 0;
        for (long i = 0; i < 100_000_000L; i++) {
            sum += i;
        }
        long durationNoGC = System.nanoTime() - startNoGC;

        long startWithGC = System.nanoTime();
        long sum2 = 0;
        for (long i = 0; i < 100_000_000L; i++) {
            sum2 += i;
            if (i % 10_000_000 == 0 && i > 0) {
                byte[] temp = new byte[1024 * 1024];
                sum2 += temp.length;
            }
        }
        long durationWithGC = System.nanoTime() - startWithGC;

        System.out.printf("无内存分配: %.3f ms (sum=%d)%n", durationNoGC / 1_000_000.0, sum);
        System.out.printf("有内存分配: %.3f ms (sum=%d)%n", durationWithGC / 1_000_000.0, sum2);
        System.out.printf("GC开销: %.1f%%%n",
                (1 - (double) durationNoGC / durationWithGC) * 100);
        System.out.println("减少不必要的对象分配可显著提升性能");
        System.out.println();
    }

    public static void printMemoryProfilingGuide() {
        System.out.println("=== 内存分析工具指南 ===");
        System.out.println();
        System.out.println("命令行工具:");
        System.out.println("  jmap -heap <pid>         查看堆配置和使用情况");
        System.out.println("  jmap -histo <pid>        查看对象直方图");
        System.out.println("  jmap -dump <pid>         生成堆转储");
        System.out.println("  jcmd <pid> GC.heap_info  查看GC堆信息");
        System.out.println();
        System.out.println("可视化工具:");
        System.out.println("  jvisualvm     JVM可视化监控");
        System.out.println("  JConsole      轻量级监控工具");
        System.out.println("  MAT           堆转储分析");
        System.out.println("  YourKit       商业性能分析工具");
        System.out.println("  JProfiler     商业性能分析工具");
        System.out.println();
        System.out.println("JVM参数:");
        System.out.println("  -XX:+PrintGCDetails                    打印GC详情");
        System.out.println("  -XX:+HeapDumpOnOutOfMemoryError       OOM时自动转储");
        System.out.println("  -XX:HeapDumpPath=/path/to/dumps        转储路径");
        System.out.println("  -Xlog:gc*=info:file=gc.log             Java 9+ GC日志");
    }
}
