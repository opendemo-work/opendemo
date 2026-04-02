package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ConditionalApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConditionalApplication.class, args);
        System.out.println("条件装配演示应用启动成功!");
    }
}
