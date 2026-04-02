package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 用户控制器
 * 
 * 演示受保护的API端点
 */
@RestController
@RequestMapping("/api")
public class UserController {
    
    @Autowired
    private AuthService authService;
    
    /**
     * 获取当前用户信息
     * 
     * 需要JWT认证
     */
    @GetMapping("/user/profile")
    public ResponseEntity<?> getProfile(Authentication authentication) {
        String username = authentication.getName();
        User user = authService.getUserByUsername(username);
        
        Map<String, Object> profile = new HashMap<>();
        profile.put("username", user.getUsername());
        profile.put("roles", user.getRoles());
        
        return ResponseEntity.ok(profile);
    }
    
    /**
     * 获取所有用户（仅管理员）
     */
    @GetMapping("/admin/users")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<List<User>> getAllUsers() {
        List<User> users = authService.getAllUsers();
        return ResponseEntity.ok(users);
    }
    
    /**
     * 公开接口
     */
    @GetMapping("/public/info")
    public ResponseEntity<Map<String, String>> publicInfo() {
        Map<String, String> info = new HashMap<>();
        info.put("message", "这是一个公开接口");
        info.put("version", "1.0");
        return ResponseEntity.ok(info);
    }
}
