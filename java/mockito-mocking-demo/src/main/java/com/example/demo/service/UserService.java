package com.example.demo.service;

import com.example.demo.model.User;
import com.example.demo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * 用户服务类
 * 
 * 用于演示Mockito的Mock测试
 */
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private NotificationService notificationService;
    
    /**
     * 根据ID获取用户
     */
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }
    
    /**
     * 获取所有用户
     */
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    /**
     * 注册用户
     * 
     * 注册成功后发送欢迎邮件
     */
    public User registerUser(User user) {
        // 验证邮箱是否已存在
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new IllegalArgumentException("邮箱已存在: " + user.getEmail());
        }
        
        // 验证年龄
        if (user.getAge() == null || user.getAge() < 18) {
            throw new IllegalArgumentException("用户年龄必须大于等于18岁");
        }
        
        // 保存用户
        User savedUser = userRepository.save(user);
        
        // 发送欢迎邮件
        notificationService.sendWelcomeEmail(savedUser);
        
        return savedUser;
    }
    
    /**
     * 删除用户
     */
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
    
    /**
     * 更新用户信息
     */
    public User updateUser(Long id, User userUpdate) {
        User existingUser = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("用户不存在: " + id));
        
        if (userUpdate.getUsername() != null) {
            existingUser.setUsername(userUpdate.getUsername());
        }
        if (userUpdate.getEmail() != null) {
            existingUser.setEmail(userUpdate.getEmail());
        }
        if (userUpdate.getAge() != null) {
            existingUser.setAge(userUpdate.getAge());
        }
        
        return userRepository.save(existingUser);
    }
    
    /**
     * 请求密码重置
     */
    public String requestPasswordReset(String email) {
        User user = userRepository.findAll().stream()
                .filter(u -> u.getEmail().equals(email))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("用户不存在: " + email));
        
        String token = UUID.randomUUID().toString();
        notificationService.sendPasswordResetEmail(email, token);
        
        return token;
    }
    
    /**
     * 根据用户名查找用户
     */
    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }
}
