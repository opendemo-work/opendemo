package com.example.demo.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * 问候服务配置属性
 * 
 * 演示@ConfigurationProperties绑定配置
 */
@ConfigurationProperties(prefix = "greeting")
public class GreetingProperties {
    
    private String prefix = "Hello";
    private boolean enabled = true;
    
    public String getPrefix() {
        return prefix;
    }
    
    public void setPrefix(String prefix) {
        this.prefix = prefix;
    }
    
    public boolean isEnabled() {
        return enabled;
    }
    
    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}
