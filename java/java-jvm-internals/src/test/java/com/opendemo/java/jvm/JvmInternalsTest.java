package com.opendemo.java.jvm;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.lang.management.*;

class JvmInternalsTest {
    @Test
    void classLoaderHierarchyExists() {
        ClassLoader loader = Thread.currentThread().getContextClassLoader();
        assertNotNull(loader);
    }

    @Test
    void bootstrapClassLoaderLoadsCoreClasses() {
        assertNull(String.class.getClassLoader());
    }

    @Test
    void appClassLoaderLoadsUserClasses() {
        assertNotNull(JvmInternalsTest.class.getClassLoader());
    }

    @Test
    void heapMemoryIsPositive() {
        MemoryUsage heap = ManagementFactory.getMemoryMXBean().getHeapMemoryUsage();
        assertTrue(heap.getUsed() > 0);
        assertTrue(heap.getMax() > 0);
    }

    @Test
    void memoryPoolsIncludeHeapPools() {
        boolean hasEden = ManagementFactory.getMemoryPoolMXBeans().stream()
                .anyMatch(p -> p.getName().toLowerCase().contains("eden") || p.getName().toLowerCase().contains("young"));
        assertTrue(hasEden, "Should have a young/eden memory pool");
    }

    @Test
    void gcBeansArePresent() {
        assertFalse(ManagementFactory.getGarbageCollectorMXBeans().isEmpty());
    }

    @Test
    void compilationMxBeanIsAvailable() {
        CompilationMXBean bean = ManagementFactory.getCompilationMXBean();
        assertNotNull(bean.getName());
        assertTrue(bean.getTotalCompilationTime() >= 0);
    }

    @Test
    void runtimeBeanHasInputArguments() {
        RuntimeMXBean bean = ManagementFactory.getRuntimeMXBean();
        assertNotNull(bean.getInputArguments());
        assertNotNull(bean.getVmName());
    }

    @Test
    void classVersionIsSet() {
        String classVersion = System.getProperty("java.class.version");
        assertNotNull(classVersion);
        assertFalse(classVersion.isEmpty());
    }

    @Test
    void availableProcessorsIsPositive() {
        assertTrue(Runtime.getRuntime().availableProcessors() > 0);
    }

    @Test
    void hotMethodComputesCorrectly() {
        long expected = 0;
        for (int i = 0; i < 100; i++) {
            long x = (long) i * i;
            x = x + i;
            x = x % (i + 1);
            expected += x;
        }
        long actual = 0;
        for (int i = 0; i < 100; i++) {
            actual += jitHotMethod(i);
        }
        assertEquals(expected, actual);
    }

    private long jitHotMethod(int value) {
        long x = (long) value * value;
        x = x + value;
        x = x % (value + 1);
        return x;
    }

    @Test
    void threadCountIsPositive() {
        assertTrue(ManagementFactory.getThreadMXBean().getThreadCount() > 0);
    }
}
