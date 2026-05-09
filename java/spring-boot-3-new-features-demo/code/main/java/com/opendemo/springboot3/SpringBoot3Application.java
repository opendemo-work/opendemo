package com.opendemo.springboot3;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Boot 3.x 主启动类
 *
 * 演示新特性:
 * - Virtual Threads (虚拟线程)
 * - Jakarta EE 10
 * - Spring Boot 3.x 自动配置增强
 */
@SpringBootApplication
public class SpringBoot3Application {

    public static void main(String[] args) {
        // 启用虚拟线程 (预览功能)
        // System.setProperty("java.threads.virtual.enabled", "true");

        SpringApplication.run(SpringBoot3Application.class, args);

        System.out.println("\n========================================");
        System.out.println("Spring Boot 3.x 应用已启动!");
        System.out.println("========================================\n");
    }
}