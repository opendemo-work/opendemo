package com.opendemo.java.troubleshooting;

import java.lang.management.*;
import java.util.Arrays;

public class JstatDemo {
    public static void main(String[] args) {
        System.out.println("=== Jstat Demo (via MXBeans) ===\n");
        printGcSummary();
        printGcCapacity();
        printGcCause();
        monitorGc(3, 1000);
    }

    static void printGcSummary() {
        System.out.println("1. GC Summary (-gc equivalent):");
        Runtime runtime = Runtime.getRuntime();
        long eden = 0, survivor = 0, old = 0;
        for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
            MemoryUsage usage = pool.getUsage();
            if (usage == null) continue;
            String name = pool.getName().toLowerCase();
            if (name.contains("eden") || name.contains("young")) {
                eden = usage.getUsed();
            } else if (name.contains("survivor")) {
                survivor = usage.getUsed();
            } else if (name.contains("old") || name.contains("tenured")) {
                old = usage.getUsed();
            }
        }
        System.out.printf("  Eden:     %8d KB%n", eden / 1024);
        System.out.printf("  Survivor: %8d KB%n", survivor / 1024);
        System.out.printf("  Old:      %8d KB%n", old / 1024);
        for (GarbageCollectorMXBean gc : ManagementFactory.getGarbageCollectorMXBeans()) {
            System.out.printf("  GC[%s]: count=%d, time=%dms%n", gc.getName(), gc.getCollectionCount(), gc.getCollectionTime());
        }
        System.out.println();
    }

    static void printGcCapacity() {
        System.out.println("2. GC Capacity (-gccapacity equivalent):");
        for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
            MemoryUsage usage = pool.getUsage();
            if (usage == null) continue;
            System.out.printf("  %-40s Used: %6d KB, Max: %6d KB%n",
                    pool.getName(),
                    usage.getUsed() / 1024,
                    (usage.getMax() == -1 ? 0 : usage.getMax()) / 1024);
        }
        System.out.println();
    }

    static void printGcCause() {
        System.out.println("3. GC Statistics:");
        for (GarbageCollectorMXBean gc : ManagementFactory.getGarbageCollectorMXBeans()) {
            System.out.printf("  %s:%n", gc.getName());
            System.out.printf("    Collection Count: %d%n", gc.getCollectionCount());
            System.out.printf("    Collection Time:  %d ms%n", gc.getCollectionTime());
            long avgTime = gc.getCollectionCount() > 0 ? gc.getCollectionTime() / gc.getCollectionCount() : 0;
            System.out.printf("    Avg Time/Collection: %d ms%n", avgTime);
        }
        System.out.println();
    }

    static void monitorGc(int intervals, long intervalMs) {
        System.out.println("4. GC Monitoring (" + intervals + " samples, " + intervalMs + "ms interval):");
        GarbageCollectorMXBean gc = ManagementFactory.getGarbageCollectorMXBeans().get(0);
        for (int i = 0; i < intervals; i++) {
            System.out.printf("  [%d] count=%d, time=%dms, heap_used=%d MB%n",
                    i, gc.getCollectionCount(), gc.getCollectionTime(),
                    (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / (1024 * 1024));
            try { Thread.sleep(intervalMs); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
        System.out.println();
    }
}
