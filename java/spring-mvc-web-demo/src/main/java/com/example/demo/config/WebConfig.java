package com.example.demo.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Spring MVC配置类
 */
@Configuration
@EnableWebMvc
@ComponentScan(basePackages = "com.example.demo")
public class WebConfig implements WebMvcConfigurer {
    // 可在此添加更多MVC配置
}
