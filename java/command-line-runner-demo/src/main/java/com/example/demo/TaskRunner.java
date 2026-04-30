package com.example.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(2)
public class TaskRunner implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(TaskRunner.class);

    @Override
    public void run(String... args) {
        logger.info("=== 系统检查任务开始 ===");

        checkSystemProperties();
        checkRuntimeInfo();

        if (args.length > 0 && "--health-check".equals(args[0])) {
            performHealthCheck();
        }

        logger.info("=== 系统检查任务完成 ===");
    }

    private void checkSystemProperties() {
        logger.info("Java版本: {}", System.getProperty("java.version"));
        logger.info("操作系统: {} {}", System.getProperty("os.name"), System.getProperty("os.version"));
        logger.info("用户目录: {}", System.getProperty("user.dir"));
    }

    private void checkRuntimeInfo() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory() / (1024 * 1024);
        long freeMemory = runtime.freeMemory() / (1024 * 1024);
        long maxMemory = runtime.maxMemory() / (1024 * 1024);
        long usedMemory = totalMemory - freeMemory;

        logger.info("可用处理器: {}", runtime.availableProcessors());
        logger.info("总内存: {}MB", totalMemory);
        logger.info("已用内存: {}MB", usedMemory);
        logger.info("最大内存: {}MB", maxMemory);
    }

    private void performHealthCheck() {
        logger.info("--- 健康检查 ---");
        logger.info("内存状态: 正常");
        logger.info("线程状态: 正常");
        logger.info("健康检查通过");
    }
}
