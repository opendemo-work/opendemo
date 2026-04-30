package com.opendemo.java.jvm.memory;

import java.util.ArrayList;
import java.util.List;

public class HeapDemo {

    public static void main(String[] args) {
        demonstrateHeapGrowth();
        demonstrateHeapRegions();
        demonstrateObjectAging();
    }

    public static void demonstrateHeapGrowth() {
        System.out.println("=== 堆内存增长演示 ===");

        Runtime runtime = Runtime.getRuntime();
        printMemoryStats("初始状态");

        List<byte[]> buffers = new ArrayList<>();

        for (int i = 1; i <= 5; i++) {
            buffers.add(new byte[1024 * 1024]);
            printMemoryStats("分配 " + i + " MB 后");
        }

        buffers.subList(0, 3).clear();
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        printMemoryStats("释放3MB并GC后");

        buffers.clear();
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        printMemoryStats("全部释放并GC后");
        System.out.println();
    }

    public static void demonstrateHeapRegions() {
        System.out.println("=== 堆内存区域演示 ===");

        System.out.println("新生代 (Young Generation):");
        System.out.println("  - Eden区: 新对象首先分配在此");
        System.out.println("  - Survivor 0 (From): 第一次GC存活的对象");
        System.out.println("  - Survivor 1 (To): 第二次GC存活的对象");
        System.out.println();

        System.out.println("老年代 (Old Generation):");
        System.out.println("  - 经过多次GC仍然存活的对象");
        System.out.println("  - 大对象直接进入老年代 (-XX:PretenureSizeThreshold)");
        System.out.println();

        for (int i = 0; i < 100_000; i++) {
            String temp = new String("young-gen-object-" + i);
        }

        System.out.println("创建了10万个短生命周期对象（Young GC回收）");

        List<Object> longLived = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            longLived.add(new byte[1024]);
        }

        System.out.println("创建了1000个长期存活对象（将晋升到老年代）");
        System.out.println();
    }

    public static void demonstrateObjectAging() {
        System.out.println("=== 对象年龄与晋升演示 ===");

        List<byte[]> survivors = new ArrayList<>();

        for (int age = 1; age <= 6; age++) {
            survivors.add(new byte[128 * 1024]);

            byte[] shortLived = new byte[512 * 1024];
            shortLived = null;

            System.gc();
            try { Thread.sleep(50); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

            Runtime runtime = Runtime.getRuntime();
            long usedMB = (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
            System.out.printf("GC第%d次后，存活对象集合大小=%d，已使用堆=%dMB%n",
                    age, survivors.size(), usedMB);
        }

        System.out.println("默认晋升年龄阈值: 15 (可通过 -XX:MaxTenuringThreshold 调整)");
    }

    private static void printMemoryStats(String label) {
        Runtime runtime = Runtime.getRuntime();
        long total = runtime.totalMemory() / (1024 * 1024);
        long free = runtime.freeMemory() / (1024 * 1024);
        long max = runtime.maxMemory() / (1024 * 1024);
        long used = total - free;
        System.out.printf("  [%s] 已使用: %dMB, 已分配: %dMB, 最大可用: %dMB%n", label, used, total, max);
    }
}
