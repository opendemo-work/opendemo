package com.opendemo.java.jvm.gc;

import java.util.ArrayList;
import java.util.List;

public class SerialGCExample {

    public static void main(String[] args) {
        System.out.println("=== Serial GC 演示 ===");
        System.out.println("启动参数: -XX:+UseSerialGC -Xms64m -Xmx128m -Xlog:gc*");
        System.out.println();

        demonstrateYoungGC();
        demonstrateOldGC();
        printCharacteristics();
    }

    public static void demonstrateYoungGC() {
        System.out.println("--- Young GC 演示 ---");

        long startTime = System.currentTimeMillis();
        List<byte[]> survivors = new ArrayList<>();

        for (int i = 0; i < 50; i++) {
            byte[] shortLived = new byte[100 * 1024];

            if (i % 10 == 0) {
                survivors.add(new byte[50 * 1024]);
            }
        }

        long duration = System.currentTimeMillis() - startTime;
        System.out.printf("Young GC耗时: %d ms%n", duration);
        System.out.printf("存活对象数: %d%n", survivors.size());
        System.out.println();
    }

    public static void demonstrateOldGC() {
        System.out.println("--- Old GC (Full GC) 演示 ---");

        List<byte[]> longLived = new ArrayList<>();
        long startTime = System.currentTimeMillis();

        try {
            for (int i = 0; i < 200; i++) {
                longLived.add(new byte[512 * 1024]);

                if (i % 20 == 0) {
                    System.out.printf("  已分配 %d MB, 已使用: %d MB%n",
                            (i + 1) / 2, GCDemo.getUsedMemoryMB());
                }
            }
        } catch (OutOfMemoryError e) {
            System.out.println("  触发OutOfMemoryError!");
        }

        long duration = System.currentTimeMillis() - startTime;
        System.out.printf("Full GC耗时: %d ms%n", duration);
        System.out.println();
    }

    public static void printCharacteristics() {
        System.out.println("=== Serial GC 特点 ===");
        System.out.println("优点:");
        System.out.println("  - 单线程，实现简单");
        System.out.println("  - 小堆内存效率高");
        System.out.println("  - 资源消耗少");
        System.out.println();
        System.out.println("缺点:");
        System.out.println("  - GC停顿时间长（STW）");
        System.out.println("  - 不适合大堆和多核环境");
        System.out.println();
        System.out.println("适用场景:");
        System.out.println("  - 客户端应用");
        System.out.println("  - 小型微服务（堆<200MB）");
        System.out.println("  - 开发测试环境");
        System.out.println();
        System.out.println("推荐参数:");
        System.out.println("  -XX:+UseSerialGC -Xms64m -Xmx128m");
    }
}
