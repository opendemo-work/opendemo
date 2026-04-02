package com.example.demo.task;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Component
public class ScheduledTasks {
    
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    @Scheduled(fixedRate = 5000)
    public void reportCurrentTime() {
        System.out.println("[固定频率] 当前时间: " + LocalDateTime.now().format(formatter));
    }
    
    @Scheduled(fixedDelay = 10000)
    public void reportWithDelay() {
        System.out.println("[固定延迟] 当前时间: " + LocalDateTime.now().format(formatter));
    }
    
    @Scheduled(cron = "0 */1 * * * ?")
    public void reportWithCron() {
        System.out.println("[Cron表达式] 每分钟执行: " + LocalDateTime.now().format(formatter));
    }
}
