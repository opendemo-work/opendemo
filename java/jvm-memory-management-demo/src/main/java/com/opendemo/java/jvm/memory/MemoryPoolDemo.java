package com.opendemo.java.jvm.memory;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryPoolMXBean;
import java.lang.management.MemoryUsage;
import java.util.List;

public class MemoryPoolDemo {

    public static void main(String[] args) {
        listAllMemoryPools();
        monitorEdenSpace();
        monitorSurvivorSpace();
        monitorOldGen();
        demonstratePoolUsage();
    }

    public static void listAllMemoryPools() {
        System.out.println("=== 所有内存池信息 ===");

        List<MemoryPoolMXBean> pools = ManagementFactory.getMemoryPoolMXBeans();
        for (MemoryPoolMXBean pool : pools) {
            System.out.printf("内存池: %s%n", pool.getName());
            System.out.printf("  类型: %s%n", pool.getType());
            MemoryUsage usage = pool.getUsage();
            if (usage != null) {
                System.out.printf("  已使用: %d KB%n", usage.getUsed() / 1024);
                System.out.printf("  已提交: %d KB%n", usage.getCommitted() / 1024);
                System.out.printf("  最大: %d KB%n", usage.getMax() / 1024);
            }
            System.out.println();
        }
    }

    public static void monitorEdenSpace() {
        System.out.println("=== Eden区监控 ===");
        MemoryPoolMXBean edenPool = findPool("Eden");
        if (edenPool != null) {
            printPoolUsage(edenPool);
        } else {
            System.out.println("未找到Eden区（取决于GC算法）");
        }
        System.out.println();
    }

    public static void monitorSurvivorSpace() {
        System.out.println("=== Survivor区监控 ===");
        MemoryPoolMXBean survivorPool = findPool("Survivor");
        if (survivorPool != null) {
            printPoolUsage(survivorPool);
        } else {
            System.out.println("未找到Survivor区（取决于GC算法）");
        }
        System.out.println();
    }

    public static void monitorOldGen() {
        System.out.println("=== 老年代监控 ===");
        MemoryPoolMXBean oldGenPool = findPool("Old");
        if (oldGenPool != null) {
            printPoolUsage(oldGenPool);
        } else {
            System.out.println("未找到老年代（取决于GC算法）");
        }
        System.out.println();
    }

    public static void demonstratePoolUsage() {
        System.out.println("=== 内存池使用变化演示 ===");

        MemoryPoolMXBean edenPool = findPool("Eden");
        MemoryPoolMXBean oldPool = findPool("Old");

        if (edenPool != null) {
            System.out.println("分配前的Eden区:");
            printPoolUsage(edenPool);
        }

        byte[][] chunks = new byte[100][];
        for (int i = 0; i < 100; i++) {
            chunks[i] = new byte[64 * 1024];
        }

        if (edenPool != null) {
            System.out.println("分配6.4MB后的Eden区:");
            printPoolUsage(edenPool);
        }

        byte[][] keepAlive = new byte[10][];
        for (int i = 0; i < 10; i++) {
            keepAlive[i] = chunks[i];
        }

        chunks = null;
        System.gc();
        try { Thread.sleep(200); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        if (oldPool != null) {
            System.out.println("GC后存活对象晋升到老年代:");
            printPoolUsage(oldPool);
        }
    }

    private static MemoryPoolMXBean findPool(String keyword) {
        List<MemoryPoolMXBean> pools = ManagementFactory.getMemoryPoolMXBeans();
        for (MemoryPoolMXBean pool : pools) {
            if (pool.getName().contains(keyword)) {
                return pool;
            }
        }
        return null;
    }

    private static void printPoolUsage(MemoryPoolMXBean pool) {
        MemoryUsage usage = pool.getUsage();
        if (usage != null) {
            long usedKB = usage.getUsed() / 1024;
            long committedKB = usage.getCommitted() / 1024;
            long maxKB = usage.getMax() / 1024;
            double usedPercent = maxKB > 0 ? (usedKB * 100.0 / maxKB) : 0;
            System.out.printf("  [%s] 已使用: %dKB, 已提交: %dKB, 最大: %dKB (%.1f%%)%n",
                    pool.getName(), usedKB, committedKB, maxKB, usedPercent);
        }

        MemoryUsage peakUsage = pool.getPeakUsage();
        if (peakUsage != null) {
            System.out.printf("  峰值使用: %dKB%n", peakUsage.getUsed() / 1024);
        }
    }
}
