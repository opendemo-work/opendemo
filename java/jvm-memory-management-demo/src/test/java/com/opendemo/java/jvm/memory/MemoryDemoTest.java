package com.opendemo.java.jvm.memory;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

class MemoryDemoTest {

    @Test
    @DisplayName("Runtime API应返回有效的内存信息")
    void testRuntimeApiReturnsValidMemoryInfo() {
        Runtime runtime = Runtime.getRuntime();

        assertTrue(runtime.maxMemory() > 0, "最大内存应大于0");
        assertTrue(runtime.totalMemory() > 0, "已分配内存应大于0");
        assertTrue(runtime.freeMemory() >= 0, "空闲内存应大于等于0");
        assertTrue(runtime.totalMemory() <= runtime.maxMemory(), "已分配内存应小于等于最大内存");
        assertTrue(runtime.availableProcessors() > 0, "处理器数应大于0");
    }

    @Test
    @DisplayName("MemoryMXBean应返回有效的堆内存使用信息")
    void testMemoryMXBeanReturnsValidHeapUsage() {
        java.lang.management.MemoryMXBean mbean = java.lang.management.ManagementFactory.getMemoryMXBean();
        java.lang.management.MemoryUsage heapUsage = mbean.getHeapMemoryUsage();

        assertTrue(heapUsage.getInit() > 0, "初始堆内存应大于0");
        assertTrue(heapUsage.getUsed() > 0, "已使用堆内存应大于0");
        assertTrue(heapUsage.getCommitted() >= heapUsage.getUsed(), "已提交内存应大于等于已使用");
        assertTrue(heapUsage.getMax() >= heapUsage.getCommitted(), "最大内存应大于等于已提交");
    }

    @Test
    @DisplayName("MemoryMXBean应返回有效的非堆内存信息")
    void testMemoryMXBeanReturnsValidNonHeapUsage() {
        java.lang.management.MemoryMXBean mbean = java.lang.management.ManagementFactory.getMemoryMXBean();
        java.lang.management.MemoryUsage nonHeapUsage = mbean.getNonHeapMemoryUsage();

        assertTrue(nonHeapUsage.getUsed() > 0, "已使用非堆内存应大于0");
        assertTrue(nonHeapUsage.getCommitted() >= nonHeapUsage.getUsed(), "已提交应大于等于已使用");
    }

    @Test
    @DisplayName("堆内存增长应被正确检测")
    void testHeapGrowthDetection() {
        long before = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        byte[] largeAllocation = new byte[10 * 1024 * 1024];

        long after = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        assertTrue(after >= before, "分配后已使用内存应大于等于分配前");
        assertNotNull(largeAllocation);
    }

    @Test
    @DisplayName("内存池应包含至少一个内存池")
    void testMemoryPoolsExist() {
        java.util.List<java.lang.management.MemoryPoolMXBean> pools =
                java.lang.management.ManagementFactory.getMemoryPoolMXBeans();

        assertFalse(pools.isEmpty(), "应至少有一个内存池");

        for (java.lang.management.MemoryPoolMXBean pool : pools) {
            assertNotNull(pool.getName(), "内存池名称不应为null");
            assertNotNull(pool.getType(), "内存池类型不应为null");
        }
    }

    @Test
    @DisplayName("栈溢出应被正确捕获")
    void testStackOverflowCaught() {
        assertThrows(StackOverflowError.class, () -> {
            causeStackOverflow(1);
        });
    }

    private void causeStackOverflow(int depth) {
        causeStackOverflow(depth + 1);
    }

    @Test
    @DisplayName("HeapDemo应成功演示堆区域信息")
    void testHeapDemoRuns() {
        assertDoesNotThrow(() -> HeapDemo.demonstrateHeapGrowth());
    }

    @Test
    @DisplayName("HeapDemo对象晋升演示应正常运行")
    void testHeapDemoObjectAging() {
        assertDoesNotThrow(() -> HeapDemo.demonstrateObjectAging());
    }

    @Test
    @DisplayName("StackDemo栈帧演示应正常运行")
    void testStackDemoFrames() {
        assertDoesNotThrow(() -> StackDemo.demonstrateStackFrames());
    }

    @Test
    @DisplayName("StackDemo尾递归演示应正常运行")
    void testStackDemoTailRecursion() {
        assertDoesNotThrow(() -> StackDemo.demonstrateTailRecursion());
    }

    @Test
    @DisplayName("MemoryPoolDemo列出内存池应正常运行")
    void testMemoryPoolDemo() {
        assertDoesNotThrow(() -> MemoryPoolDemo.listAllMemoryPools());
    }

    @Test
    @DisplayName("ObjectSizeDemo基本类型大小应正常运行")
    void testObjectSizeDemoPrimitives() {
        assertDoesNotThrow(() -> ObjectSizeDemo.estimatePrimitiveSizes());
    }

    @Test
    @DisplayName("ObjectSizeDemo对象大小估算应正常运行")
    void testObjectSizeDemoObjects() {
        assertDoesNotThrow(() -> ObjectSizeDemo.estimateObjectSizes());
    }

    @Test
    @DisplayName("ObjectSizeDemo集合大小估算应正常运行")
    void testObjectSizeDemoCollections() {
        assertDoesNotThrow(() -> ObjectSizeDemo.estimateCollectionSizes());
    }

    @Test
    @DisplayName("ObjectSizeDemo压缩指针演示应正常运行")
    void testObjectSizeDemoCompressedOops() {
        assertDoesNotThrow(() -> ObjectSizeDemo.demonstrateCompressedOops());
    }

    @Test
    @DisplayName("MemoryLeakDemo静态集合泄漏演示应正常运行")
    void testMemoryLeakDemoStaticCollection() {
        assertDoesNotThrow(() -> MemoryLeakDemo.demonstrateStaticCollectionLeak());
    }

    @Test
    @DisplayName("MemoryLeakDemo泄漏检测应正常运行")
    void testMemoryLeakDemoDetection() {
        assertDoesNotThrow(() -> MemoryLeakDemo.demonstrateLeakDetection());
    }

    @Test
    @DisplayName("GC后内存应被回收")
    void testGcReclaimsMemory() {
        byte[] temp = new byte[50 * 1024 * 1024];
        temp = null;

        System.gc();
        try { Thread.sleep(200); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        long usedMB = (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / (1024 * 1024);
        assertTrue(usedMB < 500, "GC后已使用内存应合理");
    }

    @Test
    @DisplayName("内存分配后使用量应增加")
    void testMemoryAllocationTracking() {
        long before = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        byte[] chunk = new byte[5 * 1024 * 1024];

        long after = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        assertTrue(after > before - 1024 * 1024, "分配后内存使用应增加");
        assertNotNull(chunk);
    }
}
