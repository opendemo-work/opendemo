package com.example.demo;

import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

/**
 * 依赖Bean
 * 
 * 用于演示依赖注入
 */
@Component
public class DependencyBean {
    
    private final String name = "DependencyBean";
    
    public DependencyBean() {
        System.out.println("    DependencyBean 构造器");
    }
    
    @PostConstruct
    public void init() {
        System.out.println("    DependencyBean @PostConstruct");
    }
    
    @PreDestroy
    public void destroy() {
        System.out.println("    DependencyBean @PreDestroy");
    }
    
    public String getName() {
        return name;
    }
}
