package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.mapper.UserMapper;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserMapper userMapper;

    public UserService(UserMapper userMapper) {
        this.userMapper = userMapper;
    }

    public User createUser(User user) {
        userMapper.insert(user);
        return user;
    }

    public Optional<User> getUserById(Long id) {
        return Optional.ofNullable(userMapper.findById(id));
    }

    public List<User> getAllUsers() {
        return userMapper.findAll();
    }

    public List<User> getUsersByStatus(String status) {
        return userMapper.findByStatus(status);
    }

    public List<User> searchUsers(User condition) {
        return userMapper.findByCondition(condition);
    }

    public List<User> getUsersWithPagination(int page, int size) {
        int offset = (page - 1) * size;
        return userMapper.findWithPagination(offset, size);
    }

    public User updateUser(Long id, User user) {
        user.setId(id);
        userMapper.update(user);
        return user;
    }

    public void deleteUser(Long id) {
        userMapper.deleteById(id);
    }
}
