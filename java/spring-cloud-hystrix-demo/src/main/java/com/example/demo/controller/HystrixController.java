package com.example.demo.controller;

import com.example.demo.service.HystrixService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Hystrix熔断器演示控制器
 */
@RestController
@RequestMapping("/api")
public class HystrixController {
    
    @Autowired
    private HystrixService hystrixService;
    
    /**
     * 正常服务
     */
    @GetMapping("/normal")
    public String normal() {
        return hystrixService.normalService();
    }
    
    /**
     * 慢服务（可能超时）
     */
    @GetMapping("/slow")
    public String slow() {
        return hystrixService.slowService();
    }
    
    /**
     * 不稳定服务（随机失败）
     */
    @GetMapping("/unstable")
    public String unstable() {
        return hystrixService.unstableService();
    }
    
    /**
     * 异常服务（总是失败，触发熔断）
     */
    @GetMapping("/error")
    public String error() {
        return hystrixService.errorService();
    }
    
    /**
     * 批量测试接口
     */
    @GetMapping("/batch-test")
    public String batchTest() {
        StringBuilder result = new StringBuilder();
        result.append("=== 批量测试 ===\n\n");
        
        // 测试正常服务
        result.append("【正常服务】\n");
        for (int i = 0; i < 3; i++) {
            result.append(i + 1).append(". ").append(hystrixService.normalService()).append("\n");
        }
        
        result.append("\n【慢服务】\n");
        for (int i = 0; i < 5; i++) {
            result.append(i + 1).append(". ").append(hystrixService.slowService()).append("\n");
        }
        
        result.append("\n【不稳定服务】\n");
        for (int i = 0; i < 5; i++) {
            result.append(i + 1).append(". ").append(hystrixService.unstableService()).append("\n");
        }
        
        return result.toString();
    }
}
