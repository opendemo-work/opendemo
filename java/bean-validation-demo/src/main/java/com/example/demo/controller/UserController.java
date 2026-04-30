package com.example.demo.controller;

import com.example.demo.dto.ApiResponse;
import com.example.demo.entity.User;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @PostMapping
    public ResponseEntity<ApiResponse> createUser(@Valid @RequestBody User user) {
        return ResponseEntity.ok(ApiResponse.success("用户创建成功", user));
    }

    @PostMapping("/batch")
    public ResponseEntity<ApiResponse> createUsers(@Valid @RequestBody java.util.List<@Valid User> users) {
        return ResponseEntity.ok(ApiResponse.success("批量创建成功", users));
    }

    @GetMapping("/template")
    public ResponseEntity<ApiResponse> getUserTemplate() {
        User template = new User();
        template.setUsername("template_user");
        template.setEmail("template@example.com");
        template.setAge(25);
        template.setPassword("abc123");
        template.setPhone("13800138000");
        return ResponseEntity.ok(ApiResponse.success("用户模板", template));
    }
}
