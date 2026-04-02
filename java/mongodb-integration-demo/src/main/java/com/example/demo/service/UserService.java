package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * 用户服务
 */
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    /**
     * 保存用户
     */
    public User save(User user) {
        return userRepository.save(user);
    }
    
    /**
     * 根据ID查询
     */
    public Optional<User> findById(String id) {
        return userRepository.findById(id);
    }
    
    /**
     * 查询所有
     */
    public List<User> findAll() {
        return userRepository.findAll();
    }
    
    /**
     * 删除
     */
    public void deleteById(String id) {
        userRepository.deleteById(id);
    }
    
    /**
     * 根据用户名查询
     */
    public User findByUsername(String username) {
        return userRepository.findByUsername(username);
    }
    
    /**
     * 根据年龄范围查询
     */
    public List<User> findByAgeRange(Integer minAge, Integer maxAge) {
        return userRepository.findByAgeBetween(minAge, maxAge);
    }
    
    /**
     * 根据城市查询
     */
    public List<User> findByCity(String city) {
        return userRepository.findByAddressCity(city);
    }
    
    /**
     * 根据标签查询
     */
    public List<User> findByTag(String tag) {
        return userRepository.findByTagsContaining(tag);
    }
}
