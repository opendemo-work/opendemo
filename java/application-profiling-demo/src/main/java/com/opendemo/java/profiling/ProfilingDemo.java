package com.opendemo.java.profiling;

public class ProfilingDemo {

    public static void main(String[] args) {
        System.out.println("=== Java应用性能分析演示 ===");
        System.out.println();

        JmxProfilingDemo.main(args);
        System.out.println();

        CpuProfilingDemo.main(args);
        System.out.println();

        MemoryProfilingDemo.main(args);
        System.out.println();

        PerformanceBenchmark.main(args);
        System.out.println();

        HotspotDemo.main(args);
    }
}
