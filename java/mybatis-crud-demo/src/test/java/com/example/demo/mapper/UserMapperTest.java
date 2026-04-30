package com.example.demo.mapper;

import com.example.demo.entity.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class UserMapperTest {

    @Autowired
    private UserMapper userMapper;

    @Test
    void testInsert() {
        User user = new User("测试用户", "test@example.com", 25, "13800138000", "ACTIVE");
        int rows = userMapper.insert(user);
        assertEquals(1, rows);
        assertNotNull(user.getId());
    }

    @Test
    void testFindById() {
        User user = new User("查找用户", "find@example.com", 30, "13900139000", "ACTIVE");
        userMapper.insert(user);
        User found = userMapper.findById(user.getId());
        assertNotNull(found);
        assertEquals("查找用户", found.getUsername());
    }

    @Test
    void testFindAll() {
        userMapper.insert(new User("用户A", "a@example.com", 20, "111", "ACTIVE"));
        userMapper.insert(new User("用户B", "b@example.com", 25, "222", "INACTIVE"));
        List<User> users = userMapper.findAll();
        assertNotNull(users);
        assertTrue(users.size() >= 2);
    }

    @Test
    void testUpdate() {
        User user = new User("更新前", "before@example.com", 20, "333", "ACTIVE");
        userMapper.insert(user);
        user.setUsername("更新后");
        user.setEmail("after@example.com");
        int rows = userMapper.update(user);
        assertEquals(1, rows);
        User updated = userMapper.findById(user.getId());
        assertEquals("更新后", updated.getUsername());
    }

    @Test
    void testDelete() {
        User user = new User("待删除", "delete@example.com", 22, "444", "ACTIVE");
        userMapper.insert(user);
        int rows = userMapper.deleteById(user.getId());
        assertEquals(1, rows);
        assertNull(userMapper.findById(user.getId()));
    }

    @Test
    void testFindByStatus() {
        userMapper.insert(new User("活跃用户", "active@example.com", 28, "555", "ACTIVE"));
        List<User> activeUsers = userMapper.findByStatus("ACTIVE");
        assertNotNull(activeUsers);
        assertTrue(activeUsers.size() >= 1);
    }

    @Test
    void testFindByCondition() {
        userMapper.insert(new User("条件搜索用户", "cond@example.com", 35, "666", "ACTIVE"));
        User condition = new User();
        condition.setUsername("条件");
        List<User> results = userMapper.findByCondition(condition);
        assertNotNull(results);
        assertTrue(results.size() >= 1);
    }

    @Test
    void testFindWithPagination() {
        for (int i = 0; i < 5; i++) {
            userMapper.insert(new User("分页用户" + i, "page" + i + "@example.com", 20 + i, "77" + i, "ACTIVE"));
        }
        List<User> page1 = userMapper.findWithPagination(0, 3);
        assertNotNull(page1);
        assertTrue(page1.size() <= 3);
    }
}
