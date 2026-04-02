package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * JUnit5单元测试演示应用
 */
@SpringBootApplication
public class JUnit5DemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(JUnit5DemoApplication.class, args);
        System.out.println("JUnit5测试演示应用启动成功!");
        System.out.println("运行测试: mvn test");
    }
}
