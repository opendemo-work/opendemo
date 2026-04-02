package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * 异步处理演示应用
 * 
 * @EnableAsync 启用异步支持
 */
@SpringBootApplication
@EnableAsync
public class AsyncDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(AsyncDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("异步处理演示应用启动成功!");
        System.out.println("==============================================");
    }
}
