package com.opendemo.java.jvm.gc;

import java.lang.management.GarbageCollectorMXBean;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;
import java.util.List;

public class GCDemo {

    public static void main(String[] args) {
        demonstrateSystemGC();
        demonstrateFinalize();
        demonstrateGCMXBean();
        demonstrateGCTypes();
    }

    public static void demonstrateSystemGC() {
        System.out.println("=== System.gc() 演示 ===");

        long before = getUsedMemoryMB();
        System.out.printf("GC前已使用内存: %d MB%n", before);

        byte[][] data = new byte[100][];
        for (int i = 0; i < 100; i++) {
            data[i] = new byte[1024 * 1024];
        }

        long afterAlloc = getUsedMemoryMB();
        System.out.printf("分配100MB后: %d MB%n", afterAlloc);

        data = null;

        System.gc();

        try { Thread.sleep(200); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        long afterGC = getUsedMemoryMB();
        System.out.printf("System.gc()后: %d MB%n", afterGC);
        System.out.println("注意: System.gc()仅为建议，JVM不保证立即执行");
        System.out.println();
    }

    public static void demonstrateFinalize() {
        System.out.println("=== finalize() 方法演示 ===");

        System.out.println("Java 9+ 推荐使用 Cleaner 替代 finalize()");
        System.out.println("finalize() 的问题:");
        System.out.println("  1. 不确定何时被调用");
        System.out.println("  2. 可能导致对象复活");
        System.out.println("  3. 性能开销大");
        System.out.println("  4. Java 9已标记为 @Deprecated(forRemoval=true)");
        System.out.println();

        for (int i = 0; i < 5; i++) {
            new FinalizableObject(i);
        }

        System.gc();
        try { Thread.sleep(500); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        System.out.println("建议替代方案:");
        System.out.println("  1. try-with-resources (AutoCloseable)");
        System.out.println("  2. java.lang.ref.Cleaner (Java 9+)");
        System.out.println("  3. 显式资源管理");
        System.out.println();
    }

    public static void demonstrateGCMXBean() {
        System.out.println("=== GarbageCollectorMXBean 信息 ===");

        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        for (GarbageCollectorMXBean gcBean : gcBeans) {
            System.out.printf("GC名称: %s%n", gcBean.getName());
            System.out.printf("  GC次数: %d%n", gcBean.getCollectionCount());
            System.out.printf("  GC总时间: %d ms%n", gcBean.getCollectionTime());
            System.out.printf("  管理的内存池: %s%n", gcBean.getMemoryPoolNames());
            System.out.println();
        }
    }

    public static void demonstrateGCTypes() {
        System.out.println("=== GC类型概览 ===");
        System.out.println("1. Serial GC    (-XX:+UseSerialGC)");
        System.out.println("   单线程，适合客户端应用和小堆");
        System.out.println();
        System.out.println("2. Parallel GC  (-XX:+UseParallelGC)");
        System.out.println("   多线程，Java 8默认，吞吐量优先");
        System.out.println();
        System.out.println("3. G1 GC        (-XX:+UseG1GC)");
        System.out.println("   分区收集，Java 9+默认，停顿时间可控");
        System.out.println();
        System.out.println("4. ZGC           (-XX:+UseZGC)");
        System.out.println("   超低延迟，Java 11+ (生产就绪于Java 15)");
        System.out.println();
        System.out.println("5. Shenandoah GC (-XX:+UseShenandoahGC)");
        System.out.println("   超低延迟，与ZGC竞争方案");
    }

    static long getUsedMemoryMB() {
        Runtime runtime = Runtime.getRuntime();
        return (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
    }

    static class FinalizableObject {
        private final int id;

        FinalizableObject(int id) {
            this.id = id;
        }

        @Override
        protected void finalize() throws Throwable {
            super.finalize();
            System.out.printf("  FinalizableObject-%d 被 finalize()%n", id);
        }
    }
}
