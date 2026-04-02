package com.example.demo.service;

import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;
import com.netflix.hystrix.contrib.javanica.annotation.HystrixProperty;
import org.springframework.stereotype.Service;

import java.util.Random;
import java.util.concurrent.TimeUnit;

/**
 * Hystrix熔断器演示服务
 * 
 * 演示@HystrixCommand的各种配置和使用场景
 */
@Service
public class HystrixService {
    
    private final Random random = new Random();
    
    /**
     * 正常服务调用
     * 
     * fallbackMethod: 指定降级方法
     */
    @HystrixCommand(
            fallbackMethod = "normalFallback",
            commandProperties = {
                    @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "3000")
            }
    )
    public String normalService() {
        return "服务正常响应 - " + System.currentTimeMillis();
    }
    
    /**
     * 慢服务调用（模拟超时）
     * 
     * 当响应时间超过timeoutInMilliseconds时触发熔断
     */
    @HystrixCommand(
            fallbackMethod = "slowFallback",
            commandProperties = {
                    @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "2000"),
                    @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "5"),
                    @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "10000"),
                    @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "50")
            }
    )
    public String slowService() {
        int delay = random.nextInt(3000); // 0-3000ms随机延迟
        System.out.println("[慢服务] 模拟延迟: " + delay + "ms");
        
        try {
            TimeUnit.MILLISECONDS.sleep(delay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        return "慢服务响应完成 - 延迟" + delay + "ms";
    }
    
    /**
     * 不稳定服务（模拟随机失败）
     * 
     * 演示熔断器在错误率超过阈值时的行为
     */
    @HystrixCommand(
            fallbackMethod = "unstableFallback",
            commandProperties = {
                    @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "3000"),
                    @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "5"),
                    @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "10000"),
                    @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "50"),
                    @HystrixProperty(name = "metrics.rollingStats.timeInMilliseconds", value = "10000")
            }
    )
    public String unstableService() {
        if (random.nextInt(100) < 60) { // 60%概率失败
            System.out.println("[不稳定服务] 模拟异常抛出");
            throw new RuntimeException("服务暂时不可用");
        }
        return "不稳定服务成功响应 - " + System.currentTimeMillis();
    }
    
    /**
     * 异常服务（总是失败）
     * 
     * 用于快速触发熔断状态
     */
    @HystrixCommand(
            fallbackMethod = "errorFallback",
            commandProperties = {
                    @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "3"),
                    @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "5000"),
                    @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "50")
            }
    )
    public String errorService() {
        System.out.println("[异常服务] 抛出异常");
        throw new RuntimeException("服务异常");
    }
    
    // ========== Fallback降级方法 ==========
    
    public String normalFallback() {
        return "【降级】正常服务降级响应 - 请稍后重试";
    }
    
    public String slowFallback() {
        return "【降级】慢服务响应超时 - 已返回默认结果";
    }
    
    public String unstableFallback(Throwable throwable) {
        return "【降级】不稳定服务异常: " + throwable.getMessage() + " - 使用缓存数据";
    }
    
    public String errorFallback(Throwable throwable) {
        return "【降级】服务熔断中: " + throwable.getMessage() + " - 请5秒后重试";
    }
}
