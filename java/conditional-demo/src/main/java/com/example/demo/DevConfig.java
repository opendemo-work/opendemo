package com.example.demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
@Profile("dev")
public class DevConfig {
    
    @Bean
    public String envConfig() {
        System.out.println("[条件装配] 开发环境配置加载");
        return "dev-config";
    }
}
