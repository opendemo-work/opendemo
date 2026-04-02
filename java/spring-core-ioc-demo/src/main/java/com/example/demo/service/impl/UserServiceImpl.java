package com.example.demo.service.impl;

import com.example.demo.model.User;
import com.example.demo.service.UserService;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 用户服务实现类
 * 
 * 使用@Service注解标记为Spring管理的Bean
 * 演示IoC容器的Bean生命周期管理
 */
@Service
public class UserServiceImpl implements UserService {
    
    // 模拟数据库存储
    private final Map<Long, User> userStore = new HashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);
    
    /**
     * 构造器
     */
    public UserServiceImpl() {
        System.out.println("UserServiceImpl 构造器被调用");
    }
    
    /**
     * 初始化方法 - @PostConstruct
     * 在依赖注入完成后执行
     */
    @PostConstruct
    public void init() {
        System.out.println("UserServiceImpl 初始化方法被调用 (@PostConstruct)");
        // 添加一些示例数据
        createUser(new User(null, "张三", "zhangsan@example.com", 25));
        createUser(new User(null, "李四", "lisi@example.com", 30));
        createUser(new User(null, "王五", "wangwu@example.com", 28));
    }
    
    /**
     * 销毁方法 - @PreDestroy
     * 在Bean销毁前执行
     */
    @PreDestroy
    public void destroy() {
        System.out.println("UserServiceImpl 销毁方法被调用 (@PreDestroy)");
    }
    
    @Override
    public User findById(Long id) {
        return userStore.get(id);
    }
    
    @Override
    public List<User> findAll() {
        return new ArrayList<>(userStore.values());
    }
    
    @Override
    public User createUser(User user) {
        Long id = idGenerator.getAndIncrement();
        user.setId(id);
        userStore.put(id, user);
        System.out.println("创建用户: " + user);
        return user;
    }
    
    @Override
    public User updateUser(User user) {
        if (user.getId() == null || !userStore.containsKey(user.getId())) {
            throw new IllegalArgumentException("用户不存在: " + user.getId());
        }
        userStore.put(user.getId(), user);
        System.out.println("更新用户: " + user);
        return user;
    }
    
    @Override
    public void deleteUser(Long id) {
        User removed = userStore.remove(id);
        if (removed != null) {
            System.out.println("删除用户: " + removed);
        }
    }
}
