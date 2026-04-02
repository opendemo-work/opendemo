package com.example.demo.service.impl;

import com.example.demo.service.GreetingService;

/**
 * 简单问候服务实现
 */
public class SimpleGreetingService implements GreetingService {
    
    private String greetingPrefix = "Hello";
    
    public SimpleGreetingService() {}
    
    public SimpleGreetingService(String greetingPrefix) {
        this.greetingPrefix = greetingPrefix;
    }
    
    @Override
    public String greet(String name) {
        return greetingPrefix + ", " + name + "!";
    }
    
    public void setGreetingPrefix(String greetingPrefix) {
        this.greetingPrefix = greetingPrefix;
    }
}
