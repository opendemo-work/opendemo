package com.example.demo;

import com.example.demo.config.AppConfig;
import com.example.demo.model.User;
import com.example.demo.service.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * UserService 单元测试
 * 
 * 演示Spring Test框架的使用
 */
public class UserServiceTest {
    
    private UserService userService;
    private AnnotationConfigApplicationContext context;
    
    @BeforeEach
    void setUp() {
        // 为每个测试方法创建新的容器
        context = new AnnotationConfigApplicationContext(AppConfig.class);
        userService = context.getBean(UserService.class);
    }
    
    @Test
    @DisplayName("测试容器启动和Bean获取")
    void testContextStartup() {
        assertNotNull(context);
        assertTrue(context.isActive());
        assertNotNull(userService);
    }
    
    @Test
    @DisplayName("测试根据ID查询用户")
    void testFindById() {
        User user = userService.findById(1L);
        
        assertNotNull(user);
        assertEquals(1L, user.getId());
        assertEquals("张三", user.getUsername());
    }
    
    @Test
    @DisplayName("测试查询所有用户")
    void testFindAll() {
        List<User> users = userService.findAll();
        
        assertNotNull(users);
        assertEquals(3, users.size());  // 初始化了3个用户
    }
    
    @Test
    @DisplayName("测试创建用户")
    void testCreateUser() {
        User newUser = new User(null, "测试用户", "test@example.com", 25);
        User created = userService.createUser(newUser);
        
        assertNotNull(created.getId());
        assertEquals("测试用户", created.getUsername());
        
        // 验证总数增加
        List<User> users = userService.findAll();
        assertEquals(4, users.size());
    }
    
    @Test
    @DisplayName("测试更新用户")
    void testUpdateUser() {
        User user = userService.findById(1L);
        assertNotNull(user);
        
        user.setAge(30);
        User updated = userService.updateUser(user);
        
        assertEquals(30, updated.getAge());
        
        // 验证更新持久化
        User found = userService.findById(1L);
        assertEquals(30, found.getAge());
    }
    
    @Test
    @DisplayName("测试删除用户")
    void testDeleteUser() {
        userService.deleteUser(1L);
        
        User deleted = userService.findById(1L);
        assertNull(deleted);
        
        // 验证总数减少
        List<User> users = userService.findAll();
        assertEquals(2, users.size());
    }
}
