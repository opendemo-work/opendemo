package com.opendemo.java.troubleshooting;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.lang.management.*;

class TroubleshootingTrinityTest {
    @Test
    void jstatGcSummaryIsAvailable() {
        assertFalse(ManagementFactory.getGarbageCollectorMXBeans().isEmpty());
        for (GarbageCollectorMXBean gc : ManagementFactory.getGarbageCollectorMXBeans()) {
            assertTrue(gc.getCollectionCount() >= 0);
            assertTrue(gc.getCollectionTime() >= 0);
        }
    }

    @Test
    void jstatMemoryPoolsAccessible() {
        assertFalse(ManagementFactory.getMemoryPoolMXBeans().isEmpty());
        for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
            assertNotNull(pool.getName());
            assertNotNull(pool.getType());
        }
    }

    @Test
    void jmapHeapSummaryShowsUsedMemory() {
        MemoryUsage heap = ManagementFactory.getMemoryMXBean().getHeapMemoryUsage();
        assertTrue(heap.getUsed() > 0);
        assertTrue(heap.getCommitted() > 0);
    }

    @Test
    void jmapHeapMaxIsPositive() {
        long max = ManagementFactory.getMemoryMXBean().getHeapMemoryUsage().getMax();
        assertTrue(max > 0);
    }

    @Test
    void jmapNonHeapMemoryIsTracked() {
        MemoryUsage nonHeap = ManagementFactory.getMemoryMXBean().getNonHeapMemoryUsage();
        assertTrue(nonHeap.getUsed() > 0);
    }

    @Test
    void jstackThreadCountIsPositive() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        assertTrue(bean.getThreadCount() > 0);
        assertTrue(bean.getAllThreadIds().length > 0);
    }

    @Test
    void jstackNoDeadlockInNormalExecution() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        long[] deadlocks = bean.findDeadlockedThreads();
        assertTrue(deadlocks == null || deadlocks.length == 0);
    }

    @Test
    void jstackMainThreadInfo() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        ThreadInfo info = bean.getThreadInfo(Thread.currentThread().getId());
        assertNotNull(info);
        assertEquals(Thread.State.RUNNABLE, info.getThreadState());
    }

    @Test
    void jstackThreadCpuTimeAvailable() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        assertTrue(bean.isThreadCpuTimeSupported());
        bean.setThreadCpuTimeEnabled(true);
        long cpuTime = bean.getThreadCpuTime(Thread.currentThread().getId());
        assertTrue(cpuTime >= 0);
    }

    @Test
    void gcAvgTimeIsComputable() {
        for (GarbageCollectorMXBean gc : ManagementFactory.getGarbageCollectorMXBeans()) {
            long count = gc.getCollectionCount();
            long time = gc.getCollectionTime();
            if (count > 0) {
                long avg = time / count;
                assertTrue(avg >= 0);
            }
        }
    }

    @Test
    void runtimeMemoryConsistentWithMxBeans() {
        Runtime runtime = Runtime.getRuntime();
        MemoryUsage heap = ManagementFactory.getMemoryMXBean().getHeapMemoryUsage();
        long runtimeUsed = runtime.totalMemory() - runtime.freeMemory();
        assertTrue(Math.abs(runtimeUsed - heap.getUsed()) < 10 * 1024 * 1024,
                "Runtime and MXBean used memory should be close");
    }

    @Test
    void peakThreadCountIsAtLeastCurrent() {
        ThreadMXBean bean = ManagementFactory.getThreadMXBean();
        assertTrue(bean.getPeakThreadCount() >= bean.getThreadCount());
    }
}
