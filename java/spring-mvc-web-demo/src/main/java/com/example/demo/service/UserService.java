package com.example.demo.service;

import com.example.demo.model.User;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 用户服务类
 */
@Service
public class UserService {
    
    private final Map<Long, User> users = new HashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);
    
    public UserService() {
        // 初始化数据
        createUser(new User(null, "张三", "zhangsan@example.com", 25));
        createUser(new User(null, "李四", "lisi@example.com", 30));
    }
    
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
    
    public User findById(Long id) {
        return users.get(id);
    }
    
    public User createUser(User user) {
        Long id = idGenerator.getAndIncrement();
        user.setId(id);
        users.put(id, user);
        return user;
    }
    
    public User updateUser(Long id, User user) {
        if (!users.containsKey(id)) {
            return null;
        }
        user.setId(id);
        users.put(id, user);
        return user;
    }
    
    public boolean deleteUser(Long id) {
        return users.remove(id) != null;
    }
}
