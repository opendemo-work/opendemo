package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Security JWT演示应用
 */
@SpringBootApplication
public class JwtDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(JwtDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Spring Security JWT演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("登录接口: POST http://localhost:8080/api/auth/login");
        System.out.println("请求体: {\"username\": \"admin\", \"password\": \"123456\"}");
        System.out.println("==============================================");
        System.out.println("受保护接口: GET http://localhost:8080/api/user/profile");
        System.out.println("Header: Authorization: Bearer {token}");
        System.out.println("==============================================");
    }
}
