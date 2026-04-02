package com.example.demo.controller;

import com.example.demo.entity.User;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import javax.validation.Valid;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 用户控制器
 */
@RestController
@RequestMapping("/api/users")
@Tag(name = "用户管理", description = "用户相关的CRUD操作")
public class UserController {
    
    private final List<User> users = new ArrayList<>();
    private final AtomicLong idGenerator = new AtomicLong(1);
    
    @PostConstruct
    public void init() {
        // 初始化数据
        users.add(new User(idGenerator.getAndIncrement(), "admin", "admin@example.com", 30));
        users.add(new User(idGenerator.getAndIncrement(), "john", "john@example.com", 25));
        users.add(new User(idGenerator.getAndIncrement(), "jane", "jane@example.com", 28));
    }
    
    /**
     * 获取所有用户
     */
    @Operation(summary = "获取所有用户", description = "返回系统中所有用户的列表")
    @ApiResponse(responseCode = "200", description = "成功",
            content = @Content(mediaType = "application/json",
                    schema = @Schema(implementation = User.class)))
    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(users);
    }
    
    /**
     * 根据ID获取用户
     */
    @Operation(summary = "根据ID获取用户", description = "根据用户ID返回单个用户信息")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "找到用户",
                    content = @Content(schema = @Schema(implementation = User.class))),
            @ApiResponse(responseCode = "404", description = "用户不存在")
    })
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(
            @Parameter(description = "用户ID", example = "1") @PathVariable Long id) {
        Optional<User> user = users.stream()
                .filter(u -> u.getId().equals(id))
                .findFirst();
        
        return user.map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * 创建用户
     */
    @Operation(summary = "创建用户", description = "创建一个新用户")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "创建成功",
                    content = @Content(schema = @Schema(implementation = User.class))),
            @ApiResponse(responseCode = "400", description = "参数校验失败")
    })
    @PostMapping
    public ResponseEntity<User> createUser(
            @Valid @RequestBody 
            @Parameter(description = "用户信息", required = true) User user) {
        user.setId(idGenerator.getAndIncrement());
        users.add(user);
        return ResponseEntity.ok(user);
    }
    
    /**
     * 更新用户
     */
    @Operation(summary = "更新用户", description = "根据ID更新用户信息")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "更新成功"),
            @ApiResponse(responseCode = "404", description = "用户不存在")
    })
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(
            @Parameter(description = "用户ID", example = "1") @PathVariable Long id,
            @Valid @RequestBody User userUpdate) {
        Optional<User> existingUser = users.stream()
                .filter(u -> u.getId().equals(id))
                .findFirst();
        
        if (existingUser.isPresent()) {
            User user = existingUser.get();
            user.setUsername(userUpdate.getUsername());
            user.setEmail(userUpdate.getEmail());
            user.setAge(userUpdate.getAge());
            return ResponseEntity.ok(user);
        }
        
        return ResponseEntity.notFound().build();
    }
    
    /**
     * 删除用户
     */
    @Operation(summary = "删除用户", description = "根据ID删除用户")
    @ApiResponses({
            @ApiResponse(responseCode = "204", description = "删除成功"),
            @ApiResponse(responseCode = "404", description = "用户不存在")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(
            @Parameter(description = "用户ID", example = "1") @PathVariable Long id) {
        boolean removed = users.removeIf(u -> u.getId().equals(id));
        return removed ? ResponseEntity.noContent().build() 
                      : ResponseEntity.notFound().build();
    }
}
