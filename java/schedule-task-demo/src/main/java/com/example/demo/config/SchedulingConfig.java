package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.SchedulingConfigurer;
import org.springframework.scheduling.config.ScheduledTaskRegistrar;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;

@Configuration
public class SchedulingConfig implements SchedulingConfigurer {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    @Override
    public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
        taskRegistrar.setScheduler(taskExecutor());

        taskRegistrar.addFixedRateTask(() -> {
            System.out.println("[编程式配置] 每30秒执行: " + LocalDateTime.now().format(formatter));
        }, Duration.ofSeconds(30));
    }

    @Bean(destroyMethod = "shutdown")
    public ScheduledExecutorService taskExecutor() {
        return Executors.newScheduledThreadPool(4);
    }
}
