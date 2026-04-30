package com.opendemo.java.diagnostic;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.lang.management.*;

class DiagnosticToolsTest {
    @Test
    void threadDumpCanReadThreadInfo() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        assertTrue(bean.getThreadCount() > 0);
        assertTrue(bean.getAllThreadIds().length > 0);
    }

    @Test
    void threadDumpDetectsNoDeadlock() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        long[] deadlocks = bean.findDeadlockedThreads();
        assertTrue(deadlocks == null || deadlocks.length == 0);
    }

    @Test
    void threadInfoContainsMainThread() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        ThreadInfo info = bean.getThreadInfo(Thread.currentThread().getId());
        assertNotNull(info);
        assertEquals(Thread.currentThread().getName(), info.getThreadName());
    }

    @Test
    void heapInfoShowsPositiveMemory() {
        MemoryMXBean bean = ManagementFactory.getMemoryMXBean();
        MemoryUsage heap = bean.getHeapMemoryUsage();
        assertTrue(heap.getUsed() > 0);
        assertTrue(heap.getMax() > 0);
    }

    @Test
    void memoryPoolsAreAvailable() {
        assertFalse(ManagementFactory.getMemoryPoolMXBeans().isEmpty());
    }

    @Test
    void gcBeansAreAvailable() {
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        assertFalse(gcBeans.isEmpty());
        for (GarbageCollectorMXBean gc : gcBeans) {
            assertNotNull(gc.getName());
            assertTrue(gc.getCollectionCount() >= 0);
        }
    }

    @Test
    void gcTimeIsNonNegative() {
        for (GarbageCollectorMXBean gc : ManagementFactory.getGarbageCollectorMXBeans()) {
            assertTrue(gc.getCollectionTime() >= 0);
        }
    }

    @Test
    void runtimeInfoIsSensible() {
        Runtime runtime = Runtime.getRuntime();
        assertTrue(runtime.maxMemory() > 0);
        assertTrue(runtime.totalMemory() > 0);
        assertTrue(runtime.availableProcessors() > 0);
    }

    @Test
    void classLoadingInfoIsAvailable() {
        ClassLoadingMXBean bean = ManagementFactory.getClassLoadingMXBean();
        assertTrue(bean.getLoadedClassCount() > 0);
        assertTrue(bean.getTotalLoadedClassCount() > 0);
    }

    @Test
    void threadCpuTimeSupported() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        if (bean.isThreadCpuTimeSupported()) {
            bean.setThreadCpuTimeEnabled(true);
            long cpuTime = bean.getThreadCpuTime(Thread.currentThread().getId());
            assertTrue(cpuTime >= 0);
        }
    }

    @Test
    void nonHeapMemoryUsageIsAvailable() {
        MemoryUsage nonHeap = ManagementFactory.getMemoryMXBean().getNonHeapMemoryUsage();
        assertTrue(nonHeap.getUsed() > 0);
    }

    @Test
    void objectAllocationIncreasesMemory() {
        Runtime runtime = Runtime.getRuntime();
        long usedBefore = runtime.totalMemory() - runtime.freeMemory();
        byte[] data = new byte[10 * 1024 * 1024];
        long usedAfter = runtime.totalMemory() - runtime.freeMemory();
        assertTrue(usedAfter >= usedBefore);
    }
}
