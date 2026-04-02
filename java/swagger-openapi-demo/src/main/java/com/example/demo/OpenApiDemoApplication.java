package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Swagger OpenAPI演示应用
 */
@SpringBootApplication
public class OpenApiDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(OpenApiDemoApplication.class, args);
        System.out.println("==============================================");
        System.out.println("Swagger OpenAPI演示应用启动成功!");
        System.out.println("==============================================");
        System.out.println("API文档: http://localhost:8080/swagger-ui.html");
        System.out.println("API JSON: http://localhost:8080/v3/api-docs");
        System.out.println("==============================================");
    }
}
