package com.example.demo.service;

import com.example.demo.entity.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

/**
 * 用户服务类
 * 
 * 实现UserDetailsService接口，提供用户认证信息
 */
@Service
public class UserService implements UserDetailsService {
    
    // 模拟用户数据库
    private final Map<String, User> users = new HashMap<>();
    
    public UserService() {
        // 初始化测试用户
        users.put("admin", new User(1L, "admin", "{noop}admin123", "ADMIN", true));
        users.put("user", new User(2L, "user", "{noop}user123", "USER", true));
        users.put("guest", new User(3L, "guest", "{noop}guest123", "GUEST", true));
    }
    
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = users.get(username);
        if (user == null) {
            throw new UsernameNotFoundException("用户不存在: " + username);
        }
        return user;
    }
}
