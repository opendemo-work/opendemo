package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpelApplication {
    public static void main(String[] args) {
        SpringApplication.run(SpelApplication.class, args);
        System.out.println("SpEL表达式演示应用启动成功!");
    }
}
