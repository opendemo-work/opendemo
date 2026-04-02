package com.example.demo.controller;

import com.example.demo.entity.User;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
import java.util.HashMap;
import java.util.Map;

/**
 * 用户控制器 - 演示参数校验
 */
@RestController
@RequestMapping("/api/users")
@Validated  // 启用方法级校验
public class UserController {
    
    /**
     * 创建用户 - 请求体验证
     */
    @PostMapping
    public ResponseEntity<Map<String, Object>> createUser(@Valid @RequestBody User user) {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "用户创建成功");
        result.put("user", user);
        return ResponseEntity.ok(result);
    }
    
    /**
     * 更新用户 - 路径变量和请求体验证
     */
    @PutMapping("/{id}")
    public ResponseEntity<Map<String, Object>> updateUser(
            @Min(value = 1, message = "用户ID必须大于0") @PathVariable Long id,
            @Valid @RequestBody User user) {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "用户更新成功");
        result.put("id", id);
        result.put("user", user);
        return ResponseEntity.ok(result);
    }
    
    /**
     * 搜索用户 - 请求参数验证
     */
    @GetMapping("/search")
    public ResponseEntity<Map<String, Object>> searchUsers(
            @NotBlank(message = "搜索关键词不能为空")
            @Size(min = 2, max = 20, message = "关键词长度必须在2-20之间")
            @RequestParam String keyword,
            
            @Min(value = 1, message = "页码必须大于等于1")
            @RequestParam(defaultValue = "1") Integer page,
            
            @Min(value = 1, message = "每页大小必须大于等于1")
            @RequestParam(defaultValue = "10") Integer size) {
        
        Map<String, Object> result = new HashMap<>();
        result.put("keyword", keyword);
        result.put("page", page);
        result.put("size", size);
        return ResponseEntity.ok(result);
    }
    
    /**
     * 验证通过测试
     */
    @PostMapping("/test-valid")
    public ResponseEntity<Map<String, Object>> testValid() {
        User user = new User();
        user.setId(1L);
        user.setUsername("john");
        user.setPassword("Password123");
        user.setEmail("john@example.com");
        user.setAge(25);
        user.setAgreeTerms(true);
        user.setPhone("13800138000");
        user.setPoints(100.0);
        
        Map<String, Object> result = new HashMap<>();
        result.put("message", "验证通过");
        result.put("user", user);
        return ResponseEntity.ok(result);
    }
}
