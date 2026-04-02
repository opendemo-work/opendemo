package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.circuitbreaker.EnableCircuitBreaker;

/**
 * Spring Cloud Hystrix熔断器演示应用
 * 
 * @EnableCircuitBreaker 启用熔断器功能
 */
@SpringBootApplication
@EnableCircuitBreaker
public class HystrixDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(HystrixDemoApplication.class, args);
        System.out.println("Hystrix熔断器演示应用启动成功!");
        System.out.println("访问: http://localhost:8080/api/normal");
        System.out.println("访问: http://localhost:8080/api/slow");
        System.out.println("访问: http://localhost:8080/api/error");
        System.out.println("监控: http://localhost:8080/actuator/hystrix.stream");
    }
}
