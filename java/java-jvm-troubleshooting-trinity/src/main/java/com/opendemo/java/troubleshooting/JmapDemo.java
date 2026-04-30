package com.opendemo.java.troubleshooting;

import java.lang.management.*;

public class JmapDemo {
    public static void main(String[] args) {
        System.out.println("=== Jmap Demo (via MXBeans) ===\n");
        printHeapSummary();
        printHistogram();
        printHeapDetails();
    }

    static void printHeapSummary() {
        System.out.println("1. Heap Summary (-heap equivalent):");
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        MemoryUsage heap = memoryBean.getHeapMemoryUsage();

        System.out.println("  Heap Configuration:");
        System.out.printf("    MinHeapFreeRatio:    N/A (use -XX:MinHeapFreeRatio)%n");
        System.out.printf("    MaxHeapFreeRatio:    N/A (use -XX:MaxHeapFreeRatio)%n");
        System.out.printf("    MaxHeapSize:         %d MB%n", heap.getMax() / (1024 * 1024));
        System.out.printf("    NewSize:             (see memory pools)%n");
        System.out.println();
        System.out.println("  Heap Usage:");
        System.out.printf("    Used:    %d MB%n", heap.getUsed() / (1024 * 1024));
        System.out.printf("    Capacity:%d MB%n", heap.getCommitted() / (1024 * 1024));
        double usagePercent = heap.getMax() > 0 ? (double) heap.getUsed() / heap.getMax() * 100 : 0;
        System.out.printf("    Usage:   %.1f%%%n", usagePercent);
        System.out.println();
    }

    static void printHistogram() {
        System.out.println("2. Object Histogram (-histo equivalent):");
        System.out.printf("  %-40s %10s %10s%n", "Class", "Instances", "Estimated KB");
        System.out.println("  " + "-".repeat(65));

        Object[] samples = {
                "string1", "string2", "string3",
                1, 2, 3, 4, 5,
                new int[100], new int[200],
                new java.util.ArrayList<>(), new java.util.HashMap<>(),
                new Object(), new Object(), new Object()
        };

        java.util.Map<String, long[]> counts = new java.util.LinkedHashMap<>();
        for (Object obj : samples) {
            String className = obj.getClass().getName();
            counts.computeIfAbsent(className, k -> new long[]{0, 0});
            counts.get(className)[0]++;
            counts.get(className)[1] += estimateSize(obj);
        }

        counts.entrySet().stream()
                .sorted((a, b) -> Long.compare(b.getValue()[1], a.getValue()[1]))
                .limit(10)
                .forEach(e -> System.out.printf("  %-40s %10d %10d%n",
                        e.getKey(), e.getValue()[0], e.getValue()[1] / 1024));
        System.out.println();
    }

    static void printHeapDetails() {
        System.out.println("3. Memory Pool Details:");
        for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
            MemoryUsage usage = pool.getUsage();
            MemoryUsage peak = pool.getPeakUsage();
            if (usage == null) continue;
            System.out.printf("  %s [%s]%n", pool.getName(), pool.getType());
            System.out.printf("    Current: used=%d KB, max=%d KB%n",
                    usage.getUsed() / 1024,
                    (usage.getMax() == -1 ? "N/A" : usage.getMax() / 1024 + ""));
            if (peak != null) {
                System.out.printf("    Peak:    used=%d KB%n", peak.getUsed() / 1024);
            }
        }
        System.out.println();
    }

    private static long estimateSize(Object obj) {
        if (obj instanceof String) return ((String) obj).length() * 2L + 40;
        if (obj instanceof Integer) return 16;
        if (obj instanceof int[]) return ((int[]) obj).length * 4L + 16;
        if (obj instanceof java.util.ArrayList) return 48;
        if (obj instanceof java.util.HashMap) return 64;
        return 16;
    }
}
