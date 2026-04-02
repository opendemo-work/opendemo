package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

/**
 * Spring Cloud Alibaba Nacos演示应用
 * 
 * @EnableDiscoveryClient 启用服务发现
 */
@SpringBootApplication
@EnableDiscoveryClient
public class NacosDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(NacosDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Spring Cloud Alibaba Nacos演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("服务注册中心: http://localhost:8848/nacos");
        System.out.println("本服务地址: http://localhost:8080");
        System.out.println("==============================================");
    }
}
