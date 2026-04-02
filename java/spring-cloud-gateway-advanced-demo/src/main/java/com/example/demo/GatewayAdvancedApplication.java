package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

/**
 * Spring Cloud Gateway高级特性演示应用
 * 
 * 演示功能：
 * - 动态路由
 * - 限流（Redis RateLimiter）
 * - 熔断（Circuit Breaker）
 * - 鉴权（JWT验证）
 * - 灰度发布
 */
@SpringBootApplication
@EnableDiscoveryClient
public class GatewayAdvancedApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(GatewayAdvancedApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Spring Cloud Gateway高级演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("网关地址: http://localhost:8080");
        System.out.println("Eureka: http://localhost:8761");
        System.out.println("==============================================");
    }
}
