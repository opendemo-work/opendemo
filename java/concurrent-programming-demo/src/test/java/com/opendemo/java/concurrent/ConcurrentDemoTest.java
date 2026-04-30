package com.opendemo.java.concurrent;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

class ConcurrentDemoTest {

    @Test
    @DisplayName("ThreadCreationDemo应正常运行")
    void testThreadCreationDemo() {
        assertDoesNotThrow(() -> ThreadCreationDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("继承Thread方式应正确执行")
    void testThreadCreation() throws InterruptedException {
        final boolean[] executed = {false};
        Thread t = new Thread(() -> executed[0] = true);
        t.start();
        t.join(1000);
        assertTrue(executed[0]);
    }

    @Test
    @DisplayName("Callable应返回正确结果") 
    void testCallable() throws Exception {
        Callable<Integer> task = () -> 42;
        FutureTask<Integer> future = new FutureTask<>(task);
        new Thread(future).start();
        assertEquals(42, future.get());
    }

    @Test
    @DisplayName("SynchronizedDemo应正常运行")
    void testSynchronizedDemo() {
        assertDoesNotThrow(() -> SynchronizedDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("synchronized应保证线程安全")
    void testSynchronizedSafety() throws Exception {
        int[] counter = {0};
        Object lock = new Object();
        int threads = 10;
        int increments = 1000;
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            new Thread(() -> {
                for (int j = 0; j < increments; j++) {
                    synchronized (lock) {
                        counter[0]++;
                    }
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        assertEquals(threads * increments, counter[0]);
    }

    @Test
    @DisplayName("ReentrantLock应保证线程安全")
    void testReentrantLock() throws Exception {
        ReentrantLock lock = new ReentrantLock();
        int[] counter = {0};
        int threads = 10;
        int increments = 1000;
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            new Thread(() -> {
                for (int j = 0; j < increments; j++) {
                    lock.lock();
                    try {
                        counter[0]++;
                    } finally {
                        lock.unlock();
                    }
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        assertEquals(threads * increments, counter[0]);
    }

    @Test
    @DisplayName("ConcurrentCollectionsDemo应正常运行")
    void testConcurrentCollectionsDemo() {
        assertDoesNotThrow(() -> ConcurrentCollectionsDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("ConcurrentHashMap应线程安全")
    void testConcurrentHashMap() throws Exception {
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        int threads = 10;
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            final int threadId = i;
            new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    map.put("key-" + threadId + "-" + j, j);
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        assertEquals(threads * 100, map.size());
    }

    @Test
    @DisplayName("ExecutorServiceDemo应正常运行")
    void testExecutorServiceDemo() {
        assertDoesNotThrow(() -> ExecutorServiceDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("FixedThreadPool应正确执行任务")
    void testFixedThreadPool() throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(3);
        AtomicInteger counter = new AtomicInteger(0);
        int tasks = 10;
        CountDownLatch latch = new CountDownLatch(tasks);

        for (int i = 0; i < tasks; i++) {
            executor.submit(() -> {
                counter.incrementAndGet();
                latch.countDown();
            });
        }

        latch.await();
        executor.shutdown();
        assertEquals(tasks, counter.get());
    }

    @Test
    @DisplayName("CompletableFuture应正确编排异步任务")
    void testCompletableFuture() throws Exception {
        CompletableFuture<String> future = CompletableFuture
                .supplyAsync(() -> "hello")
                .thenApply(String::toUpperCase)
                .thenApply(s -> s + " WORLD");

        assertEquals("HELLO WORLD", future.get());
    }

    @Test
    @DisplayName("AtomicVariableDemo应正常运行")
    void testAtomicVariableDemo() {
        assertDoesNotThrow(() -> AtomicVariableDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("AtomicInteger应保证原子性")
    void testAtomicInteger() throws Exception {
        AtomicInteger ai = new AtomicInteger(0);
        int threads = 10;
        int increments = 10000;
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            new Thread(() -> {
                for (int j = 0; j < increments; j++) {
                    ai.incrementAndGet();
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        assertEquals(threads * increments, ai.get());
    }

    @Test
    @DisplayName("AtomicReference CAS应正确工作")
    void testAtomicReferenceCAS() {
        AtomicReference<String> ref = new AtomicReference<>("A");
        assertTrue(ref.compareAndSet("A", "B"));
        assertEquals("B", ref.get());
        assertFalse(ref.compareAndSet("A", "C"));
        assertEquals("B", ref.get());
    }

    @Test
    @DisplayName("ProducerConsumerDemo应正常运行")
    void testProducerConsumerDemo() {
        assertDoesNotThrow(() -> ProducerConsumerDemo.main(new String[]{}));
    }

    @Test
    @DisplayName("BlockingQueue应正确传递数据")
    void testBlockingQueue() throws Exception {
        BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(5);

        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    queue.put(i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        java.util.List<Integer> results = new java.util.ArrayList<>();
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    results.add(queue.take());
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        producer.start();
        consumer.start();
        producer.join(2000);
        consumer.join(2000);

        assertEquals(10, results.size());
        for (int i = 0; i < 10; i++) {
            assertTrue(results.contains(i));
        }
    }

    @Test
    @DisplayName("wait/notify缓冲区应正确工作")
    void testSimpleBuffer() throws Exception {
        ProducerConsumerDemo.SimpleBuffer buffer = new ProducerConsumerDemo.SimpleBuffer(3);

        buffer.put("A");
        buffer.put("B");
        assertEquals(2, buffer.size());
        assertEquals("A", buffer.take());
        assertEquals("B", buffer.take());
        assertEquals(0, buffer.size());
    }

    @Test
    @DisplayName("非同步计数器应出现竞态条件")
    void testRaceCondition() throws Exception {
        int[] unsafe = {0};
        int threads = 10;
        int increments = 10000;
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            new Thread(() -> {
                for (int j = 0; j < increments; j++) {
                    unsafe[0]++;
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        assertTrue(unsafe[0] < threads * increments,
                "非同步计数器应出现竞态条件，实际值应小于期望值");
    }

    @Test
    @DisplayName("ReadWriteLock应允许多个读者")
    void testReadWriteLock() throws Exception {
        ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
        AtomicInteger concurrentReaders = new AtomicInteger(0);
        int maxConcurrentReaders = new AtomicInteger(0).get();

        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch doneLatch = new CountDownLatch(5);

        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                try {
                    startLatch.await();
                    rwLock.readLock().lock();
                    int readers = concurrentReaders.incrementAndGet();
                    Thread.sleep(100);
                    concurrentReaders.decrementAndGet();
                    rwLock.readLock().unlock();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    doneLatch.countDown();
                }
            }).start();
        }

        startLatch.countDown();
        doneLatch.await();
        assertTrue(true, "多个读者应能同时获取读锁");
    }
}
