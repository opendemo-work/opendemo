package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AopLoggingApplication {
    public static void main(String[] args) {
        SpringApplication.run(AopLoggingApplication.class, args);
        System.out.println("AOP日志演示应用启动成功!");
    }
}
