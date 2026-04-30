package com.opendemo.java.patterns.singleton;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.HashSet;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("单例模式测试")
class SingletonPatternTest {

    @Test
    @DisplayName("饿汉式 - 同一实例")
    void testEagerSingletonSameInstance() {
        EagerSingleton instance1 = EagerSingleton.getInstance();
        EagerSingleton instance2 = EagerSingleton.getInstance();
        assertSame(instance1, instance2);
    }

    @Test
    @DisplayName("懒汉式 - 同一实例")
    void testLazySingletonSameInstance() {
        LazySingleton instance1 = LazySingleton.getInstance();
        LazySingleton instance2 = LazySingleton.getInstance();
        assertSame(instance1, instance2);
    }

    @Test
    @DisplayName("双重检查锁定 - 同一实例")
    void testThreadSafeSingletonSameInstance() {
        ThreadSafeSingleton instance1 = ThreadSafeSingleton.getInstance();
        ThreadSafeSingleton instance2 = ThreadSafeSingleton.getInstance();
        assertSame(instance1, instance2);
    }

    @Test
    @DisplayName("枚举式 - 同一实例")
    void testEnumSingletonSameInstance() {
        EnumSingleton instance1 = EnumSingleton.INSTANCE;
        EnumSingleton instance2 = EnumSingleton.INSTANCE;
        assertSame(instance1, instance2);
    }

    @Test
    @DisplayName("静态内部类 - 同一实例")
    void testInnerClassSingletonSameInstance() {
        InnerClassSingleton instance1 = InnerClassSingleton.getInstance();
        InnerClassSingleton instance2 = InnerClassSingleton.getInstance();
        assertSame(instance1, instance2);
    }

    @Test
    @DisplayName("双重检查锁定 - 多线程安全")
    void testThreadSafeSingletonMultiThread() throws InterruptedException {
        final int threadCount = 100;
        final Set<ThreadSafeSingleton> instances = new HashSet<>();
        final CountDownLatch latch = new CountDownLatch(threadCount);
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);

        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                instances.add(ThreadSafeSingleton.getInstance());
                latch.countDown();
            });
        }

        latch.await(5, TimeUnit.SECONDS);
        executor.shutdown();

        assertEquals(1, instances.size());
    }

    @Test
    @DisplayName("枚举式 - 计数器共享状态")
    void testEnumSingletonSharedState() {
        EnumSingleton.INSTANCE.increment();
        EnumSingleton.INSTANCE.increment();
        EnumSingleton.INSTANCE.increment();
        assertEquals(3, EnumSingleton.INSTANCE.getCounter());
    }

    @Test
    @DisplayName("静态内部类 - 多线程安全")
    void testInnerClassSingletonMultiThread() throws InterruptedException {
        final int threadCount = 100;
        final Set<InnerClassSingleton> instances = new HashSet<>();
        final CountDownLatch latch = new CountDownLatch(threadCount);
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);

        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                instances.add(InnerClassSingleton.getInstance());
                latch.countDown();
            });
        }

        latch.await(5, TimeUnit.SECONDS);
        executor.shutdown();

        assertEquals(1, instances.size());
    }
}
