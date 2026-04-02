package com.example.demo.controller;

import com.alibaba.csp.sentinel.annotation.SentinelResource;
import com.alibaba.csp.sentinel.slots.block.BlockException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * Hello控制器
 * 
 * 演示Sentinel流量控制和熔断降级
 */
@RestController
public class HelloController {
    
    /**
     * 普通接口
     */
    @GetMapping("/hello")
    public String hello() {
        return "Hello Sentinel!";
    }
    
    /**
     * 受Sentinel保护的接口 - 限流
     * 
     * @SentinelResource: 标记需要保护的方法
     * value: 资源名
     * blockHandler: 限流/降级处理方法
     */
    @GetMapping("/rate-limit")
    @SentinelResource(value = "rateLimit", blockHandler = "rateLimitHandler")
    public Map<String, Object> rateLimit(@RequestParam(defaultValue = "1") int count) {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "请求成功");
        result.put("count", count);
        result.put("timestamp", System.currentTimeMillis());
        return result;
    }
    
    /**
     * 限流处理方法
     */
    public Map<String, Object> rateLimitHandler(int count, BlockException ex) {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "请求被限流");
        result.put("error", "Too many requests");
        result.put("count", count);
        return result;
    }
    
    /**
     * 受Sentinel保护的接口 - 熔断降级
     */
    @GetMapping("/circuit-breaker")
    @SentinelResource(value = "circuitBreaker", 
                      blockHandler = "circuitBreakerHandler",
                      fallback = "circuitBreakerFallback")
    public Map<String, Object> circuitBreaker(@RequestParam(defaultValue = "false") boolean error) {
        if (error) {
            throw new RuntimeException("模拟业务异常");
        }
        
        Map<String, Object> result = new HashMap<>();
        result.put("message", "业务处理成功");
        result.put("timestamp", System.currentTimeMillis());
        return result;
    }
    
    /**
     * 熔断处理方法
     */
    public Map<String, Object> circuitBreakerHandler(boolean error, BlockException ex) {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "请求被熔断");
        result.put("error", "Circuit breaker is open");
        return result;
    }
    
    /**
     * 业务异常降级方法
     */
    public Map<String, Object> circuitBreakerFallback(boolean error, Throwable ex) {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "业务异常，降级处理");
        result.put("error", ex.getMessage());
        return result;
    }
}
