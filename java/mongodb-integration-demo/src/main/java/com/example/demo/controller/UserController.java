package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

/**
 * 用户控制器
 */
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    /**
     * 添加用户
     */
    @PostMapping
    public ResponseEntity<User> addUser(@RequestBody User user) {
        User saved = userService.save(user);
        return ResponseEntity.ok(saved);
    }
    
    /**
     * 根据ID查询
     */
    @GetMapping("/{id}")
    public ResponseEntity<User> getById(@PathVariable String id) {
        return userService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * 查询所有
     */
    @GetMapping
    public ResponseEntity<List<User>> getAll() {
        return ResponseEntity.ok(userService.findAll());
    }
    
    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id) {
        userService.deleteById(id);
        return ResponseEntity.ok().build();
    }
    
    /**
     * 根据用户名查询
     */
    @GetMapping("/username/{username}")
    public ResponseEntity<User> getByUsername(@PathVariable String username) {
        User user = userService.findByUsername(username);
        return user != null ? ResponseEntity.ok(user) : ResponseEntity.notFound().build();
    }
    
    /**
     * 根据年龄范围查询
     */
    @GetMapping("/age-range")
    public ResponseEntity<List<User>> getByAgeRange(
            @RequestParam Integer min,
            @RequestParam Integer max) {
        return ResponseEntity.ok(userService.findByAgeRange(min, max));
    }
    
    /**
     * 根据城市查询
     */
    @GetMapping("/city/{city}")
    public ResponseEntity<List<User>> getByCity(@PathVariable String city) {
        return ResponseEntity.ok(userService.findByCity(city));
    }
    
    /**
     * 根据标签查询
     */
    @GetMapping("/tag/{tag}")
    public ResponseEntity<List<User>> getByTag(@PathVariable String tag) {
        return ResponseEntity.ok(userService.findByTag(tag));
    }
    
    /**
     * 初始化数据
     */
    @PostMapping("/init")
    public ResponseEntity<String> initData() {
        // 用户1
        User user1 = new User("john", "john@example.com", 25);
        User.Address addr1 = new User.Address("北京", "朝阳区xxx街道", "100000");
        user1.setAddress(addr1);
        user1.setTags(Arrays.asList("developer", "java"));
        userService.save(user1);
        
        // 用户2
        User user2 = new User("jane", "jane@example.com", 30);
        User.Address addr2 = new User.Address("上海", "浦东新区xxx路", "200000");
        user2.setAddress(addr2);
        user2.setTags(Arrays.asList("designer", "ui"));
        userService.save(user2);
        
        // 用户3
        User user3 = new User("bob", "bob@example.com", 35);
        User.Address addr3 = new User.Address("北京", "海淀区xxx街", "100080");
        user3.setAddress(addr3);
        user3.setTags(Arrays.asList("manager", "agile"));
        userService.save(user3);
        
        return ResponseEntity.ok("初始化数据完成");
    }
}
