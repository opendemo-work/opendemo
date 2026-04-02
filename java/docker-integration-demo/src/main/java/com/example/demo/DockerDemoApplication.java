package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Docker容器化演示应用
 */
@SpringBootApplication
public class DockerDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(DockerDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Docker容器化演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("健康检查: http://localhost:8080/actuator/health");
        System.out.println("==============================================");
    }
}
