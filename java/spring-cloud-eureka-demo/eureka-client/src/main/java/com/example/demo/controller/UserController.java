package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 用户服务控制器
 */
@RestController
@RequestMapping("/users")
public class UserController {
    
    @GetMapping
    public String getUsers() {
        return "User List from Eureka Client";
    }
    
    @GetMapping("/health")
    public String health() {
        return "Service is healthy";
    }
}
