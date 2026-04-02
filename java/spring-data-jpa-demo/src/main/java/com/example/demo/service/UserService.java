package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * 用户服务类
 * 
 * 业务逻辑层，演示Spring Data JPA的各种用法
 */
@Service
@Transactional(readOnly = true)
public class UserService {
    
    private final UserRepository userRepository;
    
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    /**
     * 创建用户
     */
    @Transactional
    public User createUser(User user) {
        if (userRepository.existsByUsername(user.getUsername())) {
            throw new RuntimeException("用户名已存在: " + user.getUsername());
        }
        return userRepository.save(user);
    }
    
    /**
     * 根据ID查询
     */
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }
    
    /**
     * 根据用户名查询
     */
    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }
    
    /**
     * 查询所有用户
     */
    public List<User> findAll() {
        return userRepository.findAll();
    }
    
    /**
     * 分页查询
     */
    public Page<User> findAllPaged(int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("id").descending());
        return userRepository.findAll(pageable);
    }
    
    /**
     * 更新用户
     */
    @Transactional
    public User updateUser(Long id, User userDetails) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("用户不存在: " + id));
        
        user.setUsername(userDetails.getUsername());
        user.setEmail(userDetails.getEmail());
        user.setAge(userDetails.getAge());
        
        return userRepository.save(user);
    }
    
    /**
     * 删除用户
     */
    @Transactional
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
    
    /**
     * 根据年龄范围查询
     */
    public List<User> findByAgeBetween(int minAge, int maxAge) {
        return userRepository.findByAgeBetween(minAge, maxAge);
    }
    
    /**
     * 模糊搜索用户名
     */
    public List<User> searchByUsername(String keyword) {
        return userRepository.findByUsernameContaining(keyword);
    }
    
    /**
     * 查询成年用户（JPQL）
     */
    public List<User> findAdultUsers(int adultAge) {
        return userRepository.findAdultUsers(adultAge);
    }
    
    /**
     * 统计用户数量
     */
    public long countUsers() {
        return userRepository.count();
    }
}
