package com.opendemo.java.concurrent;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

public class ThreadCreationDemo {

    public static void main(String[] args) throws Exception {
        demonstrateThread();
        demonstrateRunnable();
        demonstrateCallable();
        demonstrateDaemonThread();
        demonstrateThreadLifecycle();
    }

    public static void demonstrateThread() throws InterruptedException {
        System.out.println("=== 方式一: 继承Thread类 ===");

        Thread thread = new Thread("CustomThread") {
            @Override
            public void run() {
                System.out.printf("  [%s] 线程运行中, 优先级=%d%n",
                        getName(), getPriority());
            }
        };

        thread.start();
        thread.join();

        System.out.println("  优点: 简单直接");
        System.out.println("  缺点: Java单继承，无法继承其他类");
        System.out.println();
    }

    public static void demonstrateRunnable() throws InterruptedException {
        System.out.println("=== 方式二: 实现Runnable接口 ===");

        Runnable task = () -> {
            System.out.printf("  [%s] Runnable任务执行%n",
                    Thread.currentThread().getName());
        };

        Thread thread1 = new Thread(task, "RunnableThread-1");
        Thread thread2 = new Thread(task, "RunnableThread-2");

        thread1.start();
        thread2.start();
        thread1.join();
        thread2.join();

        System.out.println("  优点: 可继承其他类，可使用Lambda");
        System.out.println("  缺点: 无返回值，不能抛受检异常");
        System.out.println();
    }

    public static void demonstrateCallable() throws ExecutionException, InterruptedException {
        System.out.println("=== 方式三: 实现Callable接口 ===");

        Callable<Integer> task = () -> {
            int result = 0;
            for (int i = 1; i <= 100; i++) {
                result += i;
            }
            System.out.printf("  [%s] 计算完成: 1+2+...+100 = %d%n",
                    Thread.currentThread().getName(), result);
            return result;
        };

        FutureTask<Integer> futureTask = new FutureTask<>(task);
        Thread thread = new Thread(futureTask, "CallableThread");
        thread.start();

        Integer result = futureTask.get();
        System.out.printf("  获取结果: %d%n", result);
        System.out.println("  优点: 有返回值，可抛受检异常");
        System.out.println();
    }

    public static void demonstrateDaemonThread() throws InterruptedException {
        System.out.println("=== 守护线程 ===");

        Thread daemon = new Thread(() -> {
            int count = 0;
            while (count < 5) {
                System.out.printf("  [守护线程] 运行中... count=%d%n", count);
                count++;
                try { Thread.sleep(100); } catch (InterruptedException e) { break; }
            }
        });

        daemon.setDaemon(true);
        daemon.start();

        Thread.sleep(300);
        System.out.println("  主线程结束，守护线程随JVM退出");
        System.out.println("  用途: GC线程、后台监控线程");
        System.out.println();
    }

    public static void demonstrateThreadLifecycle() {
        System.out.println("=== 线程生命周期 ===");
        System.out.println("  NEW           → 新建，未启动");
        System.out.println("  RUNNABLE      → 可运行（就绪或运行中）");
        System.out.println("  BLOCKED       → 阻塞（等待锁）");
        System.out.println("  WAITING       → 等待（wait/join/park）");
        System.out.println("  TIMED_WAITING → 超时等待（sleep/wait(timeout)）");
        System.out.println("  TERMINATED    → 终止");

        Thread t = new Thread(() -> {});
        System.out.printf("  新建线程状态: %s%n", t.getState());

        t.start();
        System.out.printf("  启动后状态: %s%n", t.getState());
    }
}
