package com.opendemo.java.jvm.memory;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.WeakHashMap;

public class MemoryLeakDemo {

    public static void main(String[] args) {
        demonstrateStaticCollectionLeak();
        demonstrateUnclosedResourceLeak();
        demonstrateKeyInHashMapLeak();
        demonstrateThreadLocalLeak();
        demonstrateLeakDetection();
    }

    public static void demonstrateStaticCollectionLeak() {
        System.out.println("=== 静态集合导致的内存泄漏 ===");

        long beforeMem = getUsedMemoryMB();
        System.out.printf("泄漏前内存: %d MB%n", beforeMem);

        for (int i = 0; i < 10000; i++) {
            StaticLeakHolder.cache.put("key-" + i, new byte[1024]);
        }

        long afterMem = getUsedMemoryMB();
        System.out.printf("泄漏后内存: %d MB (增长 %d MB)%n", afterMem, afterMem - beforeMem);
        System.out.println("问题: 静态Map持续增长，对象无法被GC回收");
        System.out.println("修复: 使用WeakHashMap或定期清理缓存");
        System.out.println();

        StaticLeakHolder.cache.clear();
    }

    public static void demonstrateUnclosedResourceLeak() {
        System.out.println("=== 未关闭资源导致的泄漏 ===");

        System.out.println("常见场景:");
        System.out.println("  1. 数据库连接未关闭");
        System.out.println("  2. 文件流未关闭");
        System.out.println("  3. 网络连接未关闭");
        System.out.println();

        System.out.println("正确做法 - try-with-resources:");
        System.out.println("  try (Connection conn = dataSource.getConnection()) {");
        System.out.println("      // 使用连接");
        System.out.println("  } // 自动关闭");
        System.out.println();

        System.out.println("错误做法:");
        System.out.println("  Connection conn = dataSource.getConnection();");
        System.out.println("  // 使用连接后忘记关闭");
        System.out.println("  // 连接池中的连接被耗尽");
        System.out.println();
    }

    public static void demonstrateKeyInHashMapLeak() {
        System.out.println("=== HashMap键对象导致的泄漏 ===");

        Map<BadKey, String> map = new HashMap<>();

        for (int i = 0; i < 1000; i++) {
            BadKey key = new BadKey(i);
            map.put(key, "value-" + i);
            key.setValue(i + 1000);
        }

        System.out.println("Map大小: " + map.size());
        System.out.println("问题: BadKey的hashCode在put后改变，导致无法正确查找和删除");
        System.out.println("修复: 使用不可变对象作为Map的键");
        System.out.println("规则: equals和hashCode必须基于不可变字段");
        System.out.println();
    }

    public static void demonstrateThreadLocalLeak() {
        System.out.println("=== ThreadLocal泄漏 ===");

        System.out.println("场景: 线程池中ThreadLocal未清理");
        System.out.println("  1. 线程被复用，ThreadLocal值累积");
        System.out.println("  2. 大对象存储在ThreadLocal中");
        System.out.println();

        System.out.println("正确做法:");
        System.out.println("  threadLocal.set(largeObject);");
        System.out.println("  try {");
        System.out.println("      // 使用");
        System.out.println("  } finally {");
        System.out.println("      threadLocal.remove(); // 清理");
        System.out.println("  }");
        System.out.println();
    }

    public static void demonstrateLeakDetection() {
        System.out.println("=== 内存泄漏检测方法 ===");

        System.out.println("1. 堆内存对比:");
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        long baseline = getUsedMemoryMB();
        System.out.printf("   基线内存: %d MB%n", baseline);

        List<byte[]> suspectedLeak = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            suspectedLeak.add(new byte[10 * 1024]);
        }

        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        long afterOp = getUsedMemoryMB();
        System.out.printf("   操作后内存: %d MB (增长 %d MB)%n", afterOp, afterOp - baseline);

        suspectedLeak.clear();
        suspectedLeak = null;

        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        long afterGC = getUsedMemoryMB();
        System.out.printf("   清理后内存: %d MB%n", afterGC);
        System.out.println();

        System.out.println("2. 工具检测:");
        System.out.println("   - jmap -histo:pid  (查看对象直方图)");
        System.out.println("   - jmap -dump:format=b,file=heap.bin <pid>  (堆转储)");
        System.out.println("   - VisualVM / MAT 分析堆转储");
        System.out.println("   - -XX:+HeapDumpOnOutOfMemoryError (OOM时自动转储)");
        System.out.println();

        System.out.println("3. JMX监控:");
        MemoryMXBean mbean = ManagementFactory.getMemoryMXBean();
        MemoryUsage usage = mbean.getHeapMemoryUsage();
        double usagePercent = (double) usage.getUsed() / usage.getMax() * 100;
        System.out.printf("   当前堆使用率: %.1f%%%n", usagePercent);
        System.out.println("   建议设置告警阈值: 80%");
    }

    private static long getUsedMemoryMB() {
        Runtime runtime = Runtime.getRuntime();
        return (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
    }

    static class StaticLeakHolder {
        static final Map<String, byte[]> cache = new HashMap<>();
    }

    static class BadKey {
        private int value;

        BadKey(int value) {
            this.value = value;
        }

        void setValue(int value) {
            this.value = value;
        }

        @Override
        public int hashCode() {
            return value;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (!(obj instanceof BadKey)) return false;
            return value == ((BadKey) obj).value;
        }
    }
}
