package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.util.*;

/**
 * 认证服务
 */
@Service
public class AuthService {
    
    @Autowired
    private JwtUtil jwtUtil;
    
    // 模拟用户数据库
    private Map<String, User> userStore = new HashMap<>();
    
    @PostConstruct
    public void init() {
        // 初始化测试用户
        userStore.put("admin", new User(1L, "admin", "123456", 
                Arrays.asList("ROLE_ADMIN", "ROLE_USER")));
        userStore.put("user", new User(2L, "user", "123456", 
                Arrays.asList("ROLE_USER")));
        userStore.put("guest", new User(3L, "guest", "123456", 
                Arrays.asList("ROLE_GUEST")));
    }
    
    /**
     * 用户登录
     * 
     * @param username 用户名
     * @param password 密码
     * @return JWT令牌
     */
    public String login(String username, String password) {
        User user = userStore.get(username);
        if (user == null) {
            throw new RuntimeException("用户不存在");
        }
        if (!user.getPassword().equals(password)) {
            throw new RuntimeException("密码错误");
        }
        
        return jwtUtil.generateToken(username);
    }
    
    /**
     * 根据用户名获取用户
     */
    public User getUserByUsername(String username) {
        return userStore.get(username);
    }
    
    /**
     * 获取所有用户
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(userStore.values());
    }
}
