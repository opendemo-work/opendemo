package com.opendemo.java.concurrent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.CountDownLatch;

public class ConcurrentCollectionsDemo {

    public static void main(String[] args) throws Exception {
        demonstrateConcurrentHashMap();
        demonstrateCopyOnWriteArrayList();
        demonstrateSynchronizedCollection();
        demonstrateCollectionsComparison();
    }

    public static void demonstrateConcurrentHashMap() throws Exception {
        System.out.println("=== ConcurrentHashMap ===");

        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        int threadCount = 10;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            final int threadId = i;
            new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    String key = "key-" + (threadId * 100 + j);
                    map.put(key, threadId * 100 + j);
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        System.out.printf("  ConcurrentHashMap大小: %d (期望: %d)%n",
                map.size(), threadCount * 100);

        map.put("atomic-key", 0);
        map.compute("atomic-key", (k, v) -> v + 1);
        System.out.printf("  compute原子操作结果: %d%n", map.get("atomic-key"));

        map.merge("merge-key", 1, Integer::sum);
        map.merge("merge-key", 2, Integer::sum);
        System.out.printf("  merge累加结果: %d%n", map.get("merge-key"));

        System.out.println("  特点: 分段锁（Java 8+ CAS+synchronized）, 高并发读写");
        System.out.println();
    }

    public static void demonstrateCopyOnWriteArrayList() throws Exception {
        System.out.println("=== CopyOnWriteArrayList ===");

        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        int threadCount = 5;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            final int threadId = i;
            new Thread(() -> {
                for (int j = 0; j < 20; j++) {
                    list.add("item-" + threadId + "-" + j);
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        System.out.printf("  CopyOnWriteArrayList大小: %d%n", list.size());

        System.out.println("  特点: 写时复制，读无锁");
        System.out.println("  适用: 读多写少场景（如监听器列表）");
        System.out.println("  缺点: 写操作开销大（需复制整个数组）");
        System.out.println();
    }

    public static void demonstrateSynchronizedCollection() throws Exception {
        System.out.println("=== Collections.synchronizedList ===");

        List<String> syncList = Collections.synchronizedList(new ArrayList<>());
        int threadCount = 5;
        CountDownLatch latch = new CountDownLatch(threadCount);

        for (int i = 0; i < threadCount; i++) {
            final int threadId = i;
            new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    syncList.add("item-" + threadId + "-" + j);
                }
                latch.countDown();
            }).start();
        }

        latch.await();
        System.out.printf("  synchronizedList大小: %d%n", syncList.size());
        System.out.println("  特点: 使用synchronized包装，所有操作加锁");
        System.out.println("  注意: 遍历时需手动加锁");
        System.out.println();
    }

    public static void demonstrateCollectionsComparison() {
        System.out.println("=== 并发集合对比 ===");
        System.out.println("┌───────────────────────┬──────────────┬──────────────┬──────────────┐");
        System.out.println("│ 集合                  │ 线程安全     │ 读性能       │ 写性能       │");
        System.out.println("├───────────────────────┼──────────────┼──────────────┼──────────────┤");
        System.out.println("│ HashMap               │ ✗            │ 高           │ 高           │");
        System.out.println("│ ConcurrentHashMap     │ ✓            │ 高           │ 中高         │");
        System.out.println("│ Hashtable             │ ✓            │ 低           │ 低           │");
        System.out.println("│ ArrayList             │ ✗            │ 高           │ 高           │");
        System.out.println("│ CopyOnWriteArrayList  │ ✓            │ 高(无锁)     │ 低(复制)     │");
        System.out.println("│ synchronizedList      │ ✓            │ 中           │ 中           │");
        System.out.println("└───────────────────────┴──────────────┴──────────────┴──────────────┘");
    }
}
