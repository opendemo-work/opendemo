package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
public class ProfileConfig {

    @Bean
    @Profile("dev")
    public String devMessage() {
        return "开发环境配置已加载";
    }

    @Bean
    @Profile("prod")
    public String prodMessage() {
        return "生产环境配置已加载";
    }
}
