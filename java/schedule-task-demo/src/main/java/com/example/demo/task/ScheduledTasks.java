package com.example.demo.task;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.atomic.AtomicInteger;

@Component
public class ScheduledTasks {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private final AtomicInteger executionCount = new AtomicInteger(0);

    @Scheduled(fixedRate = 5000)
    public void reportCurrentTime() {
        executionCount.incrementAndGet();
        System.out.println("[固定频率] 当前时间: " + LocalDateTime.now().format(formatter));
    }

    @Scheduled(fixedDelay = 10000)
    public void reportWithDelay() {
        executionCount.incrementAndGet();
        System.out.println("[固定延迟] 当前时间: " + LocalDateTime.now().format(formatter));
    }

    @Scheduled(cron = "0 */1 * * * ?")
    public void reportWithCron() {
        executionCount.incrementAndGet();
        System.out.println("[Cron表达式] 每分钟执行: " + LocalDateTime.now().format(formatter));
    }

    @Scheduled(fixedRate = 5000, initialDelay = 10000)
    public void reportWithInitialDelay() {
        executionCount.incrementAndGet();
        System.out.println("[初始延迟] 启动后10秒首次执行: " + LocalDateTime.now().format(formatter));
    }

    public int getExecutionCount() {
        return executionCount.get();
    }
}
