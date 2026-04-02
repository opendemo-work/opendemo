package com.example.demo.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

/**
 * Spring AOP配置类
 * 
 * @EnableAspectJAutoProxy 启用AspectJ自动代理
 * - proxyTargetClass = true: 使用CGLIB代理（基于类）
 * - proxyTargetClass = false: 使用JDK动态代理（基于接口）
 */
@Configuration
@ComponentScan(basePackages = "com.example.demo")
@EnableAspectJAutoProxy(proxyTargetClass = true)
public class AopConfig {
}
