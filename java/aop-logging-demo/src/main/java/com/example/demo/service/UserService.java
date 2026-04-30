package com.example.demo.service;

import com.example.demo.annotation.Loggable;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class UserService {

    private final Map<Long, String> userStore = new ConcurrentHashMap<>();

    public UserService() {
        userStore.put(1L, "张三");
        userStore.put(2L, "李四");
        userStore.put(3L, "王五");
    }

    @Loggable(value = "查询用户", logParams = true, logResult = true, logExecutionTime = true)
    public String findById(Long id) {
        simulateDelay();
        return userStore.get(id);
    }

    @Loggable(value = "查询所有用户", logParams = false, logResult = true)
    public List<String> findAll() {
        simulateDelay();
        return new ArrayList<>(userStore.values());
    }

    @Loggable(value = "创建用户")
    public String createUser(Long id, String name) {
        userStore.put(id, name);
        return "用户创建成功: " + name;
    }

    @Loggable(value = "删除用户")
    public boolean deleteUser(Long id) {
        return userStore.remove(id) != null;
    }

    @Loggable(value = "更新用户")
    public String updateUser(Long id, String name) {
        if (!userStore.containsKey(id)) {
            throw new IllegalArgumentException("用户不存在: " + id);
        }
        userStore.put(id, name);
        return "用户更新成功: " + name;
    }

    private void simulateDelay() {
        try {
            Thread.sleep((long) (Math.random() * 100));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
