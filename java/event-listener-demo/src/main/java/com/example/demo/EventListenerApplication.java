package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.scheduling.annotation.EnableAsync;

import com.example.demo.service.EventPublisherService;

@SpringBootApplication
@EnableAsync
public class EventListenerApplication {
    public static void main(String[] args) {
        ConfigurableApplicationContext context = SpringApplication.run(EventListenerApplication.class, args);

        EventPublisherService publisher = context.getBean(EventPublisherService.class);

        System.out.println("=== Spring Events 演示 ===");
        publisher.publishUserRegistered("张三", "zhangsan@test.com");
        publisher.publishOrderCreated("ORD001", "张三", 500.0);
        publisher.publishOrderCreated("ORD002", "李四", 2000.0);

        System.out.println("事件监听演示应用启动成功!");
    }
}
