package com.opendemo.java.jvm;

import java.lang.management.*;

public class JitCompilationDemo {
    public static void main(String[] args) {
        System.out.println("=== JIT Compilation Demo ===\n");
        printCompilationInfo();
        demonstrateJitWarmup();
    }

    static void printCompilationInfo() {
        System.out.println("1. Compilation MXBean Info:");
        CompilationMXBean compBean = ManagementFactory.getCompilationMXBean();
        System.out.println("  JIT Compiler: " + compBean.getName());
        if (compBean.isCompilationTimeMonitoringSupported()) {
            System.out.println("  Total Compilation Time: " + compBean.getTotalCompilationTime() + " ms");
        }
        System.out.println();
    }

    static void demonstrateJitWarmup() {
        System.out.println("2. JIT Warm-up Demonstration:");
        CompilationMXBean compBean = ManagementFactory.getCompilationMXBean();
        boolean monitoring = compBean.isCompilationTimeMonitoringSupported();

        long compileTimeBefore = monitoring ? compBean.getTotalCompilationTime() : 0;

        long start = System.nanoTime();
        long result = 0;
        for (int i = 0; i < 1_000_000; i++) {
            result += hotMethod(i);
        }
        long elapsed = System.nanoTime() - start;

        long compileTimeAfter = monitoring ? compBean.getTotalCompilationTime() : 0;

        System.out.printf("  Computed result: %d%n", result);
        System.out.printf("  Execution time: %.2f ms%n", elapsed / 1_000_000.0);
        if (monitoring) {
            System.out.printf("  JIT compilation time delta: %d ms%n", compileTimeAfter - compileTimeBefore);
        }
        System.out.println();

        System.out.println("3. Second run (JIT should have optimized):");
        start = System.nanoTime();
        result = 0;
        for (int i = 0; i < 1_000_000; i++) {
            result += hotMethod(i);
        }
        elapsed = System.nanoTime() - start;
        System.out.printf("  Computed result: %d%n", result);
        System.out.printf("  Execution time: %.2f ms%n", elapsed / 1_000_000.0);
        System.out.println();
    }

    private static long hotMethod(int value) {
        long x = (long) value * value;
        x = x + value;
        x = x % (value + 1);
        return x;
    }
}
