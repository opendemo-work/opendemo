package com.example.demo.service;

import com.example.demo.model.User;
import java.util.List;

/**
 * 用户服务接口
 * 
 * 定义用户相关的业务逻辑
 */
public interface UserService {
    
    /**
     * 根据ID查询用户
     */
    User findById(Long id);
    
    /**
     * 查询所有用户
     */
    List<User> findAll();
    
    /**
     * 创建用户
     */
    User createUser(User user);
    
    /**
     * 更新用户
     */
    User updateUser(User user);
    
    /**
     * 删除用户
     */
    void deleteUser(Long id);
}
