package com.example.demo.config;

import com.example.demo.service.GreetingService;
import com.example.demo.service.impl.SimpleGreetingService;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 问候服务自动配置类
 * 
 * 演示Spring Boot自动配置原理
 */
@Configuration
@ConditionalOnClass(GreetingService.class)  // 类路径存在时生效
@ConditionalOnProperty(prefix = "greeting", name = "enabled", havingValue = "true", matchIfMissing = true)
@EnableConfigurationProperties(GreetingProperties.class)
public class GreetingAutoConfiguration {
    
    private final GreetingProperties properties;
    
    public GreetingAutoConfiguration(GreetingProperties properties) {
        this.properties = properties;
    }
    
    /**
     * 创建GreetingService Bean
     * 
     * @ConditionalOnMissingBean: 当容器中不存在该Bean时才创建
     */
    @Bean
    @ConditionalOnMissingBean
    public GreetingService greetingService() {
        System.out.println("  [自动配置] 创建 GreetingService Bean");
        System.out.println("    配置前缀: " + properties.getPrefix());
        
        SimpleGreetingService service = new SimpleGreetingService();
        service.setGreetingPrefix(properties.getPrefix());
        return service;
    }
}
