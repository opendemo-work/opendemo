package com.example.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(1)
public class StartupRunner implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(StartupRunner.class);

    @Override
    public void run(String... args) {
        logger.info("=== CommandLineRunner 启动任务 ===");
        logger.info("参数数量: {}", args.length);
        for (String arg : args) {
            logger.info("参数: {}", arg);
        }
        logger.info("=== 启动任务完成 ===");
    }
}
