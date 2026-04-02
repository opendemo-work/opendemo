package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * MongoDB集成演示应用
 */
@SpringBootApplication
public class MongoDbDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(MongoDbDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("MongoDB集成演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("添加用户: POST http://localhost:8080/api/users");
        System.out.println("查询用户: GET http://localhost:8080/api/users");
        System.out.println("==============================================");
    }
}
