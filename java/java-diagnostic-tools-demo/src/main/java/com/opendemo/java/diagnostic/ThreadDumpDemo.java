package com.opendemo.java.diagnostic;

import java.lang.management.*;
import java.util.Arrays;
import java.util.stream.Collectors;

public class ThreadDumpDemo {
    public static void main(String[] args) {
        System.out.println("=== Thread Dump Demo ===\n");
        printThreadInfo();
        printDeadlockInfo();
        demonstrateThreadStates();
    }

    static void printThreadInfo() {
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        System.out.println("1. Thread Info:");
        System.out.println("Thread Count: " + threadBean.getThreadCount());
        System.out.println("Peak Thread Count: " + threadBean.getPeakThreadCount());
        System.out.println("Daemon Thread Count: " + threadBean.getDaemonThreadCount());
        System.out.println("Total Started Threads: " + threadBean.getTotalStartedThreadCount());
        System.out.println();

        long[] threadIds = threadBean.getAllThreadIds();
        System.out.println("Active threads:");
        for (ThreadInfo info : threadBean.getThreadInfo(threadIds)) {
            if (info != null) {
                System.out.printf("  [%d] %s - %s%n", info.getThreadId(), info.getThreadName(), info.getThreadState());
            }
        }
        System.out.println();
    }

    static void printDeadlockInfo() {
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        System.out.println("2. Deadlock Detection:");
        long[] deadlocks = threadBean.findDeadlockedThreads();
        if (deadlocks != null && deadlocks.length > 0) {
            System.out.println("DEADLOCK DETECTED! Threads: " + Arrays.toString(deadlocks));
            for (ThreadInfo info : threadBean.getThreadInfo(deadlocks)) {
                System.out.println("Deadlocked thread: " + info.getThreadName());
            }
        } else {
            System.out.println("No deadlocks detected.");
        }
        System.out.println();
    }

    static void demonstrateThreadStates() {
        System.out.println("3. Thread States:");
        Object lock = new Object();
        Thread waitingThread = new Thread(() -> {
            synchronized (lock) {
                try {
                    lock.wait();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }, "waiting-thread");
        Thread sleepingThread = new Thread(() -> {
            try {
                Thread.sleep(60000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, "sleeping-thread");
        Thread runningThread = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                Math.sqrt(Math.random());
            }
        }, "cpu-intensive-thread");

        waitingThread.start();
        sleepingThread.start();
        runningThread.start();

        try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }

        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        for (Thread t : Arrays.asList(waitingThread, sleepingThread, runningThread)) {
            ThreadInfo info = threadBean.getThreadInfo(t.getId());
            if (info != null) {
                System.out.printf("  %s -> %s%n", t.getName(), info.getThreadState());
            }
        }

        runningThread.interrupt();
        waitingThread.interrupt();
        sleepingThread.interrupt();
        System.out.println();
    }
}
