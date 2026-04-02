package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ProfilesApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProfilesApplication.class, args);
        System.out.println("多环境配置演示应用启动成功!");
    }
}
