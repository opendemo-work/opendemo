package com.opendemo.java.concurrent;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class ProducerConsumerDemo {

    public static void main(String[] args) throws Exception {
        demonstrateBlockingQueue();
        demonstrateWaitNotify();
        demonstrateBoundedBuffer();
        printQueueComparison();
    }

    public static void demonstrateBlockingQueue() throws Exception {
        System.out.println("=== BlockingQueue 生产者消费者 ===");

        BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
        int messageCount = 20;

        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < messageCount; i++) {
                    String msg = "消息-" + i;
                    queue.put(msg);
                    System.out.printf("  [生产者] 放入: %s (队列大小: %d)%n", msg, queue.size());
                }
                queue.put("END");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, "Producer");

        Thread consumer = new Thread(() -> {
            try {
                String msg;
                while (!"END".equals(msg = queue.take())) {
                    System.out.printf("  [消费者] 取出: %s (队列大小: %d)%n", msg, queue.size());
                    Thread.sleep(50);
                }
                System.out.println("  [消费者] 收到结束信号");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, "Consumer");

        producer.start();
        consumer.start();
        producer.join();
        consumer.join();

        System.out.println("  BlockingQueue方法:");
        System.out.println("    put(e)  - 队列满时阻塞");
        System.out.println("    take()  - 队列空时阻塞");
        System.out.println("    offer(e, timeout) - 超时放弃");
        System.out.println("    poll(timeout)     - 超时放弃");
        System.out.println();
    }

    public static void demonstrateWaitNotify() throws Exception {
        System.out.println("=== wait/notify 生产者消费者 ===");

        SimpleBuffer buffer = new SimpleBuffer(5);
        int itemCount = 10;

        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < itemCount; i++) {
                    buffer.put("item-" + i);
                    System.out.printf("  [wait/notify生产者] 放入: item-%d%n", i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < itemCount; i++) {
                    String item = buffer.take();
                    System.out.printf("  [wait/notify消费者] 取出: %s%n", item);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        producer.start();
        consumer.start();
        producer.join();
        consumer.join();

        System.out.println("  wait/notify要点:");
        System.out.println("    1. 必须在synchronized块中调用");
        System.out.println("    2. 使用while循环检查条件（防止虚假唤醒）");
        System.out.println("    3. 推荐使用notifyAll()而非notify()");
        System.out.println();
    }

    public static void demonstrateBoundedBuffer() throws Exception {
        System.out.println("=== 有界缓冲区应用场景 ===");
        System.out.println("  1. 生产速度 > 消费速度: 队列积压，生产者阻塞");
        System.out.println("  2. 消费速度 > 生产速度: 队列空闲，消费者阻塞");
        System.out.println("  3. 缓冲区大小: 需根据业务场景调整");
        System.out.println();

        ArrayBlockingQueue<Integer> queue = new ArrayBlockingQueue<>(3);
        CountDownLatch latch = new CountDownLatch(2);

        new Thread(() -> {
            try {
                for (int i = 1; i <= 8; i++) {
                    long start = System.currentTimeMillis();
                    queue.put(i);
                    long waitTime = System.currentTimeMillis() - start;
                    if (waitTime > 10) {
                        System.out.printf("  [生产者] 等待了 %d ms 才放入 %d%n", waitTime, i);
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                latch.countDown();
            }
        }).start();

        new Thread(() -> {
            try {
                Thread.sleep(200);
                while (!queue.isEmpty() || true) {
                    Integer item = queue.poll(100, TimeUnit.MILLISECONDS);
                    if (item != null) {
                        System.out.printf("  [消费者] 处理: %d%n", item);
                        if (item == 8) break;
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                latch.countDown();
            }
        }).start();

        latch.await();
        System.out.println();
    }

    public static void printQueueComparison() {
        System.out.println("=== 阻塞队列对比 ===");
        System.out.println("┌────────────────────┬──────────────┬──────────────────────┐");
        System.out.println("│ 队列类型           │ 有界         │ 特点                 │");
        System.out.println("├────────────────────┼──────────────┼──────────────────────┤");
        System.out.println("│ ArrayBlockingQueue │ 是(固定)     │ 有界, 公平可选       │");
        System.out.println("│ LinkedBlockingQueue │ 可选        │ 可选有界, 吞吐高     │");
        System.out.println("│ PriorityBlockingQueue│ 否         │ 优先级排序           │");
        System.out.println("│ SynchronousQueue   │ 是(容量0)    │ 直接传递, 无缓冲     │");
        System.out.println("│ DelayQueue         │ 否           │ 延迟取出元素         │");
        System.out.println("│ LinkedTransferQueue│ 否           │ transfer()直接传递   │");
        System.out.println("└────────────────────┴──────────────┴──────────────────────┘");
    }

    static class SimpleBuffer {
        private final String[] items;
        private int putIdx = 0;
        private int takeIdx = 0;
        private int count = 0;

        SimpleBuffer(int capacity) {
            this.items = new String[capacity];
        }

        synchronized void put(String item) throws InterruptedException {
            while (count == items.length) {
                wait();
            }
            items[putIdx] = item;
            putIdx = (putIdx + 1) % items.length;
            count++;
            notifyAll();
        }

        synchronized String take() throws InterruptedException {
            while (count == 0) {
                wait();
            }
            String item = items[takeIdx];
            items[takeIdx] = null;
            takeIdx = (takeIdx + 1) % items.length;
            count--;
            notifyAll();
            return item;
        }

        synchronized int size() {
            return count;
        }
    }
}
