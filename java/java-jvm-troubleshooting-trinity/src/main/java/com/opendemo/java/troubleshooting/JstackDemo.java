package com.opendemo.java.troubleshooting;

import java.lang.management.*;
import java.util.Arrays;

public class JstackDemo {
    public static void main(String[] args) {
        System.out.println("=== Jstack Demo (via MXBeans) ===\n");
        printFullThreadDump();
        detectDeadlocks();
        findBusyThreads();
    }

    static void printFullThreadDump() {
        System.out.println("1. Full Thread Dump (-l equivalent):");
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        System.out.printf("  Total threads: %d%n", threadBean.getThreadCount());
        System.out.printf("  Peak threads: %d%n", threadBean.getPeakThreadCount());
        System.out.printf("  Daemon threads: %d%n", threadBean.getDaemonThreadCount());
        System.out.println();

        ThreadInfo[] threads = threadBean.getThreadInfo(threadBean.getAllThreadIds(), 20);
        for (ThreadInfo info : threads) {
            if (info == null) continue;
            System.out.printf("  \"%s\" #%d prio=%d tid=%d%n",
                    info.getThreadName(), info.getThreadId(),
                    info.getPriority(), info.getThreadId());
            System.out.printf("    java.lang.Thread.State: %s%n", info.getThreadState());
            StackTraceElement[] stack = info.getStackTrace();
            for (int i = 0; i < Math.min(stack.length, 5); i++) {
                System.out.printf("      at %s%n", stack[i]);
            }
            if (stack.length > 5) {
                System.out.printf("      ... %d more%n", stack.length - 5);
            }
            System.out.println();
        }
    }

    static void detectDeadlocks() {
        System.out.println("2. Deadlock Detection:");
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        long[] deadlocked = threadBean.findDeadlockedThreads();
        long[] monitorDeadlocked = threadBean.findMonitorDeadlockedThreads();

        if ((deadlocked != null && deadlocked.length > 0) ||
                (monitorDeadlocked != null && monitorDeadlocked.length > 0)) {
            System.out.println("  DEADLOCK DETECTED!");
            if (deadlocked != null) {
                System.out.println("  Cyclic deadlock threads: " + Arrays.toString(deadlocked));
                for (ThreadInfo info : threadBean.getThreadInfo(deadlocked)) {
                    printDeadlockDetail(info);
                }
            }
        } else {
            System.out.println("  No deadlocks detected.");
        }
        System.out.println();
    }

    private static void printDeadlockDetail(ThreadInfo info) {
        if (info == null) return;
        System.out.printf("  Thread \"%s\" (%s)%n", info.getThreadName(), info.getThreadState());
        System.out.printf("    Waiting on lock: %s%n", info.getLockName());
        if (info.getLockOwnerName() != null) {
            System.out.printf("    Owned by: %s (tid=%d)%n", info.getLockOwnerName(), info.getLockOwnerId());
        }
    }

    static void findBusyThreads() {
        System.out.println("3. Thread CPU Time Analysis:");
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        if (!threadBean.isThreadCpuTimeSupported()) {
            System.out.println("  Thread CPU time not supported.");
            return;
        }
        threadBean.setThreadCpuTimeEnabled(true);

        long[] ids = threadBean.getAllThreadIds();
        ThreadInfo[] infos = threadBean.getThreadInfo(ids);

        System.out.printf("  %-30s %-12s %12s%n", "Thread", "State", "CPU Time(ms)");
        System.out.println("  " + "-".repeat(58));

        java.util.List<Object[]> rows = new java.util.ArrayList<>();
        for (int i = 0; i < ids.length; i++) {
            if (infos[i] == null) continue;
            long cpuTime = threadBean.getThreadCpuTime(ids[i]);
            rows.add(new Object[]{infos[i].getThreadName(), infos[i].getThreadState(), cpuTime / 1_000_000});
        }
        rows.sort((a, b) -> Long.compare((long) b[2], (long) a[2]));
        for (Object[] row : rows.stream().limit(10).toArray(java.util.List<Object[]>::new).toArray(new Object[0][])) {
            System.out.printf("  %-30s %-12s %12d%n", row[0], row[1], row[2]);
        }
        System.out.println();
    }
}
