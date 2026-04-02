package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ExceptionHandlingApplication {
    public static void main(String[] args) {
        SpringApplication.run(ExceptionHandlingApplication.class, args);
        System.out.println("全局异常处理演示应用启动成功!");
    }
}
