package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Redis缓存集成示例应用
 * 
 * 演示Spring Boot与Redis的集成，包括:
 * - 缓存配置
 * - @Cacheable, @CachePut, @CacheEvict注解
 * - 缓存TTL设置
 */
@SpringBootApplication
public class CacheDemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(CacheDemoApplication.class, args);
    }
}
