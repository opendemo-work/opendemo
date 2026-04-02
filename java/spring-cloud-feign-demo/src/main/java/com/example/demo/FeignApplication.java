package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

/**
 * Spring Cloud Feign应用
 * 
 * @EnableFeignClients 启用Feign客户端
 */
@SpringBootApplication
@EnableFeignClients
public class FeignApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(FeignApplication.class, args);
        System.out.println("Feign应用启动成功!");
        System.out.println("访问: http://localhost:8080/feign/users");
    }
}
