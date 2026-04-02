package com.example.demo.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * 用户服务Feign客户端
 * 
 * @FeignClient 声明式HTTP客户端
 * name: 服务名称
 * url: 服务地址（开发测试时使用）
 */
@FeignClient(name = "user-service", url = "http://localhost:8081")
public interface UserServiceClient {
    
    /**
     * 获取用户信息
     * 
     * 等价于发送 GET http://localhost:8081/users/{id}
     */
    @GetMapping("/users/{id}")
    String getUserById(@PathVariable("id") Long id);
    
    /**
     * 获取所有用户
     * 
     * 等价于发送 GET http://localhost:8081/users
     */
    @GetMapping("/users")
    String getAllUsers();
}
