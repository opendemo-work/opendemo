package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class EventListenerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EventListenerApplication.class, args);
        System.out.println("事件监听演示应用启动成功!");
    }
}
