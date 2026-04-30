package com.opendemo.java.jvm.gc;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.lang.management.GarbageCollectorMXBean;
import java.lang.management.ManagementFactory;
import java.lang.ref.WeakReference;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class GCDemoTest {

    @Test
    @DisplayName("GCDemo System.gc演示应正常运行")
    void testSystemGCDemo() {
        assertDoesNotThrow(() -> GCDemo.demonstrateSystemGC());
    }

    @Test
    @DisplayName("GCDemo finalize演示应正常运行")
    void testFinalizeDemo() {
        assertDoesNotThrow(() -> GCDemo.demonstrateFinalize());
    }

    @Test
    @DisplayName("GCDemo GCMXBean应返回有效信息")
    void testGCMXBean() {
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        assertFalse(gcBeans.isEmpty(), "应至少有一个GC MXBean");

        for (GarbageCollectorMXBean gcBean : gcBeans) {
            assertNotNull(gcBean.getName());
            assertTrue(gcBean.getCollectionCount() >= 0);
            assertTrue(gcBean.getCollectionTime() >= 0);
        }
    }

    @Test
    @DisplayName("GC类型信息应正常显示")
    void testGCTypes() {
        assertDoesNotThrow(() -> GCDemo.demonstrateGCTypes());
    }

    @Test
    @DisplayName("GCLog演示应正常运行")
    void testGCLogDemo() {
        assertDoesNotThrow(() -> GCLogDemo.demonstrateGCLogFlags());
        assertDoesNotThrow(() -> GCLogDemo.demonstrateGCLogAnalysis());
    }

    @Test
    @DisplayName("GC负载生成应正常运行")
    void testGCLoadGeneration() {
        assertDoesNotThrow(() -> GCLogDemo.generateGCLoad());
    }

    @Test
    @DisplayName("SerialGC示例应正常运行")
    void testSerialGCExample() {
        assertDoesNotThrow(() -> SerialGCExample.demonstrateYoungGC());
    }

    @Test
    @DisplayName("SerialGC特点信息应正常显示")
    void testSerialGCCharacteristics() {
        assertDoesNotThrow(() -> SerialGCExample.printCharacteristics());
    }

    @Test
    @DisplayName("ParallelGC并行收集应正常运行")
    void testParallelGCExample() {
        assertDoesNotThrow(() -> ParallelGCExample.demonstrateParallelCollection());
    }

    @Test
    @DisplayName("ParallelGC吞吐量基准测试应正常运行")
    void testParallelGCThroughput() throws Exception {
        assertDoesNotThrow(() -> ParallelGCExample.demonstrateThroughputBenchmark());
    }

    @Test
    @DisplayName("G1GC Region收集应正常运行")
    void testG1GCRegion() {
        assertDoesNotThrow(() -> G1GCExample.demonstrateRegionBasedCollection());
    }

    @Test
    @DisplayName("G1GC Mixed GC应正常运行")
    void testG1GCMixedGC() {
        assertDoesNotThrow(() -> G1GCExample.demonstrateMixedGC());
    }

    @Test
    @DisplayName("G1GC大对象应正常运行")
    void testG1GCHumongous() {
        assertDoesNotThrow(() -> G1GCExample.demonstrateHumongousObjects());
    }

    @Test
    @DisplayName("GC调优策略应正常显示")
    void testGCTuningStrategies() {
        assertDoesNotThrow(() -> GCTuningDemo.demonstrateTuningStrategies());
    }

    @Test
    @DisplayName("Young GC基准测试应正常运行")
    void testYoungGCBenchmark() {
        assertDoesNotThrow(() -> GCTuningDemo.runGCBenchmark("Test", GCTuningDemo.createYoungGCWorkload()));
    }

    @Test
    @DisplayName("Old GC基准测试应正常运行")
    void testOldGCBenchmark() {
        assertDoesNotThrow(() -> GCTuningDemo.runGCBenchmark("Test", GCTuningDemo.createOldGCWorkload()));
    }

    @Test
    @DisplayName("混合负载基准测试应正常运行")
    void testMixedBenchmark() {
        assertDoesNotThrow(() -> GCTuningDemo.runGCBenchmark("Test", GCTuningDemo.createMixedWorkload()));
    }

    @Test
    @DisplayName("WeakReference应在GC后被清除")
    void testWeakReference() {
        Object obj = new Object();
        WeakReference<Object> weakRef = new WeakReference<>(obj);

        assertNotNull(weakRef.get());

        obj = null;
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        assertNull(weakRef.get(), "弱引用在GC后应为null");
    }

    @Test
    @DisplayName("WeakReference演示应正常运行")
    void testWeakReferenceDemo() {
        assertDoesNotThrow(() -> WeakReferenceDemo.demonstrateWeakReference());
    }

    @Test
    @DisplayName("SoftReference演示应正常运行")
    void testSoftReferenceDemo() {
        assertDoesNotThrow(() -> WeakReferenceDemo.demonstrateSoftReference());
    }

    @Test
    @DisplayName("PhantomReference演示应正常运行")
    void testPhantomReferenceDemo() {
        assertDoesNotThrow(() -> {
            try {
                WeakReferenceDemo.demonstratePhantomReference();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
    }

    @Test
    @DisplayName("WeakHashMap演示应正常运行")
    void testWeakHashMapDemo() {
        assertDoesNotThrow(() -> WeakReferenceDemo.demonstrateWeakHashMap());
    }

    @Test
    @DisplayName("内存分配和回收应正常工作")
    void testMemoryAllocationAndGC() {
        long before = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        byte[] chunk = new byte[10 * 1024 * 1024];
        assertNotNull(chunk);

        long afterAlloc = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        assertTrue(afterAlloc >= before);

        chunk = null;
        System.gc();
        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        long afterGC = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        assertTrue(afterGC <= afterAlloc);
    }

    @Test
    @DisplayName("GC调优建议应正常显示")
    void testTuningRecommendations() {
        assertDoesNotThrow(() -> GCTuningDemo.printTuningRecommendations());
    }
}
