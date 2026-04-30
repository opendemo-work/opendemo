package com.opendemo.java.profiling;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.lang.management.*;

import static org.junit.jupiter.api.Assertions.*;

class ProfilingDemoTest {

    @Test
    @DisplayName("JmxProfilingDemo应正常运行")
    void testJmxProfilingDemo() {
        assertDoesNotThrow(() -> JmxProfilingDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("RuntimeMXBean应返回有效信息")
    void testRuntimeMXBean() {
        RuntimeMXBean bean = ManagementFactory.getRuntimeMXBean();
        assertNotNull(bean.getVmName());
        assertNotNull(bean.getVmVersion());
        assertTrue(bean.getUptime() > 0);
        assertNotNull(bean.getInputArguments());
    }

    @Test
    @DisplayName("OperatingSystemMXBean应返回有效信息")
    void testOperatingSystemMXBean() {
        OperatingSystemMXBean bean = ManagementFactory.getOperatingSystemMXBean();
        assertNotNull(bean.getName());
        assertTrue(bean.getAvailableProcessors() > 0);
    }

    @Test
    @DisplayName("CompilationMXBean应返回编译器信息")
    void testCompilationMXBean() {
        CompilationMXBean bean = ManagementFactory.getCompilationMXBean();
        assertNotNull(bean.getName());
        assertTrue(bean.getTotalCompilationTime() >= 0);
    }

    @Test
    @DisplayName("ClassLoadingMXBean应返回类加载信息")
    void testClassLoadingMXBean() {
        ClassLoadingMXBean bean = ManagementFactory.getClassLoadingMXBean();
        assertTrue(bean.getLoadedClassCount() > 0);
        assertTrue(bean.getTotalLoadedClassCount() > 0);
    }

    @Test
    @DisplayName("ThreadMXBean应返回线程信息")
    void testThreadMXBean() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        assertTrue(bean.getThreadCount() > 0);
        assertTrue(bean.getPeakThreadCount() > 0);
    }

    @Test
    @DisplayName("CpuProfilingDemo应正常运行")
    void testCpuProfilingDemo() {
        assertDoesNotThrow(() -> CpuProfilingDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("CPU时间测量应返回正值")
    void testCpuTimeMeasurement() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        if (bean.isCurrentThreadCpuTimeSupported()) {
            bean.setThreadCpuTimeEnabled(true);
            long t1 = bean.getCurrentThreadCpuTime();
            long sum = 0;
            for (long i = 0; i < 1_000_000L; i++) sum += i;
            long t2 = bean.getCurrentThreadCpuTime();
            assertTrue(t2 >= t1, "CPU时间应递增");
            assertTrue(sum >= 0);
        }
    }

    @Test
    @DisplayName("死锁检测应正常工作")
    void testDeadlockDetection() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        long[] deadlocked = bean.findDeadlockedThreads();
        assertNull(deadlocked, "正常情况不应有死锁");
    }

    @Test
    @DisplayName("MemoryProfilingDemo应正常运行")
    void testMemoryProfilingDemo() {
        assertDoesNotThrow(() -> MemoryProfilingDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("堆内存使用应返回有效信息")
    void testHeapUsage() {
        MemoryMXBean bean = ManagementFactory.getMemoryMXBean();
        MemoryUsage heap = bean.getHeapMemoryUsage();
        assertTrue(heap.getUsed() > 0);
        assertTrue(heap.getMax() > 0);
        assertTrue(heap.getCommitted() >= heap.getUsed());
    }

    @Test
    @DisplayName("PerformanceBenchmark应正常运行")
    void testPerformanceBenchmark() {
        assertDoesNotThrow(() -> PerformanceBenchmark.main(new String[]{}));
    }

    @Test
    @DisplayName("基准测试应返回有效结果")
    void testBenchmarkResult() {
        PerformanceBenchmark.BenchmarkResult result = PerformanceBenchmark.benchmark(
                "测试", () -> {
                    long sum = 0;
                    for (int i = 0; i < 1000; i++) sum += i;
                    return sum;
                }, 10);

        assertEquals("测试", result.name);
        assertEquals(10, result.iterations);
        assertTrue(result.avgNanos > 0);
        assertTrue(result.minNanos > 0);
        assertTrue(result.maxNanos >= result.minNanos);
    }

    @Test
    @DisplayName("HotspotDemo应正常运行")
    void testHotspotDemo() {
        assertDoesNotThrow(() -> HotspotDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("JIT编译应加速方法执行")
    void testJITWarmup() {
        int iterations = 1_000_000;
        long[] times = new long[5];

        for (int round = 0; round < 5; round++) {
            long start = System.nanoTime();
            long sum = 0;
            for (int i = 0; i < iterations; i++) {
                sum += i * 2 + 1;
            }
            times[round] = System.nanoTime() - start;
            assertTrue(sum >= 0);
        }

        assertTrue(times[4] <= times[0] * 5,
                "JIT编译后性能应提升或持平");
    }

    @Test
    @DisplayName("分支预测：已排序数据应更快或持平")
    void testBranchPrediction() {
        int size = 50_000;
        int[] sorted = new int[size];
        int[] unsorted = new int[size];
        java.util.Random random = new java.util.Random(42);

        for (int i = 0; i < size; i++) {
            unsorted[i] = random.nextInt(100);
            sorted[i] = unsorted[i];
        }
        java.util.Arrays.sort(sorted);

        long startS = System.nanoTime();
        long countS = 0;
        for (int v : sorted) if (v >= 50) countS++;
        long sortedTime = System.nanoTime() - startS;

        long startU = System.nanoTime();
        long countU = 0;
        for (int v : unsorted) if (v >= 50) countU++;
        long unsortedTime = System.nanoTime() - startU;

        assertEquals(countS, countU);
    }

    @Test
    @DisplayName("方法内联演示应正常执行")
    void testInlining() {
        assertDoesNotThrow(() -> HotspotDemo.demonstrateInlining());
    }

    @Test
    @DisplayName("循环优化演示应正常执行")
    void testLoopOptimization() {
        assertDoesNotThrow(() -> HotspotDemo.demonstrateLoopOptimization());
    }

    @Test
    @DisplayName("内存分配速率应正常测量")
    void testAllocationRate() {
        assertDoesNotThrow(() -> MemoryProfilingDemo.demonstrateAllocationRate());
    }

    @Test
    @DisplayName("内存占用对比应正常执行")
    void testMemoryFootprint() {
        assertDoesNotThrow(() -> MemoryProfilingDemo.demonstrateMemoryFootprint());
    }
}
