package com.example.demo.config;

import com.example.demo.LifecycleBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

/**
 * Spring生命周期配置类
 */
@Configuration
@ComponentScan(basePackages = "com.example.demo")
@PropertySource("classpath:application.properties")
public class LifecycleConfig {
    
    /**
     * 显式定义LifecycleBean，指定init-method和destroy-method
     */
    @Bean(initMethod = "customInit", destroyMethod = "customDestroy")
    public LifecycleBean lifecycleBean() {
        return new LifecycleBean();
    }
}
