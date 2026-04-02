package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ScheduleTaskApplication {
    public static void main(String[] args) {
        SpringApplication.run(ScheduleTaskApplication.class, args);
        System.out.println("定时任务演示应用启动成功!");
    }
}
