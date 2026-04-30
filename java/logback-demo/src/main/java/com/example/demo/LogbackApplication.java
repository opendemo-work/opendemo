package com.example.demo;

import com.example.demo.service.LoggingService;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

@SpringBootApplication
public class LogbackApplication {

    public static void main(String[] args) {
        ConfigurableApplicationContext context = SpringApplication.run(LogbackApplication.class, args);

        LoggingService loggingService = context.getBean(LoggingService.class);

        System.out.println("=== Logback 日志演示 ===");
        loggingService.demonstrateAllLevels();
        loggingService.demonstrateParameterizedLogging();
        loggingService.demonstrateExceptionLogging();
        loggingService.logWithMdc("user001", "LOGIN");
        loggingService.logAudit("admin", "CONFIG_CHANGE", "修改系统配置");
    }
}
