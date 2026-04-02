package com.example.demo.controller;

import com.example.demo.client.UserServiceClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Feign演示控制器
 */
@RestController
@RequestMapping("/feign")
public class FeignController {
    
    @Autowired
    private UserServiceClient userServiceClient;
    
    @GetMapping("/users/{id}")
    public String getUser(@PathVariable Long id) {
        System.out.println("[Feign] 调用user-service获取用户: " + id);
        return userServiceClient.getUserById(id);
    }
    
    @GetMapping("/users")
    public String getAllUsers() {
        System.out.println("[Feign] 调用user-service获取所有用户");
        return userServiceClient.getAllUsers();
    }
}
