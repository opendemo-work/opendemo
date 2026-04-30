package com.opendemo.java.jvm;

import java.lang.management.*;

public class MemoryStructureDemo {
    public static void main(String[] args) {
        System.out.println("=== JVM Memory Structure Demo ===\n");
        printHeapMemory();
        printNonHeapMemory();
        printMemoryPools();
        printVmArguments();
    }

    static void printHeapMemory() {
        System.out.println("1. Heap Memory (Young + Old Generation):");
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        MemoryUsage heap = memoryBean.getHeapMemoryUsage();
        System.out.printf("  Init:      %8d KB%n", heap.getInit() / 1024);
        System.out.printf("  Used:      %8d KB%n", heap.getUsed() / 1024);
        System.out.printf("  Committed: %8d KB%n", heap.getCommitted() / 1024);
        System.out.printf("  Max:       %8d KB%n", heap.getMax() / 1024);
        double usagePercent = (double) heap.getUsed() / heap.getMax() * 100;
        System.out.printf("  Usage:     %.1f%%%n", usagePercent);
        System.out.println();
    }

    static void printNonHeapMemory() {
        System.out.println("2. Non-Heap Memory (Metaspace + Code Cache):");
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        MemoryUsage nonHeap = memoryBean.getNonHeapMemoryUsage();
        System.out.printf("  Used:      %8d KB%n", nonHeap.getUsed() / 1024);
        System.out.printf("  Committed: %8d KB%n", nonHeap.getCommitted() / 1024);
        System.out.println();
    }

    static void printMemoryPools() {
        System.out.println("3. Memory Pools (Detailed):");
        for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
            MemoryUsage usage = pool.getUsage();
            if (usage != null) {
                System.out.printf("  [%s] %s%n", pool.getType(), pool.getName());
                System.out.printf("    Used: %d KB / Max: %d KB%n",
                        usage.getUsed() / 1024,
                        (usage.getMax() == -1 ? "N/A" : usage.getMax() / 1024 + ""));
            }
        }
        System.out.println();
    }

    static void printVmArguments() {
        System.out.println("4. Runtime Memory Config:");
        Runtime runtime = Runtime.getRuntime();
        System.out.printf("  Max Memory (-Xmx): %d MB%n", runtime.maxMemory() / (1024 * 1024));
        System.out.printf("  Total Memory:      %d MB%n", runtime.totalMemory() / (1024 * 1024));
        System.out.printf("  Free Memory:       %d MB%n", runtime.freeMemory() / (1024 * 1024));

        RuntimeMXBean runtimeBean = ManagementFactory.getRuntimeMXBean();
        System.out.println("  VM Arguments:");
        for (String arg : runtimeBean.getInputArguments()) {
            System.out.println("    " + arg);
        }
        System.out.println();
    }
}
