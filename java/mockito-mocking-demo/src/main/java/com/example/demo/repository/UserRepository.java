package com.example.demo.repository;

import com.example.demo.model.User;

import java.util.List;
import java.util.Optional;

/**
 * 用户数据访问接口
 */
public interface UserRepository {
    
    /**
     * 根据ID查找用户
     */
    Optional<User> findById(Long id);
    
    /**
     * 查找所有用户
     */
    List<User> findAll();
    
    /**
     * 保存用户
     */
    User save(User user);
    
    /**
     * 删除用户
     */
    void deleteById(Long id);
    
    /**
     * 根据用户名查找
     */
    Optional<User> findByUsername(String username);
    
    /**
     * 检查邮箱是否存在
     */
    boolean existsByEmail(String email);
}
