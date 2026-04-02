package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 参数校验演示应用
 */
@SpringBootApplication
public class ValidationDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(ValidationDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("参数校验演示应用启动成功!");
        System.out.println("==============================================");
    }
}
