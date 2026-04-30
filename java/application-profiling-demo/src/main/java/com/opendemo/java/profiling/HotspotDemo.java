package com.opendemo.java.profiling;

public class HotspotDemo {

    private static int virtualMethodCalls = 0;

    public static void main(String[] args) {
        demonstrateInterpreterVsJIT();
        demonstrateInlining();
        demonstrateBranchPrediction();
        demonstrateLoopOptimization();
        printJITGuide();
    }

    public static void demonstrateInterpreterVsJIT() {
        System.out.println("=== 解释器 vs JIT编译 ===");
        System.out.println("JVM执行模式:");
        System.out.println("  1. 解释执行 (Interpreter): 逐行解释字节码，启动快但执行慢");
        System.out.println("  2. JIT编译 (Just-In-Time): 将热点代码编译为本地机器码，执行快");
        System.out.println();

        System.out.println("--- 测试方法调用性能 ---");

        int iterations = 10_000_000;

        long start = System.nanoTime();
        long sum = 0;
        for (int i = 0; i < iterations; i++) {
            sum += simpleAdd(i, i + 1);
        }
        long firstRun = System.nanoTime() - start;

        start = System.nanoTime();
        sum = 0;
        for (int i = 0; i < iterations; i++) {
            sum += simpleAdd(i, i + 1);
        }
        long secondRun = System.nanoTime() - start;

        start = System.nanoTime();
        sum = 0;
        for (int i = 0; i < iterations; i++) {
            sum += simpleAdd(i, i + 1);
        }
        long thirdRun = System.nanoTime() - start;

        System.out.printf("  第1次 (解释+JIT): %.3f ms%n", firstRun / 1_000_000.0);
        System.out.printf("  第2次 (已JIT编译): %.3f ms%n", secondRun / 1_000_000.0);
        System.out.printf("  第3次 (已JIT编译): %.3f ms%n", thirdRun / 1_000_000.0);
        System.out.printf("  JIT加速比: %.2fx%n", (double) firstRun / thirdRun);
        System.out.println("  (sum=" + sum + " 防止死代码消除)");
        System.out.println();
    }

    public static void demonstrateInlining() {
        System.out.println("=== 方法内联 (Method Inlining) ===");
        System.out.println("JIT编译器将短方法直接嵌入调用处，消除方法调用开销");
        System.out.println();

        int iterations = 100_000_000;

        long startDirect = System.nanoTime();
        long sum1 = 0;
        for (int i = 0; i < iterations; i++) {
            sum1 += i * 2 + 1;
        }
        long directTime = System.nanoTime() - startDirect;

        long startMethod = System.nanoTime();
        long sum2 = 0;
        for (int i = 0; i < iterations; i++) {
            sum2 += compute(i);
        }
        long methodTime = System.nanoTime() - startMethod;

        System.out.printf("  直接计算: %.3f ms (sum=%d)%n", directTime / 1_000_000.0, sum1);
        System.out.printf("  方法调用: %.3f ms (sum=%d)%n", methodTime / 1_000_000.0, sum2);
        System.out.printf("  内联后差异: %.2fx%n", (double) methodTime / directTime);

        System.out.println();
        System.out.println("  内联条件:");
        System.out.println("    - 方法足够小（<325字节，-XX:MaxInlineSize）");
        System.out.println("    - 频繁调用的热点方法");
        System.out.println("    - 被调用方法不是太大（<35字节码，-XX:FreqInlineSize）");
        System.out.println();
    }

    public static void demonstrateBranchPrediction() {
        System.out.println("=== 分支预测 (Branch Prediction) ===");

        int size = 100_000;
        int[] sorted = new int[size];
        int[] unsorted = new int[size];

        java.util.Random random = new java.util.Random(42);
        for (int i = 0; i < size; i++) {
            unsorted[i] = random.nextInt(100);
            sorted[i] = unsorted[i];
        }
        java.util.Arrays.sort(sorted);

        long startSorted = System.nanoTime();
        long count1 = 0;
        for (int i = 0; i < size; i++) {
            if (sorted[i] >= 50) count1++;
        }
        long sortedTime = System.nanoTime() - startSorted;

        long startUnsorted = System.nanoTime();
        long count2 = 0;
        for (int i = 0; i < size; i++) {
            if (unsorted[i] >= 50) count2++;
        }
        long unsortedTime = System.nanoTime() - startUnsorted;

        System.out.printf("  已排序数组: %.3f ms (count=%d)%n", sortedTime / 1_000_000.0, count1);
        System.out.printf("  未排序数组: %.3f ms (count=%d)%n", unsortedTime / 1_000_000.0, count2);
        System.out.printf("  分支预测加速: %.2fx%n", (double) unsortedTime / sortedTime);
        System.out.println();
        System.out.println("  原理: CPU预测分支走向，预测正确则无开销");
        System.out.println("  已排序数据分支模式稳定，预测准确率高");
        System.out.println();
    }

    public static void demonstrateLoopOptimization() {
        System.out.println("=== 循环优化 ===");

        int size = 10_000_000;
        int[] data = new int[size];
        java.util.Random random = new java.util.Random(42);
        for (int i = 0; i < size; i++) {
            data[i] = random.nextInt(1000);
        }

        long start1 = System.nanoTime();
        long sum1 = 0;
        for (int i = 0; i < size; i++) {
            sum1 += data[i];
        }
        long simpleLoopTime = System.nanoTime() - start1;

        long start2 = System.nanoTime();
        long sum2 = 0;
        int mid = size / 2;
        for (int i = 0; i < mid; i++) {
            sum2 += data[i];
        }
        for (int i = mid; i < size; i++) {
            sum2 += data[i];
        }
        long splitLoopTime = System.nanoTime() - start2;

        System.out.printf("  单循环: %.3f ms (sum=%d)%n", simpleLoopTime / 1_000_000.0, sum1);
        System.out.printf("  拆分循环: %.3f ms (sum=%d)%n", splitLoopTime / 1_000_000.0, sum2);
        System.out.println();
        System.out.println("  JIT循环优化:");
        System.out.println("    - 循环展开 (Loop Unrolling): 减少循环控制开销");
        System.out.println("    - 循环不变量外提 (LICM): 移出不变计算");
        System.out.println("    - 数组边界检查消除: 消除不必要的检查");
    }

    public static void printJITGuide() {
        System.out.println();
        System.out.println("=== JIT编译相关参数 ===");
        System.out.println();
        System.out.println("  -XX:+PrintCompilation              打印JIT编译信息");
        System.out.println("  -XX:+UnlockDiagnosticVMOptions      解锁诊断选项");
        System.out.println("  -XX:+PrintInlining                  打印内联信息");
        System.out.println("  -XX:CompileThreshold=10000          JIT编译阈值");
        System.out.println("  -XX:+TieredCompilation              分层编译(默认开启)");
        System.out.println();
        System.out.println("分层编译级别:");
        System.out.println("  Level 0: 解释执行");
        System.out.println("  Level 1: C1简单编译 (快速编译, 简单优化)");
        System.out.println("  Level 2: C1有限编译 (C1+部分优化)");
        System.out.println("  Level 3: C1完全编译 (C1+全部优化)");
        System.out.println("  Level 4: C2编译 (慢速编译, 深度优化)");
    }

    private static int simpleAdd(int a, int b) {
        return a + b;
    }

    private static int compute(int i) {
        return i * 2 + 1;
    }
}
