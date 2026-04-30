package com.opendemo.java.diagnostic;

import java.lang.management.*;

public class HeapInfoDemo {
    public static void main(String[] args) {
        System.out.println("=== Heap Info Demo ===\n");
        printHeapInfo();
        printMemoryPoolInfo();
        demonstrateObjectAllocation();
        printClassLoadingInfo();
    }

    static void printHeapInfo() {
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        System.out.println("1. Heap Memory Usage:");
        MemoryUsage heapUsage = memoryBean.getHeapMemoryUsage();
        System.out.printf("  Init: %d MB%n", heapUsage.getInit() / (1024 * 1024));
        System.out.printf("  Used: %d MB%n", heapUsage.getUsed() / (1024 * 1024));
        System.out.printf("  Committed: %d MB%n", heapUsage.getCommitted() / (1024 * 1024));
        System.out.printf("  Max: %d MB%n", heapUsage.getMax() / (1024 * 1024));

        System.out.println("\n  Non-Heap Memory Usage:");
        MemoryUsage nonHeap = memoryBean.getNonHeapMemoryUsage();
        System.out.printf("  Used: %d MB%n", nonHeap.getUsed() / (1024 * 1024));
        System.out.printf("  Committed: %d MB%n", nonHeap.getCommitted() / (1024 * 1024));
        System.out.println();
    }

    static void printMemoryPoolInfo() {
        System.out.println("2. Memory Pool Info:");
        for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
            MemoryUsage usage = pool.getUsage();
            if (usage != null) {
                System.out.printf("  Pool: %s%n", pool.getName());
                System.out.printf("    Type: %s%n", pool.getType());
                System.out.printf("    Used: %d MB / %d MB%n",
                        usage.getUsed() / (1024 * 1024),
                        usage.getMax() == -1 ? usage.getCommitted() : usage.getMax() / (1024 * 1024));
            }
        }
        System.out.println();
    }

    static void demonstrateObjectAllocation() {
        System.out.println("3. Object Allocation Impact:");
        Runtime runtime = Runtime.getRuntime();
        long before = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("  Memory before allocation: %d MB%n", before / (1024 * 1024));

        byte[][] data = new byte[100][];
        for (int i = 0; i < 100; i++) {
            data[i] = new byte[1024 * 1024];
        }

        long after = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("  Memory after allocating 100MB: %d MB%n", after / (1024 * 1024));
        System.out.printf("  Delta: %d MB%n", (after - before) / (1024 * 1024));
        data = null;
        System.out.println();
    }

    static void printClassLoadingInfo() {
        System.out.println("4. Class Loading Info:");
        ClassLoadingMXBean classBean = ManagementFactory.getClassLoadingMXBean();
        System.out.printf("  Loaded Classes: %d%n", classBean.getLoadedClassCount());
        System.out.printf("  Total Loaded: %d%n", classBean.getTotalLoadedClassCount());
        System.out.printf("  Unloaded: %d%n", classBean.getUnloadedClassCount());
        System.out.println();
    }
}
