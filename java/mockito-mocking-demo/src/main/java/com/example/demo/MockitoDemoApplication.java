package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Mockito Mock测试演示应用
 */
@SpringBootApplication
public class MockitoDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(MockitoDemoApplication.class, args);
        System.out.println("Mockito Mock测试演示应用启动成功!");
        System.out.println("运行测试: mvn test");
    }
}
