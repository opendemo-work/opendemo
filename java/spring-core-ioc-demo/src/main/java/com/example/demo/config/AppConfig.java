package com.example.demo.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

/**
 * Spring配置类
 * 
 * 使用Java配置方式替代XML配置
 * @Configuration 标记这是一个配置类
 * @ComponentScan 启用组件扫描，自动发现和注册Bean
 */
@Configuration
@ComponentScan(basePackages = "com.example.demo")
public class AppConfig {
    
    // 这里可以显式定义Bean
    // @Bean
    // public UserService userService() {
    //     return new UserServiceImpl();
    // }
    
    // 但在本例中，我们使用@ComponentScan自动扫描
    // 配合@Service注解实现自动注册
}
