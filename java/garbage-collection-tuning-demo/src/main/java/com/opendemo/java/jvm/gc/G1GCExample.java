package com.opendemo.java.jvm.gc;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class G1GCExample {

    public static void main(String[] args) {
        System.out.println("=== G1 GC 演示 ===");
        System.out.println("启动参数: -XX:+UseG1GC -Xms256m -Xmx512m -Xlog:gc*");
        System.out.println();

        demonstrateRegionBasedCollection();
        demonstrateMixedGC();
        demonstrateHumongousObjects();
        printCharacteristics();
    }

    public static void demonstrateRegionBasedCollection() {
        System.out.println("--- Region分区收集演示 ---");
        System.out.println("G1将堆划分为多个等大小的Region(1-32MB)");
        System.out.println("每个Region可以是: Eden, Survivor, Old, Humongous, Free");
        System.out.println();

        long startTime = System.currentTimeMillis();

        List<byte[]> longLived = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            byte[] shortLived = new byte[5 * 1024];

            if (i % 100 == 0) {
                longLived.add(new byte[50 * 1024]);
            }
        }

        long duration = System.currentTimeMillis() - startTime;
        System.out.printf("混合分配耗时: %d ms%n", duration);
        System.out.printf("长期存活对象: %d 个%n", longLived.size());
        System.out.println();
    }

    public static void demonstrateMixedGC() {
        System.out.println("--- Mixed GC 演示 ---");
        System.out.println("Mixed GC同时回收新生代和部分老年代Region");
        System.out.println("触发条件: 并发标记完成后，选择收益最高的老年代Region");
        System.out.println();

        List<byte[]> oldGenCandidates = new ArrayList<>();
        Random random = new Random(42);

        for (int i = 0; i < 200; i++) {
            oldGenCandidates.add(new byte[100 * 1024]);
        }

        for (int i = 0; i < 50; i++) {
            int index = random.nextInt(oldGenCandidates.size());
            oldGenCandidates.set(index, null);
        }

        System.out.println("创建了200个长期对象，随机释放了50个");
        System.out.println("G1会选择回收率高的Region进行Mixed GC");
        System.out.println();

        System.out.println("Mixed GC参数:");
        System.out.println("  -XX:InitiatingHeapOccupancyPercent=45  触发并发标记的堆占用率");
        System.out.println("  -XX:G1MixedGCCountTarget=8             Mixed GC次数目标");
        System.out.println("  -XX:G1MixedGCLiveThresholdPercent=85   Region存活对象阈值");
        System.out.println();
    }

    public static void demonstrateHumongousObjects() {
        System.out.println("--- 大对象(Humongous)演示 ---");

        int regionSize = 1;
        System.out.printf("假设Region大小: %dMB%n", regionSize);
        System.out.println("大于Region大小50%的对象直接分配为Humongous对象");
        System.out.println();

        long startTime = System.currentTimeMillis();

        byte[] huge = new byte[2 * 1024 * 1024];
        System.out.printf("分配2MB大对象 (Humongous)%n");

        byte[] normal = new byte[256 * 1024];
        System.out.printf("分配256KB普通对象%n");

        long duration = System.currentTimeMillis() - startTime;
        System.out.printf("分配耗时: %d ms%n", duration);

        System.out.println();
        System.out.println("大对象优化建议:");
        System.out.println("  1. 增大Region大小: -XX:G1HeapRegionSize=4m");
        System.out.println("  2. 避免频繁创建大对象");
        System.out.println("  3. 使用对象池复用大对象");
    }

    public static void printCharacteristics() {
        System.out.println();
        System.out.println("=== G1 GC 特点 ===");
        System.out.println("优点:");
        System.out.println("  - 停顿时间可预测");
        System.out.println("  - 适合大堆(>4GB)");
        System.out.println("  - 无内存碎片");
        System.out.println("  - Java 9+ 默认GC");
        System.out.println();
        System.out.println("缺点:");
        System.out.println("  - 额外内存开销(约10-20%)");
        System.out.println("  - 小堆性能不如Parallel GC");
        System.out.println();
        System.out.println("适用场景:");
        System.out.println("  - 大堆内存应用(>4GB)");
        System.out.println("  - 需要低延迟的服务");
        System.out.println("  - 一般服务端应用");
        System.out.println();
        System.out.println("推荐参数:");
        System.out.println("  -XX:+UseG1GC -XX:MaxGCPauseMillis=200");
        System.out.println("  -XX:G1HeapRegionSize=4m -XX:InitiatingHeapOccupancyPercent=45");
    }
}
