package com.opendemo.java.jvm.memory;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;

public class MemoryDemo {

    public static void main(String[] args) {
        demonstrateRuntimeApi();
        demonstrateMemoryMXBean();
        demonstrateHeapVsStack();
    }

    public static void demonstrateRuntimeApi() {
        Runtime runtime = Runtime.getRuntime();

        long maxMemory = runtime.maxMemory();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;

        System.out.println("=== Runtime API 内存信息 ===");
        System.out.printf("最大可用内存 (-Xmx): %d MB%n", maxMemory / (1024 * 1024));
        System.out.printf("当前已分配内存: %d MB%n", totalMemory / (1024 * 1024));
        System.out.printf("当前空闲内存: %d MB%n", freeMemory / (1024 * 1024));
        System.out.printf("当前已使用内存: %d MB%n", usedMemory / (1024 * 1024));
        System.out.printf("可用处理器数: %d%n", runtime.availableProcessors());
        System.out.println();
    }

    public static void demonstrateMemoryMXBean() {
        MemoryMXBean memoryMXBean = ManagementFactory.getMemoryMXBean();

        MemoryUsage heapUsage = memoryMXBean.getHeapMemoryUsage();
        MemoryUsage nonHeapUsage = memoryMXBean.getNonHeapMemoryUsage();

        System.out.println("=== MemoryMXBean 堆内存信息 ===");
        System.out.printf("初始内存: %d MB%n", heapUsage.getInit() / (1024 * 1024));
        System.out.printf("已使用内存: %d MB%n", heapUsage.getUsed() / (1024 * 1024));
        System.out.printf("已提交内存: %d MB%n", heapUsage.getCommitted() / (1024 * 1024));
        System.out.printf("最大内存: %d MB%n", heapUsage.getMax() / (1024 * 1024));
        System.out.println();

        System.out.println("=== MemoryMXBean 非堆内存信息 ===");
        System.out.printf("初始内存: %d MB%n", nonHeapUsage.getInit() / (1024 * 1024));
        System.out.printf("已使用内存: %d MB%n", nonHeapUsage.getUsed() / (1024 * 1024));
        System.out.printf("已提交内存: %d MB%n", nonHeapUsage.getCommitted() / (1024 * 1024));
        System.out.printf("最大内存: %d MB%n", nonHeapUsage.getMax() / (1024 * 1024));
        System.out.println();

        System.out.printf("待回收的对象数: %d%n", memoryMXBean.getObjectPendingFinalizationCount());
    }

    public static void demonstrateHeapVsStack() {
        System.out.println("=== 堆内存 vs 栈内存 ===");

        long heapBefore = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        HeapObject obj = new HeapObject(1024 * 1024);

        long heapAfter = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        System.out.printf("创建堆对象前已用内存: %d MB%n", heapBefore / (1024 * 1024));
        System.out.printf("创建堆对象后已用内存: %d MB%n", heapAfter / (1024 * 1024));
        System.out.printf("堆对象大致占用: %d MB%n", (heapAfter - heapBefore) / (1024 * 1024));
        System.out.println();

        demonstrateStackAllocation(5);
    }

    private static void demonstrateStackAllocation(int depth) {
        long localVar1 = System.currentTimeMillis();
        double localVar2 = Math.random();
        String localVar3 = "stack-frame-" + depth;

        System.out.printf("栈帧深度 %d: localVar1=%d, localVar2=%.4f, localVar3=%s%n",
                depth, localVar1, localVar2, localVar3);

        if (depth > 0) {
            demonstrateStackAllocation(depth - 1);
        }
    }

    static class HeapObject {
        private final byte[] data;

        HeapObject(int size) {
            this.data = new byte[size];
        }
    }
}
