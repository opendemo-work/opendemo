package com.opendemo.java.diagnostic;

import java.lang.management.*;
import java.util.*;

public class GcInfoDemo {
    public static void main(String[] args) {
        System.out.println("=== GC Info Demo ===\n");
        printGcInfo();
        triggerGcAndReport();
        printRuntimeInfo();
    }

    static void printGcInfo() {
        System.out.println("1. Garbage Collector Info:");
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        for (GarbageCollectorMXBean gc : gcBeans) {
            System.out.printf("  GC Name: %s%n", gc.getName());
            System.out.printf("    Collection Count: %d%n", gc.getCollectionCount());
            System.out.printf("    Collection Time: %d ms%n", gc.getCollectionTime());
            System.out.printf("    Memory Pools: %s%n", gc.getMemoryPoolNames() != null ?
                    String.join(", ", gc.getMemoryPoolNames()) : "N/A");
        }
        System.out.println();
    }

    static void triggerGcAndReport() {
        System.out.println("2. GC Before/After Comparison:");
        GarbageCollectorMXBean mainGc = ManagementFactory.getGarbageCollectorMXBeans().get(0);
        long countBefore = mainGc.getCollectionCount();
        long timeBefore = mainGc.getCollectionTime();

        System.out.printf("  Before GC: count=%d, time=%dms%n", countBefore, timeBefore);

        byte[] waste = new byte[10 * 1024 * 1024];
        waste = null;
        System.gc();

        long countAfter = mainGc.getCollectionCount();
        long timeAfter = mainGc.getCollectionTime();
        System.out.printf("  After GC:  count=%d, time=%dms%n", countAfter, timeAfter);
        System.out.printf("  Delta: %d collections, %dms%n", countAfter - countBefore, timeAfter - timeBefore);
        System.out.println();
    }

    static void printRuntimeInfo() {
        System.out.println("3. Runtime Memory Info:");
        Runtime runtime = Runtime.getRuntime();
        System.out.printf("  Max Memory: %d MB%n", runtime.maxMemory() / (1024 * 1024));
        System.out.printf("  Total Memory: %d MB%n", runtime.totalMemory() / (1024 * 1024));
        System.out.printf("  Free Memory: %d MB%n", runtime.freeMemory() / (1024 * 1024));
        System.out.printf("  Used Memory: %d MB%n", (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024));
        System.out.printf("  Available Processors: %d%n", runtime.availableProcessors());
        System.out.println();
    }
}
