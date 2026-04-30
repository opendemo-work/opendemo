package com.opendemo.java.profiling;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;

public class PerformanceBenchmark {

    public static void main(String[] args) {
        demonstrateSimpleBenchmark();
        demonstrateComparativeBenchmark();
        demonstrateWarmupEffect();
        printBenchmarkingBestPractices();
    }

    public static void demonstrateSimpleBenchmark() {
        System.out.println("=== 简单基准测试 ===");

        BenchmarkResult result = benchmark("字符串拼接", () -> {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 10000; i++) {
                sb.append("item-").append(i).append(",");
            }
            return sb.toString();
        }, 100);

        printResult(result);
        System.out.println();
    }

    public static void demonstrateComparativeBenchmark() {
        System.out.println("=== 对比基准测试 ===");

        int iterations = 50;
        int size = 10000;

        BenchmarkResult listResult = benchmark("ArrayList顺序访问", () -> {
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < size; i++) list.add(i);
            long sum = 0;
            for (int val : list) sum += val;
            return sum;
        }, iterations);

        BenchmarkResult mapResult = benchmark("HashMap随机访问", () -> {
            Map<Integer, Integer> map = new HashMap<>();
            for (int i = 0; i < size; i++) map.put(i, i);
            long sum = 0;
            for (int i = 0; i < size; i++) sum += map.get(i);
            return sum;
        }, iterations);

        printResult(listResult);
        printResult(mapResult);

        double speedup = (double) mapResult.avgNanos / listResult.avgNanos;
        System.out.printf("  ArrayList比HashMap快 %.2fx%n", speedup);
        System.out.println();
    }

    public static void demonstrateWarmupEffect() {
        System.out.println("=== 预热效果演示 (JIT编译) ===");

        System.out.println("观察每次迭代的时间变化:");
        System.out.println();

        for (int iteration = 1; iteration <= 15; iteration++) {
            long start = System.nanoTime();
            long sum = 0;
            for (int i = 0; i < 1_000_000; i++) {
                sum += fibonacciFast(30);
            }

            if (iteration <= 5 || iteration == 10 || iteration == 15) {
                double durationMs = (System.nanoTime() - start) / 1_000_000.0;
                System.out.printf("  第%2d次: %.3f ms (sum=%d)%n", iteration, durationMs, sum);
            }
        }

        System.out.println();
        System.out.println("前几次执行较慢（解释执行），后续JIT编译后显著加速");
        System.out.println("因此基准测试需要预热（warmup）阶段");
        System.out.println();
    }

    public static <T> BenchmarkResult benchmark(String name, Supplier<T> task, int iterations) {
        List<Long> durations = new ArrayList<>(iterations);

        for (int i = 0; i < 3; i++) {
            task.get();
        }

        for (int i = 0; i < iterations; i++) {
            long start = System.nanoTime();
            task.get();
            durations.add(System.nanoTime() - start);
        }

        long min = durations.stream().mapToLong(Long::longValue).min().orElse(0);
        long max = durations.stream().mapToLong(Long::longValue).max().orElse(0);
        double avg = durations.stream().mapToLong(Long::longValue).average().orElse(0);
        double variance = durations.stream()
                .mapToLong(Long::longValue)
                .mapToDouble(d -> Math.pow(d - avg, 2))
                .average().orElse(0);
        double stdDev = Math.sqrt(variance);

        BenchmarkResult result = new BenchmarkResult();
        result.name = name;
        result.iterations = iterations;
        result.minNanos = min;
        result.maxNanos = max;
        result.avgNanos = (long) avg;
        result.stdDevNanos = (long) stdDev;
        return result;
    }

    public static void printResult(BenchmarkResult result) {
        System.out.printf("  [%s] %d次迭代%n", result.name, result.iterations);
        System.out.printf("    平均: %.3f ms | 最小: %.3f ms | 最大: %.3f ms | 标准差: %.3f ms%n",
                result.avgNanos / 1_000_000.0,
                result.minNanos / 1_000_000.0,
                result.maxNanos / 1_000_000.0,
                result.stdDevNanos / 1_000_000.0);
    }

    public static void printBenchmarkingBestPractices() {
        System.out.println("=== 基准测试最佳实践 ===");
        System.out.println();
        System.out.println("1. 预热 (Warmup):");
        System.out.println("   JIT编译需要多次执行才能触发");
        System.out.println("   建议: 至少运行5-10次预热迭代");
        System.out.println();
        System.out.println("2. 多次测量:");
        System.out.println("   单次测量不可靠，受多种因素影响");
        System.out.println("   建议: 至少运行30次取统计值");
        System.out.println();
        System.out.println("3. 避免死代码消除:");
        System.out.println("   JIT可能优化掉未使用的结果");
        System.out.println("   建议: 使用结果（如打印或累加）");
        System.out.println();
        System.out.println("4. 控制变量:");
        System.out.println("   确保对比测试的其他条件相同");
        System.out.println("   建议: 相同JVM参数、系统负载");
        System.out.println();
        System.out.println("5. 推荐工具:");
        System.out.println("   JMH (Java Microbenchmark Harness)");
        System.out.println("   OpenJDK官方微基准测试框架");
    }

    private static long fibonacciFast(int n) {
        if (n <= 1) return n;
        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            long temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }

    static class BenchmarkResult {
        String name;
        int iterations;
        long minNanos;
        long maxNanos;
        long avgNanos;
        long stdDevNanos;
    }
}
