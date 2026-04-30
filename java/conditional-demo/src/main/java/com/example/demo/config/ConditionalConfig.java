package com.example.demo.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ConditionalConfig {

    @Bean
    @ConditionalOnProperty(name = "feature.swagger.enabled", havingValue = "true", matchIfMissing = false)
    public String swaggerConfig() {
        System.out.println("[条件装配] Swagger配置已加载 (feature.swagger.enabled=true)");
        return "swagger-enabled";
    }

    @Bean
    @ConditionalOnProperty(name = "feature.rate-limit.enabled", havingValue = "true", matchIfMissing = true)
    public String rateLimitConfig() {
        System.out.println("[条件装配] 限流配置已加载 (默认启用)");
        return "rate-limit-enabled";
    }

    @Bean
    @ConditionalOnProperty(name = "feature.cache.type", havingValue = "redis")
    public String redisCacheConfig() {
        System.out.println("[条件装配] Redis缓存配置已加载 (feature.cache.type=redis)");
        return "redis-cache";
    }

    @Bean
    @ConditionalOnProperty(name = "feature.cache.type", havingValue = "local", matchIfMissing = true)
    public String localCacheConfig() {
        System.out.println("[条件装配] 本地缓存配置已加载 (feature.cache.type=local)");
        return "local-cache";
    }
}
