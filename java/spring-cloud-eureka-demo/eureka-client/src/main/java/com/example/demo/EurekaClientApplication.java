package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

/**
 * Eureka客户端应用
 * 
 * @EnableEurekaClient 启用Eureka客户端
 */
@SpringBootApplication
@EnableEurekaClient
public class EurekaClientApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(EurekaClientApplication.class, args);
        System.out.println("Eureka Client 启动成功!");
    }
}
