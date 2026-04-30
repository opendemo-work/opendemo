package com.opendemo.java.jvm.gc;

import java.lang.management.GarbageCollectorMXBean;
import java.lang.management.ManagementFactory;
import java.util.List;

public class GCLogDemo {

    public static void main(String[] args) {
        demonstrateGCLogFlags();
        demonstrateGCLogAnalysis();
        generateGCLoad();
    }

    public static void demonstrateGCLogFlags() {
        System.out.println("=== GC日志参数 ===");
        System.out.println();
        System.out.println("Java 8 GC日志参数:");
        System.out.println("  -XX:+PrintGC                    打印GC基本信息");
        System.out.println("  -XX:+PrintGCDetails             打印GC详细信息");
        System.out.println("  -XX:+PrintGCTimeStamps          打印GC时间戳");
        System.out.println("  -XX:+PrintGCDateStamps          打印GC日期时间戳");
        System.out.println("  -XX:+PrintGCApplicationStoppedTime  打印停顿时间");
        System.out.println("  -Xloggc:/path/to/gc.log         GC日志输出到文件");
        System.out.println();
        System.out.println("Java 9+ 统一日志参数:");
        System.out.println("  -Xlog:gc                        打印GC基本信息");
        System.out.println("  -Xlog:gc*                       打印所有GC信息");
        System.out.println("  -Xlog:gc*=info                  info级别GC日志");
        System.out.println("  -Xlog:gc*:file=/path/to/gc.log  输出到文件");
        System.out.println("  -Xlog:gc+heap=debug             堆详细信息");
        System.out.println("  -Xlog:gc+phases=debug           GC阶段信息");
        System.out.println();
    }

    public static void demonstrateGCLogAnalysis() {
        System.out.println("=== GC日志分析要点 ===");
        System.out.println();
        System.out.println("关注指标:");
        System.out.println("  1. GC停顿时间 (Pause Time)");
        System.out.println("  2. GC频率 (Frequency)");
        System.out.println("  3. 各区域回收前后大小变化");
        System.out.println("  4. Full GC的触发原因");
        System.out.println();

        System.out.println("G1 GC日志示例:");
        System.out.println("  [GC pause (G1 Evacuation Pause) (young), 0.0123456 secs]");
        System.out.println("  [Eden: 256.0M(256.0M)->0.0B(230.0M)");
        System.out.println("   Survivors: 0.0B->26.0M");
        System.out.println("   Heap: 256.0M(512.0M)->24.5M(512.0M)]");
        System.out.println();

        System.out.println("分析工具:");
        System.out.println("  1. GCViewer        - 可视化GC日志分析");
        System.out.println("  2. GCEasy          - 在线GC日志分析 (https://gceasy.io)");
        System.out.println("  3. JClarity Censum - 商业GC分析工具");
        System.out.println();
    }

    public static void generateGCLoad() {
        System.out.println("=== 生成GC负载 ===");

        List<GarbageCollectorMXBean> gcBeansBefore = ManagementFactory.getGarbageCollectorMXBeans();
        long totalGcCountBefore = gcBeansBefore.stream()
                .mapToLong(GarbageCollectorMXBean::getCollectionCount)
                .sum();
        long totalGcTimeBefore = gcBeansBefore.stream()
                .mapToLong(GarbageCollectorMXBean::getCollectionTime)
                .sum();

        System.out.printf("GC前: 总次数=%d, 总时间=%dms%n", totalGcCountBefore, totalGcTimeBefore);

        for (int round = 0; round < 10; round++) {
            byte[][] chunks = new byte[100][];
            for (int i = 0; i < 100; i++) {
                chunks[i] = new byte[50 * 1024];
            }
        }

        List<GarbageCollectorMXBean> gcBeansAfter = ManagementFactory.getGarbageCollectorMXBeans();
        long totalGcCountAfter = gcBeansAfter.stream()
                .mapToLong(GarbageCollectorMXBean::getCollectionCount)
                .sum();
        long totalGcTimeAfter = gcBeansAfter.stream()
                .mapToLong(GarbageCollectorMXBean::getCollectionTime)
                .sum();

        System.out.printf("GC后: 总次数=%d, 总时间=%dms%n", totalGcCountAfter, totalGcTimeAfter);
        System.out.printf("GC增量: 次数=%d, 时间=%dms%n",
                totalGcCountAfter - totalGcCountBefore,
                totalGcTimeAfter - totalGcTimeBefore);
    }
}
