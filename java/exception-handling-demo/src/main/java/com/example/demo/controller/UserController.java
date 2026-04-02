package com.example.demo.controller;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ResourceNotFoundException;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final Map<Long, String> users = new HashMap<>();
    
    public UserController() {
        users.put(1L, "User1");
        users.put(2L, "User2");
    }
    
    @GetMapping("/{id}")
    public String getUser(@PathVariable Long id) {
        if (!users.containsKey(id)) {
            throw new ResourceNotFoundException("用户不存在: " + id);
        }
        return users.get(id);
    }
    
    @PostMapping
    public String createUser(@RequestParam String name) {
        if (name == null || name.isEmpty()) {
            throw new BusinessException(400001, "用户名不能为空");
        }
        return "用户创建成功: " + name;
    }
    
    @GetMapping("/error")
    public String triggerError() {
        throw new RuntimeException("系统内部错误");
    }
}
