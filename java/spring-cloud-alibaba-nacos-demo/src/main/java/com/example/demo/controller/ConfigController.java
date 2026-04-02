package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * 配置管理控制器
 * 
 * @RefreshScope 支持配置动态刷新
 */
@RestController
@RequestMapping("/config")
@RefreshScope
public class ConfigController {
    
    @Value("${user.name:default}")
    private String userName;
    
    @Value("${user.age:0}")
    private Integer userAge;
    
    @Value("${app.message:Hello Nacos}")
    private String appMessage;
    
    /**
     * 获取配置信息
     */
    @GetMapping
    public Map<String, Object> getConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("user.name", userName);
        config.put("user.age", userAge);
        config.put("app.message", appMessage);
        config.put("source", "Nacos Config Center");
        return config;
    }
    
    /**
     * 获取应用消息
     */
    @GetMapping("/message")
    public String getMessage() {
        return appMessage;
    }
}
