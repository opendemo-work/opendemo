package com.opendemo.java.profiling;

import java.lang.management.ClassLoadingMXBean;
import java.lang.management.CompilationMXBean;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import java.lang.management.RuntimeMXBean;
import java.lang.management.ThreadMXBean;
import java.util.List;

public class JmxProfilingDemo {

    public static void main(String[] args) {
        demonstrateRuntimeMXBean();
        demonstrateOperatingSystemMXBean();
        demonstrateCompilationMXBean();
        demonstrateClassLoadingMXBean();
        demonstrateThreadMXBeanOverview();
    }

    public static void demonstrateRuntimeMXBean() {
        System.out.println("=== RuntimeMXBean 运行时信息 ===");

        RuntimeMXBean runtimeBean = ManagementFactory.getRuntimeMXBean();

        System.out.printf("JVM名称: %s%n", runtimeBean.getVmName());
        System.out.printf("JVM版本: %s%n", runtimeBean.getVmVersion());
        System.out.printf("JVM供应商: %s%n", runtimeBean.getVmVendor());
        System.out.printf("启动时间: %d ms%n", runtimeBean.getStartTime());
        System.out.printf("运行时间: %d ms%n", runtimeBean.getUptime());
        System.out.printf("进程ID: %s%n", getProcessId(runtimeBean));

        System.out.println("JVM参数:");
        List<String> args = runtimeBean.getInputArguments();
        for (String arg : args) {
            System.out.printf("  %s%n", arg);
        }
        System.out.println();
    }

    public static void demonstrateOperatingSystemMXBean() {
        System.out.println("=== OperatingSystemMXBean 操作系统信息 ===");

        OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();

        System.out.printf("操作系统: %s%n", osBean.getName());
        System.out.printf("系统版本: %s%n", osBean.getVersion());
        System.out.printf("系统架构: %s%n", osBean.getArch());
        System.out.printf("可用CPU: %d%n", osBean.getAvailableProcessors());
        System.out.printf("系统负载: %.2f%n", osBean.getSystemLoadAverage());

        if (osBean instanceof com.sun.management.OperatingSystemMXBean) {
            com.sun.management.OperatingSystemMXBean sunOsBean =
                    (com.sun.management.OperatingSystemMXBean) osBean;
            System.out.printf("进程CPU使用率: %.1f%%%n", sunOsBean.getProcessCpuLoad() * 100);
            System.out.printf("系统CPU使用率: %.1f%%%n", sunOsBean.getSystemCpuLoad() * 100);
            System.out.printf("总物理内存: %d MB%n", sunOsBean.getTotalPhysicalMemorySize() / (1024 * 1024));
            System.out.printf("可用物理内存: %d MB%n", sunOsBean.getFreePhysicalMemorySize() / (1024 * 1024));
        }
        System.out.println();
    }

    public static void demonstrateCompilationMXBean() {
        System.out.println("=== CompilationMXBean JIT编译信息 ===");

        CompilationMXBean compBean = ManagementFactory.getCompilationMXBean();

        System.out.printf("JIT编译器名称: %s%n", compBean.getName());
        System.out.printf("JIT编译总时间: %d ms%n", compBean.getTotalCompilationTime());
        System.out.println();
    }

    public static void demonstrateClassLoadingMXBean() {
        System.out.println("=== ClassLoadingMXBean 类加载信息 ===");

        ClassLoadingMXBean clBean = ManagementFactory.getClassLoadingMXBean();

        System.out.printf("已加载类数: %d%n", clBean.getLoadedClassCount());
        System.out.printf("总加载类数: %d%n", clBean.getTotalLoadedClassCount());
        System.out.printf("已卸载类数: %d%n", clBean.getUnloadedClassCount());
        System.out.printf("是否开启详细输出: %b%n", clBean.isVerbose());
        System.out.println();
    }

    public static void demonstrateThreadMXBeanOverview() {
        System.out.println("=== ThreadMXBean 线程概览 ===");

        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();

        System.out.printf("当前线程数: %d%n", threadBean.getThreadCount());
        System.out.printf("峰值线程数: %d%n", threadBean.getPeakThreadCount());
        System.out.printf("守护线程数: %d%n", threadBean.getDaemonThreadCount());
        System.out.printf("启动线程总数: %d%n", threadBean.getTotalStartedThreadCount());
        System.out.printf("是否支持CPU时间: %b%n", threadBean.isCurrentThreadCpuTimeSupported());
        System.out.printf("是否开启CPU时间: %b%n", threadBean.isThreadCpuTimeEnabled());
    }

    private static String getProcessId(RuntimeMXBean runtimeBean) {
        String name = runtimeBean.getName();
        return name.contains("@") ? name.substring(0, name.indexOf('@')) : name;
    }
}
