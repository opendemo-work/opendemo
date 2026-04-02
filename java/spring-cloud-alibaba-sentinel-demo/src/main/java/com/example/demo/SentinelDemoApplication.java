package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Cloud Alibaba Sentinel演示应用
 * 
 * Sentinel: 流量控制、熔断降级、系统负载保护
 */
@SpringBootApplication
public class SentinelDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(SentinelDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Spring Cloud Alibaba Sentinel演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("Sentinel Dashboard: http://localhost:8080");
        System.out.println("测试接口: http://localhost:8080/hello");
        System.out.println("流量控制: http://localhost:8080/rate-limit");
        System.out.println("==============================================");
    }
}
